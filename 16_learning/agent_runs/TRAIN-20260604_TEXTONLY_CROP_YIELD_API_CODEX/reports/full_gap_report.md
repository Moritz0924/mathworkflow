# Agent Training Gap Report

- run_id: TRAIN-20260604_TEXTONLY_CROP_YIELD_API_CODEX
- draft: 16_learning/agent_runs/TRAIN-20260604_TEXTONLY_CROP_YIELD_API_CODEX/workspace/09_paper/full_draft.md
- draft_status: normalized_from_final_paper.md
- benchmark_source: local prior DB

## Benchmark Sources

- SRCadd1f8e9f5ab | 预测回归 | 拟合模型 | card=CARD243e877b5fdf | score=0.216001
- SRC936eade783e1 | 预测回归 | 拟合模型 | card=CARD243e877b5fdf | score=0.216001
- SRCc5bda7492d45 | 预测回归 | 拟合模型 | card=CARD243e877b5fdf | score=0.216001

## Feature Comparison

| metric | sandbox | benchmark_average |
|---|---:|---:|
| chars | 101 | 22127.67 |
| sections | 2 | 0.00 |
| figure_mentions | 0 | 14.33 |
| table_mentions | 0 | 9.67 |
| formula_mentions | 0 | 5.33 |
| validation_mentions | 0 | 40.00 |
| citation_mentions | 0 | 11.00 |

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
