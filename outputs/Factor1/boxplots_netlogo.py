"""
Crea box plots a partir de los resultados de varias simulaciones de NetLogo.

Genera dos tipos de graficos:

1. Comparacion entre modos:
   - Una figura por indicador.
   - Car, bike y pedestrian aparecen juntos.
   - Todos los runs se agrupan.

2. Analisis individual por modo:
   - Una figura por indicador y modo.
   - Cada caja representa una simulacion (run_id).

Coloca este archivo en la carpeta principal del modelo
(donde existe la carpeta "outputs") o directamente dentro de "outputs".
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# =============================================================================
# CONFIGURACION
# =============================================================================

METRICS_TO_PLOT = [
    "trajectory_duration_min",
    "average_speed_kmh",
    "trajectory_distance_km",
    "congestion_duration_min",
    "copresence_car_percentage",
    "copresence_bike_percentage",
    "copresence_pedestrian_percentage",
]

# Generar grafico comparando modos.
GENERATE_MODE_COMPARISON = True

# Generar un grafico separado para cada modo.
GENERATE_PER_MODE_PLOTS = True

# Mostrar puntos considerados outliers.
SHOW_OUTLIERS = True

# Abrir las figuras en pantalla.
# Los PNG se guardan siempre.
SHOW_FIGURES = True


METRIC_LABELS = {
    "trajectory_duration_min":
        "Duracion del trayecto (min)",

    "average_speed_kmh":
        "Velocidad media (km/h)",

    "trajectory_distance_km":
        "Distancia del trayecto (km)",

    "congestion_duration_min":
        "Tiempo detenido / congestion (min)",

    "copresence_car_percentage":
        "Copresencia con coches (%)",

    "copresence_bike_percentage":
        "Copresencia con bicicletas (%)",

    "copresence_pedestrian_percentage":
        "Copresencia con peatones (%)",
}


MODE_LABELS = {
    "car": "Coche",
    "bike": "Bicicleta",
    "pedestrian": "Peaton",
}


MODE_ORDER = [
    "car",
    "bike",
    "pedestrian",
]


# Copresencia que no tiene sentido representar para cada modo.
SAME_MODE_COPRESENCE = {
    "car": "copresence_car_percentage",
    "bike": "copresence_bike_percentage",
    "pedestrian": "copresence_pedestrian_percentage",
}


# =============================================================================
# CARGA DE DATOS
# =============================================================================

def find_data_folder() -> Path:
    """
    Busca los CSV en outputs o junto al propio script.
    """

    script_folder = Path(__file__).resolve().parent
    outputs_folder = script_folder / "outputs"

    if outputs_folder.exists():
        return outputs_folder

    return script_folder


def load_trip_results(data_folder: Path) -> pd.DataFrame:
    """
    Lee y une todos los archivos trip_results_run_*.csv.
    """

    csv_files = sorted(
        data_folder.glob("trip_results_run_*.csv")
    )

    if not csv_files:
        raise FileNotFoundError(
            "No se encontro ningun archivo "
            f"trip_results_run_*.csv en {data_folder}"
        )

    frames = []

    for csv_file in csv_files:

        try:
            frame = pd.read_csv(csv_file)

            if not frame.empty:
                frames.append(frame)

        except pd.errors.EmptyDataError:
            print(
                f"AVISO: se ignora archivo vacio: "
                f"{csv_file.name}"
            )

    if not frames:
        raise ValueError(
            "Los archivos encontrados no contienen datos."
        )

    data = pd.concat(
        frames,
        ignore_index=True
    )

    required_columns = {
        "run_id",
        "mode",
        *METRICS_TO_PLOT,
    }

    missing_columns = sorted(
        required_columns - set(data.columns)
    )

    if missing_columns:
        raise ValueError(
            f"Faltan columnas en los CSV: "
            f"{missing_columns}"
        )

    # Mantener solamente los modos analizados.
    data = data[
        data["mode"].isin(MODE_ORDER)
    ].copy()

    print()
    print("==========================================")
    print("DATOS CARGADOS")
    print("==========================================")

    print(
        f"Archivos leidos: {len(csv_files)}"
    )

    print(
        f"Simulaciones: "
        f"{data['run_id'].nunique()}"
    )

    print(
        f"Trayectos totales: {len(data)}"
    )

    print()
    print("Trayectos por simulacion y modo:")

    print(
        data.groupby(
            ["run_id", "mode"]
        ).size()
    )

    print()

    check_copresence_values(data)

    return data


def check_copresence_values(data: pd.DataFrame) -> None:
    """
    Comprueba que los porcentajes de copresencia
    permanezcan entre 0 y 100.
    """

    copresence_columns = [
        "copresence_car_percentage",
        "copresence_bike_percentage",
        "copresence_pedestrian_percentage",
    ]

    for column in copresence_columns:

        over_100 = int(
            (data[column] > 100).sum()
        )

        below_zero = int(
            (data[column] < 0).sum()
        )

        if over_100:
            print(
                f"AVISO: {column} contiene "
                f"{over_100} valor(es) > 100 %."
            )

        if below_zero:
            print(
                f"AVISO: {column} contiene "
                f"{below_zero} valor(es) < 0 %."
            )


# =============================================================================
# COMPARACION ENTRE MODOS
# =============================================================================

def create_mode_comparison_boxplot(
    data: pd.DataFrame,
    metric: str,
    output_folder: Path
) -> None:
    """
    Compara los tres modos de transporte en una misma figura.

    Todos los runs se agrupan para mostrar la distribucion
    global de cada modo.
    """

    plot_data = data.copy()

    # Para indicadores de copresencia eliminamos
    # el modo que coincide con el objetivo.
    if metric == "copresence_car_percentage":
        plot_data = plot_data[
            plot_data["mode"] != "car"
        ]

    elif metric == "copresence_bike_percentage":
        plot_data = plot_data[
            plot_data["mode"] != "bike"
        ]

    elif metric == "copresence_pedestrian_percentage":
        plot_data = plot_data[
            plot_data["mode"] != "pedestrian"
        ]

    if plot_data.empty:
        return

    available_modes = [
        mode
        for mode in MODE_ORDER
        if mode in plot_data["mode"].unique()
    ]

    plt.figure(
        figsize=(9, 6)
    )

    sns.boxplot(
        data=plot_data,
        x="mode",
        y=metric,
        order=available_modes,
        showfliers=SHOW_OUTLIERS,
    )

    plt.title(
        METRIC_LABELS.get(
            metric,
            metric
        )
        + " - comparacion entre modos"
    )

    plt.xlabel(
        "Modo de transporte"
    )

    plt.ylabel(
        METRIC_LABELS.get(
            metric,
            metric
        )
    )

    plt.xticks(
        ticks=range(len(available_modes)),
        labels=[
            MODE_LABELS.get(
                mode,
                mode
            )
            for mode in available_modes
        ]
    )

    plt.grid(
        axis="y",
        alpha=0.25
    )

    plt.tight_layout()

    output_file = (
        output_folder
        / f"boxplot_{metric}_comparison.png"
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    print(
        f"Guardado: {output_file}"
    )

    if SHOW_FIGURES:
        plt.show()

    plt.close()


# =============================================================================
# BOXPLOTS INDIVIDUALES POR MODO
# =============================================================================

def create_per_mode_boxplot(
    data: pd.DataFrame,
    mode: str,
    metric: str,
    output_folder: Path
) -> None:
    """
    Crea un grafico exclusivo para un modo.

    Cada caja corresponde a una simulacion diferente.
    """

    # No representar copresencia con el mismo modo.
    if (
        mode in SAME_MODE_COPRESENCE
        and
        metric == SAME_MODE_COPRESENCE[mode]
    ):
        print(
            f"Omitido: {mode} - {metric} "
            "(copresencia con el mismo modo)"
        )

        return

    mode_data = data[
        data["mode"] == mode
    ].copy()

    if mode_data.empty:
        print(
            f"Sin datos para el modo: {mode}"
        )
        return

    # Orden numerico de los runs.
    run_order = sorted(
        mode_data["run_id"].unique()
    )

    plt.figure(
        figsize=(max(9, len(run_order) * 0.7), 6)
    )

    sns.boxplot(
        data=mode_data,
        x="run_id",
        y=metric,
        order=run_order,
        showfliers=SHOW_OUTLIERS,
    )

    mode_label = MODE_LABELS.get(
        mode,
        mode
    )

    metric_label = METRIC_LABELS.get(
        metric,
        metric
    )

    plt.title(
        f"{metric_label} - {mode_label}"
    )

    plt.xlabel(
        "Simulacion"
    )

    plt.ylabel(
        metric_label
    )

    plt.grid(
        axis="y",
        alpha=0.25
    )

    plt.tight_layout()

    mode_folder = (
        output_folder
        / mode
    )

    mode_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        mode_folder
        / f"boxplot_{mode}_{metric}.png"
    )

    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    print(
        f"Guardado: {output_file}"
    )

    if SHOW_FIGURES:
        plt.show()

    plt.close()


# =============================================================================
# MAIN
# =============================================================================

def main() -> None:

    sns.set_theme(
        style="whitegrid",
        context="notebook"
    )

    data_folder = find_data_folder()

    boxplots_folder = (
        data_folder
        / "boxplots"
    )

    boxplots_folder.mkdir(
        exist_ok=True
    )

    comparison_folder = (
        boxplots_folder
        / "comparison"
    )

    comparison_folder.mkdir(
        exist_ok=True
    )

    data = load_trip_results(
        data_folder
    )

    # -------------------------------------------------------------------------
    # Comparacion global entre modos
    # -------------------------------------------------------------------------

    if GENERATE_MODE_COMPARISON:

        print()
        print(
            "Generando comparaciones entre modos..."
        )

        for metric in METRICS_TO_PLOT:

            create_mode_comparison_boxplot(
                data,
                metric,
                comparison_folder
            )

    # -------------------------------------------------------------------------
    # Un box plot por modo
    # -------------------------------------------------------------------------

    if GENERATE_PER_MODE_PLOTS:

        print()
        print(
            "Generando graficos individuales por modo..."
        )

        for mode in MODE_ORDER:

            for metric in METRICS_TO_PLOT:

                create_per_mode_boxplot(
                    data,
                    mode,
                    metric,
                    boxplots_folder
                )

    print()
    print(
        "Todos los box plots han sido generados."
    )


if __name__ == "__main__":
    main()