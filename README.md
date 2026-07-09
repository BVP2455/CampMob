# CampusMob with NetLogo

This project is a multi-agent mobility simulation developed in NetLogo.
The goal is to simulate mobility flows on a university campus using GIS data, graph-based routing and different types of agents.

The model is built from shapefiles and represents the campus as a directed graph. Each edge contains information about the transport modes that are allowed to use it.

## Main Features

* GIS-based campus map loading
* Graph construction from shapefiles
* Directed links and mode-specific accessibility
* Four types of agents:
  * cars
  * buses
  * bicycles
  * pedestrians
* Shortest-path routing
* Random origin and destination generation
* Fixed-duration simulation
* Basic congestion behaviours:
  * safety distance
  * waiting time
  * intersection priority
  * roundabout priority
* Integration of real inflow/outflow data using GeoJSON-to-CSV script.

## Simulation Modes

The model currently has two main simulation modes.

## 1. Random Origin/Destination Mode

This mode is mainly used for testing.

Agents are generated with random valid origins and destinations. The model selects graph nodes compatible with the selected transport mode and computes a shortest path between them.

Main procedures:

```netlogo
initialize-simulation
go
```

The `go` button should be used as a forever button.

## 2. Real Flow

## Real Flow Data

The real flow data is originally provided as a GeoJSON file.

This GeoJSON contains measurement points for a full day. Each measurement point corresponds to a specific zone, transport modality and count type (`inflow` or `outflow`). The flow values are aggregated into 15-minute time slots.

The GeoJSON does not provide individual trajectories or origin-destination pairs. It only provides observed counts at measurement points.

A Python preprocessing script is used to extract the flow profiles from the GeoJSON and convert them into a CSV file that can be read more easily by NetLogo.

## Real Flow Model

In the real flow mode, agents are generated from observed inflow counts.

For a selected 15-minute time slot, NetLogo reads the inflow values from the CSV file and creates the corresponding number of agents for each zone and transport mode.

The model then assigns each agent a destination using the available outflow counts for the same transport mode.

Since the GeoJSON does not provide individual origin-destination trajectories, the destination is not directly known.
It is estimated using the outflow distribution and the valid precomputed routes between flow zones.

The main procedures are:

setup-real-flow-simulation
go-real-flow

The setup-real-flow-simulation procedure loads the network, creates the flow zones, loads the CSV flow counts, precomputes valid zone-to-zone routes and prepares the scheduled trips.

The go-real-flow procedure runs the simulation and generates agents according to their scheduled spawn times.

## Real Flow Logic

The real flow simulation follows these steps:

1. Load the campus GIS data
2. Build the graph
3. Load measurement points from the GeoJSON file as flow zones
4. Assign nearby graph nodes to each flow zone according to transport mode and count type
5. Load the 15-minute inflow/outflow counts from the CSV file
6. Precompute valid routes between zones
7. Generate agents according to the observed flows
8. Move agents through the network

For each agent, the destination is selected using the available outflow data for the same transport mode.

## Agent Types

The model supports four transport modes:

* `car`
* `bus`
* `bike`
* `pedestrian`

Each agent can only move through edges where its mode is allowed.

In the current real-flow dataset, the `vehicle` modality is interpreted as `car`.

## Current Status

Implemented:

* GIS loading
* graph construction
* four agent types
* mode-specific routing
* random simulation mode
* fixed simulation duration
* basic congestion behaviours
* real flow data loading
* flow zones
* route precomputation
* scheduled agent generation

Still in progress:

* improving the connection between flow zones and graph nodes
* reducing missing zone-to-zone routes
* exporting congestion metrics
* validating results with real data
* completing technical documentation and diagrams

## Current Limitations

The model is still a prototype.

Some limitations are:

* flow zones are approximated using circular areas
* some routes are still missing for certain transport modes
* real data is aggregated in 15-minute intervals
* congestion is currently represented behaviourally, but quantitative metrics are still being developed

## Future Work

Next steps:

* improve candidate node selection inside flow zones
* improve route precomputation
* reduce failed paths
* export simulation metrics
* define and test mobility scenarios
* complete UML or architecture diagrams
