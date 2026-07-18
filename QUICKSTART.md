# v4 快速上手

## 1. 准备比赛工作区

每场比赛复制一份仓库。将题面放入 `00_problem/inbox/`，原始数据放入 `03_data/raw/`，然后初始化：

```powershell
python scripts/workflow.py init --project-id contest-2026-a
python scripts/workflow.py status
```

从 v3.2 工作区升级时只运行一次：

```powershell
python scripts/workflow.py migrate --from v3.2 --project-id contest-2026-a
```

迁移会备份旧状态、登记正式资产哈希，并把旧 `model_route` 映射到 `model_design/pending_chatgpt`。训练运行历史不会迁移。

## 2. 交给 ChatGPT

```powershell
python scripts/workflow.py prepare --target chatgpt
```

命令会在 `10_ai_logs/handoffs/<id>/` 生成：

- `manifest.yaml`
- `chatgpt_prompt.md`

把提示词复制到 ChatGPT 网页端。回复必须保留开头的协议字段：`protocol`、`project_id`、`stage`、`handoff_id`、`context_sha256`。将完整回复保存到本地，再导入：

```powershell
python scripts/workflow.py import --handoff-id <id> --response chatgpt_response.md
```

原始回复不可覆盖。需要修改时，创建新的 revision/交接，不要编辑已导入文件。

## 3. 交给 Codex 验证

```powershell
python scripts/workflow.py prepare --target codex --handoff-id <id>
```

Codex 按 `codex_task.md` 检查数据、实现代码、运行结果和合同，并产生 JSON 回执。回执包含：

```text
verdict, checks, artifacts, contract_rows, conflicts, next_action
```

导入验证：

```powershell
python scripts/workflow.py verify --handoff-id <id> --report codex_receipt.json
```

只有 `verdict=pass`、无冲突并且阶段验收通过才能推进。实现错误可由 Codex 修复；模型假设、路线和结论冲突必须退回 ChatGPT。

若状态为 `blocked`，先补齐外部信息或修复阻塞条件，再重新运行 `prepare --target chatgpt` 创建新的只读 revision；不要改写旧交接。

## 4. 人工闸门

状态显示 `pending_human` 时，先人工检查产物，再使用状态中显示的精确闸门 ID：

```powershell
python scripts/workflow.py confirm --gate model_freeze_gate
```

五个闸门依次是：

| 阶段 | 闸门 |
|---|---|
| `model_design` | `model_freeze_gate` |
| `result_freeze` | `result_freeze_gate` |
| `evidence_design` | `evidence_gate` |
| `paper_review` | `paper_gate` |
| `finalize` | `final_submission_gate` |

不存在 `pending_gate` 时，任何已知闸门 ID 都不能被确认。

## 5. 合同与最终检查

论文中的数字、图表、公式、引用和论断必须先登记到 `14_contracts/`。未登记证据不得入文。

```powershell
python scripts/validate_contracts.py --stage current
python scripts/check_gates.py
python scripts/workflow.py status
```

控制台启动命令：

```powershell
python scripts/start_dashboard.py --port 8765
```

控制台只是 CLI 的可视化外壳，不直接写状态，也不能绕过校验器。
