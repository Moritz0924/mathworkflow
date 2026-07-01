# 阶段提示词：`compile` - 编译与提交检查

> 中文注释：使用阶段为 `compile`；使用场景是在润色通过后，编译论文包并运行最终结构门禁。

## 1. 阶段身份

```yaml
stage_id: compile
stage_name: 编译与提交检查
stage_order: 14
gate_type: hard
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. 目标

编译论文包，并在最终导出前运行结构性门禁。

## 3. 必需输入

```text
- 02_latex_template/main.tex
- 02_latex_template/sections/
- 14_contracts/polish_diff_check.csv
- 14_contracts/revision_tasks.csv
```

## 4. 可选输入

```text
- 12_submission/submission_checklist.md
- 人工提交格式说明
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 02_latex_template/
- 08_figures/
- 09_paper/
- 11_review/
- 12_submission/
- 14_contracts/
```

## 6. 允许写入路径

```text
- 12_submission/
- 11_review/
- 10_ai_logs/
```

## 7. 禁止动作

```text
- 不得改写论文事实来修复编译。
- 不得删除引用或图表来掩盖合同问题。
- 不得跳过最终提交闸门。
- 不得创建未经人工确认的最终交付。
```

## 8. 必需输出

```text
- 编译日志
- 最终提交检查清单
- 门禁报告
- 阶段总结和人工闸门说明
```

## 9. 合同更新

```text
可更新：无
只读并校验所有必需合同
```

## 10. 允许技能

```text
- 无
```

## 11. 代理提示词模板

```text
你正在执行 compile 阶段。
编译论文包并运行最终结构检查。
如发现事实、合同或引用问题，报告并返回上游，不通过删除内容掩盖问题。
```

## 12. 校验命令

```bash
python scripts/compile_latex.py
```

```bash
python scripts/check_gates.py
```

```bash
python scripts/validate_contracts.py --stage final_export
```

## 13. 人工确认问题

```text
是否批准该编译论文包作为最终提交候选？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| LaTeX 编译失败 | 只修复格式或路径问题；事实问题返回上游。 |
| 合同校验失败 | 回到相应合同生产阶段。 |
| 未关闭修订任务 | 返回 revision。 |
| 人工未确认 | 停在 `final_submission_gate`。 |

## 15. 完成条件

```text
- 编译和门禁结果已记录。
- 终稿候选没有 fail 级结构问题。
- 等待或完成最终人工确认。
```
