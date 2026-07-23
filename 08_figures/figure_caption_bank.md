# 正式证据图题与图注库

所有图均由 `06_code/generate_evidence.py` 从冻结包与已登记验证文件重建。

## F001 展示冻结场景的初始几何关系，作为后续轨迹图的空间参照。

图注：单面板：目标、三枚导弹与五架无人机初始位置。 数据来源：00_problem/problem_statement.md;06_code/src/constants.py;07_results/frozen/frozen_manifest.json。几何示意不得被解释为轨迹求解结果。

## F002 Q1 固定策略的释放、起爆与有效遮蔽区间可由冻结记录复现。

图注：单面板：FY1、M1、干扰弹释放点和起爆点。 数据来源：07_results/frozen/q1_results.csv;07_results/frozen/metrics_summary.csv;06_code/src/constants.py。干扰弹曲线仅作空间关系示意，时长以冻结 CSV 为准。

## F003 Q2 冻结方案的有效遮蔽时长高于 Q1 固定策略。

图注：单面板：Q1 与 Q2 的有效区间及对应时长。 数据来源：07_results/frozen/q1_results.csv;07_results/frozen/q2_results.csv;07_results/frozen/metrics_summary.csv。仅比较冻结方案，不声明全局最优。

## F004 Q3 中第 2、3 枚弹的有效时长为零，三弹并集未超过 Q2 主指标。

图注：四行：三枚弹逐项区间及三弹并集；零贡献行保留。 数据来源：07_results/frozen/q3_results.csv;07_results/frozen/metrics_summary.csv。不得省略零贡献行或暗示多弹协同增益。

## F005 Q4 中 FY2、FY3 的有效时长为零，三机并集未超过 Q2 主指标。

图注：四行：FY1–FY3 逐项区间及三机并集；零贡献行保留。 数据来源：07_results/frozen/q4_results.csv;07_results/frozen/metrics_summary.csv。不得将参与投放解释为形成有效遮蔽或额外收益。

## F006 Q5 冻结主方案使用 FY1、FY2、FY5 的第 1 枚弹，分别服务 M1、M2、M3。

图注：二部网络：五架无人机、三枚导弹和三条已使用分配边。 数据来源：07_results/frozen/q5_results.csv;07_results/frozen/metrics_summary.csv。未连边无人机和弹位表示未使用，不得补画。

## F007 Q5 的三枚导弹各有一段正有效遮蔽区间，三段不表示连续联合保护。

图注：三行：M1、M2、M3 的有效遮蔽时间轴。 数据来源：07_results/frozen/q5_results.csv;07_results/frozen/metrics_summary.csv。时间轴间隙必须保留，避免误读为连续保护。

## F008 Q2、Q3、Q4 的冻结主指标相同，Q1 较短。

图注：单面板：Q1–Q4 的 M1 有效遮蔽时长点图。 数据来源：07_results/frozen/metrics_summary.csv。相等的数值不应被解释为因果或协同效果。

## F009 全代表点连续判定结果与两类基线在所列对象上可逐项比较。

图注：单面板：主模型、中心点基线、固定网格基线的散点对照。 数据来源：07_results/frozen/metrics_summary.csv;07_results/result_freeze_validation/baseline_and_sensitivity.csv。基线仅作口径对照，不得当作额外优化结论。

## F010 A08 的 80% 覆盖半径敏感性随问题和导弹而异。

图注：单面板：各对象从全代表点判定到 80% 半径的数值变化。 数据来源：07_results/frozen/metrics_summary.csv;07_results/result_freeze_validation/baseline_and_sensitivity.csv。仅代表已检验的 A08 情景，不外推到其他口径。

## F011 A03、A08、A11 是需要在论文中明确说明的高风险假设或目标口径。

图注：矩阵：时长、分配和结论层面的变化类别。 数据来源：07_results/frozen/metrics_summary.csv;07_results/result_freeze_validation/baseline_and_sensitivity.csv;07_results/result_freeze_validation/q5_assignment_sensitivity.csv。矩阵是验证摘要，不能替代数值表和边界条件。
