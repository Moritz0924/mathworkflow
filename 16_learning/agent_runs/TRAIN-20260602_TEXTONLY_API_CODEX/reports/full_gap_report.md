# Agent Training Gap Report

- run_id: TRAIN-20260602_TEXTONLY_API_CODEX
- draft: 16_learning/agent_runs/TRAIN-20260602_TEXTONLY_API_CODEX/workspace/09_paper/full_draft.md
- draft_status: existing
- benchmark_source: local prior DB

## Benchmark Sources

- SRC96c94e147798 | 统计评价 | 主成分分析 | card=CARD539e1199b391 | score=0.293970
- SRC350a76b8f19f | 统计评价 | 主成分分析 | card=CARD539e1199b391 | score=0.293970
- SRC0c8fae18caad | 统计评价 | 主成分分析 | card=CARD539e1199b391 | score=0.293970

## Feature Comparison

| metric | sandbox | benchmark_average |
|---|---:|---:|
| chars | 101 | 38960.33 |
| sections | 2 | 0.00 |
| figure_mentions | 0 | 7.67 |
| table_mentions | 0 | 13.33 |
| formula_mentions | 0 | 2.67 |
| validation_mentions | 0 | 27.33 |
| citation_mentions | 0 | 16.67 |

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
