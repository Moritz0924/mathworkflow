# Agent Training Gap Report

- run_id: TRAIN-20260604_TEXTONLY_CROP_YIELD_LOCAL_V2_CODEX
- draft: 16_learning/agent_runs/TRAIN-20260604_TEXTONLY_CROP_YIELD_LOCAL_V2_CODEX/workspace/09_paper/full_draft.md
- draft_status: existing
- benchmark_source: local prior DB

## Benchmark Sources

- SRCadd1f8e9f5ab | 预测回归 | 拟合模型 | card=CARD243e877b5fdf | score=0.340844
- SRC936eade783e1 | 预测回归 | 拟合模型 | card=CARD243e877b5fdf | score=0.340844
- SRCc5bda7492d45 | 预测回归 | 拟合模型 | card=CARD243e877b5fdf | score=0.340844

## Feature Comparison

| metric | sandbox | benchmark_average |
|---|---:|---:|
| chars | 3157 | 22127.67 |
| sections | 11 | 0.00 |
| figure_mentions | 6 | 14.33 |
| table_mentions | 0 | 9.67 |
| formula_mentions | 3 | 5.33 |
| validation_mentions | 37 | 40.00 |
| citation_mentions | 0 | 11.00 |

## Gap Findings

- No major structural gap found by the lightweight benchmark checks.

## Safety

- This report compares counts, structure signals, and risk patterns only.
- It intentionally does not copy prior-paper text, abstracts, captions, tables, or conclusions.
- Any promotion into the formal workflow must go through contracts, review tasks, and human gates.
