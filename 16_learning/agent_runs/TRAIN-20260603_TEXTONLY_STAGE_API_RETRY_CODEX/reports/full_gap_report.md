# Agent Training Gap Report

- run_id: TRAIN-20260603_TEXTONLY_STAGE_API_RETRY_CODEX
- draft: 16_learning/agent_runs/TRAIN-20260603_TEXTONLY_STAGE_API_RETRY_CODEX/workspace/09_paper/full_draft.md
- draft_status: existing
- benchmark_source: local prior DB

## Benchmark Sources

- SRC69777a615e69 | 机器学习 | 决策树 | card=CARD3d784a37f4f2 | score=0.364201
- SRCa58b1eab1b4a | 机器学习 | 神经网络 | card=CARD6c9687c45c27 | score=0.274044
- SRC42db0da28d08 | 机器学习 | 神经网络 | card=CARD6c9687c45c27 | score=0.274044

## Feature Comparison

| metric | sandbox | benchmark_average |
|---|---:|---:|
| chars | 2895 | 29817.00 |
| sections | 22 | 0.00 |
| figure_mentions | 2 | 24.67 |
| table_mentions | 0 | 13.67 |
| formula_mentions | 2 | 3.67 |
| validation_mentions | 14 | 33.00 |
| citation_mentions | 4 | 48.00 |

## Gap Findings

- [major] figure_density: Add result-bound figures and register them in the sandbox figure contract before citing them.

## Safety

- This report compares counts, structure signals, and risk patterns only.
- It intentionally does not copy prior-paper text, abstracts, captions, tables, or conclusions.
- Any promotion into the formal workflow must go through contracts, review tasks, and human gates.
