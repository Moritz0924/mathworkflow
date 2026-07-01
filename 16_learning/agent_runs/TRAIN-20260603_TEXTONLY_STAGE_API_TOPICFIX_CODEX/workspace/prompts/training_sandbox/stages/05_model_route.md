# Training Sandbox Prompt Backup: model_route

Formal source prompt: `prompts/stages/05_model_route.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Preserve the locked problem topic throughout the sandbox run; do not drift to unrelated prior benchmark topics such as AQI or wine quality.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`model_route` - 模型族路由

> 中文注释：使用阶段为 `model_route`；使用场景是在任务拆解和数据检查后，为各子问题选择主模型、备选模型、变量、公式路线和验证方案。

## 1. 阶段身份

```yaml
stage_id: model_route
stage_name: 模型族路由
stage_order: 5
gate_type: hard
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. 目标

根据可行性、数据状态和评分风险，为每个子问题选择模型族和备选方案。算力集中在题型-数据-模型适配、可解释性、复现难度、结果可验证性、图表表达潜力和人工确认点上。

## 3. 必需输入

```text
- 01_task_analysis/task_decomposition.md
- 01_task_analysis/problem_model_profile.csv
- 03_data/data_quality_report.md
```

## 4. 可选输入

```text
- 13_prior_db/pre_solve_cards.md
- 04_eda/eda_summary_for_paper.md
- 人工模型偏好或约束
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 00_problem/
- 01_task_analysis/
- 03_data/
- 04_eda/
- 13_prior_db/
- 14_contracts/
```

## 6. 允许写入路径

```text
- 05_model/
- 14_contracts/formula_contract.csv
- 10_ai_logs/
- 11_review/
```

## 7. 禁止动作

```text
- 不得在人工确认前冻结模型路线。
- 不得生成求解代码。
- 不得把先验卡片当作答案。
- 不得选择数据无法支撑的模型而不标风险。
- 不得为追求复杂度选择不可复现或不可解释模型。
- 不得登记尚未定义符号的重要公式。
```

## 8. 必需输出

```text
- 05_model/model_route.md
- 05_model/fallback_plan.md
- 05_model/symbols.md 或等价符号说明
- 每个子问题的主模型、备选模型、验证方案和图表表达建议
- 14_contracts/formula_contract.csv 草稿行（如有重要公式）
- 阶段总结和人工闸门说明
```

## 9. 合同更新

```text
可更新：14_contracts/formula_contract.csv
只读：其他合同
```

## 10. 允许技能

```text
- 无；Prior DB 只能作为已归档经验输入
```

## 11. 代理提示词模板

```text
你正在执行 model_route 阶段。

输入核验：
1. 检查 task_decomposition、problem_model_profile 和 data_quality_report。
2. 若允许读取路径中存在 13_prior_db/pre_solve_cards.md 或 13_prior_db/cards/prior_cards.jsonl，可读取抽象经验；不得读取未授权路径。
3. 确认当前阶段需要人工硬闸门，模型路线不得自动冻结。

阶段目标：
为每个子问题选择主模型和备选模型，说明数据适配性、可解释性、复现性、风险和人工确认点；不得生成代码或论文结果。

深度分析：
1. 对每个子问题建立候选路线矩阵：模型族、输入变量、输出指标、核心假设、公式对象、可验证性、复现成本、失败后备选。
2. 使用题目和 EDA 优先原则：数据不能支撑的模型不得作为主模型；先验卡片只能提醒常见路线和评分风险。
3. 针对模型族做专业判断：
   - 统计评价：指标体系、权重来源、排序稳定性和敏感性。
   - 优化决策：决策变量、目标函数、约束、基线方案和可行性。
   - 预测回归：特征选择、误差指标、残差诊断、外推边界和预测区间。
   - 机理仿真：状态变量、参数来源、情景设定、稳定性和敏感性。
   - 机器学习：训练/验证划分、数据泄漏、解释性、泛化风险和可复现种子。
4. 为每个重要公式登记 formula_contract 草稿：formula_id、question_id、symbols_defined、derivation_source、validation_note。
5. 为 figures 阶段预留图表表达建议，但不生成正式图。

证据绑定：
每个模型选择必须绑定子问题 ID、数据字段、EDA 发现、先验卡片 ID 或人工约束；无法绑定的路线降级为备选或 blocked。

风险清单：
记录数据不匹配、变量缺失、假设过强、模型不可复现、公式符号不清、图表表达不足和人工确认需求。

自检清单：
1. 未生成代码。
2. 未写结果。
3. 未把先验当答案。
4. 每个主模型都有备选模型。
5. 重要公式已登记或说明暂不登记。
6. 校验命令已运行或记录 not_run。

人工确认输出：
请人类批准每个子问题的模型族、备选方案和不可接受风险。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage current --warn-only
```

## 13. 人工确认问题

```text
是否批准每个子问题的模型族、备选方案、核心假设和失败降级路线？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 模型与数据不匹配 | 降级为更稳健的备选方案并说明原因。 |
| 关键变量缺失 | 返回数据或任务分析阶段补齐。 |
| 公式无法解释 | 不写入公式合同，先补模型说明。 |
| 先验提示冲突 | 优先题面和数据，将先验冲突写为风险。 |
| 人工未确认 | 停在 `model_route_gate`。 |

## 15. 完成条件

```text
- 每个子问题有主模型、备选模型、验证方案和风险说明。
- 重要公式已登记或说明暂不登记。
- 模型路线不依赖历史论文答案。
- 等待或完成人工模型路线确认。
- 未触发本阶段禁止动作。
```

