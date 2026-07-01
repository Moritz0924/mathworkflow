# 合同引用接口说明

本模板为后续阶段提供合同绑定接口的说明。当前阶段无权修改 `14_contracts/`，仅声明预期接口。

## 1. 结果引用（result_contract.csv）

- 论文中出现的所有数值、数据点、曲线值、统计检验结果必须源自 `14_contracts/result_contract.csv` 中登记的结果。
- 引用方式：在行文时使用合同编号（如 `R-01`）或通过共同键（如标签）关联。
- 模板中预留 `\cite{}` 等引用命令不得硬编码事例，最终将由写作阶段根据合同填充。

## 2. 图表引用（figure_contract.csv）

- 所有 `\includegraphics{}` 插入的图形以及表格环境，必须在 `figure_contract.csv` 中登记。
- 模板章节中 `fig:` 和 `tab:` 前缀的 `\label{}` 即为图表的合同标签。
- 图表文件存放在 `08_figures/`（或根据具体结构），模板内使用相对路径 `figures/filename.pdf`。

## 3. 公式引用（formula_contract.csv）

- 所有带 `eq:` 标签的公式环境需在 `formula_contract.csv` 中登记公式意义与推导来源。
- 模板不包含具体公式，仅预留 `equation` 和 `align` 等环境注释。

## 4. 引用合同（citation_contract.csv）

- `\cite{}` 命令使用的 BibTeX 键必须在 `citation_contract.csv` 中登记。
- 模板中 `references.bib` 为占位，不得含有未验证的引用条目。

## 5. 论断合同（claim_evidence_map.csv）

- 论文中所有明确论断（如“模型 A 优于模型 B”）需在 `claim_evidence_map.csv` 中记录，并指明支持的证据（结果编号、图表编号）。
- 模板阶段不产生论断，在 `paper_draft` 阶段写作时，每个论据必须可以追溯到合同条目。

---
*本文件由 `latex_template` 阶段生成，无需修改，仅作为接口规范参考。*
