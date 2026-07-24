# v4 架构说明

```text
ChatGPT 网页端
  │  chatgpt_response.md（协议字段 + 阶段结果）
  ▼
10_ai_logs/handoffs/<id>/
  │  codex_task.md
  ▼
Codex 本地实现与核验
  │  codex_receipt.json
  ▼
mmwf 校验器 ──失败/冲突──> 阻塞并退回
  │ pass + 阶段验收
  ▼
人工闸门（仅指定阶段）或下一阶段
```

## 内核模块

| 模块 | 职责 |
|---|---|
| `mmwf/state.py` | 状态模型、顺序转换和精确闸门 |
| `mmwf/context.py` | 上下文收集、秘密/隐藏/大文件过滤和哈希 |
| `mmwf/handoff.py` | 交接创建、导入、不可变回执和推进 |
| `mmwf/validators.py` | 阶段产物与合同最低验收 |
| `mmwf/migration.py` | v3.2 正式资产迁移和哈希清单 |
| `mmwf/dashboard.py` | 控制台到 CLI 的适配，不直接写状态 |
| `mmwf/cli.py` | 统一命令入口 |

## 状态模型

`workflow_state.yaml` 固定记录：`project_id`、`current_stage`、`status`、`active_handoff_id`、`context_sha256`、`pending_gate`、`completed_stages`、`history`。

阶段状态仅允许：`pending_chatgpt`、`pending_codex`、`blocked`、`pending_human`、`completed`。

## 安全边界

- 上下文默认拒绝隐藏文件、`.env`、已知密钥后缀、包含秘密模式的内容和未显式允许的大文件。
- ChatGPT 回复元数据必须与交接清单和上下文哈希一致。
- 回复和回执只写一次；修改使用新 revision。
- 控制台任何操作都有等价 CLI，任务失败后状态仍以磁盘为准。
- 项目不包含正式模型 API 调用路径。
