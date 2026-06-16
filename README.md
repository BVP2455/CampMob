# Campus Mobility Simulation with NetLogo

This project implements a multi-agent mobility simulation model in NetLogo using real geographic data. The objective is to represent and analyze mobility flows in a university campus environment through a graph-based transport network.

The model loads GIS data, builds a directed graph from road geometries, and simulates different types of mobile agents such as cars, buses, bicycles and pedestrians. Each agent moves through the network according to its transport mode, available routes, speed and basic traffic interaction rules.

## Main Features

* GIS-based map loading using the NetLogo GIS extension.
* Construction of a directed graph from geographic road data.
* Support for multiple mobility modes:

  * Cars
  * Buses
  * Bicycles
  * Pedestrians
* Mode-specific routing based on allowed road types.
* Shortest-path calculation using a Dijkstra-based algorithm.
* Use of intermediate waypoints to preserve road geometry.
* Basic traffic behavior:

  * Safety distance between agents
  * Intersection handling
  * Roundabout priority
  * Waiting time management
* Random route precomputation for simulation efficiency.
* Basic simulation metrics such as generated agents, completed trips and failed paths.

## Project Context

This project was developed as part of a research internship at IRIT and is intended to support a final degree project focused on mobility simulation.

The long-term goal is to integrate real mobility data, including GeoJSON-based datasets and movement observations, in order to calibrate the simulation and analyze different mobility scenarios inside a campus area.

## Technical Overview

The simulation follows this general workflow:

1. Load geographic datasets.
2. Build graph nodes and directed edges.
3. Assign allowed transport modes to each road segment.
4. Create turn connectors between compatible road directions.
5. Detect intersections and roundabout nodes.
6. Precompute valid routes for each transport mode.
7. Generate mobile agents during the simulation.
8. Move agents through the graph while applying traffic rules.
9. Export or analyze simulation results.

## Technologies Used

* NetLogo
* NetLogo GIS extension
* GIS vector data
* Directed graph modeling
* Multi-agent simulation

