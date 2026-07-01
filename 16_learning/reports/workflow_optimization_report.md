# 工作流优化报告

- generated_at: 2026-05-24T06:57:29Z
- status: suggestion_only
- auto_apply: false
- corpus_samples: 312
- prior_cards: 36
- scorer_available: True

## 建议复核的配置

- [high] `05_model/model_family_weight_config.csv` / 统计评价：复核“统计评价”的章节权重；本地语料中有 105 个样本。
- [high] `08_figures/model_chart_priority_matrix.csv` / 统计评价：保留或复核优先图型：指标体系层级图、权重热力图、综合得分矩阵图、平行坐标/雷达图、排序坡度图。
- [high] `prompts/stages/11_auto_review.md` / 统计评价：审稿器应检查：指标含义不清、权重来源薄弱、排序解释缺少支撑。
- [high] `05_model/model_family_weight_config.csv` / 优化决策：复核“优化决策”的章节权重；本地语料中有 95 个样本。
- [high] `08_figures/model_chart_priority_matrix.csv` / 优化决策：保留或复核优先图型：目标约束结构图、可行域/路径规划图、Pareto 前沿图、调度甘特图、敏感性热力图。
- [high] `prompts/stages/11_auto_review.md` / 优化决策：审稿器应检查：约束不可追踪、目标函数与结果表脱节、缺少敏感性分析。
- [high] `05_model/model_family_weight_config.csv` / 预测回归：复核“预测回归”的章节权重；本地语料中有 59 个样本。
- [high] `08_figures/model_chart_priority_matrix.csv` / 预测回归：保留或复核优先图型：变量关系热力图、趋势分解图、预测区间图、残差诊断组图、误差分布/QQ 图。
- [high] `prompts/stages/11_auto_review.md` / 预测回归：审稿器应检查：缺少残差诊断、缺少预测区间、外推边界不清。
- [high] `05_model/model_family_weight_config.csv` / 机理仿真：复核“机理仿真”的章节权重；本地语料中有 32 个样本。
- [high] `08_figures/model_chart_priority_matrix.csv` / 机理仿真：保留或复核优先图型：机制示意图、状态转移图、仿真轨迹图、参数敏感性曲面、情景对比图。
- [high] `prompts/stages/11_auto_review.md` / 机理仿真：审稿器应检查：假设未连接机理、参数缺少来源、情景验证薄弱。
- [high] `05_model/model_family_weight_config.csv` / 机器学习：复核“机器学习”的章节权重；本地语料中有 14 个样本。
- [high] `08_figures/model_chart_priority_matrix.csv` / 机器学习：保留或复核优先图型：模型结构图、特征重要性图、混淆矩阵、ROC/PR 曲线、消融实验图。
- [high] `prompts/stages/11_auto_review.md` / 机器学习：审稿器应检查：训练/测试划分不清、只报告准确率、缺少可解释性或消融实验。
- [medium] `05_model/model_family_weight_config.csv` / 其他：复核“其他”类别的章节权重；本地语料中有 7 个样本。
- [medium] `prompts/stages/11_auto_review.md` / 其他：审稿器应检查：证据链薄弱、验证章节不足。

## 防护规则

- 不得自动应用这些建议。
- 任何模型路线变更仍然需要 `model_route` 人工闸门。
- Prior cards 和评分器只具有建议性质，不能直接支撑论文论断。
