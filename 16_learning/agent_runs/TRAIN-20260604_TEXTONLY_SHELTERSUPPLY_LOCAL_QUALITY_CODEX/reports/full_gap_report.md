# Agent Training Gap Report

- run_id: TRAIN-20260604_TEXTONLY_SHELTERSUPPLY_LOCAL_QUALITY_CODEX
- draft: 16_learning/agent_runs/TRAIN-20260604_TEXTONLY_SHELTERSUPPLY_LOCAL_QUALITY_CODEX/workspace/09_paper/full_draft.md
- draft_status: existing
- benchmark_source: local prior DB

## Benchmark Sources

- SRC40871b5a0dfa | 优化决策 | 图论Dijkstra模型 | card=CARDbd4d453938cf | score=0.206470
- SRC993662e79f45 | 优化决策 | 图论Dijkstra模型 | card=CARDbd4d453938cf | score=0.206470
- SRCa83d97f8d98c | 优化决策 | 图论Dijkstra模型 | card=CARDbd4d453938cf | score=0.206470

## Feature Comparison

| metric | sandbox | benchmark_average |
|---|---:|---:|
| chars | 22509 | 34444.00 |
| sections | 17 | 1.00 |
| figure_mentions | 17 | 12.33 |
| table_mentions | 34 | 12.00 |
| formula_mentions | 15 | 3.33 |
| validation_mentions | 847 | 5.33 |
| citation_mentions | 0 | 20.00 |

## Gap Findings

- No major structural gap found by the lightweight benchmark checks.

## Safety

- This report compares counts, structure signals, and risk patterns only.
- It intentionally does not copy prior-paper text, abstracts, captions, tables, or conclusions.
- Any promotion into the formal workflow must go through contracts, review tasks, and human gates.
