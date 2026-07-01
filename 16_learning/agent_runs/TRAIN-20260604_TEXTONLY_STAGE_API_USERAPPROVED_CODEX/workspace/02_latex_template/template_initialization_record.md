# LaTeX 模板初始化记录

## 阶段

- 阶段 ID: latex_template
- 日期: 2026-06-04
- 执行模式: deep_sequential

## 创建的文件

- `02_latex_template/main.tex` — 主文件
- `02_latex_template/sections/00_abstract.tex` — 摘要
- `02_latex_template/sections/01_problem_restatement.tex` — 问题重述
- `02_latex_template/sections/02_assumptions.tex` — 模型假设
- `02_latex_template/sections/03_notations.tex` — 符号说明
- `02_latex_template/sections/04_model.tex` — 模型建立与求解
- `02_latex_template/sections/05_results.tex` — 结果分析
- `02_latex_template/sections/06_evaluation.tex` — 模型评价与改进
- `02_latex_template/sections/07_references.tex` — 参考文献
- `02_latex_template/sections/08_appendix.tex` — 附录

## 中文论文结构说明

模板采用标准数学建模竞赛论文结构：

1. **摘要**：独立页面，包含主要方法、结果和结论，底部附关键词。
2. **问题重述**：用自己的语言复述问题，不直接复制题目原文。
3. **模型假设**：列出建模过程中做出的合理简化假设。
4. **符号说明**：以表格形式集中说明主要符号的含义和单位。
5. **模型建立与求解**：分模型叙述，含公式、算法、求解步骤；公式使用 \eqref{} 引用。
6. **结果分析**：展示数值结果、图表，并进行分析讨论；图表引用遵循 `fig:` 和 `tab:` 命名规则。
7. **模型评价与改进**：总结模型优点、局限性和可能的改进方向。
8. **参考文献**：列出所有引用的文献，引用格式规范。
9. **附录**：包含主要代码、补充数据等。

## 后续合同引用接口

- 摘要中每一句量化论断必须能在 `14_contracts/claim_evidence_map.csv` 中找到对应的 claim_id；数值结果必须在 `result_contract.csv` 中冻结。
- 所有图（`\label{fig:...}`）在引用前必须完成 `figure_contract.csv` 登记且文件存在于 `08_figures/`。
- 所有表（`\label{tab:...}`）的关键数值必须在 `result_contract.csv` 中有依据。
- 所有公式（`\label{eq:...}`）应在 `formula_contract.csv` 中登记，以便审阅追踪。
- 所有引用条目（`\bibitem{...}`）必须在 `citation_contract.csv` 中注册并经过 nature-citation 校验。
- 任意 L a T e X 交叉引用使用 `\ref{}`，无需直接提及合同编号，但作者应确保引用目标合规。

## 编译说明

- 编译器: XeLaTeX（支持中文）
- 文档类: `ctexart`（确保已安装 TeX Live 或 MiKTeX 完整中文支持）
- 推荐编译命令: `xelatex main.tex && xelatex main.tex`
- 注意：子文件通过 `\include` 加载，必须与主文件放在同一级目录的 `sections/` 下。

## 标签命名规则

参见 `label_conventions.md`。
