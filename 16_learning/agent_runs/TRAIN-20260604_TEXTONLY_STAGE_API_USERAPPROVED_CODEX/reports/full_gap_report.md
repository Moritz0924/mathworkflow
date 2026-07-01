# Agent Training Gap Report

- run_id: TRAIN-20260604_TEXTONLY_STAGE_API_USERAPPROVED_CODEX
- draft: 16_learning/agent_runs/TRAIN-20260604_TEXTONLY_STAGE_API_USERAPPROVED_CODEX/workspace/09_paper/full_draft.md
- draft_status: existing
- benchmark_source: local prior DB

## Benchmark Sources

- SRCadd1f8e9f5ab | 预测回归 | 拟合模型 | card=CARD243e877b5fdf | score=0.317191
- SRC936eade783e1 | 预测回归 | 拟合模型 | card=CARD243e877b5fdf | score=0.317191
- SRCc5bda7492d45 | 预测回归 | 拟合模型 | card=CARD243e877b5fdf | score=0.317191

## Feature Comparison

| metric | sandbox | benchmark_average |
|---|---:|---:|
| chars | 2825 | 22127.67 |
| sections | 15 | 0.00 |
| figure_mentions | 4 | 14.33 |
| table_mentions | 1 | 9.67 |
| formula_mentions | 3 | 5.33 |
| validation_mentions | 34 | 40.00 |
| citation_mentions | 4 | 11.00 |

## Gap Findings

- No major structural gap found by the lightweight benchmark checks.

## Safety

- This report compares counts, structure signals, and risk patterns only.
- It intentionally does not copy prior-paper text, abstracts, captions, tables, or conclusions.
- Any promotion into the formal workflow must go through contracts, review tasks, and human gates.
