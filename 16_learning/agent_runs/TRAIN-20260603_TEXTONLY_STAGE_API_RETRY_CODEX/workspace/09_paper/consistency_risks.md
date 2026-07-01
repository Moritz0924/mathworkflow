# 全文一致性风险说明

1. **图像文件缺失实际内容**：`08_figures/F001_scatter.png` 与 `F002_importance.png` 文件仅含11字节元数据，无法验证图表与论文描述一致。需返回 figures 阶段重新生成。

2. **结果合同缺失**：`14_contracts/result_contract.csv` 未被允许阶段创建（上游 results_freeze 锁定），导致 `claim_evidence_map` 中的 `result_id` 无对应数值支撑。需人工确认或补建合同。

3. **数据来源未固化**：论文引用UCI数据集，但未在 `data_contract.yaml` 或 `00_problem/inbox/` 中提供原始数据文件及预处理脚本，可复现性存疑。

4. **引用未充分核实**：参考文献基于常见文献假设，未通过 `nature-citation` 技能核验，存在虚构风险。

5. **中文术语统一性**：文中“基尼重要性”与“Gini重要性”混用，部分LaTeX命令与中文空格不一致。

6. **图表引用标签**：正文中引用的`F001`和`F002`已在 `figure_contract.csv` 中注册，但实际图像文件不可用，属于高风险。
