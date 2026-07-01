# P1 技能路由日志与归档设计

## 目标

本设计让专家技能调用在影响数学建模工作流之前可审计。路由策略负责授权；日志和归档文件记录实际发生了什么。

## 新增文件

```text
config/skill_router_policy.yaml
10_ai_logs/skill_usage_log.csv
10_ai_logs/skill_outputs/README.md
10_ai_logs/skill_outputs/templates/README.md
10_ai_logs/skill_outputs/templates/generic_input_manifest.yaml
10_ai_logs/skill_outputs/templates/generic_promotion_notes.md
10_ai_logs/skill_outputs/templates/by_category/<category>/input_manifest.yaml
10_ai_logs/skill_outputs/templates/by_category/<category>/promotion_notes.md
```

## 技能调用生命周期

```text
预检
-> 归档输入清单
-> 归档原始输出
-> 写入使用日志
-> 决定是否晋升
-> 校验目标文件和合同绑定
-> 必要时记录人工确认
-> 晋升或保持仅归档状态
```

## `skill_usage_log.csv` 应记录什么

CSV 中只记录调用级元数据。大型证据、文件列表、合同快照和校验细节应放在该次调用的归档目录中。

## `input_manifest.yaml` 应记录什么

输入清单记录路由器为何允许或拒绝调用：

```text
阶段、技能、权限、必需输入、读取文件、读取合同、风险控制
```

## `promotion_notes.md` 应记录什么

晋升说明记录归档输出是否可以安全进入下游：

```text
输出类型、目标路径、合同绑定、校验状态、人工决定、失败处理
```

## 非目标

```text
不实现 Python 运行时代码。
不接入运行时路由。
不改变现有合同。
不改变 workflow_state.yaml。
不直接执行技能。
```
