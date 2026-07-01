# 阶段提示词：`intake` - 赛题接收

> 中文注释：使用阶段为 `intake`；使用场景是在收到赛题和附件后，整理题面、附件清单、比赛元数据和缺失信息风险。

## 1. 阶段身份

```yaml
stage_id: intake
stage_name: 赛题接收
stage_order: 1
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. 目标

在不求解问题的前提下，规范化赛题文本、附件清单、比赛元数据和缺失信息风险。

## 3. 必需输入

```text
- workflow_state.yaml
- config/execution_policy.yaml
- 00_problem/inbox/
```

## 4. 可选输入

```text
- 03_data/raw/
- 人工补充的题面文本
- TASK_PACKET.md 中明确点名的相关文件
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 00_problem/
- 03_data/raw/
```

## 6. 允许写入路径

```text
- 00_problem/
- 01_task_analysis/
- 10_ai_logs/
```

## 7. 禁止动作

```text
- 不得求解问题或给出模型结论。
- 不得虚构附件内容。
- 不得跳过扫描版或缺失附件风险。
- 不得写入允许写入路径之外的位置。
```

## 8. 必需输出

```text
- 00_problem/problem_statement.md
- 00_problem/attachments_overview.md
- 01_task_analysis/missing_information.md
- 阶段总结和风险说明
```

## 9. 合同更新

```text
可更新：无
只读：14_contracts/*.csv
```

## 10. 允许技能

```text
- 无
```

## 11. 代理提示词模板

```text
你正在执行 intake 阶段。
目标是整理题面、附件和缺失信息，不做建模求解。
只读写本文件允许的路径。
记录任何 OCR、附件缺失、字段含义不明或比赛元数据缺失风险。
产出题面整理、附件清单、缺失信息报告、校验说明和人工确认问题。
```

## 12. 校验命令

```bash
python scripts/check_gates.py --dev-debug
```

## 13. 人工确认问题

```text
题面和附件清单是否完整？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 题面无法读取 | 记录 OCR 或文本缺失风险，并请求人工补录。 |
| 附件缺失 | 在缺失信息报告中列明，不得虚构。 |
| 格式无法识别 | 只登记文件与风险，等待人工处理。 |
| 阶段锁不匹配 | 停止执行并报告当前 `current_stage`。 |

## 15. 完成条件

```text
- 题面和附件状态已记录。
- 不确定信息已进入 missing_information。
- 未产生任何模型、结果或论文结论。
```
