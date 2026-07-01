# 阶段提示词：`latex_template` - LaTeX 模板初始化

> 中文注释：使用阶段为 `latex_template`；使用场景是在建模内容产生前，初始化并核验 LaTeX 论文骨架。

## 1. 阶段身份

```yaml
stage_id: latex_template
stage_name: LaTeX 模板初始化
stage_order: 0
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. 目标

在建模内容产生前创建并核验 LaTeX 论文骨架。

## 3. 必需输入

```text
- workflow_state.yaml
- config/execution_policy.yaml
- templates/ 或 02_latex_template/
```

## 4. 可选输入

```text
- 人工说明
- 上游阶段风险报告
- TASK_PACKET.md 中明确点名的相关文件
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- templates/
- 02_latex_template/
```

## 6. 允许写入路径

```text
- 02_latex_template/
- 10_ai_logs/
```

## 7. 禁止动作

```text
- 不得违反 AGENTS.md 或 config/execution_policy.yaml。
- 不得写入允许写入路径之外的位置。
- 不得虚构数据、结果、引用、公式、图表或人工确认。
- 不得删除合同、日志或审稿文件来让校验通过。
```

## 8. 必需输出

```text
- 允许写入路径中的阶段产物
- 阶段总结
- 风险报告
- 合同更新说明
- 校验状态说明
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

技能输出在写入允许输出、必要时绑定合同并通过校验前，只有建议性质。

## 11. 代理提示词模板

```text
你正在执行 v3.2-MVP 合同驱动数学建模工作流的 latex_template 阶段。

目标：
在建模内容产生前创建并核验 LaTeX 论文骨架。

只使用本文件列出的允许读取路径和允许写入路径。

写入前：
1. 检查必需输入。
2. 检查 workflow_state.yaml 阶段兼容性或明确任务包授权。
3. 检查相关合同要求。
4. 拒绝任何禁止动作。

产出：
1. 本阶段必需产物。
2. 合同更新说明。
3. 校验命令结果或计划校验说明。
4. 风险报告。
5. 人工确认问题。
6. 标准阶段总结。
```

## 12. 校验命令

```bash
python scripts/compile_latex.py
```

```bash
python scripts/check_gates.py --dev-debug
```

## 13. 人工确认问题

```text
模板是否符合目标比赛格式以及页数或章节约束？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 编译失败 | 只修复模板文件并重新运行。格式不确定时，在生成内容前询问人类。 |
| 必需输入缺失 | 记录缺失项，不自行推断；若阻塞下游，则询问人类。 |
| 校验命令不可用 | 标记为计划运行或尚未实现，不得声称通过。 |
| 合同冲突 | 保留合同，报告冲突，并返回拥有该合同的上游阶段。 |

## 15. 完成条件

```text
- 必需输出存在，或阻塞项已明确记录。
- 合同更新说明符合权限。
- 校验命令已运行，或如实记录未运行状态。
- 人工确认问题已给出。
- 完成本阶段不需要任何禁止动作。
```
