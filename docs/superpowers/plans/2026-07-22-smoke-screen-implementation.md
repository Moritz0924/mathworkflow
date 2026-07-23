# Smoke-Screen Solver Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reproducible implementation of the frozen smoke-screen model that evaluates Q1–Q5, produces candidate results, and exports official-template copies without treating those candidates as frozen results.

**Architecture:** The solver is split into pure modules for constants/entities, deterministic motion, target sampling and line-of-sight occlusion, continuous-time interval evaluation, constraints, optimization, and export. `run_all.py` becomes the only entry point; it writes candidate artifacts to `07_results/` and never overwrites the official input templates.

**Tech Stack:** Python 3.9, NumPy 1.26.4, SciPy 1.13.1, Pandas 2.3.3, OpenPyXL 3.1.5, unittest.

## Global Constraints

- Preserve the model frozen by `model_freeze_gate` and all D-IMP-01–D-IMP-24 decisions in `H-EE549FF90321`.
- Q1 uses the fixed 1.5 s release and 3.6 s delay; Q2–Q5 do not inherit those times.
- All formal numeric results remain unfrozen until the later `result_freeze` stage.
- The original `03_data/raw/*.xlsx` templates are read-only; write candidate copies only under `07_results/`.
- Record dependency versions, solver configuration, seeds, commands, and outcomes in `06_code/execution_log.md`.
- Any proposed change to frozen dynamics, occlusion, interval-union accounting, Q5 objective, or Q5 credit assignment must return to ChatGPT as a model revision.

---

### Task 1: Freeze-record synchronization and core domain objects

**Files:**
- Modify: `05_model/model_route.md`, `05_model/assumptions.csv`, `05_model/implementation_contract.md`
- Create: `06_code/src/constants.py`, `06_code/src/entities.py`
- Test: `tests/test_smoke_solver.py`

**Interfaces:**
- Produces `Missile`, `UAV`, `BombPlan`, `BombEvaluation`, and `QuestionResult` immutable data objects.
- Produces official constants and ID lookup maps used by all later modules.

- [ ] Write a failing test that resolves M1, FY1, and the Q1 fixed plan through the public data objects.
- [ ] Verify the test fails because the domain module does not exist.
- [ ] Implement only the constants and immutable data objects needed by that test.
- [ ] Re-run the focused test and then the full test suite.

### Task 2: Deterministic motion, geometry, and continuous-time intervals

**Files:**
- Create: `06_code/src/dynamics.py`, `06_code/src/target_geometry.py`, `06_code/src/occlusion.py`, `06_code/src/intervals.py`
- Test: `tests/test_smoke_solver.py`

**Interfaces:**
- `missile_position(missile_id, t)`, `uav_position(uav_id, heading_rad, speed_mps, t)`, `detonation_point(plan)`, and `smoke_center(plan, t)` return 3D NumPy vectors.
- `target_sample_points(config)` returns a deterministic set of cylinder representative points.
- `line_of_sight_clearance(missile_xyz, target_xyz, smoke_xyz)` returns `(lambda, perpendicular_distance)`.
- `find_true_intervals(predicate, start, end, config)` and `merge_intervals(intervals, tolerance)` implement scan/refine/merge accounting.

- [ ] Add failing tests for Q1 kinematics, line-segment endpoint rules, target-point inclusion, and interval merge behavior.
- [ ] Verify each test fails for its missing behavior.
- [ ] Implement the minimal pure functions to make the focused tests pass.
- [ ] Re-run focused and full tests before proceeding.

### Task 3: Constraints, per-question evaluation, and solver routing

**Files:**
- Create: `06_code/src/constraints.py`, `06_code/src/evaluator.py`, `06_code/src/solvers.py`, `06_code/solver_config.yaml`
- Test: `tests/test_smoke_solver.py`

**Interfaces:**
- `validate_plans(question_id, plans)` returns explicit violations without changing plans.
- `evaluate_plan(plan, missile_id, evaluator_config)` returns a `BombEvaluation` with intervals and duration.
- `evaluate_q1(config)` uses no optimizer.
- `solve_q2`, `solve_q3`, `solve_q4`, and `solve_q5` return candidate plans plus diagnostics and preserve frozen constraints.

- [ ] Add failing tests for Q1 fixed timing, same-UAV release gaps, Q5 prefix use, primary-target-only credit, and positive-coverage feasibility checks.
- [ ] Verify each failure is caused by missing behavior rather than a test typo.
- [ ] Implement the least-complex evaluator and solver route consistent with D-IMP-01–D-IMP-24.
- [ ] Re-run focused and full tests; record seed and configuration values.

### Task 4: Candidate exports, reproducible entry point, and execution evidence

**Files:**
- Modify: `06_code/run_all.py`, `06_code/requirements.txt`, `06_code/execution_log.md`
- Create: `06_code/src/exporters.py`, `07_results/candidate_run_manifest.json`, `07_results/q1_results.csv`, `07_results/q2_results.csv`, `07_results/q3_results.csv`, `07_results/q4_results.csv`, `07_results/q5_results.csv`, `07_results/metrics_summary.csv`, `07_results/result_source_map.csv`
- Test: `tests/test_smoke_solver.py`

**Interfaces:**
- `run_all.py` runs from the workspace root, records versions/configuration/seeds, exits non-zero on failure, and creates candidate result artifacts.
- `export_template_copy(question_id, plans, destination)` copies a read-only official template and leaves unused Q5 calculation fields blank.

- [ ] Add failing tests that candidate exports preserve source templates and leave unused Q5 fields blank.
- [ ] Verify the focused export test fails before exporter implementation.
- [ ] Implement exporter and entry point without registering candidate values as formal `result_contract` rows.
- [ ] Run `06_code/run_all.py` from clean inputs, run the full test suite, validate contracts/gates, and record exact outcomes.
