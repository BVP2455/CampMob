# Rangueil Campus Mobility Simulation

## 1. Overview

This NetLogo model simulates multimodal mobility on the Rangueil campus using GIS transport networks and observed 15-minute inflow/outflow data.

The main operational mode is the **real-flow simulation**, which currently creates:

- Cars
- Bicycles
- Pedestrians

The model also includes general support for buses in the random traffic mode.

Main features:

- Directed multimodal transport graph
- Weighted shortest-path routing
- Real-flow trip generation
- Simplified traffic interactions
- Trip, congestion and speed indicators
- Multimodal copresence analysis
- Multimodal encounter detection
- Encounter heatmap
- Repeated simulation runs
- CSV and PNG exports
- External box-plot generation with Python

## 2. Project Structure

```text
project-folder/
│
├── campus_model.nlogo
├── data/
│   └── 10731/
│       ├── buildings_gross.shp
│       ├── Roads_gross.shp
│       ├── zone.shp
│       ├── Netlogo_nodes.shp
│       ├── osmRoads.shp
│       └── In_Out_15min.geojson
│
├── dataNetlogo/
│   └── flow_counts.csv
│
├── outputs/
│
└── boxplots_netlogo.py
```

The `outputs` folder must exist before running the model.

## 3. Data and Transport Network

The model loads GIS files from:

```text
data/10731/
```

These datasets define:

- Buildings
- Campus zones
- Graph nodes
- Road geometries
- Flow-zone locations

Observed mobility flows are read from:

```text
dataNetlogo/flow_counts.csv
```

Each row contains:

- 15-minute slot
- Zone
- Transport mode
- Direction (`inflow` / `outflow`)
- Number of agents

The real-flow mode currently uses:

```text
car
bike
pedestrian
```

The GIS network is converted into a directed graph formed by `nodes`, `waypoints` and directed `edges`. Each edge stores its length and the transport modes that can use it.

## 4. Routing

The model uses a custom weighted Dijkstra implementation:

```netlogo
shortest-path
```

Routes are calculated using:

```text
road-length
```

as edge weight and are filtered according to the agent transport mode.

The model does **not** currently use the NetLogo `nw` extension.

For real-flow simulations, required zone-to-zone routes are precomputed and stored in:

```netlogo
real-route-cache
```

This avoids recalculating shortest paths for every agent during the simulation.

## 5. Real-Flow Simulation

Initialise a real-flow simulation with:

```netlogo
setup-real-flow-simulation
```

The procedure:

1. Loads the GIS network
2. Loads the flow zones
3. Assigns compatible graph points to each zone
4. Loads flow counts
5. Selects the requested 15-minute slots
6. Precomputes required routes
7. Creates the scheduled trip list

The starting flow slot is controlled by:

```text
selected-flow-slot
```

and the duration by:

```text
simulation-duration-minutes
```

The duration should normally be selected in multiples of 15 minutes.

A useful test configuration is:

```text
selected-flow-slot = 48
simulation-duration-minutes = 15
```

Run the simulation with:

```netlogo
go-real-flow
```

The simulation finishes after the configured flow period has ended and all scheduled and active agents have completed their trips.

## 6. Agent Movement

Agents move through the directed graph following their precomputed route.

The movement model includes simplified:

- Same-segment following
- Safety distance
- Intersection priority
- Roundabout priority
- Deadlock release

Speeds are specified in km/h and converted to NetLogo units per tick.

Important time and scale values include:

```netlogo
seconds-per-tick
meters-per-netlogo-unit
movement-step-size
```

Each agent also receives an individual speed factor from a bounded normal distribution.

## 7. Metrics

When an agent reaches its destination, the model stores:

- Transport mode
- Trajectory duration
- Average speed
- Travelled distance
- Congestion duration
- Low-speed duration
- Intermediate-speed duration
- High-speed duration
- Copresence percentages
- Origin zone
- Destination zone
- Flow slot
- Scheduled spawn time
- Arrival time

Trajectory duration is measured from the moment the agent is actually created in the simulation until it reaches its destination.

## 8. Copresence and Encounters

### Copresence

Copresence measures the percentage of trip time spent near agents of a **different transport mode**.

Same-mode copresence is not counted.

Current distance thresholds are:

```text
Car:        5 m
Bicycle:    3 m
Pedestrian: 2 m
```

### Encounters

Encounter events are recorded separately.

An encounter is created when two agents of **different modes** are within:

```text
5 m
```

Each encounter stores:

- Agent IDs and modes
- Start and end time
- Duration
- Start and end midpoint
- Minimum distance

Encounter data are stored in `completed-encounters` and exported at the end of each run.

## 9. Encounter Heatmap

The model includes a dynamic heatmap based on multimodal encounter locations.

Each patch stores the number of encounter events that started on it:

```netlogo
encounter-count
```

The heatmap is controlled with:

```text
show-encounter-heatmap?
```

Hotter areas represent locations where more multimodal encounters occurred.

The final heatmap can be exported as:

```text
outputs/encounter_heatmap_run_X.png
```

The heatmap is intended as a visual analysis tool. Quantitative encounter analysis should be based on the exported CSV data.

## 10. Multiple Runs and Box Plots

Repeated simulations can be executed using:

```netlogo
run-multiple-simulations
```

The number of repetitions is controlled by:

```text
number-of-runs
```

Each run starts from a fresh simulation state and exports its own results.

The Python script:

```text
boxplots_netlogo.py
```

reads the exported `trip_results_run_*.csv` files and generates box plots for:

- Trajectory duration
- Average speed
- Travelled distance
- Congestion
- Copresence

The script can be used to compare transport modes and repeated simulation runs.

## 11. Outputs

Each run can generate:

### Trip results

```text
outputs/trip_results_run_X.csv
```

One row per completed trip.

### Simulation summary

```text
outputs/simulation_summary_run_X.csv
```

Summary values for:

```text
all
car
bike
pedestrian
```

### Encounter events

```text
outputs/encounters_run_X.csv
```

One row per completed multimodal encounter.

### Encounter heatmap

```text
outputs/encounter_heatmap_run_X.png
```

Final visual representation of encounter concentration.

The run identifier is selected automatically using the next available output number.

## 12. Current Limitations

The main current limitations are:

- The custom Dijkstra implementation does not use a priority queue and may be slower than the NetLogo `nw` extension.
- Some origin/mode combinations may fail to obtain a valid cached route and are counted as `failed_paths`.
- Encounter coordinates are exported as NetLogo `xcor` / `ycor`, not original GIS coordinates.
- Copresence and encounter detection use different distance thresholds.
- Buses are not currently generated in the real-flow mode.
- Traffic rules are simplified and do not represent a full microscopic traffic model.
- The full GIS graph is rebuilt before every batch run, increasing computation time.
- Results for modes with very few agents should be interpreted carefully.

## 13. Quick Start

Recommended sequence:

```text
1. Open the NetLogo model
2. Confirm that the data folders and outputs folder exist
3. Select an active flow slot
4. Set the simulation duration
5. Run setup-real-flow-simulation
6. Check that precomputed trips are greater than zero
7. Run go-real-flow
8. Review the exported CSV and heatmap files
9. Use run-multiple-simulations for repeated experiments
10. Run boxplots_netlogo.py for post-processing
```

## 14. Model Summary

The model converts the Rangueil campus GIS network into a directed multimodal graph and uses observed 15-minute inflow/outflow data to generate scheduled trips. Agents follow weighted shortest paths compatible with their transport mode, interact through simplified mobility rules, and produce trip, congestion, copresence and encounter indicators. Results can be exported for repeated statistical analysis and spatial visualisation.
