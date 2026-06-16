# NetLogo Mobility Model - Python Integration

## Main NetLogo file

`campus_netlogo.nlogox`

## Main procedures

### initialize-simulation

Runs:

setup
create.vehicles

This prepares the simulation.

### go

Runs one simulation step.

In the current model:

1 tick = 1 simulated second

Python can call `go` as many times as needed.

### export-results

Exports a simple CSV file to:

outputs/simulation_results.csv

## Input variables

Python can modify these variables before running the simulation:

- `vehicle-speed-kmh`: speed of vehicles in km/h.
- `number-of-vehicles`: number of vehicles created.

Example:

vehicle-speed-kmh = 20
number-of-vehicles = 5

## Suggested Python execution flow

initialize-simulation

Then repeat:

go

as many times as needed.

Finally:

export-results

## Output file

outputs/simulation_results.csv

Current columns:

- sim_time_seconds
- number_of_vehicles
- vehicle_speed_kmh
- total_vehicles

This is a temporary/simple output for testing the Python integration.