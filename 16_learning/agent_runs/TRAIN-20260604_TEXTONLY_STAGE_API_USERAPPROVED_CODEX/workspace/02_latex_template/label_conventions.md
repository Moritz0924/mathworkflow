# 标签命名规则

| 对象类型 | 前缀  | 示例                | 说明 |
|----------|-------|---------------------|------
| 图       | fig:  | `\label{fig:flowchart}` | 用于 `08_figures` 中的图片 |
| 表       | tab:  | `\label{tab:params}`   | 表格环境内 |
| 公式     | eq:   | `\label{eq:energy_balance}` | 公式环境内 |
| 章节     | sec:  | `\label{sec:model}` | 各节标题后 |
| 算法     | alg:  | `\label{alg:genetic}` | 算法浮动体 |
| 结果     | result: | 可选，用于 result_contract 对应 `\label{result:r001}` | 将合同 ID 映射到 LaTeX 引用 |

## 规则

1. 所有标签必须唯一，不允许重复。
2. 标签只能包含字母、数字、冒号和连字符。
3. 优先使用描述性英文标签，如 `fig:temperature_profile`。
4. 结果标签（`result:`）为可选辅助机制；论文中若采用需保证与 `result_contract.csv` 一致。
5. 不得出现未登记标签，即所有 `\label{}` 对应的对象必须在相应的合同中有记录（图表、公式、结果等）。
6. 标签仅用于交叉引用，不作为论文事实依据。
