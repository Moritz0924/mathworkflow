# API Agent Issue Collection

- run_id: `TRAIN-20260602_TEXTONLY_API_CODEX`
- mode: `training_sandbox`
- problem input: `00_problem/inbox/text_only_color_concentration_problem.md`
- run status: `completed_with_open_gaps`
- collected_at: `2026-06-02`

## Executive Summary

本次强制 API 大模型代理重跑证明了三件事：

1. `deep` 自动升档已生效：第 2、3 轮从 `light`/`intake` 转为 `deep`，`reasoning_effort=max`，触发原因是 `open_major_gap:structure_depth`。
2. 流式长思考监控已生效：`deepseek_stream_status.jsonl` 按约记录 chunk 数、正文字符数、reasoning 活动字符数、idle 秒数和 elapsed 秒数，未观察到 idle 卡死。
3. 训练沙盒仍不能升级为正式工作流反馈源：运行结束仍有 open fail/major queue，合同为空，提交级产物和训练增强点缺失。

主要失败不是“模型思考不够久”，而是 API agent 仍按 `intake` 阶段行动，且模型输出协议与 runner 可执行协议不匹配，导致后续 deep 轮次没有实际文件动作。

## Issue Register

| id | severity | category | problem | evidence | impact | recommended fix | blocks promotion |
|---|---|---|---|---|---|---|---|
| API-001 | critical | runner/stage scope | API 代理没有执行完整训练沙盒，只执行了当前 `intake` 阶段。 | `run_manifest.yaml` 的 initial/iteration 日志均显示 `stage: intake`；`workspace/workflow_state.yaml` 中 `current_stage: intake`，后续阶段仍 locked。 | 即使 `agent_prompt.md` 包含 16 阶段要求，模型仍被当前阶段路由限制，不能产生完整建模、代码、结果、图表、论文和反馈闭环。 | 训练沙盒 API runner 需要独立的 full-agent prompt/execution mode；不要把 `training_sandbox` 的主任务压到当前正式 workflow stage。 | yes |
| API-002 | critical | input control | 题面发生漂移：选中的纯文本题面是颜色/浓度识别，但 API 写入的 `problem_statement.md` 变成 2022 C 古代玻璃题。 | `workspace/00_problem/inbox/text_only_color_concentration_problem.md` 与 `workspace/00_problem/problem_statement.md` 内容不一致；后者标题为 2022 C 古代玻璃制品。 | benchmark、gap report 和后续产物都可能基于错误题目，训练结论不可用。 | 加入 problem source lock：运行期间输出题名、变量、样本表必须与原始 problem 文件校验；发现漂移立即 fail 并重试。 | yes |
| API-003 | critical | output protocol | deep 迭代中模型未输出 runner 可执行的 JSON file actions。 | `deepseek_file_actions.json` 显示 `action_count: 0`；iteration 2/3 logs 的 `file_actions: []`。 | deep 思考虽然发生，但没有任何修复落盘，queue 无法改善。 | 强化系统提示：只允许顶层 JSON，禁止普通 prose、伪工具标签；对非 JSON 响应立即记录 protocol fail 并重试。 | yes |
| API-004 | major | tool contract | 模型尝试使用 `<read_file/>`、`<list_files/>` 一类伪工具，但 runner 不执行这些工具。 | `deepseek_response.md` 中出现伪工具调用；`deepseek_file_actions.json` 无动作。 | 模型以为自己在检查文件，实际没有读到新上下文，也没有应用修复。 | 二选一：明确禁止伪工具并提供上下文摘要；或实现安全的 read/list 工具协议，并把结果返回下一轮。 | yes |
| API-005 | critical | iteration loop | open fail/major queue 连续两轮没有改善，触发停止。 | `run_manifest.yaml`: iteration 2 before/after 均为 4，iteration 3 before/after 均为 4，`iteration_stop_reason: same_blocking_gap_not_improving`。 | gap-driven loop 的刹车是正确的，但也说明继续加轮不会解决当前执行问题。 | 将同一 gap 两轮不改善归因到 runner/prompt/reviewer，而不是盲目增加 `max_iterations`。 | yes |
| API-006 | critical | validation | 存在 4 个阻塞项：3 个 major、1 个 fail。 | `reports/agent_revision_queue.csv`: structure_depth、figure_density、validation_completeness 为 major，contract_binding 为 fail。 | 不允许推广为训练反馈源，也不允许注入正式工作流。 | 先解决 contract_binding 和 file action protocol，再处理结构、图表、验证密度。 | yes |
| API-007 | critical | contracts | 关键合同为空。 | `reports/agent_run_validation.md` 报告 `result_contract.csv`、`claim_evidence_map.csv`、`figure_contract.csv` has no rows。 | 没有合同绑定，任何论文论断、结果和图表都不能算正式可用。 | 训练沙盒必须生成最小合同行；没有合同则 validation hard fail。 | yes |
| API-008 | critical | deliverables | 缺失提交级论文产物。 | `reports/agent_run_validation.md`: `workspace/12_submission/final_submit_paper.md` missing or empty。 | 沙盒没有完整走到可交付状态。 | full-agent mode 必须明确生成 `final_submit_paper.md`，并在生成前通过合同绑定检查。 | yes |
| API-009 | major | workflow feedback | 缺失训练增强点。 | `reports/agent_run_validation.md`: missing `training_enhancement_points.csv` and `.md`。 | 无法把沙盒发现转成 system/prompt/gate 类 workflow 改进候选。 | 在通过 validation 后生成 enhancement points；未通过时可生成 issue-only report，但不能 promotion。 | yes |
| API-010 | major | gates | 缺失模拟人工 gate 日志。 | `reports/agent_run_validation.md`: expected simulated logs for major gates, got 0。 | 沙盒没有验证深度顺序工作流的 gate 行为。 | 训练沙盒每个关键阶段写入 simulated gate log，并标出 pass/fail/blocked。 | yes |
| API-011 | major | benchmark quality | 结构深度、图表密度、验证完整性、公式细节、合同绑定均低于 benchmark。 | `reports/full_gap_report.md` 和 `reports/agent_revision_queue.csv`。 | 模型产物太短且缺乏结果支撑，不能作为建模训练样本。 | reviewer 应按 gap 类型给出可执行修复任务；figure_density 和 contract_binding 触发 deep 后必须要求文件动作落盘。 | yes |
| API-012 | major | validator strength | `validate_contracts.py --stage final_export` 可以通过/仅 warn，但 `validate_agent_run.py` 发现合同为空等 11 个 fail。 | sandbox 合同检查报告与 `reports/agent_run_validation.md` 结果不一致。 | 合同校验强度在训练/终稿场景下不够，可能让空合同漏过基础 gate。 | 收紧 `validate_contracts.py` 对 final/training stage 的必需行数、引用绑定、图文件存在检查。 | yes |
| API-013 | major | benchmark routing | benchmark 对比源受到题面漂移和极短 draft 影响，偏向 PCA/统计评价类，而非颜色浓度识别题的预期回归路线。 | `reports/full_gap_report.md` 的 benchmark source/feature comparison 与当前题面不一致。 | gap 报告方向可能仍指出“密度不足”，但具体修复建议不可靠。 | benchmark 选择应绑定 problem fingerprint；题面漂移时不应继续生成 benchmark queue。 | yes |
| API-014 | major | observability | DeepSeek 响应、route、request manifest、file action manifest 使用同名文件覆盖，只有 stream jsonl 保留多次调用。 | `deepseek_response.md`、`deepseek_route.json`、`deepseek_request_manifest.json`、`deepseek_file_actions.json` 为最终轮状态；前两轮细节主要嵌在 logs/run manifest。 | 事后审计每轮行为成本高，难以定位哪一轮出现 protocol drift。 | 每轮写独立文件：`deepseek_response_initial.md`、`deepseek_response_iteration_02.md` 等，同时保留 latest 快捷文件。 | no |
| API-015 | major | encoding | 中文内容在 shell 输出和若干生成文件中出现 mojibake。 | `workspace/00_problem/*.md` 读取结果显示大量乱码字符。 | 影响模型理解、关键词匹配、benchmark 题面识别和人工审阅。 | 统一 UTF-8 读写；对输入题面和生成文件增加 encoding sanity check。 | maybe |
| API-016 | minor | environment | pytest 不可用，且安装因代理/网络失败。 | `python -m pytest ...` 报 No module named pytest；`pip install pytest` 失败。 | 自动测试只能依赖 self-test/py_compile，覆盖不足。 | 在本地环境预装 pytest，或加入无 pytest 的 unittest fallback。 | no |
| API-017 | minor | environment | PowerShell profile 输出 `thefuck` alias 相关错误，污染命令日志。 | 多次 shell 输出开头出现 `Invoke-Expression (& thefuck --alias)` 错误。 | 对功能无直接影响，但会污染 run/debug logs。 | CI/agent shell 使用无 profile 模式，或修复本机 profile。 | no |
| API-018 | major | data governance | 外部 API 运行需要明确发送题面、提示词和项目上下文；首次 escalation 因数据外传风险被拦截，用户随后明确批准。 | 用户已明确批准本次发送 DeepSeek API；审批前 escalation 被拒。 | 这是正确的安全边界；后续批量训练不能默认外发。 | 记录 per-run external API consent，manifest 写入 approval source/time/scope。 | no |

## What Worked

- `provider.stream=true` 已进入 request manifest。
- `deep` profile 已在 open major gap 场景触发。
- `deepseek_stream_status.jsonl` 显示 reasoning-only chunk 被计为有效活动，未误判 idle。
- open fail/major queue 阻止了 `completed` 和 promotion，停止条件 `same_blocking_gap_not_improving` 生效。
- copy-risk 检查通过，没有发现高重合复制风险。

## Highest Priority Fix Order

1. 修复 full-agent API execution scope：训练沙盒不能继续被 `current_stage=intake` 限制。
2. 修复 response protocol：要求可执行 JSON file actions；非 JSON 或伪工具调用必须 fail/retry。
3. 加 problem source lock：防止题面漂移后继续 benchmark。
4. 收紧合同与提交产物 gate：空合同、缺 final paper、缺 enhancement points 均 hard fail。
5. 加 per-iteration manifests：保留每轮响应、路由、request、file actions，方便审计。
6. 修复中文编码与测试环境：减少误判和人工复盘成本。

## Promotion Decision

本 run 不能作为正式工作流改进反馈源。原因：

- `agent_revision_queue.csv` 仍有 open fail/major。
- 合同为空。
- 缺少 `training_enhancement_points.csv` 和 `.md`。
- 缺少 `final_submit_paper.md`。
- 题面发生漂移。

可推广的只有 runner 层经验：deep 自动升档、stream heartbeat、open-gap stop 条件本身是有效的；但这些应作为工程观察记录，而不是来自通过沙盒验证的 training enhancement。
