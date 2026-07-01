# EDA Summary

## Data Scope
Four data tables provided: orders (10,000 records), AGV status (20 AGVs), warehouse map (JSON grid), inventory (500 SKUs). Data snapshot represents a single operational shift (8 hours).

## Key Descriptive Findings
1. **Spatial distribution**: Pick locations are nearly uniform but with a modality near the packing station, suggesting zone-based picking efficiency.
2. **Temporal profile**: Order arrivals peak at hour 2 and hour 6 of the shift; deadlines distribute similarly due to short lead times.
3. **AGV fleet**: 20 heterogeneous vehicles with varying speeds (0.5–2.0 m/s) and battery capacities (5000–10000 mAh). Two AGVs have speed 0, suspected as idle/errors.
4. **Workload**: Average order inter-arrival time ~2.9 seconds, requiring rapid assignment. Total travel distance if single AGV would exceed fleet capacity, justifying need for multi-AGV.
5. **Battery constraints**: Initial battery levels range 30%–95%; moderate consumption expected; charging stations placed at (5,15) and (45,15).

## Model Route Implications
- **Optimization route**: The problem naturally maps to multi-agent path finding (MAPF) with time windows, constraints on battery and capacity. CP-SAT, MILP, or A*-based approaches feasible given moderate fleet size.
- **Simulation/Heuristic route**: Given stochastic order arrivals, a rolling horizon heuristic with conflict resolution may be practical.
- **ML route**: Less suitable; data is deterministic after order release; no complex pattern to learn.
- **Statistical route**: May use to analyze congestion metrics but not primary solver.

## Figures
- No exploratory figures generated. Reasons: 1) Preliminary tables sufficient for initial quality assessment; 2) Graphical exploration deferred to post-cleaning stage; 3) Map visualization depends on confirmed coordinate system.

## Risk Log
- See `04_eda/reproducibility_risks.md`.

## Next Steps
- Human to confirm handling of data anomalies (negative lead time orders, speed=0 AGVs, missing weights).
- After confirmation, proceed to `task_analysis` to formalize problem decomposition.
