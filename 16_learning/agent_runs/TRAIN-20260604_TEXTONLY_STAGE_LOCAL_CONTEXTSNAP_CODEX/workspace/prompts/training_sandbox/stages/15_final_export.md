# Training Sandbox Prompt Backup: final_export

Formal source prompt: `prompts/stages/15_final_export.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Preserve the locked problem topic throughout the sandbox run; do not drift to unrelated prior benchmark topics such as AQI or wine quality.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

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

打包最终批准的交付物，并可选地只从已批准论文生成展示材料。算力集中在最终来源核验、包完整性、展示材料不越界、中文可见文字和最终审计记录上。

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
- 不得修改已批准论文来适配展示材料。
```

## 8. 必需输出

```text
- 最终提交包说明
- 可选 PPT 导出目录
- 最终阶段总结
- 最终来源清单和人工确认记录
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

输入核验：
1. 确认最终人工闸门已记录。
2. 检查 final_submission_checklist、最终合同和提交包来源。
3. 若生成展示材料，确认人工明确需要 PPT 或展示材料。

阶段目标：
只打包已批准的最终产物。如果生成展示材料，必须只来源于已批准论文，且不得新增模型结果或结论。

深度分析：
1. 建立最终来源清单：论文 PDF、LaTeX 源、图表文件、提交说明、AI 使用说明、可选 PPT。
2. 检查所有文件是否来自 compile 阶段批准产物或终稿后允许派生产物。
3. 生成 PPT 时只压缩和重组论文已有内容：问题、模型、结果、图表、结论和局限，不新增结果数字或图表论断。
4. 检查所有最终可见文字为中文；必要英文缩写、变量名、文件名和指标名可保留。
5. 记录导出命令、输出路径、缺失文件和人工确认状态。

证据绑定：
最终导出说明必须绑定最终人工确认、门禁报告和合同校验状态；展示材料必须能追溯到最终论文章节或图表。

风险清单：
记录最终闸门未确认、合同失败、PPT 越界、文件缺失、中文文字不合规、提交格式不明和导出失败风险。

自检清单：
1. 最终人工确认已存在。
2. 没有新增论文事实。
3. PPT 不含论文外结果。
4. 最终导出物可见文字为中文。
5. 校验命令已运行或记录 not_run。

人工确认输出：
请人类确认是否只基于已批准论文生成终稿后的展示材料。
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
| 展示材料引入新事实 | 删除新事实，改为引用已批准论文内容。 |
| 导出文件缺失 | 重新运行编译或打包步骤，不改事实。 |

## 15. 完成条件

```text
- 最终提交包来源明确。
- 可选展示材料不超出已批准论文。
- 所有最终检查和人工确认已记录。
- 最终导出物及其中图片/图表文字已检查为中文。
- 未触发本阶段禁止动作。
```

