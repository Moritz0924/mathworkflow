# 数学建模工作流 v3.2-MVP 快速上手

这份教程面向第一次使用本仓库的人。它只讲正式比赛流程里最常用、最不容易走错的路径：按 `deep_sequential` 单阶段推进，先产出真实模型和合同记录，再写图表与论文。

## 1. 先记住三条铁律

1. 只运行当前阶段：状态由 `workflow_state.yaml` 控制，后续阶段默认锁定。
2. 先有合同再写论文：结果、图、公式、引用、正式论断都要落到 `14_contracts/`。
3. 人工闸门不能跳：遇到 `pending_gate` 时，先人工检查产物，再运行确认命令。

这套工作流不是“一键生成全文”，而是一个可追踪的建模生产线。

## 2. 准备环境

在项目根目录执行：

```bash
python -m pip install -r requirements.txt
```

快速检查核心脚本能否被 Python 解析：

```bash
python -m py_compile scripts/workflow_utils.py scripts/run_current_stage.py scripts/validate_contracts.py scripts/check_gates.py
```

如果需要编译 LaTeX，另行确认本机已经安装可用的 TeX 发行版；仓库脚本只负责调用和检查，不负责安装 TeX。

## 3. 放入赛题和数据

把赛题文件放到：

```text
00_problem/inbox/
```

把原始附件数据放到：

```text
03_data/raw/
```

推荐同时提供一份文字版赛题，例如 `.txt` 或 `.md`。如果只有扫描版 PDF 或图片，自动抽取可能不可靠，需要人工补齐题面文字。

## 4. 看当前阶段

先打开 `workflow_state.yaml`，重点看这几个字段：

```yaml
execution_mode: deep_sequential
allow_parallel: false
current_stage: latex_template
pending_gate: null
completed_stages: []
locked_stages:
  - intake
  - eda
  - task_analysis
```

含义很简单：

- `current_stage`：现在只能跑这一阶段。
- `locked_stages`：暂时不能跑的阶段。
- `pending_gate`：如果不是 `null`，说明需要人工确认后才能继续。
- `completed_stages`：已经完成的阶段。

不要手动把后续阶段解锁；让脚本根据阶段完成情况推进。

## 5. 正式运行一个阶段

正式入口优先使用：

```bash
python scripts/run_current_stage.py
```

它会读取 `workflow_state.yaml` 中的 `current_stage`，运行对应脚本，并在阶段完成后自动更新状态。

常见阶段顺序如下：

```text
latex_template
intake
eda
task_analysis
prior_retrieval
model_route
codegen
results_freeze
figures
paper_draft
paper_full
auto_review
revision
polish
compile
final_export
```

有些阶段支持附加参数：

```bash
python scripts/run_current_stage.py --question Q1
python scripts/run_current_stage.py --section 06_model_q1
```

`--question` 主要用于 `codegen` 阶段，`--section` 主要用于 `paper_draft`、`paper_full`、`polish` 阶段。

## 6. 每阶段跑完后看哪里

阶段脚本会把阶段总结写到：

```text
11_review/<stage>_stage_summary.md
```

建议每次跑完都检查三件事：

- 当前阶段产物是否真的生成。
- 阶段总结里有没有风险、占位符或缺失项。
- `workflow_state.yaml` 是否进入下一阶段，或者停在人工闸门。

核心产物位置如下：

| 阶段 | 主要产物 |
|---|---|
| `latex_template` | `02_latex_template/main.tex`、`02_latex_template/sections/*.tex` |
| `intake` | `00_problem/problem_statement.md`、`00_problem/attachments_overview.md` |
| `eda` | `03_data/data_dictionary.csv`、`03_data/data_quality_report.md`、`04_eda/` |
| `task_analysis` | `01_task_analysis/task_decomposition.md`、`01_task_analysis/problem_model_profile.csv` |
| `model_route` | `05_model/model_route.md`、`14_contracts/formula_contract.csv` |
| `codegen` | `06_code/`、`07_results/` 中的真实模型输出 |
| `results_freeze` | `07_results/result_freeze_report.md`、`14_contracts/result_contract.csv` |
| `figures` | `08_figures/`、`14_contracts/figure_contract.csv` |
| `paper_draft` / `paper_full` | `02_latex_template/sections/*.tex`、`09_paper/` |
| `auto_review` / `revision` | `11_review/*_reviewer_comments.md`、`14_contracts/revision_tasks.csv` |
| `polish` | 润色后的 LaTeX 章节、`14_contracts/polish_diff_check.csv` |
| `compile` | 编译后的论文包和终稿检查报告 |

## 7. 人工闸门怎么过

以下阶段完成后会停下来等待人工确认：

| 阶段 | 闸门名 | 人工要确认什么 |
|---|---|---|
| `model_route` | `model_route_gate` | 模型路线、变量、公式和风险是否合理 |
| `results_freeze` | `results_freeze_gate` | 模型是否真实运行，结果是否可复核，`result_contract.csv` 是否完整 |
| `paper_full` | `draft_review_gate` | 全文是否有事实跳跃，图表/结果/引用是否可追踪 |
| `revision` | `revision_closure_gate` | fail/major 修订任务是否关闭或被人工豁免 |
| `compile` | `final_submission_gate` | 终稿、合同、审稿分数和提交包是否满足最终门禁 |

当你人工检查通过后，运行对应确认命令。例如：

```bash
python scripts/confirm_gate.py model_route_gate
```

确认后脚本会解锁下一阶段。不要用 `--dev-debug` 绕过正式闸门。

## 8. 合同总线怎么用

`14_contracts/` 是整套工作流的事实来源。论文里出现的正式内容，都要能在这里找到对应记录。

最常用的文件：

- `result_contract.csv`：论文会使用的数值结果和模型输出。
- `figure_contract.csv`：论文会引用的图，必须有真实文件路径。
- `claim_evidence_map.csv`：每条正式论断对应哪些结果、图、公式或引用。
- `formula_contract.csv`：重要公式、符号和使用章节。
- `citation_contract.csv`：参考文献支撑关系和元数据验证。
- `artifact_freeze_registry.csv`：冻结后的产物，润色不能改动其事实原子。
- `polish_diff_check.csv`：润色是否改变数字、公式、label/ref、引用等受保护内容。
- `revision_tasks.csv`：审稿意见转成可关闭的任务。

进入关键阶段前可以单独检查合同：

```bash
python scripts/validate_contracts.py --stage figures
python scripts/validate_contracts.py --stage paper_draft
python scripts/validate_contracts.py --stage polish
```

如果校验失败，先补合同或补真实产物，再继续跑阶段。

## 9. 图表、论文和润色的安全顺序

推荐顺序是：

```text
真实代码运行
→ 结果写入 result_contract.csv
→ 冻结结果
→ 图表写入 figure_contract.csv
→ 论断写入 claim_evidence_map.csv
→ 分章节生成论文
→ 审稿与修订
→ 事实保护润色
→ 编译与最终门禁
```

不要在 `result_contract.csv` 为空时写结果分析。不要在 `figure_contract.csv` 没有登记且文件不存在时引用图。不要让润色阶段改变数字、公式、模型名、图表编号或引用含义。

## 10. Prior DB 和 nature-skills 的用法边界

Prior DB 只能当经验教练：

- 求解前只能输出题型经验、常见模型族、常见图型和评分风险。
- 有完整初稿后，才可以做结构、论证缺口、图密度和评分风险对比。
- 禁止复制历史论文正文、摘要、图注、表格和结论。

`nature-skills` 是阶段局部专家，不是流程控制器。正式接入时，整目录放在：

```text
vendor/nature-skills/skills/
```

本地 Codex 使用时再同步到：

```text
~/.codex/skills/
```

所有 skill 输出仍然必须经过合同校验和人工闸门。

## 11. 最终提交前检查

终稿前至少运行：

```bash
python scripts/validate_contracts.py --stage final_export
python scripts/check_gates.py
python scripts/compile_latex.py
```

最终交付必须满足：

- `scripts/check_gates.py` 通过。
- `scripts/validate_contracts.py` 通过。
- `11_review/review_scorecard.csv` 没有未关闭的 fail 项。
- `14_contracts/revision_tasks.csv` 中必需修订任务已关闭或人工豁免。
- 人工确认 `final_submission_gate`。

## 12. 常见问题

**提示当前阶段不允许运行某脚本**

说明你正在尝试跑非当前阶段。回到 `workflow_state.yaml` 查看 `current_stage`，然后运行：

```bash
python scripts/run_current_stage.py
```

**合同校验失败**

不要跳过。打开 `11_review/contract_validation_report.md`，按 fail 项补齐合同或真实产物。

**论文里还有 TODO**

这是正常的阶段中间态。终稿前 `scripts/check_gates.py` 会把未清理占位符列为风险。

**想从某一阶段调试**

正式流程不要这么做。开发调试才使用 `--dev-debug` 或 `--skip-precheck`，并且调试产物不能直接当作正式比赛产物。

**想一键跑完全流程**

正式比赛不推荐，也会被规则限制。这个仓库的核心价值就是“慢一点，但每一步可查、可复核、可人工把关”。
