# Agent Training Gap Report

- run_id: TRAIN-20260604_TEXTONLY_MEDSUPPLY_LOCAL_QUALITY_CODEX
- draft: 16_learning/agent_runs/TRAIN-20260604_TEXTONLY_MEDSUPPLY_LOCAL_QUALITY_CODEX/workspace/09_paper/full_draft.md
- draft_status: existing
- benchmark_source: local prior DB

## Benchmark Sources

- SRC0fdbfd3f87b3 | 预测回归 | 时间序列ARMA | card=CARD05a952067824 | score=0.205283
- SRCe874b12d08d2 | 预测回归 | 时间序列ARMA | card=CARD05a952067824 | score=0.205283
- SRC40871b5a0dfa | 优化决策 | 图论Dijkstra模型 | card=CARDbd4d453938cf | score=0.196605

## Feature Comparison

| metric | sandbox | benchmark_average |
|---|---:|---:|
| chars | 22481 | 22291.33 |
| sections | 17 | 0.00 |
| figure_mentions | 17 | 11.00 |
| table_mentions | 34 | 6.67 |
| formula_mentions | 15 | 4.00 |
| validation_mentions | 847 | 11.33 |
| citation_mentions | 0 | 18.00 |

## Gap Findings

- No major structural gap found by the lightweight benchmark checks.

## Safety

- This report compares counts, structure signals, and risk patterns only.
- It intentionally does not copy prior-paper text, abstracts, captions, tables, or conclusions.
- Any promotion into the formal workflow must go through contracts, review tasks, and human gates.
