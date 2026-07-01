# 数学建模工作流 v3.2-MVP 导出版

本导出版基于 v3.0 deep_sequential 工作流叠加 v3.2-MVP 增量治理层：

- `AGENTS.md`：Codex / workflow / reviewer / nature-skills 权限边界。
- `config/*.yaml`：执行策略、技能增强、契约策略、迭代策略、Prior DB 策略。
- `14_contracts/`：claim-result-figure-formula-citation-polish-revision 契约总线。
- `scripts/`：已替换为 v3.2-MVP 版本的核心流程脚本。
- `11_review/`、`13_prior_db/`、`15_iteration_memory/`：审稿、先验经验、迭代记忆骨架。

## 快速开始

```bash
cd math_modeling_workflow_v32_mvp_export
python -m py_compile \
  scripts/workflow_utils.py \
  scripts/run_current_stage.py \
  scripts/validate_contracts.py \
  scripts/check_gates.py \
  scripts/generate_paper_sections.py \
  scripts/polish_latex_sections.py \
  scripts/check_figure_quality.py

python scripts/check_gates.py --dev-debug
python scripts/run_current_stage.py --skip-precheck
```

## nature-skills 接入

本包默认只保留 `vendor/nature-skills/VERSION.txt` 占位，不内嵌完整第三方仓库。正式使用时建议：

```bash
git clone https://github.com/Yuan1z0825/nature-skills.git vendor/nature-skills
mkdir -p ~/.codex/skills
cp -R vendor/nature-skills/skills/nature-* ~/.codex/skills/
```

如果比赛环境不能联网，请提前把 `vendor/nature-skills/skills/` 离线带入项目。

## 严格规则

- 不允许并行阶段。
- 不允许没有 result_contract 就写结果结论。
- 不允许没有 figure_contract 就引用图。
- 不允许没有 verified citation 就写文献支撑句。
- 不允许 reviewer 直接修改正式产物。
- 不允许 Prior DB 复制历史论文正文、摘要、图注、结论。
- polish 阶段不得改变数字、公式、引用、label/ref、模型名。

## 建议第一轮操作

1. 填写 `00_problem/problem_statement.md` 和附件。
2. 运行 `latex_template` 阶段。
3. 逐阶段推进到 `results_freeze`。
4. 填写 `14_contracts/result_contract.csv` 和 `14_contracts/figure_contract.csv`。
5. 再进入 `figures`、`paper_draft` 和 `paper_full`。
