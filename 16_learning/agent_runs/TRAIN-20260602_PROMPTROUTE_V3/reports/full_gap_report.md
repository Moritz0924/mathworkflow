# Agent Training Gap Report

- run_id: TRAIN-20260602_PROMPTROUTE_V3
- draft: 16_learning/agent_runs/TRAIN-20260602_PROMPTROUTE_V3/workspace/09_paper/full_draft.md
- draft_status: existing
- benchmark_source: local prior DB

## Benchmark Sources

- SRCadd1f8e9f5ab | 预测回归 | 拟合模型 | card=CARD243e877b5fdf | score=0.244858
- SRC936eade783e1 | 预测回归 | 拟合模型 | card=CARD243e877b5fdf | score=0.244858
- SRCc5bda7492d45 | 预测回归 | 拟合模型 | card=CARD243e877b5fdf | score=0.244858

## Feature Comparison

| metric | sandbox | benchmark_average |
|---|---:|---:|
| chars | 3120 | 22127.67 |
| sections | 13 | 0.00 |
| figure_mentions | 1 | 14.33 |
| table_mentions | 0 | 8.67 |
| formula_mentions | 4 | 5.33 |
| validation_mentions | 30 | 34.33 |
| citation_mentions | 0 | 11.00 |

## Gap Findings

- [major] figure_density: Add result-bound figures and register them in the sandbox figure contract before citing them.

## Safety

- This report compares counts, structure signals, and risk patterns only.
- It intentionally does not copy prior-paper text, abstracts, captions, tables, or conclusions.
- Any promotion into the formal workflow must go through contracts, review tasks, and human gates.
