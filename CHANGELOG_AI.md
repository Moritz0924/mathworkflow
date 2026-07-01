# AI 变更日志

本文件记录 AI 辅助对仓库所做的变更。

每个 AI 代理在修改文件后都必须追加一条记录。

不要删除历史记录。

---

## 记录模板

### YYYY-MM-DD — TASK_ID — 简短任务名

#### 操作者

```text
Web GPT | Codex | Local DeepSeek Claude | Human
```

#### 角色

```text
planner | implementer | reviewer | scanner | debugger | editor
```

#### 关联路线图项

```text
Protocol | P0 | P1 | P2 | P3 | P4 | P5 | P6 | P7
```

#### 任务来源

```text
TASK_PACKET.md
```

#### 摘要

用 3 到 6 条要点说明变更内容。

```text
- ...
- ...
```

#### 变更文件

```text
新增：
- ...

修改：
- ...

删除：
- ...
```

#### 校验命令

| 命令 | 结果 | 说明 |
|---|---|---|
| `command here` | passed / failed / not run | 解释 |

#### 合同影响

```text
未修改合同文件。
```

或：

```text
修改的合同文件：
- 14_contracts/xxx.csv

原因：
- ...
```

#### 闸门影响

```text
未改变闸门行为。
```

或：

```text
改变的闸门行为：
- ...
```

#### 相对 TASK_PACKET.md 的偏离

```text
无。
```

或：

```text
- 偏离：
  原因：
  风险：
```

#### 风险与未解决问题

```text
- ...
```

#### 建议下一步

```text
一个具体下一步。
```

---

# 历史记录

### YYYY-MM-DD — PROTO-001 — 添加 AI 协作交接协议文件

#### 操作者

```text
Web GPT
```

#### 角色

```text
planner
```

#### 关联路线图项

```text
Protocol
```

#### 任务来源

```text
Web GPT 对话中的用户请求
```

#### 摘要

```text
- 增加 Web GPT、Codex 与本地 DeepSeek Claude 的文件式协作协议。
- 将 PROJECT_CONTEXT.md 定义为项目地图和工作流控制参考。
- 将 TASK_PACKET.md 定义为窄范围任务交接文件。
- 将 CHANGELOG_AI.md 定义为 AI 辅助修改日志。
- 将 DECISIONS.md 定义为架构决策记录。
```

#### 变更文件

```text
新增：
- PROJECT_CONTEXT.md
- TASK_PACKET.md
- CHANGELOG_AI.md
- DECISIONS.md

修改：
- 无

删除：
- 无
```

#### 校验命令

| 命令 | 结果 | 说明 |
|---|---|---|
| `ls PROJECT_CONTEXT.md TASK_PACKET.md CHANGELOG_AI.md DECISIONS.md` | not run | 文件放入仓库后运行 |
| `git diff --stat` | not run | 文件放入仓库后可选运行 |

#### 合同影响

```text
未修改合同文件。
```

#### 闸门影响

```text
未改变闸门行为。
```

#### 相对 TASK_PACKET.md 的偏离

```text
无。
```

#### 风险与未解决问题

```text
- PROJECT_CONTEXT.md 中的路径列表应与真实仓库结构核对。
- 后续任务包必须保持窄范围，以保护 Codex 时间。
- P0-P7 未由本协议任务实现。
```

#### 建议下一步

```text
使用 TASK_PACKET.md 创建 P0-001：阶段提示词合同骨架。
```

### 2026-05-23 — P0-001 — 阶段提示词合同骨架

#### 操作者

```text
Web GPT
```

#### 角色

```text
planner | prompt designer
```

#### 关联路线图项

```text
P0
```

#### 任务来源

```text
TASK_PACKET.md
```

#### 摘要

```text
- 在仓库根目录应用 AI 协作交接协议文件。
- 增加 prompts/stage_prompt_contract.md 作为上级提示词标准。
- 在 prompts/stages/ 下为每个有序工作流阶段增加一个阶段提示词模板文件。
- 保持本次变更为纯设计，不修改 Python 代码、合同 CSV、workflow_state.yaml 或 AGENTS.md。
```

#### 变更文件

```text
新增：
- PROJECT_CONTEXT.md
- DECISIONS.md
- prompts/stage_prompt_contract.md
- prompts/stages/*.md

修改：
- TASK_PACKET.md
- CHANGELOG_AI.md

删除：
- 无
```

#### 校验命令

| 命令 | 结果 | 说明 |
|---|---|---|
| `ls PROJECT_CONTEXT.md TASK_PACKET.md CHANGELOG_AI.md DECISIONS.md prompts/stage_prompt_contract.md` | passed | 确认协议和上级提示词文件存在 |
| `find prompts/stages -maxdepth 1 -type f | sort` | passed | 确认阶段提示词文件存在 |
| `python scripts/check_stage_prompt_contracts.py` | not run | 计划中，尚未实现 |

#### 合同影响

```text
未修改合同文件。
```

#### 闸门影响

```text
未改变闸门行为。P0 仍是纯设计，尚未接入运行时脚本。
```

#### 风险与未解决问题

```text
- 阶段提示词文件是人类可读 Markdown，尚未机器校验。
- 一些校验命令依赖真实输入，可能需要到对应阶段才可通过。
- P1 应决定是直接解析 Markdown，还是生成更严格的 YAML/JSON 权限图。
```

#### 建议下一步

```text
创建 P1-001，用 prompts/stages/*.md 作为事实来源设计 Skill Router 权限图。
```

### 2026-05-23 — P1-001 — 技能路由策略与归档日志设计

#### 操作者

```text
Web GPT
```

#### 角色

```text
planner | policy designer
```

#### 摘要

```text
- 增加 config/skill_router_policy.yaml 作为默认拒绝的 Skill Router 策略。
- 增加 10_ai_logs/skill_usage_log.csv 调用级审计表头。
- 增加 10_ai_logs/skill_outputs/ 作为技能调用标准归档层。
- 增加通用和按类别区分的 input_manifest.yaml 与 promotion_notes.md 模板。
- 增加 docs/p1_skill_router_logging_design.md 作为人类可读设计说明。
```

#### 校验命令

| 命令 | 结果 | 说明 |
|---|---|---|
| `python -c "import yaml; yaml.safe_load(open('config/skill_router_policy.yaml', encoding='utf-8'))"` | passed | 确认路由策略 YAML 可解析 |
| `python scripts/validate_v32_export.py` | passed | 确认导出包基线检查通过 |
| `python scripts/validate_contracts.py` | passed | 确认现有合同校验保持完整 |

#### 风险与未解决问题

```text
- config/skill_router_policy.yaml 尚未由脚本强制执行。
- skill_usage_log.csv 当前只有表头，运行时日志尚未实现。
- 模板占位字段需要由后续路由器实现填充。
```

## P1 运行时落地计划

增加 `docs/p1_runtime_landing_plan.md` 作为未来 Skill Router 运行时层的实现计划文件。本项仅为文档；未修改 Python 代码、合同、提示词、工作流状态或 `AGENTS.md`。

## P1 运行时路由器实现

基于 `docs/p1_runtime_landing_plan.md` 增加第一版可执行 Skill Router 运行时层。

新增：
- `scripts/check_skill_router.py`
- `11_review/skill_router_report.json`
- `11_review/skill_router_report.md`

修改：
- `scripts/check_gates.py`
- `CHANGELOG_AI.md`
- `DECISIONS.md`

校验：
- `python scripts/check_skill_router.py --validate-policy` 通过
- `python scripts/check_gates.py` 通过
- `python scripts/validate_v32_export.py` 通过

说明：
- 路由器校验策略、预检、归档脚手架、晋升资格和技能使用日志。
- 它不执行专家技能，不直接修改合同，不修改工作流状态，也不自动晋升输出。

## P1.1 运行时路由器加固

修补 `scripts/check_skill_router.py`，关闭三个 blocker 级运行时防护缺口。

变更：
- `--init-archive` 现在创建归档脚手架前必须通过 `--preflight`。
- 初始化的 `raw_output.md` 带有明确的 `RAW_OUTPUT_STATUS: EMPTY_INITIALIZED` 哨兵。
- `--validate-promotion` 会拒绝脚手架内容或哨兵标记的空原始输出。
- `--validate-promotion` 会用真实合同 CSV 校验 `resolved_bindings`，不再信任自报 `status: valid` 文本。

## P1.2 运行时路由器合同绑定加固

继续强化合同绑定晋升检查：

- 支持 `section_id` 作为章节级引用和公式语境的绑定令牌。
- 空合同状态字段默认视为无效。
- `section_draft` 与 `claim_rewrite` 要求论断/证据或论断/结果关系一致。
- `figure_blueprint` 与 `caption_candidate` 在同时提供结果/图表 ID 时检查关系一致性。
- `citation_candidate` 支持 `section_id`，并检查引用/论断或引用/章节一致性。

## 学习层 v1：RAG 加轻量评分器

实现受控本地学习层：

新增：
- `config/learning_policy.yaml`
- `scripts/learning_utils.py`
- `scripts/build_prior_corpus.py`
- `scripts/build_prior_cards.py`
- `scripts/build_prior_index.py`
- `scripts/retrieve_prior_cards.py`
- `scripts/check_prior_copy_risk.py`
- `scripts/train_workflow_scorers.py`
- `scripts/optimize_workflow_policy.py`
- 生成 `13_prior_db/` 与 `16_learning/` 相关产物

关键结果：
- 识别 PDF 语料：312 / 312。
- 抽取失败：7 份 PDF。
- 生成 prior cards：36。
- 评分器样本：312；可用样本：305。
- 确定性划分上的模型族评分准确率：0.5082。
- 直接复制烟测按预期失败，最终 prior-card 拷贝风险报告通过。

## 本地仪表盘 v1：Web 控制与人工闸门台

实现本地 React/Vite 仪表盘和 Python 标准库后端。

行为：
- 从 `127.0.0.1:8765` 提供仪表盘。
- 读取工作流状态、产物、报告、任务和白名单预览文件。
- 动作只调用现有控制脚本：当前阶段、闸门确认、门禁检查、合同校验、技能路由校验和导出校验。
- 同时只允许一个活跃任务。
- 状态变更动作要求输入精确确认文本。
- 非 `127.0.0.1` 绑定时禁用写动作。

## 代理模式 v1：训练沙盒与正式辅助

实现独立的 `agent_mode` 层，不向正式 `deep_sequential` 工作流新增阶段。

新增：
- `config/agent_mode_policy.yaml`
- `scripts/agent_mode_utils.py`
- `scripts/run_agent_mode.py`
- `scripts/benchmark_agent_run.py`
- `scripts/validate_agent_run.py`
- `16_learning/agent_runs/` 下示例运行

行为：
- `training_sandbox` 在 `16_learning/agent_runs/<run_id>/workspace/` 创建隔离运行工作区。
- 沙盒只复制配置允许的项目输入，并在没有代理执行器时写入提示包。
- 代理执行通过策略或 `MMWF_AGENT_CMD_JSON` 进行可选命令列表调用。
- 本地 Prior DB 基准会生成结构和证据信号对比报告，不复制历史论文文本。
- `formal_assist` 生成当前阶段提示词，且永不确认人工闸门。
