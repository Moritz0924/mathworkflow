# Training Enhancement Points

- generated_at: 2026-06-03T19:12:20
- iteration: 1
- scope: system, prompt, gate
- status: candidate only; formal adoption requires human gate and normal contract checks.

## ENH-SYS-001 (system)

- severity: major
- evidence: reports/prompt_route_manifest.csv; 09_paper/full_draft.md
- proposed_change: 训练模式应强制生成 prompt route manifest，并在 run 级验证中检查训练是否覆盖全部 16 个阶段提示词。
- acceptance_check: validate_agent_run.py 对完成训练 run 检查 prompt_route_manifest.csv 行数不少于 16 且无 missing stage prompt。

## ENH-PROMPT-001 (prompt)

- severity: major
- evidence: agent_prompt.md; prompts/stage_prompt_contract.md
- proposed_change: 训练提示词应要求每个阶段输出目标重述、输入核验、合同绑定、风险清单、自检清单和人工闸门状态。
- acceptance_check: agent_prompt.md 包含 stage prompt route 和每阶段执行骨架要求。

## ENH-GATE-001 (gate)

- severity: major
- evidence: 12_submission/final_submit_paper.md; 14_contracts/*.csv
- proposed_change: 训练完成门禁应同时检查三类增强点、可提交论文、提交包和核心合同非空，而不是只检查 gap report。
- acceptance_check: validate_agent_run.py 对 training_enhancement_points.csv、final_submit_paper.md、final_submit_package.md 和核心合同给出 fail 级校验。

## ENH-PROMPT-002 (prompt)

- severity: minor
- evidence: 08_figures/figure_template_registry.csv
- proposed_change: figures 阶段提示词在训练模式中应要求图表选择说明绑定数据特征，不允许只生成装饰性图片。
- acceptance_check: 训练论文图表说明段落引用 figure_contract.csv 中的 result_id 或 evidence_source。
