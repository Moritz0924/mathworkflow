# 数学建模双 AI 正式工作流 v4

本仓库是一套“一场比赛一个工作区”的 8 阶段薄工作流。ChatGPT 网页端负责建模决策、解释与论文写作；Codex 负责本地数据、代码、复现和数值核验。两者通过文件交接，不调用模型 API。

## 工作流

```text
intake → data_analysis → model_design → implementation
       → result_freeze → evidence_design → paper_review → finalize
```

控制器独占状态推进权。模型、结果、证据、正文和最终提交共设五个人工闸门，任何 AI 都不能代替人工确认。

## 最短使用路径

```powershell
python -m pip install -r requirements.txt
python scripts/workflow.py init --project-id <比赛ID>
python scripts/workflow.py status
python scripts/workflow.py prepare --target chatgpt
```

把生成的 `chatgpt_prompt.md` 复制到 ChatGPT 网页端，再将回复保存为文件：

```powershell
python scripts/workflow.py import --handoff-id <id> --response <回复文件>
python scripts/workflow.py prepare --target codex --handoff-id <id>
python scripts/workflow.py verify --handoff-id <id> --report <Codex回执JSON>
```

只有 Codex 回执为 `pass` 且阶段产物、合同均通过校验后，流程才进入下一阶段或人工闸门：

```powershell
python scripts/workflow.py confirm --gate <pending_gate中的精确ID>
```

详细步骤见 [QUICKSTART.md](QUICKSTART.md)，架构见 [docs/formal_v4_architecture.md](docs/formal_v4_architecture.md)。

## 核心目录

| 路径 | 用途 |
|---|---|
| `mmwf/` | v4 状态机、上下文、交接、校验和 CLI 内核 |
| `prompts/formal_v4/` | 8 个阶段的 ChatGPT/Codex 结果合同模板 |
| `10_ai_logs/handoffs/` | 每次交接的不可变记录 |
| `14_contracts/` | 结果、公式、图表、论断、引用、冻结与修订合同 |
| `06_code/` | 唯一正式求解代码目录 |
| `12_submission/` | 唯一最终提交目录 |
| `11_dashboard/web/` | 轻量比赛控制台 |

`02_literature/` 与 `13_prior_db/` 只可作为可选证据来源，不参与状态推进，也不得把历史论文当作当前题目的答案。

## 旧提示词保护

`prompts/stages/*.md` 和 `prompts/stage_prompt_contract.md` 是只读历史资产。它们不得删除、修改或覆盖；`config/legacy_prompt_hashes.yaml` 与测试会核验其哈希。v4 只能写入 `prompts/formal_v4/`。

旧 v3.2 系统的唯一恢复入口是 Git 标签 `v3.2-pre-thin-core`（归档分支 `codex/archive-v3.2-pre-thin-core`）。

## 控制台与验收

```powershell
python scripts/start_dashboard.py --port 8765
python -m unittest discover -s tests -p "test_*.py" -v
python -m compileall mmwf scripts tests
python scripts/validate_contracts.py --stage current
python scripts/check_gates.py
```

前端单独构建：

```powershell
cd 11_dashboard/web
npm ci
npm run build
```
