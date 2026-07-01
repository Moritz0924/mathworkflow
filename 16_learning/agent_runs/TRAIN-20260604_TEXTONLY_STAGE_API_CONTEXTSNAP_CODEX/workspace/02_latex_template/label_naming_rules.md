# LaTeX 标签命名规则

## 前缀约定

| 对象类型 | 前缀 | 示例 | 说明 |
|---------|------|------|------|
| 图 (figure) | `fig:` | `fig:q1_scatter` | 所有图形使用 `fig:` 前缀 |
| 表 (table) | `tab:` | `tab:q1_coefficients` | 所有表格使用 `tab:` 前缀 |
| 公式 (equation) | `eq:` | `eq:linear_model` | 独立成行的公式使用 `eq:` 前缀 |
| 节 (section) | `sec:` | `sec:model_q1` | 章节标签使用 `sec:` 前缀 |
| 算法 (algorithm) | `algo:` | `algo:ridge_cv` | 算法环境使用 `algo:` 前缀 |
| 附录 (appendix) | `apx:` | `apx:code_list` | 附录章节使用 `apx:` 前缀 |

## 命名规则

- 标签中不得出现空格，使用下划线 `_` 连接单词。
- 使用简短且描述性的名称，包含问题编号和对象类型。
- 每个标签在文档内必须唯一。
- 与 `figure_contract.csv`、`formula_contract.csv` 中的 `latex_label` 字段保持一致。

## 合同映射

- 每个图、表、公式标签必须在对应的合同文件中记录。
- 在正文引用时，使用 `\ref{label}` 命令，并在 `claim_evidence_map.csv` 中登记证据。
