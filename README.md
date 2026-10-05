# CampMob — Rangueil Campus Mobility Simulation

NetLogo model developed for a Software Engineering bachelor's thesis at the University of Seville, following a research internship at IRIT, Toulouse. It combines GIS networks and observed 15-minute mobility counts to simulate **cars, bicycles and pedestrians** on the Rangueil campus.

The model supports random traffic generation and a mode driven by observed flows. It exports trip indicators, multimodal encounters and spatial heatmaps for analysis in Python.

## Main features

- Directed GIS graph with transport-mode permissions.
- Custom Dijkstra routing weighted by edge length, with cached zone-to-zone routes.
- Scheduled trip generation from observed inflow/outflow counts.
- Simplified following, safety-distance, intersection and roundabout rules.
- Travel-time, speed, distance and stopped-time indicators.
- Multimodal copresence, encounter detection and encounter-start heatmaps.
- Repeated experiments, CSV exports and Python figures.

## Data and scripts

| Component | Purpose |
| --- | --- |
| NetLogo model file | Interface, network construction, simulation and exports |
| `data/10731/` | GIS layers and source flow GeoJSON |
| `preprocess_flow_geojson.py` | Conversion of GeoJSON flow profiles into CSV |
| `dataNetlogo/flow_counts.csv` | Mobility counts read by the model |
| `outputs/` | Results exported by simulation runs |
| `boxplots_netlogo.py` | Post-processing and statistical visualisation |

Keep GIS datasets together with their companion files and preserve the relative directory structure. Flow records describe a time slot, zone, mode, direction and count. They are aggregate observations, not individual trajectories or an observed origin–destination matrix.

## Running the model

Use NetLogo to open the model and Python for data preparation and analysis. Keep the data folders beside the model and ensure that `outputs/` exists.

1. Open the NetLogo model.
2. Check that the GIS files and `dataNetlogo/flow_counts.csv` are available. If regenerating the CSV, check the input and output paths in `preprocess_flow_geojson.py` first.
3. Select a flow slot with available observations and set the demand duration.
4. Run `setup-real-flow-simulation` to load the network and counts, prepare compatible routes and schedule trips.
5. Check that trips have been scheduled, then run `go-real-flow` using the model's execution control.
6. Inspect the exported results. Use `run-multiple-simulations` for repeated runs, with the repetition count set through `number-of-runs`.

For the demand window used in the thesis:

```netlogo
set selected-flow-slot 38
set simulation-duration-minutes 15
```

These two settings select the window; the remaining experimental parameters are listed below. A simulation continues beyond the demand window until scheduled and active trips have finished. Trip duration is measured from actual agent creation to arrival, so it differs from total simulation duration.

## Thesis experiments

The final study compares three demand levels while keeping the network and other model settings fixed.

| Parameter | Value |
| --- | --- |
| Flow slot | 38, corresponding to 09:30–09:45 |
| Demand duration | 15 minutes |
| Demand multipliers | 1, 2 and 3 |
| Scheduled trips per run | 139, 278 and 417, respectively |
| Repetitions | 10 per scenario; 30 runs in total |
| Random seeds | 21092026–21092035, reused across scenarios |
| Maximum active agents | 500 |
| Reference speeds | Cars: 18 km/h; bicycles: 15 km/h; pedestrians: 5 km/h |
| Time step | 0.2 seconds |
| Initial state | Empty network |

The thesis reports the final experimental batch. Preliminary runs were used during development and should not be mixed with the final results.

To repeat the study, use the same model version, datasets, seeds and settings. Keep each demand scenario's exports separate and retain its configuration alongside the files. Shared seeds identify corresponding repetitions but do not guarantee identical individual trips when demand changes.

Use `boxplots_netlogo.py` for post-processing, checking its input paths and options against the location of the scenario results. Analyse variability across runs; pooled trip distributions and distributions of run-level means answer different questions.

## Outputs and interpretation

| Output | Contents |
| --- | --- |
| `trip_results_run_X.csv` | One record per completed trip |
| `simulation_summary_run_X.csv` | Global and per-mode indicators |
| `encounters_run_X.csv` | Completed multimodal encounter episodes |
| `encounter_heatmap_run_X.png` | Spatial distribution of encounter starts |

Simulation exports are written under `outputs/`.

**Copresence** measures the percentage of trip time spent near agents of another mode. Distance thresholds depend on the observing agent: 5 m for cars, 3 m for bicycles and 2 m for pedestrians.

**Encounters** are episodes between agents of different modes within 5 m. They are proximity events, not collisions or direct measures of accident risk.

**Heatmaps** count where encounter episodes begin. They represent encounter-start concentration, not occupancy or traffic density. Exported encounter coordinates use the NetLogo coordinate system. For comparisons between scenarios, use consistent spatial bounds, colour scales and aggregation across repetitions.

## Scope and limitations

The experiments assess internal model behaviour under controlled changes in demand. They use one observed time window, start from an empty network and apply simplified destination-assignment and movement rules. The available counts do not independently validate simulated travel times, speeds or encounters, so the results are not predictions of real campus mobility.

Network connectivity and mode permissions constrain feasible routes. Check route and trip-completion diagnostics when changing the data or configuration. Results for modes represented by few trips require particular care.

## Author

Francisco Javier Martos Romero - Software Engineering bachelor's thesis, University of Seville, 2026.

