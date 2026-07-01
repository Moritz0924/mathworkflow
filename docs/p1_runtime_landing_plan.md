# P1 技能路由运行时落地计划

版本：`v3.2-p1-runtime-plan`  
状态：仅规划  
范围：P1 运行时路由器实现计划，不包含代码  
负责人：`workflow_controller`  
主配置：`config/skill_router_policy.yaml`

## 0. 目的

本文件定义 P1 设计文件落地后还需要实现什么。

目标是把现有 Skill Router 设计层转为确定性的运行时防护栏：

```text
config/skill_router_policy.yaml
→ scripts/check_skill_router.py
→ 技能预检 / 归档 / 使用日志 / 晋升校验
→ check_gates 集成
```

路由器不得自行执行专家技能。它只判断某次技能调用是否允许、输入是否有效、输出应归档到哪里，以及归档输出是否具备晋升资格。

## 1. 当前已落地基线

以下 P1 设计产物已经存在，必须作为源输入：

```text
config/skill_router_policy.yaml
10_ai_logs/skill_usage_log.csv
10_ai_logs/skill_outputs/README.md
10_ai_logs/skill_outputs/templates/generic_input_manifest.yaml
10_ai_logs/skill_outputs/templates/generic_promotion_notes.md
10_ai_logs/skill_outputs/templates/by_category/*/input_manifest.yaml
10_ai_logs/skill_outputs/templates/by_category/*/promotion_notes.md
docs/p1_skill_router_logging_design.md
prompts/stage_prompt_contract.md
prompts/stages/*.md
```

第一版运行时实现期间不要重新设计这些文件，只实现符合它们的检查。

## 2. 非目标

第一版运行时不得实现：

```text
1. 不自动执行技能。
2. 不调用外部 API。
3. 不进行网页检索。
4. 不直接修改终稿论文文件。
5. 不允许技能输出直接修改合同。
6. 不在未校验时自动晋升输出。
7. 不做多代理编排。
8. 不做 UI 或仪表盘。
9. 不替换 run_current_stage.py。
10. 不删除或迁移 config/skill_enhancement.yaml。
```

路由器是守门员，不是执行工人。

## 3. 新增或修改文件

### 3.1 新增

```text
scripts/check_skill_router.py
11_review/skill_router_report.json
11_review/skill_router_report.md
10_ai_logs/skill_outputs/.gitkeep
```

第一版之后可选：

```text
tests/test_skill_router_policy.py
tests/fixtures/skill_router/
docs/p1_skill_router_runtime_usage.md
```

### 3.2 修改

只做最小安全修改：

```text
scripts/check_gates.py
CHANGELOG_AI.md
DECISIONS.md
```

### 3.3 P1 运行时第一版不得修改

```text
AGENTS.md
workflow_state.yaml
14_contracts/*.csv
14_contracts/*.yaml
prompts/stages/*.md
scripts/run_current_stage.py
scripts/validate_contracts.py
```

这些可以在路由器检查器稳定后，于 P2 或之后集成。

## 4. 必需 CLI 接口

实现 `scripts/check_skill_router.py` 的以下命令。

### 4.1 校验策略文件

```bash
python scripts/check_skill_router.py --validate-policy
```

检查项：

```text
1. YAML 可解析。
2. 必需顶层键存在。
3. ordered_stages 与 prompts/stages 映射一致。
4. stage_routes 只使用真实工作流阶段。
5. 拒绝遗留阶段名。
6. 每个允许技能都在技能注册表中存在。
7. 每个引用权限都存在于 permission_model.levels。
8. 每个必需输入规则都引用已注册技能。
9. usage_log.columns 与 10_ai_logs/skill_usage_log.csv 表头一致。
10. promotion_rules 目标使用已知输出类型，或明确注册。
```

预期输出：

```text
11_review/skill_router_report.json
11_review/skill_router_report.md
```

### 4.2 检查某技能是否可调用

```bash
python scripts/check_skill_router.py --stage figures --skill nature-figure --preflight
```

检查项：

```text
1. 阶段存在。
2. 阶段是当前阶段，或有明确授权。
3. 技能已注册。
4. 技能在该阶段允许使用。
5. 权限等级有效。
6. 必需输入存在。
7. 必需时已满足人工最终闸门。
8. 未发现冻结产物违规。
```

退出行为：

```text
0: 允许
1: 拒绝或阻塞
2: 策略/配置错误
3: 缺失必需输入
4: 校验失败
```

### 4.3 初始化归档脚手架

```bash
python scripts/check_skill_router.py --stage figures --skill nature-figure --init-archive
```

创建：

```text
10_ai_logs/skill_outputs/figures/nature-figure/<call_id>/input_manifest.yaml
10_ai_logs/skill_outputs/figures/nature-figure/<call_id>/raw_output.md
10_ai_logs/skill_outputs/figures/nature-figure/<call_id>/promotion_notes.md
```

规则：

```text
1. call_id 使用 SKILL-<stage>-<skill>-<YYYYMMDDTHHMMSSZ>。
2. 有类别模板时复制类别模板。
3. 通用模板作为 fallback。
4. raw_output.md 初始化时带警告头。
5. promotion_notes.md 初始为 archive_only，直到显式请求晋升。
```

### 4.4 校验归档输出是否可晋升

```bash
python scripts/check_skill_router.py --validate-promotion 10_ai_logs/skill_outputs/figures/nature-figure/<call_id>
```

检查项：

```text
1. input_manifest.yaml 存在且可解析。
2. raw_output.md 存在且非空。
3. promotion_notes.md 存在且结构可解析。
4. output_type 对该技能允许。
5. promotion target 被 config/skill_router_policy.yaml 允许。
6. 必需合同绑定存在。
7. 必要时存在人工确认。
8. 润色输出保留受保护事实原子。
9. prior_card 输出记录拷贝风险状态。
10. 终稿后技能不修改最终论文。
```

注意：该命令只校验晋升资格，不执行晋升。

### 4.5 追加使用日志行

```bash
python scripts/check_skill_router.py --log-call 10_ai_logs/skill_outputs/figures/nature-figure/<call_id>
```

规则：

```text
1. 向 10_ai_logs/skill_usage_log.csv 追加一行。
2. 不覆盖已有日志行。
3. 写入前校验 CSV 表头。
4. router_decision 使用 allow, deny, skip, block, archive_only, promotion_validated, promotion_blocked。
5. 适用时使用 config/skill_router_policy.yaml 中的 failure_code。
```

## 5. 数据结构

### 5.1 路由器 JSON 报告

`11_review/skill_router_report.json` 必须使用以下结构：

```json
{
  "version": "v3.2-p1-runtime",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "policy_path": "config/skill_router_policy.yaml",
  "status": "pass|warning|fail",
  "summary": {
    "stages_checked": 16,
    "skills_registered": 9,
    "stage_routes_checked": 16,
    "errors": 0,
    "warnings": 0
  },
  "checks": [],
  "skill_call_decision": {
    "stage_id": null,
    "skill_id": null,
    "router_decision": null,
    "permission_level": null,
    "required_inputs_status": null,
    "failure_code": null,
    "human_confirmation_required": false
  }
}
```

### 5.2 路由器 Markdown 报告

`11_review/skill_router_report.md` 应总结：

```text
1. 总体状态。
2. 已检查策略文件。
3. 阶段路由覆盖。
4. 技能注册表覆盖。
5. 使用日志兼容性。
6. 错误。
7. 警告。
8. 建议下一步。
```

### 5.3 使用日志行

`10_ai_logs/skill_usage_log.csv` 必须保持以下表头：

```csv
call_id,timestamp,stage_id,skill_id,permission_level,router_decision,required_inputs_status,archive_path,output_type,promotion_target,validation_status,failure_code,human_confirmation_required,notes
```

## 6. 校验规则

### 6.1 阶段身份校验

规则 ID：

```text
SR-STAGE-001: 所有 ordered stages 都已知。
SR-STAGE-002: 每个 ordered stage 都有提示词文件。
SR-STAGE-003: 每个 stage route key 都是真实有序阶段。
SR-STAGE-004: 拒绝遗留阶段名。
SR-STAGE-005: 未明确授权时禁止跨阶段技能调用。
```

### 6.2 技能注册表校验

```text
SR-SKILL-001: 每个路由技能都已注册。
SR-SKILL-002: 每个注册技能都有 category、status、source、mode、default_permission。
SR-SKILL-003: 每个权限都已定义。
SR-SKILL-004: 每个 output_type 都显式允许或阻止。
SR-SKILL-005: 未知技能动作是 deny_call。
```

### 6.3 权限校验

```text
SR-PERM-001: 技能不能修改 workflow_state.yaml。
SR-PERM-002: 技能不能修改 AGENTS.md。
SR-PERM-003: 技能不能修改 scripts/。
SR-PERM-004: 技能不能直接写合同。
SR-PERM-005: 技能不能修改最终提交物。
SR-PERM-006: post_final 技能需要人工最终闸门。
```

## 7. 失败代码映射

运行时检查器必须映射到 `config/skill_router_policy.yaml` 中的失败代码。

最低必需映射：

```text
技能目录缺失 → SKILL_NOT_INSTALLED
未知技能 ID → UNKNOWN_SKILL
技能不允许在该阶段使用 → STAGE_NOT_ALLOWED
遗留阶段名 → LEGACY_STAGE_NAME
缺少 all_of 输入 → REQUIRED_INPUT_MISSING
缺少合同 → CONTRACT_MISSING
合同无效或 CSV/YAML 格式错误 → CONTRACT_INVALID
归档路径超出允许根目录 → OUTPUT_PATH_VIOLATION
输出含无支撑数据/结果论断 → FABRICATED_DATA_OR_RESULT
输出含未验证引用元数据 → FABRICATED_CITATION
Prior 文本拷贝风险超阈值 → PRIOR_COPY_RISK
润色改变受保护事实原子 → PROTECTED_ATOM_CHANGED
晋升检查失败 → VALIDATION_FAILED
需要人工闸门但缺失 → HUMAN_CONFIRMATION_REQUIRED
输出类型未注册 → UNKNOWN_SKILL_OUTPUT
```

检查器不得猜测恢复动作。可行时应复制 `failure_policy.failure_codes.<code>.recovery` 中的恢复文本。

## 8. 与 `check_gates.py` 集成

### 8.1 最小集成

向 `scripts/check_gates.py` 增加一个门禁：

```text
skill_router_policy_gate
```

只检查：

```text
1. config/skill_router_policy.yaml 存在。
2. 10_ai_logs/skill_usage_log.csv 存在。
3. 使用日志表头与策略一致。
4. 10_ai_logs/skill_outputs/templates/ 存在。
5. 运行路由器校验后，11_review/skill_router_report.json 存在。
6. 路由器报告状态不是 fail。
```

### 8.2 `check_gates.py` 不得做的事

```text
1. 不执行技能。
2. 不初始化归档。
3. 不晋升输出。
4. 不修改 skill_usage_log.csv。
5. 不深度解析原始技能输出。
```

边界：

```text
check_skill_router.py = 路由器专用校验和日志
check_gates.py = 工作流级就绪检查
```

## 9. 实现里程碑

1. 策略校验器。
2. 预检检查器。
3. 归档脚手架。
4. 晋升校验器。
5. 使用日志追加器。
6. 门禁集成。

## 10. 验收定义

P1 运行时实现只有同时满足以下条件才算完成：

```text
1. scripts/check_skill_router.py 存在。
2. --validate-policy 在当前包上通过。
3. --preflight 能正确允许和阻止阶段-技能组合。
4. --init-archive 能创建有效归档脚手架。
5. --validate-promotion 能阻止不安全晋升。
6. --log-call 能追加一行有效 CSV。
7. check_gates.py 包含 skill_router_policy_gate。
8. validate_v32_export.py 仍通过。
9. 技能输出不能直接修改合同。
10. 技能调用不能修改最终论文产物。
```

## 11. 建议实现顺序

```text
步骤 1：实现纯策略解析和静态校验。
步骤 2：增加阶段和技能路由校验。
步骤 3：增加必需输入检查。
步骤 4：增加归档脚手架创建。
步骤 5：增加晋升校验。
步骤 6：增加使用日志追加。
步骤 7：增加 check_gates 集成。
步骤 8：增加测试和回归检查。
```

不要从归档创建开始。先让策略检查器足够严格，否则工作流只会学会为错误决策创建整齐的文件夹。

## 12. 后续 P2 桥接

P1 运行时稳定后，P2 可以把路由器接入实际阶段执行：

```text
run_current_stage.py
→ 读取当前阶段
→ 加载 prompts/stages/<stage>.md
→ 从 skill_router_policy.yaml 查询允许技能
→ 在用户或阶段请求技能时初始化技能归档
→ 要求人类或外部技能调用填充 raw_output.md
→ 校验晋升资格
→ 将结果写入阶段总结
```

P2 仍应避免自动执行技能，除非人类确认该调用。
