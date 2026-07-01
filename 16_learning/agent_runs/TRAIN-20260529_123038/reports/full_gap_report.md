# Agent Training Gap Report

- run_id: TRAIN-20260529_123038
- draft: 16_learning/agent_runs/TRAIN-20260529_123038/workspace/09_paper/full_draft.md
- draft_status: normalized_from_final_paper.md
- benchmark_source: local prior DB

## Benchmark Sources

- SRC008b3f1bda54 | 预测回归 | 逻辑回归（logistic regression） | card=fallback_manifest | score=0.000000
- SRC00b6137b988d | 统计评价 | 聚类模型 | card=fallback_manifest | score=0.000000
- SRC035d612214a3 | 统计评价 | 层次分析法 | card=fallback_manifest | score=0.000000

## Feature Comparison

| metric | sandbox | benchmark_average |
|---|---:|---:|
| chars | 101 | 30236.67 |
| sections | 2 | 0.00 |
| figure_mentions | 0 | 16.00 |
| table_mentions | 0 | 23.67 |
| formula_mentions | 0 | 1.67 |
| validation_mentions | 0 | 15.67 |
| citation_mentions | 0 | 12.67 |

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
