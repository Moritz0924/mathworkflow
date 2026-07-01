# Agent Training Gap Report

- run_id: TRAIN-20260603_TEXTONLY_STAGE_API_PROMPTSET_CODEX
- draft: 16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_API_PROMPTSET_CODEX/workspace/09_paper/full_draft.md
- draft_status: normalized_from_final_paper.md
- benchmark_source: local prior DB

## Benchmark Sources

- SRCad03b2fb65cc | 预测回归 | 多元回归 | card=CARD60dd60d8f596 | score=0.313034
- SRCfb178d4139ba | 预测回归 | 多元回归 | card=CARD60dd60d8f596 | score=0.313034
- SRC4225edb1178d | 预测回归 | 多元回归 | card=CARD60dd60d8f596 | score=0.313034

## Feature Comparison

| metric | sandbox | benchmark_average |
|---|---:|---:|
| chars | 101 | 30069.67 |
| sections | 2 | 0.00 |
| figure_mentions | 0 | 4.33 |
| table_mentions | 0 | 13.67 |
| formula_mentions | 0 | 1.67 |
| validation_mentions | 0 | 44.67 |
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
