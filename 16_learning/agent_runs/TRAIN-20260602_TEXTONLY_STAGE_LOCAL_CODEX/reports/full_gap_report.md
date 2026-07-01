# Agent Training Gap Report

- run_id: TRAIN-20260602_TEXTONLY_STAGE_LOCAL_CODEX
- draft: 16_learning/agent_runs/TRAIN-20260602_TEXTONLY_STAGE_LOCAL_CODEX/workspace/09_paper/full_draft.md
- draft_status: existing
- benchmark_source: local prior DB

## Benchmark Sources

- SRCad03b2fb65cc | 预测回归 | 多元回归 | card=CARD60dd60d8f596 | score=0.294291
- SRCfb178d4139ba | 预测回归 | 多元回归 | card=CARD60dd60d8f596 | score=0.294291
- SRC4225edb1178d | 预测回归 | 多元回归 | card=CARD60dd60d8f596 | score=0.294291

## Feature Comparison

| metric | sandbox | benchmark_average |
|---|---:|---:|
| chars | 3120 | 30069.67 |
| sections | 13 | 0.00 |
| figure_mentions | 1 | 2.67 |
| table_mentions | 0 | 13.67 |
| formula_mentions | 4 | 1.67 |
| validation_mentions | 30 | 44.67 |
| citation_mentions | 0 | 11.00 |

## Gap Findings

- [major] figure_density: Add result-bound figures and register them in the sandbox figure contract before citing them.

## Safety

- This report compares counts, structure signals, and risk patterns only.
- It intentionally does not copy prior-paper text, abstracts, captions, tables, or conclusions.
- Any promotion into the formal workflow must go through contracts, review tasks, and human gates.
