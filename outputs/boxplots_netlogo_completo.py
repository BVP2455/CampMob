"""Figuras del TFG CampusMob. Python 3.9+.
Instalación: python -m pip install pandas numpy matplotlib
Uso: python boxplots_netlogo_completo.py --inputs Factor1.zip Factor2.zip Factor3.zip
También acepta carpetas (busca recursivamente). Sin argumentos busca CSV junto
al script y en sus subcarpetas. NO incluir versiones antiguas ni ZIP duplicados.
Salida: figuras_tfg (PNG 300 dpi, PDF vectorial, tablas CSV y metodología).
Cada caja principal contiene las medias de las repeticiones, no todos los viajes.
--legacy añade distribuciones de viajes por modo y por ejecución como el script
original. No cambia CSV ni simulaciones. Los mapas son cuadrículas sin fondo GIS.
"""
from pathlib import Path
import argparse
import io
import zipfile
import hashlib
import json
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

MODES = ['car', 'bike', 'pedestrian']
LABELS = {'all': 'Todos los modos', 'car': 'Coches', 'bike': 'Bicicletas', 'pedestrian': 'Peatones'}
METRICS = {
 'trajectory_duration_min': 'Duración del viaje (min)',
 'average_speed_kmh': 'Velocidad media (km/h)',
 'trajectory_distance_km': 'Distancia recorrida (km)',
 'congestion_duration_min': 'Tiempo detenido (min)',
 'copresence_car_percentage': 'Copresencia con coches (%)',
 'copresence_bike_percentage': 'Copresencia con bicicletas (%)',
 'copresence_pedestrian_percentage': 'Copresencia con peatones (%)',
}
SUMMARY = dict(zip(METRICS, ['mean_duration_min','mean_speed_kmh','mean_distance_km','mean_congestion_min','mean_copresence_car_percentage','mean_copresence_bike_percentage','mean_copresence_pedestrian_percentage']))
KEY = ['demand_factor', 'seed', 'run_id']
COLORS = ['#3679a8', '#df9238', '#419477']

def require(frame, columns, source):
    missing = set(columns) - set(frame.columns)
    if missing:
        raise ValueError(f'{source}: faltan columnas {sorted(missing)}')

def load(inputs):
    records = {'trip_results': [], 'simulation_summary': [], 'encounters': []}
    manifest = []
    def add(name, raw):
        basename = name.replace('\\', '/').split('/')[-1]
        kind = next((k for k in records if basename.startswith(k+'_run_') and basename.endswith('.csv')), None)
        if not kind:
            return
        frame = pd.read_csv(io.BytesIO(raw))
        require(frame, KEY, name)
        frame['_source'] = name
        records[kind].append(frame)
        manifest.append({'source': name, 'rows': len(frame), 'sha256': hashlib.sha256(raw).hexdigest()})
    for p in inputs:
        p = Path(p)
        if p.is_dir():
            for csv in sorted(p.rglob('*.csv')):
                add(str(csv), csv.read_bytes())
        elif p.suffix.lower() == '.zip':
            with zipfile.ZipFile(p) as z:
                for name in sorted(z.namelist()):
                    if not name.startswith('__MACOSX/') and name.endswith('.csv'):
                        add(str(p)+'/'+name, z.read(name))
        elif p.is_file():
            add(str(p), p.read_bytes())
        else:
            raise ValueError(f'No existe: {p}')
    out = {}
    for kind, frames in records.items():
        if not frames:
            raise ValueError(f'No se encontraron archivos {kind}_run_*.csv')
        out[kind] = pd.concat(frames, ignore_index=True)
    return out, manifest

def validate(data, expected):
    t,s,e = (data[k] for k in ['trip_results','simulation_summary','encounters'])
    require(t, ['mode', *METRICS], 'viajes')
    require(s, ['mode','run_status','completed_trips','active_agents_total','pending_entries_total','failed_paths_total', *SUMMARY.values()], 'resúmenes')
    require(e, ['encounter_id','agent_1_mode','agent_2_mode','start_x','start_y','duration_s'], 'encuentros')
    for name, df, cols in [('viajes',t,list(METRICS)), ('resúmenes',s,list(SUMMARY.values())), ('encuentros',e,['start_x','start_y','duration_s'])]:
        for col in KEY+cols:
            df[col] = pd.to_numeric(df[col], errors='raise')
            if not np.isfinite(df[col]).all():
                raise ValueError(f'{name}: valores ausentes/no finitos en {col}')
    if not set(t['mode']).issubset(MODES):
        raise ValueError('Modos inesperados en los viajes')
    if s.duplicated(KEY+['mode']).any():
        raise ValueError('Resúmenes duplicados: revise carpetas/ZIP y versiones')
    for _, g in t.groupby(KEY):
        if g['_source'].nunique()!=1:
            raise ValueError('Viajes duplicados en varios archivos para una misma ejecución')
    if e.duplicated(KEY+['encounter_id']).any():
        raise ValueError('Encuentros duplicados')
    base = s[s['mode']=='all'].copy()
    if base.empty or (base['run_status']!='completed').any():
        raise ValueError('Faltan resúmenes globales o hay ejecuciones incompletas')
    for col in ['active_agents_total','pending_entries_total','failed_paths_total']:
        if (base[col]!=0).any():
            raise ValueError(f'Hay ejecuciones con {col} distinto de cero')
    sets = lambda df: set(map(tuple, df[KEY].drop_duplicates().to_numpy()))
    if sets(t)!=sets(base) or not sets(e).issubset(sets(base)):
        raise ValueError('Las ejecuciones de viajes/resúmenes/encuentros no corresponden')
    # Un archivo de encuentros con cabecera y cero filas sí es válido.
    sources = {Path(str(x)).name for x in e['_source'].unique()}
    for _, row in base.iterrows():
        p = str(row['_source']).replace('simulation_summary_run_', 'encounters_run_')
        if p not in data['_encounter_sources']:
            raise ValueError(f'Falta el archivo de encuentros: {p}')
    counts = t.groupby(KEY+['mode']).size()
    for _, row in s.iterrows():
        k = tuple(row[c] for c in KEY)
        n = len(t[(t[KEY]==pd.Series(k,index=KEY)).all(axis=1)]) if row['mode']=='all' else counts.get(k+(row['mode'],),0)
        if n!=row['completed_trips']:
            raise ValueError(f'Número de viajes incoherente: {k}, {row["mode"]}')
    factors = sorted(base['demand_factor'].unique())
    if factors != [1,2,3]:
        raise ValueError(f'Se esperaban factores 1, 2 y 3; encontrados: {factors}')
    seed_sets=[]
    for f,g in base.groupby('demand_factor'):
        if len(g)!=expected or g['seed'].duplicated().any():
            raise ValueError(f'Factor {f}: se esperan {expected} semillas distintas; hay {len(g)} runs')
        seed_sets.append(set(g['seed']))
    if any(x!=seed_sets[0] for x in seed_sets):
        raise ValueError('Los factores no utilizan el mismo conjunto de semillas')
    means = t.groupby(KEY+['mode'])[list(METRICS)].mean().reset_index()
    total = t.groupby(KEY)[list(METRICS)].mean()
    # Copresencia global: excluir agentes del propio modo objetivo.
    for target in MODES:
        col = f'copresence_{target}_percentage'
        total[col] = t[t['mode'] != target].groupby(KEY)[col].mean()
    total = total.reset_index().assign(mode='all')
    means = pd.concat([means,total],ignore_index=True)
    joined=means.merge(s,on=KEY+['mode'],validate='one_to_one')
    if len(joined)!=len(means):
        raise ValueError('Faltan resúmenes por modo')
    for m,sm in SUMMARY.items():
        if not np.allclose(joined[m],joined[sm],atol=2e-6,rtol=0):
            raise ValueError(f'La media de viajes no coincide con el resumen: {m}')
    for m in METRICS:
        if (t[m]<0).any() or (m.startswith('copresence') and (t[m]>100).any()):
            raise ValueError(f'Fuera de rango: {m}')
    return t,e,base,means

def save(fig, out, name):
    for ext in ['png','pdf']:
        fig.savefig(out/f'{name}.{ext}',dpi=300,bbox_inches='tight')
    plt.close(fig)

def boxes(ax, groups, labels):
    bp=ax.boxplot(groups,patch_artist=True,showfliers=False)
    ax.set_xticks(range(1,len(labels)+1),labels)
    for i,(box,values) in enumerate(zip(bp['boxes'],groups)):
        box.set_facecolor(COLORS[i%3]); box.set_alpha(.45)
        # Jitter fijo, independiente de la aleatoriedad de las simulaciones.
        offsets=np.linspace(-.09,.09,len(values))
        ax.scatter(i+1+offsets,values,s=17,c=COLORS[i%3],edgecolors='white',linewidths=.3,zorder=3)
    ax.grid(axis='y',alpha=.25)
    ax.set_axisbelow(True)

def mean_plots(means,out):
    for metric,label in METRICS.items():
        modes=[m for m in MODES if metric!=f'copresence_{m}_percentage']
        fig,axes=plt.subplots(1,len(modes),figsize=(4.2*len(modes),4),squeeze=False)
        for ax,mode in zip(axes[0],modes):
            groups=[means[(means['mode']==mode)&(means.demand_factor==f)].sort_values('seed')[metric].to_numpy() for f in [1,2,3]]
            boxes(ax,groups,['×1','×2','×3']); ax.set_title(LABELS[mode]); ax.set_xlabel('Factor de demanda'); ax.set_ylabel(label)
        fig.suptitle('Distribución de las medias por ejecución',fontsize=13)
        fig.tight_layout(); save(fig,out,metric)
    fig,axes=plt.subplots(1,3,figsize=(12.6,4))
    for ax,metric in zip(axes,list(METRICS)[:2]+['congestion_duration_min']):
        boxes(ax,[means[(means['mode']=='all')&(means.demand_factor==f)].sort_values('seed')[metric].to_numpy() for f in [1,2,3]],['×1','×2','×3'])
        ax.set_ylabel(METRICS[metric]); ax.set_xlabel('Factor de demanda')
    fig.suptitle('Resultados globales: medias por ejecución'); fig.tight_layout(); save(fig,out,'resumen_global')

def legacy(t,out):
    for f,g in t.groupby('demand_factor'):
        folder=out/f'factor_{int(f)}'; folder.mkdir(exist_ok=True)
        for metric,label in METRICS.items():
            modes=[m for m in MODES if metric!=f'copresence_{m}_percentage']
            fig,ax=plt.subplots(figsize=(7,4))
            ax.boxplot([g[g['mode']==m][metric] for m in modes])
            ax.set_xticks(range(1,len(modes)+1),[LABELS[m] for m in modes])
            ax.set_ylabel(label); ax.set_title(f'Factor ×{int(f)} · viajes individuales'); fig.tight_layout(); save(fig,folder,'viajes_'+metric)
            for mode in modes:
                h=g[g['mode']==mode]; seeds=sorted(h.seed.unique())
                fig,ax=plt.subplots(figsize=(10,4))
                ax.boxplot([h[h.seed==seed][metric] for seed in seeds])
                ax.set_xticks(range(1,len(seeds)+1),[str(int(seed)) for seed in seeds])
                ax.tick_params(axis='x',rotation=45); ax.set_xlabel('Semilla'); ax.set_ylabel(label); ax.set_title(f'Factor ×{int(f)} · {LABELS[mode]} · viajes por ejecución')
                fig.tight_layout(); save(fig,folder,f'por_run_{mode}_{metric}')

def encounters(e,base,out,bounds,scale):
    e=e.copy()
    pairs=['bike–car','bike–pedestrian','car–pedestrian']
    e['pair']=['–'.join(sorted([a,b])) for a,b in zip(e.agent_1_mode,e.agent_2_mode)]
    if not set(e['pair']).issubset(pairs):
        raise ValueError('Tipos de pareja inesperados')
    counts=e.groupby(KEY+['pair']).size()
    rows=[]
    for _,r in base.iterrows():
        k=tuple(r[c] for c in KEY)
        row=dict(zip(KEY,k))
        for p in pairs: row[p]=counts.get(k+(p,),0)
        row['total']=sum(row[p] for p in pairs)
        row['episodes_per_trip']=row['total']/r.completed_trips
        rows.append(row)
    result=pd.DataFrame(rows); result.to_csv(out/'encuentros_por_ejecucion.csv',index=False)
    names=['Bicicleta–coche','Bicicleta–peatón','Coche–peatón','Total']
    fig,axes=plt.subplots(1,4,figsize=(15,4))
    for ax,p,name in zip(axes,pairs+['total'],names):
        boxes(ax,[result[result.demand_factor==f].sort_values('seed')[p].to_numpy() for f in [1,2,3]],['×1','×2','×3'])
        ax.set_title(name); ax.set_ylabel('Episodios por ejecución'); ax.set_xlabel('Factor de demanda')
    fig.tight_layout(); save(fig,out,'encuentros_por_pareja')
    fig,ax=plt.subplots(figsize=(6,4)); boxes(ax,[result[result.demand_factor==f].episodes_per_trip.to_numpy() for f in [1,2,3]],['×1','×2','×3'])
    ax.set_ylabel('Episodios / viajes completados'); ax.set_xlabel('Factor de demanda'); fig.tight_layout(); save(fig,out,'encuentros_por_viaje')
    lo,hi=bounds
    e['cell_x']=np.floor(e.start_x+.5).astype(int); e['cell_y']=np.floor(e.start_y+.5).astype(int)
    if not e.cell_x.between(lo,hi).all() or not e.cell_y.between(lo,hi).all():
        raise ValueError('Hay encuentros fuera de los límites del mapa; ajuste --bounds')
    cell=e.groupby(['demand_factor','cell_x','cell_y']).size().rename('episodes_total').reset_index()
    reps=base.groupby('demand_factor').size()
    cell['episodes_mean_per_run']=cell.episodes_total/cell.demand_factor.map(reps)
    cell.to_csv(out/'encuentros_por_celda.csv',index=False)
    top=cell.sort_values(['demand_factor','episodes_total','cell_x','cell_y'],ascending=[True,False,True,True]).groupby('demand_factor').head(5).copy()
    top['share_of_scenario_percent']=100*top.episodes_total/top.demand_factor.map(e.groupby('demand_factor').size())
    top.to_csv(out/'cinco_celdas_principales.csv',index=False)
    grids=[]
    for f in [1,2,3]:
        grid=np.zeros((hi-lo+1,hi-lo+1))
        for _,r in cell[cell.demand_factor==f].iterrows():
            grid[int(r.cell_y)-lo,int(r.cell_x)-lo]=r.episodes_mean_per_run
        grids.append(grid)
    norm=Normalize(vmin=0,vmax=max(1,max(g.max() for g in grids)))
    fig,axes=plt.subplots(1,3,figsize=(13,5),layout='constrained')
    for ax,f,grid in zip(axes,[1,2,3],grids):
        im=ax.imshow(grid,origin='lower',extent=[lo-.5,hi+.5,lo-.5,hi+.5],cmap='YlOrRd',norm=norm,interpolation='nearest')
        ax.set_title(f'Factor ×{f}'); ax.set_xlabel('X (unidades NetLogo)'); ax.set_ylabel('Y (unidades NetLogo)')
    fig.colorbar(im,ax=axes,label='Inicios de encuentros por celda · media por ejecución',shrink=.75)
    fig.suptitle(f'Cuadrícula espacial · lado de celda ≈ {scale:.2f} m · escala común')
    save(fig,out,'mapas_encuentros_comparables')

def main():
    parser=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--inputs',nargs='+',type=Path,default=[Path(__file__).resolve().parent])
    parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'figuras_tfg')
    parser.add_argument('--expected-runs',type=int,default=10)
    parser.add_argument('--bounds',nargs=2,type=int,default=[-16,16],metavar=('MIN','MAX'))
    parser.add_argument('--meters-per-unit',type=float,default=21.39540387800133)
    parser.add_argument('--legacy',action='store_true',help='También genera los boxplots originales de viajes (muchas figuras)')
    args=parser.parse_args()
    if args.expected_runs<2 or args.bounds[0]>=args.bounds[1] or args.meters_per_unit<=0:
        parser.error('Parámetros de repeticiones/escala/límites no válidos')
    data,manifest=load(args.inputs)
    data['_encounter_sources']={r['source'] for r in manifest if Path(r['source']).name.startswith('encounters_run_')}
    t,e,base,means=validate(data,args.expected_runs)
    out=args.output; out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'pdf.fonttype':42})
    means.to_csv(out/'medias_por_ejecucion.csv',index=False)
    means.groupby(['demand_factor','mode'])[list(METRICS)].agg(['mean','std','median','min','max']).to_csv(out/'estadisticas_entre_repeticiones.csv')
    mean_plots(means,out)
    encounters(e,base,out,args.bounds,args.meters_per_unit)
    if args.legacy: legacy(t,out)
    (out/'manifest.json').write_text(json.dumps({'inputs':manifest,'parameters':vars(args)},default=str,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'LEEME_RESULTADOS.txt').write_text('''Las cajas principales resumen medias por ejecución. Cada punto es una ejecución.
Caja: cuartiles 25–75 %, línea: mediana, bigotes: hasta 1,5 RIQ.
Se muestran todos los puntos, incluidos los atípicos, sin duplicarlos.
La copresencia global excluye el modo objetivo del promedio.
Los paneles pueden tener diferentes escalas Y: comparar factores dentro del panel.
Las estadísticas utilizan desviación estándar muestral entre repeticiones.
Las medias se recalculan desde viajes y se contrastan con los resúmenes (tolerancia 0,000002).
Los gráficos legacy, si se solicitan, representan viajes individuales, no medias.
Encuentros: un registro es un episodio, no una persona ni un accidente.
Episodios/viaje no elimina el efecto de las oportunidades de interacción.
Mapas: celda = floor(coordenada inicial + 0,5), origen abajo, sin envoltura.
La intensidad es el total de inicios dividido entre las repeticiones del factor.
Se utiliza una sola escala lineal para los tres mapas, sin saturación a 20.
No representan ocupación, duración de copresencia ni congestión.
El CSV espacial contiene totales y medias. Las cinco celdas se eligen por factor;
no son necesariamente las mismas en los tres escenarios. No se superpone GIS.
Los archivos PNG son de 300 dpi y los PDF permiten exportación vectorial.
manifest.json registra las fuentes y sus hashes para conservar la trazabilidad.
''',encoding='utf-8')
    print(f'Correcto: {len(base)} ejecuciones, {len(t)} viajes, {len(e)} encuentros. Salida: {out.resolve()}')

if __name__=='__main__':
    try:
        main()
    except (ValueError,FileNotFoundError,KeyError,pd.errors.ParserError,pd.errors.EmptyDataError,zipfile.BadZipFile) as exc:
        print(f'ERROR: {exc}',file=sys.stderr)
        sys.exit(1)
