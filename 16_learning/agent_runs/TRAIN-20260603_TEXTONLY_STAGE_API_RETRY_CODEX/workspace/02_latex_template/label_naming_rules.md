# 标签命名规则

本文档定义 LaTeX 中各类元素标签（`\label{}`）的统一命名规范，确保与合同系统的可追溯性。

| 元素类型 | 标签前缀 | 示例 | 对应合同 |
|----------|----------|------|----------|
| 章节 | `sec:` | `\label{sec:introduction}` | - |
| 图 | `fig:` | `\label{fig:result_curve}` | `figure_contract.csv` |
| 表 | `tab:` | `\label{tab:param_estimation}` | `figure_contract.csv` |
| 公式 | `eq:` | `\label{eq:main_model}` | `formula_contract.csv` |
| 算法 | `alg:` | `\label{alg:solver}` | - |
| 引用 | `cite:` | `\cite{key2023}` | `citation_contract.csv` |

**使用规则**：
1. 所有图、表和公式的标签必须与对应合同的登记条目名称一致。
2. 章节标签采用英文简写，避免中文重音。
3. 交叉引用统一使用 `\ref{}`，参考文献使用 `\cite{}`。
4. 未在合同中登记的标签不得在论文中出现。
