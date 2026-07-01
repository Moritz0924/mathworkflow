# Training Sandbox Prompt Backup: compile

Formal source prompt: `prompts/stages/14_compile.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Preserve the locked problem topic throughout the sandbox run; do not drift to unrelated prior benchmark topics such as AQI or wine quality.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

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

编译论文包，并在最终导出前运行结构性门禁。算力集中在编译日志、合同一致性、图表文件、引用标签、未关闭修订、提交格式和最终人工确认风险上。

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
- 不得为通过编译改变数字、公式、标签、引用、模型名或结果含义。
```

## 8. 必需输出

```text
- 编译日志
- 最终提交检查清单
- 门禁报告
- 图表、引用、标签和合同一致性说明
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

输入核验：
1. 检查 main.tex、sections、polish_diff_check.csv、revision_tasks.csv。
2. 检查所有正文引用的图表文件、latex_label、公式标签和 citation key。
3. 确认 polish 阶段没有保护原子变化，revision 没有未关闭 fail/major 任务。

阶段目标：
编译论文包并运行最终结构检查。如发现事实、合同或引用问题，报告并返回上游，不通过删除内容掩盖问题。

深度分析：
1. 运行 LaTeX 编译并保存日志，区分语法/路径问题和事实/合同问题。
2. 检查重复 label、缺失 ref、未登记图表引用、图文件缺失和 TODO/占位文本。
3. 运行合同校验和 gate 检查，汇总 fail/warn。
4. 检查最终提交候选是否仍为中文，图题、表题、图注、表注和可见图中文字是否为中文。
5. 对每个失败项给出返回阶段：figures、paper_draft、revision、polish 或 results_freeze。

证据绑定：
编译通过只说明结构和文件可用，不代表人工最终确认；最终包必须等待 final_submission_gate。

风险清单：
记录编译失败、合同失败、未关闭修订、缺失图表、引用错误、中文字体、提交格式和人工未确认风险。

自检清单：
1. 没有改写事实。
2. 没有删除引用或图表掩盖问题。
3. 编译日志和门禁报告已保存。
4. fail 项已指向上游恢复路径。
5. 校验命令已运行或记录 not_run。

人工确认输出：
请人类批准该编译论文包作为最终提交候选。
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
| 图表或引用缺失 | 返回 figures、paper_draft 或合同修正。 |
| 人工未确认 | 停在 `final_submission_gate`。 |

## 15. 完成条件

```text
- 编译和门禁结果已记录。
- 终稿候选没有 fail 级结构问题，或 fail 已明确返回上游。
- 未通过删除事实、引用或图表掩盖问题。
- 等待或完成最终人工确认。
- 未触发本阶段禁止动作。
```

