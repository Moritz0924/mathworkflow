# 合同总线模板

合同总线是 v3.2-MVP 的共享事实层。每个阶段都可以创建草稿行，但正式论文只能使用状态为 `ready` 或 `frozen` 的记录。

## 文件说明

| 文件 | 用途 | 主要生产者 | 主要消费者 |
|---|---|---|---|
| `claim_evidence_map.csv` | 将论文论断映射到结果、引用、图表或公式证据 | `paper_draft` | `nature-writing`, `check_gates` |
| `result_contract.csv` | 冻结图表和论文使用的数值/定性结果 | `results_freeze` | `figures`, `paper_draft`, `polish` |
| `figure_contract.csv` | 定义图表论断、证据来源、输出路径和论文使用位置 | `figures` | `nature-figure`, LaTeX, `check_gates` |
| `formula_contract.csv` | 跟踪公式、符号、假设和章节使用位置 | `model_route` | `paper_draft`, `polish` |
| `citation_contract.csv` | 跟踪引用支撑等级和元数据核验状态 | `literature` | `nature-citation`, `paper_draft` |
| `artifact_freeze_registry.csv` | 记录冻结后事实不得改变的产物 | `results_freeze`, `paper_full` | `polish`, final gate |
| `polish_diff_check.csv` | 记录润色后受保护事实原子的变化 | `polish` | `check_gates` |
| `revision_tasks.csv` | 将审稿意见转为可追踪任务 | `auto_review` | `revision`, final gate |
| `data_contract.yaml` | 可选的数据来源和可复现性合同 | `data` | `nature-data`, submission |

## 状态值

使用以下值之一：

- `draft`
- `ready`
- `frozen`
- `blocked`
- `closed`
- `waived`

## 严重程度值

使用以下值之一：

- `fail`
- `major`
- `minor`
- `suggestion`

## 支撑等级

使用以下值之一：

- `strong`
- `partial`
- `background`
- `limiting`
- `metadata_only`
- `none`
