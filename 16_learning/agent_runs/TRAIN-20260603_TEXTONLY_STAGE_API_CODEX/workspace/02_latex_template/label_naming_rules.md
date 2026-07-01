# 标签命名规则（Label Naming Rules）

本文档定义论文中所有 LaTeX 标签（label）的命名规则，确保可追踪且不冲突。

## 1. 基本前缀

| 类型 | 前缀 | 示例 |
|------|------|------|
| 图   | `fig:` | `\label{fig:model_architecture}` |
| 表   | `tab:` | `\label{tab:notation}` |
| 公式 | `eq:` | `\label{eq:objective}` |
| 算法 | `alg:` | `\label{alg:gradient_descent}` |
| 章节 | `sec:` | `\label{sec:intro}` |
| 附录 | `app:` | `\label{app:code}` |

## 2. 名称组成

- 由前缀、冒号、小写描述组成，单词用下划线分隔，禁止空格、中文或特殊字符。
- 建议使用有实际意义的英文短语，如 `fig:temperature_distribution`。
- 同一类型标签需唯一，不同章节间的同类标签不强制分段号，但推荐包含逻辑层级，如 `tab:model1_params`。

## 3. 合同绑定

- 所有被论文引用的图表、公式、章节标签必须在对应合同（figure_contract.csv, formula_contract.csv, result_contract.csv）中声明。
- 标签名称将成为合同的 `label` 字段值。
- 在 `paper_draft` 阶段生成内容时，严格使用登记的标签。

## 4. 禁止事项

- 不得使用系统保留标签名（如 `fig:`, `tab:` 后直接跟数字）。
- 不得在无合同登记的情况下定义标签（占位符除外）。
- 修订时不得更改已冻结的标签名，除非同步更新所有合同与引用。
