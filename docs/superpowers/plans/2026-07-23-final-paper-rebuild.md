# Final Paper Rebuild Implementation Plan

> **For Codex:** Execute this plan task-by-task in the current workspace. Preserve user-owned dirty files, do not advance `final_submission_gate`, and use frozen evidence as the numerical authority.

**Goal:** Rebuild the A-problem contest paper as a validated, evidence-bound 10--14 page XeLaTeX PDF with eight publication-quality Chinese figures.

**Architecture:** Add a thin reproducible publication layer above the frozen result package. One validator checks frozen metrics and model invariants; one figure builder reads only registered evidence and exports the chart suite; one paper builder emits XeLaTeX and compiles it. Tests assert the publication contract before final visual QA.

**Tech Stack:** Python 3.9, pandas, numpy, matplotlib, networkx, XeLaTeX/MiKTeX, Poppler, unittest.

---

### Task 1: Lock publication acceptance tests

**Files:**
- Create: `tests/test_final_paper_build.py`

**Steps:**
1. Add tests for the exact blueprint columns, eight unique figure IDs, and non-empty evidence/risk fields.
2. Add tests requiring PNG/SVG/PDF outputs for every figure and quality scores of at least 4.2.
3. Add tests for model-validation pass status and frozen headline metrics.
4. Add TeX/PDF tests: figures and formulas present, internal audit headings absent, page count 10--14, and no unresolved references.
5. Run the test module and record the expected failures before implementation.

### Task 2: Validate frozen model and results

**Files:**
- Create: `06_code/validate_model_for_paper.py`
- Create: `11_review/final_model_validation.json`
- Create: `11_review/final_model_validation.md`

**Steps:**
1. Load frozen Q1--Q5 result files, metrics, result contracts, and validation scenarios.
2. Recompute interval lengths/unions and compare them against every headline metric.
3. Check Q5 assignment uniqueness and summary aggregation.
4. Quantify seed, grid/tolerance, and A03/A07/A08 sensitivity behavior.
5. Emit machine-readable and human-readable reports; fail the command on any hard inconsistency.

### Task 3: Build the chart blueprint and eight formal figures

**Files:**
- Create: `06_code/build_final_figures.py`
- Create: `08_figures/final_figure_blueprint.csv`
- Create: `08_figures/final_figure_quality.csv`
- Create: `08_figures/final_figures/PF001_model_chain.{png,svg,pdf}`
- Create: `08_figures/final_figures/PF002_scene_los.{png,svg,pdf}`
- Create: `08_figures/final_figures/PF003_q1_q2_comparison.{png,svg,pdf}`
- Create: `08_figures/final_figures/PF004_q3_q4_contribution.{png,svg,pdf}`
- Create: `08_figures/final_figures/PF005_q5_assignment.{png,svg,pdf}`
- Create: `08_figures/final_figures/PF006_q5_intervals.{png,svg,pdf}`
- Create: `08_figures/final_figures/PF007_convergence_stability.{png,svg,pdf}`
- Create: `08_figures/final_figures/PF008_sensitivity.{png,svg,pdf}`
- Modify: `08_figures/active_visual_profile.md`

**Steps:**
1. Correct the active visual profile to “optimization decision + mechanism simulation”.
2. Define publication fonts, line weights, annotation rules, and the two approved palettes.
3. Draw each figure from frozen/registered evidence only; keep Chinese visible text.
4. Export all three formats and score legibility, evidence fidelity, semantic fit, and layout.
5. Reject any figure with total quality below 4.2.

### Task 4: Rebuild the XeLaTeX paper

**Files:**
- Create: `06_code/build_final_paper.py`
- Create: `09_paper/final_submission.tex`
- Create: `09_paper/final_references.bib`
- Replace generated artifact: `12_submission/final_paper.pdf`

**Steps:**
1. Curate the approved paper content from the frozen model, formula, result, claim, and citation contracts.
2. Write a compact contest-facing structure with abstract, assumptions, model, algorithm, Q1--Q5 results, validation, limitations, conclusion, references, and a short result appendix.
3. Insert eight registered figures, roughly seven exact-value tables, and the core formula groups with stable labels.
4. Keep all claims within frozen evidence boundaries and omit internal workflow/revision chapters.
5. Compile twice with XeLaTeX; fail on missing figures, unresolved labels, missing characters, or compilation warnings that affect output.

### Task 5: Automated and visual acceptance

**Files:**
- Create: `11_review/final_pdf_visual_qa.md`
- Create rendered pages under: `tmp/pdfs/final_render/`

**Steps:**
1. Run the publication test module and full repository test suite.
2. Run `scripts/validate_contracts.py --stage finalize` and `scripts/check_gates.py --json` without confirming the human gate.
3. Inspect PDF metadata/text and assert 10--14 pages.
4. Render every page to PNG and create a contact sheet.
5. Inspect all pages, iterate on typography/floats/page breaks, and document the final visual verdict.
6. Deliver the stable `12_submission/final_paper.pdf` path to the user.

