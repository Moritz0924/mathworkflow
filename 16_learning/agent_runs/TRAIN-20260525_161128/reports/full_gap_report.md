# Agent Training Gap Report

- run_id: TRAIN-20260525_161128
- draft: 16_learning/agent_runs/TRAIN-20260525_161128/workspace/09_paper/final_paper.md
- draft_status: existing
- benchmark_source: local prior DB

## Benchmark Sources

- No prior DB benchmark source was selected.

## Feature Comparison

| metric | sandbox | benchmark_average |
|---|---:|---:|
| chars | 47 | 0.00 |
| sections | 1 | 0.00 |
| figure_mentions | 0 | 0.00 |
| table_mentions | 0 | 0.00 |
| formula_mentions | 0 | 0.00 |
| validation_mentions | 0 | 0.00 |
| citation_mentions | 0 | 0.00 |

## Gap Findings

- [major] structure_depth: Expand the paper structure so problem analysis, model building, results, validation, and conclusion are all visible.
- [major] figure_density: Add result-bound figures and register them in the sandbox figure contract before citing them.
- [major] validation_completeness: Add validation, sensitivity, robustness, or error analysis tied to model outputs.
- [minor] formula_and_model_detail: Make the core model equations and variable definitions explicit.
- [fail] contract_binding: Populate sandbox result_contract and claim_evidence_map before treating draft claims as paper-ready.

## Safety

- This report compares counts, structure signals, and risk patterns only.
- It intentionally does not copy prior-paper text, abstracts, captions, tables, or conclusions.
- Any promotion into the formal workflow must go through contracts, review tasks, and human gates.
