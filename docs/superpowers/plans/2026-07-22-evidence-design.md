# Frozen Evidence Design Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build reproducible evidence tables, eleven frozen-result figures, and contract bindings for the evidence-design stage.

**Architecture:** A single evidence generator reads only `07_results/frozen/`, frozen validation CSVs, problem constants, and existing contracts. It writes CSV tables and SVG/PNG figures under `08_figures/`, then produces figure and claim contract rows whose IDs point to actual frozen result IDs.

**Tech Stack:** Python 3, Matplotlib, NumPy, repository CSV contracts.

## Global Constraints

- Never read candidate or ready result files as formal figure inputs.
- Preserve and visibly report Q3 bomb 2/3 and Q4 FY2/FY3 zero contributions.
- Use `RF-20260722T114756Z` frozen package and existing `RES-*` result IDs only.
- Do not modify model assumptions, numerical result values, or any human gate.

---

### Task 1: Frozen evidence data builder

**Files:**
- Create: `tests/test_evidence_generation.py`
- Create: `06_code/generate_evidence.py`

**Interfaces:**
- Consumes: frozen metrics and plan CSVs plus validation CSVs.
- Produces: `build_evidence_data(root: Path) -> dict[str, list[dict[str, object]]]`.

- [ ] **Step 1: Write the failing test**

```python
def test_build_evidence_data_preserves_q3_q4_zero_contributions():
    evidence = build_evidence_data(Path.cwd())
    assert [row["duration_s"] for row in evidence["q3_contributions"]] == [2.2381643772125575, 0.0, 0.0]
    assert [row["duration_s"] for row in evidence["q4_contributions"]] == [2.2381643772125575, 0.0, 0.0]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_evidence_generation`

Expected: FAIL because `generate_evidence` does not exist.

- [ ] **Step 3: Write minimal implementation**

```python
def build_evidence_data(root: Path) -> dict[str, list[dict[str, object]]]:
    # Read frozen CSVs only and normalize intervals/durations into figure-ready rows.
    ...
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_evidence_generation`

Expected: PASS with exact frozen zero rows retained.

### Task 2: Figure and table export

**Files:**
- Modify: `06_code/generate_evidence.py`
- Create: `08_figures/tables/T1_parameters.csv` through `08_figures/tables/T9_sensitivity.csv`
- Create: `08_figures/main_figures/F1_initial_3d_scene.svg` through `08_figures/main_figures/F11_assumption_matrix.svg`

**Interfaces:**
- Consumes: `build_evidence_data` output.
- Produces: `generate_artifacts(root: Path) -> list[dict[str, object]]` with real paths and hashes.

- [ ] **Step 1: Write the failing test**

```python
def test_generation_writes_zero_contribution_figures_and_tables(tmp_path):
    artifacts = generate_artifacts(Path.cwd(), output_root=tmp_path)
    assert (tmp_path / "tables" / "T4_q3_contributions.csv").exists()
    assert (tmp_path / "main_figures" / "F4_q3_bomb_intervals.png").exists()
    assert any(item["figure_id"] == "F004" for item in artifacts)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_evidence_generation`

Expected: FAIL because `generate_artifacts` does not exist.

- [ ] **Step 3: Write minimal implementation**

```python
def generate_artifacts(root: Path, output_root: Path) -> list[dict[str, object]]:
    # Export each table and chart with titles, units, source-aware captions, and visual zero rows.
    ...
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_evidence_generation`

Expected: PASS with all required files present.

### Task 3: Contract and visual QA

**Files:**
- Modify: `06_code/generate_evidence.py`
- Modify: `14_contracts/figure_contract.csv`
- Modify: `14_contracts/claim_evidence_map.csv`
- Modify: `08_figures/active_figure_plan.csv`

**Interfaces:**
- Consumes: generated artifacts and existing `RES-*` rows.
- Produces: `write_contracts(root: Path, artifacts: list[dict[str, object]]) -> None`.

- [ ] **Step 1: Write the failing test**

```python
def test_contract_rows_reference_existing_frozen_results_and_files(tmp_path):
    artifacts = generate_artifacts(Path.cwd(), output_root=tmp_path)
    rows = build_contract_rows(Path.cwd(), artifacts)
    assert all(row["result_id"].startswith("RES-") for row in rows["figures"])
    assert {"F004", "F005", "F006"}.issubset({row["figure_id"] for row in rows["figures"]})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_evidence_generation`

Expected: FAIL because contract rows are not built.

- [ ] **Step 3: Write minimal implementation**

```python
def build_contract_rows(root: Path, artifacts: list[dict[str, object]]) -> dict[str, list[dict[str, object]]]:
    # Bind F001-F011 and C001-C010 to frozen sources, result IDs, labels, and limitations.
    ...
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_evidence_generation`

Expected: PASS with actual result IDs and nonempty outputs.

### Task 4: End-to-end verification

**Files:**
- Modify: `08_figures/evidence_generation_report.md`

- [ ] **Step 1: Generate the evidence bundle**

Run: `python 06_code/generate_evidence.py`

Expected: eleven SVG/PNG figures, nine CSV tables, active figure plan, figure contract, claim map, and report.

- [ ] **Step 2: Verify formal outputs**

Run: `python scripts/validate_contracts.py --stage current; python scripts/check_gates.py --json; python -m unittest discover -s tests -p 'test_*.py'`

Expected: no contract failures, no gate failures, and a passing test suite.
