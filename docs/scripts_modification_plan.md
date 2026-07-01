# v3.2-MVP 脚本修改计划

## 修改现有脚本

| 脚本 | 优先级 | 必需修改 | 原因 |
|---|---:|---|---|
| `scripts/workflow_utils.py` | P0 | 增加阶段：`prior_retrieval`、`results_freeze`、`auto_review`、`revision`、`final_export`；更新闸门映射 | v3.2 增加先验、结果冻结、审稿和迭代闭环 |
| `scripts/start_full_pipeline.py` | P0 | 遵守扩展后的有序阶段，并在闸门处停止 | 防止一次性全流程行为 |
| `scripts/run_current_stage.py` | P0 | 将新阶段路由到新脚本；阻止未知手动跳转 | 保持深度顺序控制 |
| `scripts/check_gates.py` | P0 | 加载 `contract_policy.yaml`；校验合同文件、修订关闭、润色差异和 prior 拷贝风险 | 现有门禁对 v3.2 过浅 |
| `scripts/check_figure_quality.py` | P0 | 校验 `figure_contract.csv`、SVG/PNG/PDF 文件存在、DPI、LaTeX label 和结果链接 | 将 `nature-figure` 与结果绑定图表连接起来 |
| `scripts/generate_paper_sections.py` | P0 | 只从 `claim_evidence_map.csv`、`result_contract.csv`、`figure_contract.csv`、`formula_contract.csv`、`citation_contract.csv` 生成章节 | 防止无支撑论断 |
| `scripts/polish_latex_sections.py` | P0 | 润色前抽取受保护事实原子，润色后写入 `polish_diff_check.csv` | 防止润色造成事实漂移 |
| `scripts/generate_model_code.py` | P1 | 向 `result_contract.csv` 写出 run ID、随机种子、来源文件和结果 ID | 让结果可追踪 |
| `scripts/decompose_problem.py` | P1 | 输出先验检索查询种子和题型 ID | 支持受控 prior 检索 |
| `scripts/route_weight_config.py` | P1 | 允许 prior cards 以 source ID 影响模型族权重 | 使用 Prior DB 但不复制答案 |
| `scripts/generate_dashboard.py` | P2 | 展示合同状态、审稿分数和开放修订任务 | 让工作流健康状态可见 |
| `scripts/compile_latex.py` | P2 | 最终闸门合同无效时失败 | 防止不合格终稿导出 |

## 新增脚本

| 脚本 | 优先级 | 用途 |
|---|---:|---|
| `scripts/validate_contracts.py` | P0 | `14_contracts/` 全部文件的中央校验器 |
| `scripts/retrieve_prior_cards.py` | P0 | 从 `13_prior_db/` 和遗留 `13_sample_prior/` 检索求解前经验卡片 |
| `scripts/check_prior_copy_risk.py` | P0 | 检测与历史论文或 prior cards 的高重叠风险 |
| `scripts/auto_review.py` | P0 | 运行审稿角色，生成原始评论和评分表 |
| `scripts/build_revision_tasks.py` | P0 | 将审稿评论转为 `revision_tasks.csv` |
| `scripts/apply_revision_tasks.py` | P1 | 按任务逐项应用修订，并做合同感知检查 |
| `scripts/check_revision_closure.py` | P0 | 在润色/终稿前确保必需任务已关闭 |
| `scripts/polish_diff_check.py` | P0 | 比较原始章节和润色章节中的受保护事实原子变化 |
| `scripts/sync_nature_skills.py` | P2 | 可选：将 vendored 技能同步到 `~/.codex/skills/` |

## 最小 P0 实现顺序

1. 增加 `AGENTS.md`。
2. 增加五个配置 YAML 文件。
3. 增加 `14_contracts/` 模板。
4. 修改 `workflow_utils.py` 和 `run_current_stage.py`。
5. 增加 `validate_contracts.py`。
6. 修改 `check_gates.py`，调用 `validate_contracts.py`。
7. 修改 `generate_paper_sections.py` 和 `polish_latex_sections.py`。
8. 增加审稿脚本。
9. 增加先验检索和拷贝风险脚本。
