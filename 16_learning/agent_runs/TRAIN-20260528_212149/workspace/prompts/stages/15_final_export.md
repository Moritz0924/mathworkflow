# 阶段提示词：`final_export` - 最终导出与可选 PPT

> 中文注释：使用阶段为 `final_export`；使用场景是在最终人工闸门确认后，打包提交材料并可选生成展示材料。

## 1. 阶段身份

```yaml
stage_id: final_export
stage_name: 最终导出与可选 PPT
stage_order: 15
gate_type: final
execution_mode: deep_sequential
roadmap_item: P7
```

## 2. 目标

打包最终批准的交付物，并可选地只从已批准论文生成展示材料。

## 3. 必需输入

```text
- 已人工确认的最终论文包
- 11_review/final_submission_checklist.md
- 14_contracts/ 全部最终校验通过
```

## 4. 可选输入

```text
- 人工确认的展示材料需求
- 12_export/pptx/
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 02_latex_template/
- 09_paper/
- 11_review/
- 12_submission/
- 12_export/
- 14_contracts/
```

## 6. 允许写入路径

```text
- 12_submission/
- 12_export/
- 10_ai_logs/
- 11_review/
```

## 7. 禁止动作

```text
- 未经最终人工确认不得导出。
- 不得在导出阶段新增论文事实。
- PPT 不得包含论文外结果。
- 不得跳过最终门禁失败项。
- 不得导出英文正文、英文展示说明或英文图中文字作为最终面向评审材料；必要英文缩写和变量名除外。
```

## 8. 必需输出

```text
- 最终提交包说明
- 可选 PPT 导出目录
- 最终阶段总结
- 最终提交包说明、PPT 文本、图片中文字、图表标题、图例、注释和节点文字必须为中文。
```

## 9. 合同更新

```text
可更新：无
只读：全部最终合同
```

## 10. 允许技能

```text
- nature-paper2ppt（仅终稿后且如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 final_export 阶段。
只打包已批准的最终产物。
如果生成展示材料，必须只来源于已批准论文，且不得新增模型结果或结论。
最终导出物必须面向中文提交：提交说明、PPT、图片、图表和所有可见文字均为中文；图片生成提示词必须明确要求“图片中的文字为中文”。必要英文缩写、变量名、文件名和指标名可以保留。
```

## 12. 校验命令

```bash
python scripts/check_gates.py
```

```bash
python scripts/validate_contracts.py --stage final_export
```

## 13. 人工确认问题

```text
是否只基于已批准论文生成终稿后的展示材料？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 最终闸门未确认 | 停止导出，等待人工确认。 |
| 合同校验失败 | 返回相应上游阶段。 |
| PPT 需求不清 | 只打包论文，不生成展示材料。 |
| 导出文件缺失 | 重新运行编译或打包步骤，不改事实。 |

## 15. 完成条件

```text
- 最终提交包来源明确。
- 可选展示材料不超出已批准论文。
- 所有最终检查和人工确认已记录。
- 最终导出物及其中图片/图表文字已检查为中文。
```
