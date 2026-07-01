# Training Sandbox Prompt Backup: eda

Formal source prompt: `prompts/stages/02_eda.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Preserve the locked problem topic throughout the sandbox run; do not drift to unrelated prior benchmark topics such as AQI or wine quality.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`eda` - 探索性数据分析

> 中文注释：使用阶段为 `eda`；使用场景是在正式建模前检查数据质量、字段含义、分布特征、异常结构、可复现性和描述性风险。

## 1. 阶段身份

```yaml
stage_id: eda
stage_name: 探索性数据分析
stage_order: 2
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. 目标

刻画可用数据，产出谨慎的描述性发现，为模型路由提供依据，但不得形成冻结结果。算力集中在字段画像、数据质量、分布形态、缺失异常、单位口径、可视化探索和复现风险上。

## 3. 必需输入

```text
- workflow_state.yaml
- config/execution_policy.yaml
- 03_data/raw/ 或已登记数据说明
```

## 4. 可选输入

```text
- 00_problem/problem_statement.md
- 00_problem/attachments_overview.md
- 人工字段解释
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 00_problem/
- 03_data/
- 04_eda_code/
```

## 6. 允许写入路径

```text
- 03_data/
- 04_eda/
- 04_eda_code/
- 08_figures/eda_figures/
- 10_ai_logs/
```

## 7. 禁止动作

```text
- 不得把 EDA 输出当作冻结结果。
- 不得写最终结果分析。
- 不得生成正式论文图表引用。
- 不得伪造缺失字段或单位。
- 不得为了建模方便静默删除异常样本。
- 不得在未说明口径时比较不同来源数据。
```

## 8. 必需输出

```text
- 数据字典或字段说明
- 数据质量报告
- EDA 摘要
- 探索性图表或未生成图表的原因
- 可复现性风险说明
- 阶段总结
```

## 9. 合同更新

```text
可更新：data_contract.yaml 草稿（如适用）
只读：其他 14_contracts/*.csv
```

## 10. 允许技能

```text
- nature-data（如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 eda 阶段。

输入核验：
1. 检查数据文件、题面整理和附件概览是否存在。
2. 检查数据读取命令、编码、分隔符、表头、缺失标记和单位说明。
3. 只读写本阶段允许路径。

阶段目标：
描述数据、发现质量风险、为模型路线提供依据；不得把描述性发现写成最终结论。

深度分析：
1. 为每个字段建立画像：类型、单位、缺失率、唯一值、范围、异常值、是否与题面变量对应。
2. 检查样本量、分组结构、时间/空间字段、重复记录、异常记录、量纲混用和数据泄漏风险。
3. 对数值字段做分布、相关、趋势、离群和尺度检查；对类别字段做频数、稀疏类别和编码风险检查。
4. 生成探索性图表时只放入 08_figures/eda_figures/，并标记为 exploratory，不得登记为正式论文图。
5. 明确哪些数据特征支持统计评价、优化决策、预测回归、机理仿真或机器学习路线，哪些路线受限。

证据绑定：
EDA 摘要中的每个描述性发现必须能追溯到数据文件、字段和计算脚本；尚未复核的发现只写成风险或候选。

风险清单：
记录缺失、异常、单位、口径、样本量、数据来源、复现命令、字段解释和图表可用性风险。

自检清单：
1. 未冻结结果。
2. 未写结果分析。
3. 未生成正式论文图表引用。
4. 未静默清洗数据。
5. 校验命令已运行或记录 not_run。

人工确认输出：
请人类确认是否需要先修正数据，再进入 task_analysis 或 model_route。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage current --warn-only
```

## 13. 人工确认问题

```text
EDA 警告是否需要在模型路由前先修正数据或补充字段解释？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 数据文件缺失 | 回到 intake 或请求人工补充。 |
| 字段含义不明 | 标记为风险，不自行猜测。 |
| EDA 代码失败 | 记录失败命令和报错，先修复数据读取。 |
| 图表无法生成 | 保留表格摘要，不晋升为正式图。 |
| 清洗规则不确定 | 写入风险并请求人工确认，不静默处理。 |

## 15. 完成条件

```text
- 数据质量和字段含义风险已记录。
- EDA 产物没有被当作冻结结果。
- 探索性图表未被登记为正式论文图。
- 下游模型路由可以读取本阶段摘要。
- 未触发本阶段禁止动作。
```

