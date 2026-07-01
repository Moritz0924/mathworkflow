# 任务包

## 0. 任务元数据

任务 ID：`P1-001`  
任务名称：`技能路由策略与归档日志设计`  
创建者：`Web GPT`  
分配对象：`Human, Codex, or Local DeepSeek Claude`  
创建日期：`2026-05-23`  
优先级：`P1`  
状态：`design-complete`

---

## 1. 任务摘要

新增 P1 技能路由策略，以及技能调用日志/归档设计；本任务不修改 Python 代码。

必需文件：

```text
config/skill_router_policy.yaml
10_ai_logs/skill_usage_log.csv
10_ai_logs/skill_outputs/README.md
10_ai_logs/skill_outputs/templates/README.md
10_ai_logs/skill_outputs/templates/generic_input_manifest.yaml
10_ai_logs/skill_outputs/templates/generic_promotion_notes.md
10_ai_logs/skill_outputs/templates/by_category/<category>/input_manifest.yaml
10_ai_logs/skill_outputs/templates/by_category/<category>/promotion_notes.md
docs/p1_skill_router_logging_design.md
```

---

## 2. 任务存在原因

问题：

```text
专家技能很有用，但如果没有路由、归档、晋升说明和日志行，
它们可能静默绕过阶段权限、合同或人工闸门。
```

原因：

```text
P0 标准化了阶段提示词，但还没有定义专家技能的运行时权限和审计模型。
```

设计响应：

```text
建立默认拒绝的技能路由策略，并要求每次允许的技能调用都进入归档结构。
```

预期改进：

```text
- 技能使用变得可审计。
- 技能输出在晋升前只具有建议性质。
- 合同绑定晋升变得显式。
- 失败处理可以分类。
```

---

## 3. 与当前路线图的关系

路线图条目：

```text
P1: Skill Router
```

本任务支持：

```text
P2: Prior Cards and Copy Risk
P3: Auto Review and Revision Tasks
P5: Claim-bound Writing
P6: Figure Contract Strengthening
P7: Optional Skill Wrapper
```

本任务不实现：

```text
运行时技能执行
运行时路由校验
新的 Python 脚本
合同结构迁移
实际安装 nature-skills
标准 ChatGPT Skill 打包
```

---

## 4. 范围

### 4.1 允许修改的文件和目录

分配代理只能修改：

```text
config/skill_router_policy.yaml
10_ai_logs/skill_usage_log.csv
10_ai_logs/skill_outputs/
docs/p1_skill_router_logging_design.md
TASK_PACKET.md
CHANGELOG_AI.md
DECISIONS.md
```

### 4.2 禁止修改的文件和目录

不得修改：

```text
workflow_state.yaml
AGENTS.md
14_contracts/
scripts/
02_latex_template/
05_model/
06_code/
07_results/
08_figures/
09_paper/
12_submission/
```

---

## 5. 验收标准

任务完成时应满足：

1. `config/skill_router_policy.yaml` 定义默认拒绝的路由策略。
2. `10_ai_logs/skill_usage_log.csv` 包含调用级审计表头。
3. `10_ai_logs/skill_outputs/` 包含标准归档说明和模板。
4. 每个输出类别都有 `input_manifest.yaml` 和 `promotion_notes.md` 模板。
5. `docs/p1_skill_router_logging_design.md` 解释生命周期、日志字段和晋升规则。
6. 未修改 Python 代码和合同 CSV。

---

## 6. 建议校验

```bash
python -c "import yaml; yaml.safe_load(open('config/skill_router_policy.yaml', encoding='utf-8'))"
```

```bash
python scripts/validate_contracts.py --stage current --warn-only
```

如本任务仍为纯设计任务，Python 脚本校验可以记录为未运行，但不得声称通过。
