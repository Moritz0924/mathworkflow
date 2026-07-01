# 工作流评分器训练报告

- generated_at: 2026-05-24T06:57:21Z
- seed: 20260524
- sample_count: 312
- usable_sample_count: 305
- train_count: 244
- test_count: 61
- family_accuracy: 0.5081967213114754
- max_features_per_label: 2000
- unavailable_reason: none

## 模型族分布

- 统计评价: 105
- 优化决策: 95
- 预测回归: 59
- 机理仿真: 32
- 机器学习: 14
- 其他: 7

## 类别分布

- 线性规划: 41
- 层次分析法: 31
- 拟合模型: 22
- 遗传算法: 18
- 多元回归: 16
- 模糊综合评价: 16
- 相关系数: 16
- 微分方程: 15
- 神经网络: 12
- 主成分分析: 12
- 聚类模型: 11
- 灰色预测: 10
- 方差分析: 8
- 蒙特卡洛 Monte-Carlo 模拟: 8
- 插值: 7
- 模拟退火: 6
- 逻辑回归（logistic regression）: 6
- 图论 floyd 算法: 5
- 动态规划: 4
- 博弈论: 4
- 灰色关联分析: 4
- 排队论: 4
- 蚁群算法: 4
- 优劣解距离法（TOPSIS）: 4
- 元胞自动机: 4
- 因子分析: 4
- 图论 Dijkstra 模型: 3
- 马尔科夫 Markov Model: 3
- 逐步回归: 3
- 典型相关分析: 2
- 粒子群算法: 2
- 时间序列 ARMA: 2
- 小波分析: 2
- 决策树: 1
- 投影寻踪综合评价法: 1
- 支持向量机: 1

## 低样本警告

- 典型相关分析: 2
- 决策树: 1
- 小波分析: 2
- 投影寻踪综合评价法: 1
- 支持向量机: 1
- 时间序列 ARMA: 2
- 粒子群算法: 2

## 抽取失败示例

- SRC18316436842a: `2/模拟退火/基于自适应模拟退火遗传算法的月球软着陆轨道优化.pdf`
- SRC8dc9c811e201: `2/模拟退火/基于蚁群算法的月球软着陆轨迹优化.pdf`
- SRCf83885a6e4f2: `3/3/线性规划/基于SQP方法的常推力月球软着陆轨道优化方法.pdf`
- SRCceadb5b398ca: `3/3/遗传算法/基于自适应模拟退火遗传算法的月球软着陆轨道优化.pdf`
- SRCa432397b14d2: `3/3/遗传算法/基于蚁群算法的月球软着陆轨迹优化.pdf`
- SRC85624e8329ec: `3/3/遗传算法/月球探测器软着陆的最优控制.pdf`
- SRCf09889dca91c: `3/3/遗传算法/登月飞行器软着陆轨道的遗传算法优化.pdf`

## 误分类评估示例

- source_id: SRC1f1a6ffaddb0；真实：统计评价；预测：预测回归；confidence: 1.0
- source_id: SRC6f2ec1407698；真实：统计评价；预测：优化决策；confidence: 0.9999
- source_id: SRC4951d7c947b5；真实：统计评价；预测：预测回归；confidence: 0.9985
- source_id: SRC0363a0bdf887；真实：统计评价；预测：预测回归；confidence: 1.0
- source_id: SRCeacf8de932a4；真实：统计评价；预测：机理仿真；confidence: 1.0
- source_id: SRCc12b92550a71；真实：统计评价；预测：机理仿真；confidence: 0.9986
- source_id: SRCc5945c207845；真实：机器学习；预测：统计评价；confidence: 1.0
- source_id: SRC42db0da28d08；真实：机器学习；预测：统计评价；confidence: 1.0
- source_id: SRC51fc21196706；真实：优化决策；预测：预测回归；confidence: 1.0
- source_id: SRCfc084277c98e；真实：优化决策；预测：统计评价；confidence: 1.0

## 安全说明

- 该评分器只提供模型路由、图表和审稿风险建议。
- 它不得自动修改工作流策略、合同、论文文本或结果。
