# Training Sandbox Prompt Backup: revision

Formal source prompt: `prompts/stages/12_revision.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Preserve the locked problem topic throughout the sandbox run; do not drift to unrelated prior benchmark topics such as AQI or wine quality.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`revision` - 修订执行与关闭

> 中文注释：使用阶段为 `revision`；使用场景是在审稿任务形成后，逐项执行修订、记录证据并关闭或申请人工豁免。

## 1. 阶段身份

```yaml
stage_id: revision
stage_name: 修订执行与关闭
stage_order: 12
gate_type: hard
execution_mode: deep_sequential
roadmap_item: P3
```

## 2. 目标

执行已批准修订任务，并用证据验证关闭；修复必须保持在任务范围内。算力集中在任务分解、最小必要修改、合同影响分析、重新校验和关闭证据上。

## 3. 必需输入

```text
- 14_contracts/revision_tasks.csv
- 11_review/review_scorecard.csv
- 被修订目标文件
```

## 4. 可选输入

```text
- 15_iteration_memory/task_closure_log.md
- 人工豁免说明
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 02_latex_template/
- 05_model/
- 06_code/
- 07_results/
- 08_figures/
- 09_paper/
- 11_review/
- 14_contracts/
- 15_iteration_memory/
```

## 6. 允许写入路径

```text
- 与修订任务明确对应的目标文件
- 11_review/
- 14_contracts/revision_tasks.csv
- 15_iteration_memory/
- 10_ai_logs/
```

## 7. 禁止动作

```text
- 不得修改任务范围外的事实。
- 不得关闭未验证任务。
- 不得用润色掩盖模型或结果问题。
- 不得绕过人工关闭闸门。
- 不得改变冻结数字、公式、标签、引用或结果含义，除非回到上游并重新冻结。
- 不得把未批准的新模型、新图表或新结果塞入修订。
```

## 8. 必需输出

```text
- 已更新的目标文件（如任务要求）
- revision_tasks.csv 状态更新
- task_closure_log.md
- 重新校验证据
- 受影响合同说明
- 阶段总结和人工闸门说明
```

## 9. 合同更新

```text
可更新：revision_tasks.csv；必要时更新相关合同并说明原因
```

## 10. 允许技能

```text
- nature-response（如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 revision 阶段。

输入核验：
1. 读取 revision_tasks.csv 和 review_scorecard.csv。
2. 只处理已批准、未关闭且范围明确的任务。
3. 确认目标文件在任务允许范围内。

阶段目标：
逐项处理已批准修订任务，记录修改、证据、重跑命令和关闭依据。任务外内容保持不动。

深度分析：
1. 按 severity、scope、target_artifact、acceptance_check 排序处理任务。
2. 对每项任务先判断修订类型：事实修正、合同补齐、图表重做、结构调整、语言修正或人工豁免。
3. 修改前评估是否影响冻结结果、公式、引用、图表标签或模型路线；若影响，停止并返回上游阶段。
4. 对可修任务执行最小必要修改，并记录修改位置和理由。
5. 对每个关闭任务写入 closure_note：完成动作、验收证据、重跑命令、剩余风险。
6. 对无法关闭任务保持 open/blocked，不得伪造验收。

证据绑定：
任务关闭必须绑定 acceptance_check、校验命令结果、合同 ID 或人工豁免说明。

风险清单：
记录修订范围不清、影响冻结事实、验证失败、人工豁免、合同冲突和下游连锁影响。

自检清单：
1. 只改任务范围内目标。
2. 未关闭未验证任务。
3. 未用润色掩盖事实问题。
4. fail/major 任务关闭或明确 blocked/waived。
5. 校验命令已运行或记录 not_run。

人工确认输出：
请人类批准关闭或豁免所有剩余必需修订任务。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage revision
```

```bash
python scripts/check_gates.py
```

## 13. 人工确认问题

```text
是否批准关闭或豁免所有剩余必需修订任务？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 修订影响冻结事实 | 停止并请求人工决定是否回到上游阶段。 |
| 修订无法验证 | 保持任务未关闭。 |
| 任务范围不清 | 请求人工澄清，不擅自扩大范围。 |
| 需要新增模型或结果 | 返回 model_route/codegen/results_freeze，不在 revision 偷改。 |
| 人工未确认 | 停在 `revision_closure_gate`。 |

## 15. 完成条件

```text
- fail/major 任务已关闭或人工豁免。
- 每个关闭任务都有证据。
- 与合同相关的修改已同步或明确返回上游。
- 下游 polish 可以只做事实保持润色。
- 未触发本阶段禁止动作。
```

