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

执行已批准修订任务，并用证据验证关闭；修复必须保持在任务范围内。

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
```

## 8. 必需输出

```text
- 已更新的目标文件（如任务要求）
- revision_tasks.csv 状态更新
- task_closure_log.md
- 重新校验证据
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
逐项处理已批准修订任务，记录修改、证据、重跑命令和关闭依据。
任务外内容保持不动。
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
| 人工未确认 | 停在 `revision_closure_gate`。 |

## 15. 完成条件

```text
- fail/major 任务已关闭或人工豁免。
- 每个关闭任务都有证据。
- 下游 polish 可以只做事实保持润色。
```
