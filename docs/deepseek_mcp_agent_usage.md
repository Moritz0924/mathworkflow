# DeepSeek V4 外部代理与 MCP 图像识别操作文档

本文档说明如何在 Math Modeling Workflow v3.2-MVP 中启用 DeepSeek V4 外部代理，并通过 MCP 工具获得图像识别能力。

## 1. 功能边界

DeepSeek V4 代理运行在现有 `deep_sequential` 工作流外层，不替代工作流控制器。

- 工作流阶段顺序仍由 `workflow_state.yaml` 控制。
- 人工 gate 仍必须由人确认。
- 正式结果、图表、公式、引用和论文内容仍必须经过 `14_contracts/` 契约总线。
- MCP 图像识别结果只作为观察材料，不能直接作为论文事实或结论。

权限模式：

| 模式 | 写入权限 | 说明 |
|---|---:|---|
| `training_sandbox` | 允许写入沙盒 workspace | 用于训练、试跑、自动生成候选产物 |
| `formal_assist` | 默认不直接写正式产物 | 只能辅助当前阶段，不能确认 gate 或绕过契约校验 |

## 2. 关键文件

| 文件 | 用途 |
|---|---|
| `config/llm_router_policy.yaml` | DeepSeek 模型档位、阶段路由、MCP 视觉配置 |
| `config/agent_mode_policy.yaml` | 外部代理命令入口 |
| `scripts/deepseek_agent_runner.py` | DeepSeek V4 代理运行器 |
| `scripts/mcp_client.py` | stdio MCP 客户端 |
| `mcp_servers/vision_server.py` | 图像识别 MCP server |
| `.env.example` | 环境变量模板 |
| `tests/` | 离线测试用例 |

## 3. 环境变量配置

复制 `.env.example` 为 `.env`，只在本机填写真实密钥。

```powershell
Copy-Item .env.example .env
```

最小配置：

```env
DEEPSEEK_API_KEY=你的 DeepSeek API Key
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

如果需要启用真实图像识别后端，再配置：

```env
QWEN_VL_API_KEY=
QWEN_VL_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_VL_MODEL=qwen3-vl-plus

# 兼容旧配置名；默认同样指向阿里云百炼 Qwen-VL。
VISION_API_KEY=
VISION_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
VISION_MODEL=qwen3-vl-plus
VISION_MAX_IMAGE_BYTES=10485760
VISION_OFFLINE=0
```

`QWEN_VL_API_KEY` 是预留的 API key 位置；不要写入 `.env.example`。如使用海外地域，可将 base URL 切换为 `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` 或 `https://dashscope-us.aliyuncs.com/compatible-mode/v1`。

离线测试或暂时没有视觉模型时：

```env
VISION_OFFLINE=1
```

注意：不要把 `.env` 提交或复制进论文产物。仓库已通过 `.gitignore` 忽略 `.env`。

## 4. 模型档位路由

路由配置在 `config/llm_router_policy.yaml`。

| 档位 | 模型 | Thinking | 推理等级 | 典型用途 |
|---|---|---|---|---|
| `light` | `deepseek-v4-flash` | 关闭 | 无 | 模板、格式、编译、最终导出准备 |
| `standard` | `deepseek-v4-pro` | 开启 | `high` | EDA、草稿、图表、普通阶段辅助 |
| `deep` | `deepseek-v4-pro` | 开启 | `max` | 高风险修复、模型选择、代码生成、评审修订 |

固定阶段默认：

```text
latex_template / intake / compile / final_export -> light
eda / task_analysis / prior_retrieval / figures / paper_draft / paper_full / polish -> standard
model_route / codegen / auto_review / revision -> standard
```

当 `model_route`、`codegen`、`auto_review`、`revision` 阶段任务中出现高风险、失败、契约冲突、冻结产物、模型选择等关键词时，自动升为 `deep`。

## 5. 离线自检

先运行不需要 API Key 的离线自检：

```powershell
python scripts\deepseek_agent_runner.py --self-test --offline
```

预期输出包含：

```json
{
  "status": "pass",
  "mcp_offline": "pass"
}
```

再检查脚本语法：

```powershell
python -m compileall scripts\simple_yaml.py scripts\deepseek_agent_runner.py scripts\mcp_client.py mcp_servers\vision_server.py tests
```

检查现有工作流契约和技能路由：

```powershell
python scripts\check_skill_router.py --validate-policy
python scripts\validate_contracts.py --stage current
```

如果当前 Python 没有 `pytest`，`python -m pytest tests` 会失败。安装依赖后再运行：

```powershell
python -m pip install -r requirements.txt
python -m pytest tests
```

## 6. 通过工作流代理入口运行

推荐使用现有代理入口：

```powershell
python scripts\run_agent_mode.py --mode training_sandbox
```

流程：

1. `run_agent_mode.py` 创建 `16_learning/agent_runs/<RUN_ID>/workspace`。
2. 写入 `agent_prompt.md`。
3. 根据 `config/agent_mode_policy.yaml` 调用 `scripts/deepseek_agent_runner.py`。
4. runner 读取当前 stage、stage prompt、仓库规则和任务提示。
5. runner 根据 `config/llm_router_policy.yaml` 自动选择 DeepSeek 模型档位。
6. 如检测到图片路径或图像关键词，先调用 MCP `image_recognize`。
7. DeepSeek 输出被写入 run 目录日志；沙盒模式下允许应用安全文件动作。

常用参数：

```powershell
python scripts\run_agent_mode.py --mode training_sandbox --max-iterations 3
python scripts\run_agent_mode.py --mode formal_assist
python scripts\run_agent_mode.py --mode training_sandbox --dry-run
python scripts\run_agent_mode.py --mode formal_assist --feedback-run-id TRAIN-YYYYMMDD_HHMMSS
```

`formal_assist` 默认会尝试读取最新一个已通过验证和 copy-risk 检查的 `training_sandbox` run，把其中的 `agent_revision_queue.csv` 整理为 `15_iteration_memory/training_feedback/<RUN_ID>_feedback.*`，并作为候选修正附加到正式辅助提示词。该反馈是 `suggestion_only`，不会自动修改正式论文、合同或结果。

## 7. 直接调用 DeepSeek runner

也可以直接调用 runner：

```powershell
python scripts\deepseek_agent_runner.py `
  --prompt 16_learning\agent_runs\<RUN_ID>\workspace\agent_prompt.md `
  --workspace 16_learning\agent_runs\<RUN_ID>\workspace `
  --run-dir 16_learning\agent_runs\<RUN_ID> `
  --mode training_sandbox `
  --max-iterations 3
```

正式辅助模式：

```powershell
python scripts\deepseek_agent_runner.py `
  --prompt 16_learning\agent_runs\<RUN_ID>\formal_agent_prompt.md `
  --workspace . `
  --run-dir 16_learning\agent_runs\<RUN_ID> `
  --mode formal_assist `
  --max-iterations 1
```

`formal_assist` 模式不会自动确认人工 gate，也不会直接写入受保护正式产物。训练反馈如果被采纳，仍需进入正式修订任务、合同校验和人工闸门。

## 8. MCP 图像识别

### 8.1 查看 MCP 工具

```powershell
python scripts\mcp_client.py --command python mcp_servers\vision_server.py --list-tools
```

预期包含：

```json
{
  "name": "image_recognize"
}
```

### 8.2 调用图像识别

图片必须位于 workspace 内，例如 `00_problem/inbox/problem.png`。

```powershell
python scripts\mcp_client.py `
  --command python mcp_servers\vision_server.py `
  --call-tool image_recognize `
  --arguments-json "{\"workspace\":\"I:\\数模\\math-workflow\",\"image_path\":\"00_problem/inbox/problem.png\",\"prompt\":\"识别赛题图片中的文字和图表线索\"}"
```

返回结构：

```json
{
  "structuredContent": {
    "summary": "...",
    "ocr_text": "...",
    "objects": [],
    "table_or_chart_clues": [],
    "confidence": "...",
    "risks": []
  }
}
```

安全限制：

- 拒绝 workspace 外路径。
- 拒绝不存在的文件。
- 拒绝超出 `VISION_MAX_IMAGE_BYTES` 的文件。
- 仅支持 `.png/.jpg/.jpeg/.webp/.bmp/.tif/.tiff/.gif`。

## 9. 日志与审计

每次 runner 调用会在 `run_dir` 下写入：

| 文件 | 内容 |
|---|---|
| `deepseek_route.json` | 当前 stage、模型档位、是否高风险 |
| `deepseek_request_manifest.json` | 请求摘要、模型名、估算 token、是否调用视觉工具 |
| `deepseek_response.md` | DeepSeek 返回正文 |
| `deepseek_file_actions.json` | 文件动作提取与是否应用 |

日志不会写入 `DEEPSEEK_API_KEY`、`QWEN_VL_API_KEY` 或 `VISION_API_KEY`。

## 10. 常见问题

### 10.1 `missing API key env: DEEPSEEK_API_KEY`

说明 `.env` 或系统环境变量没有配置 DeepSeek Key。

处理：

```powershell
Copy-Item .env.example .env
notepad .env
```

填入 `DEEPSEEK_API_KEY` 后重试。

### 10.2 `No module named pytest`

当前 Python 没有安装 pytest。

处理：

```powershell
python -m pip install -r requirements.txt
python -m pytest tests
```

如果当前 Python 没有 pip，请换用带 pip 的 Python 解释器运行。

### 10.3 `image_path must stay inside workspace`

MCP 视觉工具拒绝读取 workspace 外的图片。

处理：把图片复制到当前 workspace 的 `00_problem/inbox/` 或 `03_data/raw/` 下，再使用相对路径调用。

### 10.4 `formal_assist` 没有写入文件

这是预期行为。正式模式默认不直接写受保护产物，避免绕过人类 gate 和 contract bus。

如需让代理实际生成文件，请在 `training_sandbox` 模式试跑，审核后再由正式阶段流程接收。

## 11. 推荐使用顺序

```text
1. 配置 .env
2. 运行离线自检
3. 运行 MCP 工具列表检查
4. 用 training_sandbox 试跑
5. 查看 run_dir 下 DeepSeek 日志和文件动作
6. 通过契约校验与人工 gate 后，再进入正式阶段
```
