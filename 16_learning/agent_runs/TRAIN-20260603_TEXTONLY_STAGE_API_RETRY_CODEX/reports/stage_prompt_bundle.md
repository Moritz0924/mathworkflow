# Formal Stage Prompt Bundle For Full-Agent Training

This file is assembled from sandbox prompt backups derived from the normal competition prompts. The formal source prompt for each stage is listed; sandbox overlays are allowed only inside training runs.

## Global Contract

Source: `prompts/stage_prompt_contract.md`

# 阶段提示词合同 v0.2

> 中文注释：本文件是所有阶段提示词的上级规范；使用场景是在新增、审查或修订 `prompts/stages/` 下的阶段提示词时，统一输入、输出、权限、合同、校验和人工确认要求。

## 0. 目的

本文档统一数学建模工作流中每个阶段提示词的编写和执行方式。

目标不是让代理输出更多文字，而是让代理在当前阶段内充分分析、比较、核验和反思，并把算力稳定释放到既定道路上：

```text
可追踪
可审阅
绑定合同
可恢复
可由人类控制
阶段内深度推理
失败显式暴露
```

一个阶段提示词只有在清楚定义以下内容时才有效：

```text
输入
输出
权限
合同更新
校验命令
人工确认问题
失败恢复策略
阶段内深度执行骨架
```

本合同是后续 P1 技能路由、P3 自动审稿、P4 结果合同、P5 论断绑定写作和 P6 图表合同强化的 P0 基础。

---

## 1. 权威顺序

当阶段提示词与其他规则冲突时，按以下顺序执行：

```text
1. 人类最终决定或明确任务包
2. AGENTS.md
3. workflow_state.yaml 与 config/execution_policy.yaml
4. prompts/stage_prompt_contract.md
5. 当前 prompts/stages/<stage>.md
6. 专家技能说明
7. 先验数据库说明
8. 代理自由建议
```

任何阶段提示词都不得削弱更高层规则。若本合同要求深度分析，但阶段状态、合同、路径权限或人工闸门不允许执行，则必须停止并报告阻塞，而不是跨阶段代办。

---

## 2. 全局执行规则

所有阶段提示词必须遵守：

```text
- 只能使用 deep_sequential 模式。
- 不得跳过锁定阶段。
- 不得并行运行多个工作流阶段。
- 在结果和论断合同存在前，不得生成完整论文。
- 不得虚构数值结果、引用、图表文件、公式或数据字段。
- 不得复制历史论文或历史解法文本。
- 不得删除合同、日志或审稿文件来让校验通过。
- 不得允许审稿提示词直接修改交付物。
- 不得允许润色提示词改变数字、公式、标签、引用、文献、模型名或结果含义。
- 所有面向读者、评委或提交材料的最终输出必须使用中文。
- 图表、图片、流程图、PPT 和其他视觉产物中的标题、坐标轴、图例、注释、节点文字和说明文字必须使用中文；必要的英文缩写、变量名、文件名、LaTeX 命令和指标名可保留。
```

---

## 3. 阶段提示词必需结构

`prompts/stages/` 下的每个文件必须包含以下部分。

### 3.1 阶段身份

必需字段：

```yaml
stage_id: <工作流阶段 id>
stage_name: <人类可读名称>
stage_order: <整数>
roadmap_item: P0
controller: workflow_state.yaml
execution_mode: deep_sequential
```

### 3.2 目标

必须回答：

```text
本阶段产生什么决定或产物？
本阶段为什么存在于工作流中？
哪些下游阶段依赖它？
本阶段必须把算力集中到哪些判断上？
```

### 3.3 输入

必须区分：

```text
required_inputs: 阶段运行前必须存在
optional_inputs: 有帮助但非必需
human_inputs: 可能需要人类回答的问题
```

### 3.4 允许读取路径

列出阶段可以查看的精确路径或路径组，例如：

```text
00_problem/
03_data/raw/
14_contracts/result_contract.csv
```

阶段提示词可以引用全局语料规律，但阶段执行时不得读取本阶段未授权路径。若某个参考资产不在允许读取路径中，只能使用上游阶段已经写入允许路径的摘要。

### 3.5 允许写入路径

列出阶段可以写入的精确路径或路径组。不得使用含糊表述，例如“任何需要的文件”。

### 3.6 禁止动作

必须列出本阶段不能做的事。至少包含：

```text
不得绕过当前阶段锁。
不得写入允许写入路径之外的位置。
不得虚构事实、结果、引用或人工确认。
不得删除合同或日志来掩盖错误。
不得把阶段内建议直接提升为下游事实。
不得用先验语料或历史论文生成当前题目的答案。
```

### 3.7 必需输出

列出阶段完成时必须存在或明确记录阻塞原因的文件、摘要和风险报告。

若阶段会产出论文正文、图表、图片、展示材料或提交说明，必须明确写入中文输出要求：正文为中文，图中文字为中文，最终面向评审的说明为中文。

### 3.8 合同更新

说明本阶段可以读取或更新哪些合同文件，以及允许的状态变化。合同更新必须匹配 `14_contracts/` 中现有表头，不得私自改表头或新增不可校验字段。

### 3.9 允许技能

列出阶段可使用的 `nature-skills`。未列出的技能默认禁止。技能只提供阶段内专家建议，输出在归档、绑定合同并通过校验前不得成为正式事实。

### 3.10 代理提示词模板

给出可直接执行的阶段内提示词，必须重申目标、允许路径、禁止动作、校验和人工确认。

每个阶段模板都必须包含以下执行骨架：

```text
1. 输入核验：确认必需输入、阶段状态、合同和路径权限。
2. 阶段目标重述：只说明本阶段要解决的判断，不扩展到下游。
3. 深度分析：列出本阶段内需要比较、反证、交叉核验的关键点。
4. 证据绑定：说明输出如何绑定数据、代码、合同、图表、公式或引用。
5. 风险清单：列出不足、冲突、缺失和需要人工确认的点。
6. 自检清单：按禁止动作、合同字段、中文输出和校验命令逐项检查。
7. 人工确认输出：给出清晰的人工闸门问题。
```

### 3.11 校验命令

列出阶段结束前应该运行的命令。无法运行时必须如实记录 `not_run`，不得声称通过。

### 3.12 人工确认问题

给出一个具体问题，用于阶段交付后的人类确认。

### 3.13 失败恢复

用表格列出失败模式和安全恢复方式。

### 3.14 完成条件

列出阶段真正完成的判定标准。完成条件必须包含“未触发本阶段禁止动作”或等价约束。

---

## 4. 推荐状态值

```text
pending
running
blocked
completed_waiting_gate
completed_confirmed
```

合同状态值应优先使用 `config/contract_policy.yaml` 中允许的状态：

```text
draft
ready
frozen
blocked
closed
waived
```

---

## 5. 论文数据集抽象规律

本仓库的本地先验语料已经抽取为抽象特征和经验卡片，可作为提示词设计依据，但不得作为当前题目的事实答案。

```text
语料规模：312 篇 PDF，305 篇可用抽取文本。
模型族分布：统计评价 105，优化决策 95，预测回归 59，机理仿真 32，机器学习 14，其他 7。
整体优秀样本图/表/公式提及中位数约为 12/8/2。
主要资产：
- 13_prior_db/cards/prior_cards.jsonl
- 13_prior_db/screening/pdf_manifest.csv
- 16_learning/training_data/corpus_features.csv
- 16_learning/reports/training_report.md
- 08_figures/figure_template_registry.csv
```

使用规则：

```text
- 只能提取题型经验、模型族倾向、图表族倾向、评分风险和结构风险。
- 不得复制历史论文摘要、正文段落、图注、表格或结论。
- 不得把历史论文的模型输出、数值或结论当作当前题目的结果。
- 若阶段允许读取路径不包含某项资产，只能使用上游阶段已归档到允许路径中的摘要。
- 数据集规律是校准“密度、类型和风险”的参考，不是强制套模板。
```

---

## 6. 图表与写作质量原则

图表系统必须服务于论证，不得装饰化。正式图表应优先考虑与数据特征和模型族匹配的高级图表：

```text
统计评价：指标体系图、权重热力图、综合得分矩阵图、排序坡度图。
优化决策：目标约束结构图、Pareto 前沿图、路径/网络图、甘特图、敏感性热力图。
预测回归：变量关系热力图、预测区间图、残差诊断组图、误差分布图。
机理仿真：机制示意图、状态转移图、仿真轨迹图、参数敏感性图、情景对比图。
机器学习：特征重要性图、混淆矩阵、误差诊断图、嵌入/聚类可视化、消融对比图。
```

图表数量和种类必须与题型、模型和证据密度相称。优秀样本的宏观规律提示图表应足够支撑论证，但不得为了追求数量制造重复图、冲突图或无证据图。

正式图表必须：

```text
- 绑定 result_id、evidence_source、claim_id 或 used_in_section。
- 使用非默认配色，优先复用 08_figures/figure_template_registry.csv 中的模板与调色板。
- 图中文字为中文，必要英文缩写和变量名除外。
- 通过 `quality_score >= 4.2` 的质量门槛，或明确降级为探索性材料。
```

论文写作必须围绕 `claim_evidence_map.csv`，不得新增无证据强论断。若图表、表格、公式或引用密度不足以支撑章节论证，必须写入缺口报告或返回上游阶段。

---

## 7. 编写原则

阶段提示词应当明确、可执行、可校验。它应该帮助代理少猜测、多核验，在当前阶段内充分思考，并在信息不足时停下来暴露风险。

强约束提示词不等于冗长输出。每个阶段都应优先产出可复用的结构化判断、合同绑定说明和阻塞原因，而不是泛泛的长篇说明。


## Stage 0: latex_template

Sandbox source: `prompts/training_sandbox/stages/00_latex_template.md`
Formal source: `prompts/stages/00_latex_template.md`

# Training Sandbox Prompt Backup: latex_template

Formal source prompt: `prompts/stages/00_latex_template.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`latex_template` - LaTeX 模板初始化

> 中文注释：使用阶段为 `latex_template`；使用场景是在建模内容产生前，初始化并核验 LaTeX 论文骨架，只建立可承载后续合同绑定内容的结构。

## 1. 阶段身份

```yaml
stage_id: latex_template
stage_name: LaTeX 模板初始化
stage_order: 0
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. 目标

在建模内容产生前创建并核验 LaTeX 论文骨架。算力集中在模板结构、中文排版、章节接口、图表/公式/引用占位规范和后续合同引用接口上，不生成任何当前题目的事实、模型结果或论文正文。

## 3. 必需输入

```text
- workflow_state.yaml
- config/execution_policy.yaml
- templates/ 或 02_latex_template/
```

## 4. 可选输入

```text
- 人工说明
- 上游阶段风险报告
- TASK_PACKET.md 中明确点名的相关文件
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- templates/
- 02_latex_template/
```

## 6. 允许写入路径

```text
- 02_latex_template/
- 10_ai_logs/
```

## 7. 禁止动作

```text
- 不得违反 AGENTS.md 或 config/execution_policy.yaml。
- 不得写入允许写入路径之外的位置。
- 不得虚构数据、结果、引用、公式、图表或人工确认。
- 不得删除合同、日志或审稿文件来让校验通过。
- 不得把模板占位文字写成可提交论文事实。
- 不得在模板阶段插入未登记图表、未验证引用或未冻结结果。
```

## 8. 必需输出

```text
- 可编译或可诊断的 LaTeX 主文件和章节骨架
- 中文论文结构说明或模板初始化记录
- 图表、公式、引用标签命名规则说明
- 阶段总结
- 风险报告
- 合同更新说明
- 校验状态说明
```

## 9. 合同更新

```text
可更新：无
只读：14_contracts/*.csv
```

## 10. 允许技能

```text
- 无
```

技能输出在写入允许输出、必要时绑定合同并通过校验前，只有建议性质。

## 11. 代理提示词模板

```text
你正在执行 v3.2-MVP 合同驱动数学建模工作流的 latex_template 阶段。

输入核验：
1. 确认 workflow_state.yaml、config/execution_policy.yaml、templates/ 或 02_latex_template/ 可读。
2. 确认 execution_mode 为 deep_sequential，且本阶段未绕过人工闸门。
3. 只使用允许读取路径和允许写入路径。

阶段目标：
建立中文数学建模论文骨架，使后续章节可以安全插入合同绑定的论断、结果、图表、公式和引用。模板不是论文内容，不得产生当前题目的模型事实。

深度分析：
1. 检查主文件、章节文件、参考文献入口、图片路径、编译命令和中文字体支持。
2. 设计统一的 label 前缀：图、表、公式、算法、章节必须可追踪且不冲突。
3. 检查模板是否给后续 result_contract、figure_contract、formula_contract、citation_contract 留出清晰引用接口。
4. 检查是否存在会误导下游的示例数字、示例图表或示例引用；若存在，标为占位或移除。

证据绑定：
本阶段不新增合同事实；只说明后续章节应如何引用合同登记的结果、图表、公式和引用。

风险清单：
记录中文编译风险、模板格式风险、占位文本风险、路径风险和比赛格式不确定性。

自检清单：
1. 未写入允许路径之外的位置。
2. 未生成模型、数据结果、论文论断或引用。
3. 模板中的最终可见文字默认中文。
4. 校验命令已运行，或如实记录 not_run。

人工确认输出：
给出模板是否符合目标比赛格式、页数和章节约束的确认问题。
```

## 12. 校验命令

```bash
python scripts/compile_latex.py
```

```bash
python scripts/check_gates.py --dev-debug
```

## 13. 人工确认问题

```text
模板是否符合目标比赛格式以及页数或章节约束？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 编译失败 | 只修复模板、字体、路径或 LaTeX 语法；不得用删除正文事实来修复。 |
| 必需输入缺失 | 记录缺失项，不自行推断；若阻塞下游，则询问人类。 |
| 模板含伪事实 | 删除或标记为占位，不得保留为论文内容。 |
| 校验命令不可用 | 标记为 `not_run` 或尚未实现，不得声称通过。 |
| 合同冲突 | 保留合同，报告冲突，并返回拥有该合同的上游阶段。 |

## 15. 完成条件

```text
- 必需输出存在，或阻塞项已明确记录。
- 模板只提供结构，不包含当前题目事实。
- 合同更新说明符合权限。
- 校验命令已运行，或如实记录未运行状态。
- 人工确认问题已给出。
- 完成本阶段不需要任何禁止动作。
```



## Stage 1: intake

Sandbox source: `prompts/training_sandbox/stages/01_intake.md`
Formal source: `prompts/stages/01_intake.md`

# Training Sandbox Prompt Backup: intake

Formal source prompt: `prompts/stages/01_intake.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`intake` - 赛题接收

> 中文注释：使用阶段为 `intake`；使用场景是在收到赛题和附件后，整理题面、附件清单、比赛元数据、变量单位、显式约束和缺失信息风险。

## 1. 阶段身份

```yaml
stage_id: intake
stage_name: 赛题接收
stage_order: 1
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. 目标

在不求解问题的前提下，规范化赛题文本、附件清单、比赛元数据和缺失信息风险。算力集中在准确抽取题面事实、数据附件、变量单位、目标约束、交付物和评分暗示上，为 EDA 与任务拆解提供可靠入口。

## 3. 必需输入

```text
- workflow_state.yaml
- config/execution_policy.yaml
- 00_problem/inbox/
```

## 4. 可选输入

```text
- 03_data/raw/
- 人工补充的题面文本
- TASK_PACKET.md 中明确点名的相关文件
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 00_problem/
- 03_data/raw/
```

## 6. 允许写入路径

```text
- 00_problem/
- 01_task_analysis/
- 10_ai_logs/
```

## 7. 禁止动作

```text
- 不得求解问题或给出模型结论。
- 不得虚构附件内容。
- 不得跳过扫描版、损坏文件、缺失附件或 OCR 风险。
- 不得写入允许写入路径之外的位置。
- 不得把题面重述改写成带有解题假设的版本。
- 不得把历史论文或先验材料写入题面整理。
```

## 8. 必需输出

```text
- 00_problem/problem_statement.md
- 00_problem/attachments_overview.md
- 01_task_analysis/missing_information.md
- 题面事实清单：变量、单位、对象、时空范围、目标、约束、显式交付物
- 阶段总结和风险说明
```

## 9. 合同更新

```text
可更新：无
只读：14_contracts/*.csv
```

## 10. 允许技能

```text
- 无
```

## 11. 代理提示词模板

```text
你正在执行 intake 阶段。

输入核验：
1. 检查 00_problem/inbox/ 与 03_data/raw/ 中的题面和附件。
2. 确认当前 workflow_state 允许执行 intake，且未跨过锁定阶段。
3. 只读写本文件列出的路径。

阶段目标：
整理题面、附件和缺失信息，不建模、不求解、不写结果。

深度分析：
1. 逐项提取题目对象、变量、单位、时间范围、空间范围、约束、目标函数暗示和交付要求。
2. 区分官方事实、附件事实、人工补充、无法确认信息和代理推测；推测不得进入题面事实。
3. 建立附件清单：文件名、类型、可读性、字段概览、是否需要 OCR、是否可能缺失。
4. 识别评分风险：题目问法不清、附件不全、单位口径不一致、数据来源不明、提交格式不明。
5. 为 task_analysis 留出问题编号候选，但不确定子问题边界时只写多种解释。

证据绑定：
所有题面事实必须能追溯到题面原文、附件或人工补充说明；缺少来源的内容写入 missing_information。

风险清单：
记录 OCR、附件缺失、字段含义不明、单位不明、比赛元数据缺失和题目解释歧义。

自检清单：
1. 未选择模型。
2. 未写任何结果或论文结论。
3. 未复制先验论文文本。
4. 未把不确定信息写成事实。
5. 校验命令已运行或记录 not_run。

人工确认输出：
请人类确认题面和附件清单是否完整，以及哪些歧义解释应保留。
```

## 12. 校验命令

```bash
python scripts/check_gates.py --dev-debug
```

## 13. 人工确认问题

```text
题面和附件清单是否完整，是否存在需要人工补录或澄清的官方要求？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 题面无法读取 | 记录 OCR 或文本缺失风险，并请求人工补录。 |
| 附件缺失 | 在缺失信息报告中列明，不得虚构。 |
| 格式无法识别 | 只登记文件与风险，等待人工处理。 |
| 题面解释冲突 | 保留多种解释并要求人工确认，不提前建模。 |
| 阶段锁不匹配 | 停止执行并报告当前 `current_stage`。 |

## 15. 完成条件

```text
- 题面和附件状态已记录。
- 变量、单位、对象、约束和交付要求已尽力抽取。
- 不确定信息已进入 missing_information。
- 未产生任何模型、结果或论文结论。
- 未触发本阶段禁止动作。
```



## Stage 2: eda

Sandbox source: `prompts/training_sandbox/stages/02_eda.md`
Formal source: `prompts/stages/02_eda.md`

# Training Sandbox Prompt Backup: eda

Formal source prompt: `prompts/stages/02_eda.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`eda` - 探索性数据分析

> 中文注释：使用阶段为 `eda`；使用场景是在正式建模前检查数据质量、字段含义、分布特征、异常结构、可复现性和描述性风险。

## 1. 阶段身份

```yaml
stage_id: eda
stage_name: 探索性数据分析
stage_order: 2
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. 目标

刻画可用数据，产出谨慎的描述性发现，为模型路由提供依据，但不得形成冻结结果。算力集中在字段画像、数据质量、分布形态、缺失异常、单位口径、可视化探索和复现风险上。

## 3. 必需输入

```text
- workflow_state.yaml
- config/execution_policy.yaml
- 03_data/raw/ 或已登记数据说明
```

## 4. 可选输入

```text
- 00_problem/problem_statement.md
- 00_problem/attachments_overview.md
- 人工字段解释
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 00_problem/
- 03_data/
- 04_eda_code/
```

## 6. 允许写入路径

```text
- 03_data/
- 04_eda/
- 04_eda_code/
- 08_figures/eda_figures/
- 10_ai_logs/
```

## 7. 禁止动作

```text
- 不得把 EDA 输出当作冻结结果。
- 不得写最终结果分析。
- 不得生成正式论文图表引用。
- 不得伪造缺失字段或单位。
- 不得为了建模方便静默删除异常样本。
- 不得在未说明口径时比较不同来源数据。
```

## 8. 必需输出

```text
- 数据字典或字段说明
- 数据质量报告
- EDA 摘要
- 探索性图表或未生成图表的原因
- 可复现性风险说明
- 阶段总结
```

## 9. 合同更新

```text
可更新：data_contract.yaml 草稿（如适用）
只读：其他 14_contracts/*.csv
```

## 10. 允许技能

```text
- nature-data（如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 eda 阶段。

输入核验：
1. 检查数据文件、题面整理和附件概览是否存在。
2. 检查数据读取命令、编码、分隔符、表头、缺失标记和单位说明。
3. 只读写本阶段允许路径。

阶段目标：
描述数据、发现质量风险、为模型路线提供依据；不得把描述性发现写成最终结论。

深度分析：
1. 为每个字段建立画像：类型、单位、缺失率、唯一值、范围、异常值、是否与题面变量对应。
2. 检查样本量、分组结构、时间/空间字段、重复记录、异常记录、量纲混用和数据泄漏风险。
3. 对数值字段做分布、相关、趋势、离群和尺度检查；对类别字段做频数、稀疏类别和编码风险检查。
4. 生成探索性图表时只放入 08_figures/eda_figures/，并标记为 exploratory，不得登记为正式论文图。
5. 明确哪些数据特征支持统计评价、优化决策、预测回归、机理仿真或机器学习路线，哪些路线受限。

证据绑定：
EDA 摘要中的每个描述性发现必须能追溯到数据文件、字段和计算脚本；尚未复核的发现只写成风险或候选。

风险清单：
记录缺失、异常、单位、口径、样本量、数据来源、复现命令、字段解释和图表可用性风险。

自检清单：
1. 未冻结结果。
2. 未写结果分析。
3. 未生成正式论文图表引用。
4. 未静默清洗数据。
5. 校验命令已运行或记录 not_run。

人工确认输出：
请人类确认是否需要先修正数据，再进入 task_analysis 或 model_route。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage current --warn-only
```

## 13. 人工确认问题

```text
EDA 警告是否需要在模型路由前先修正数据或补充字段解释？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 数据文件缺失 | 回到 intake 或请求人工补充。 |
| 字段含义不明 | 标记为风险，不自行猜测。 |
| EDA 代码失败 | 记录失败命令和报错，先修复数据读取。 |
| 图表无法生成 | 保留表格摘要，不晋升为正式图。 |
| 清洗规则不确定 | 写入风险并请求人工确认，不静默处理。 |

## 15. 完成条件

```text
- 数据质量和字段含义风险已记录。
- EDA 产物没有被当作冻结结果。
- 探索性图表未被登记为正式论文图。
- 下游模型路由可以读取本阶段摘要。
- 未触发本阶段禁止动作。
```



## Stage 3: task_analysis

Sandbox source: `prompts/training_sandbox/stages/03_task_analysis.md`
Formal source: `prompts/stages/03_task_analysis.md`

# Training Sandbox Prompt Backup: task_analysis

Formal source prompt: `prompts/stages/03_task_analysis.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`task_analysis` - 任务拆解

> 中文注释：使用阶段为 `task_analysis`；使用场景是在题面和数据初查后，将赛题拆成可建模子问题、交付物、评价标准、依赖关系和风险边界。

## 1. 阶段身份

```yaml
stage_id: task_analysis
stage_name: 任务拆解
stage_order: 3
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. 目标

将赛题拆解为子问题、交付物、假设、依赖关系和建模要求。算力集中在题目问法、数据可用性、问题类型、输出格式、评价标准和下游依赖上，不提前选择最终模型或写结果。

## 3. 必需输入

```text
- 00_problem/problem_statement.md
- 00_problem/attachments_overview.md
- 03_data/data_quality_report.md（如已有数据）
```

## 4. 可选输入

```text
- 04_eda/eda_summary_for_paper.md
- 人工任务理解说明
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 00_problem/
- 01_task_analysis/
- 03_data/
- 04_eda/
```

## 6. 允许写入路径

```text
- 01_task_analysis/
- 10_ai_logs/
```

## 7. 禁止动作

```text
- 不得选择最终模型。
- 不得写模型结果。
- 不得忽略题目显式交付要求。
- 不得把先验论文内容写入题目拆解。
- 不得把题面歧义强行解释成单一路线。
- 不得为迎合常见模板而改变题目目标。
```

## 8. 必需输出

```text
- 01_task_analysis/task_decomposition.md
- 01_task_analysis/problem_model_profile.csv
- 01_task_analysis/question_dependency_map.md 或同等说明
- 子问题输入/输出/风险/交付物矩阵
- 阶段总结和风险说明
```

## 9. 合同更新

```text
可更新：无
只读：14_contracts/*.csv
```

## 10. 允许技能

```text
- 无
```

## 11. 代理提示词模板

```text
你正在执行 task_analysis 阶段。

输入核验：
1. 读取题面、附件概览和已有数据质量报告。
2. 确认没有跳过 intake/eda 的必要风险。
3. 只读写本阶段允许路径。

阶段目标：
拆解子问题、交付物、依赖和风险，为 prior_retrieval 与 model_route 提供问题画像；不得直接给出最终模型或结果。

深度分析：
1. 按官方问法拆出 Q1、Q2、Q3 等子问题，标明每个问题的目标、输入、输出、约束和评价口径。
2. 判断每个子问题更接近数据评价型、优化决策型、预测分析型、机理仿真型、机器学习型或混合型，但不得锁定模型。
3. 建立依赖关系：哪些问题依赖前一问结果、哪些共享数据、哪些需要人工假设。
4. 提取交付物要求：公式、算法、结果表、图表、方案建议、敏感性分析、误差分析或提交说明。
5. 识别评分风险：问题边界不清、目标函数不明确、评价标准缺失、数据支撑不足、结果可解释性不足。
6. 为先验检索输出关键词和模型族候选，但所有候选保持 advisory。

证据绑定：
拆解中的每个子问题必须对应题面语句、附件数据或 EDA 风险；无法绑定的解释写为待确认项。

风险清单：
记录题面歧义、数据不匹配、交付物冲突、依赖顺序不明和人工确认需求。

自检清单：
1. 未选择最终模型。
2. 未产生结果。
3. 未复制历史论文结构或文本。
4. 每个子问题都有输入、输出和风险。
5. 校验命令已运行或记录 not_run。

人工确认输出：
请人类确认拆解是否覆盖官方题目要求，以及是否接受保留的歧义解释。
```

## 12. 校验命令

```bash
python scripts/check_gates.py --dev-debug
```

## 13. 人工确认问题

```text
拆解结果是否与官方题目交付要求一致，是否需要合并、拆分或重命名子问题？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 题面不完整 | 回到 intake 补齐题面。 |
| 子问题边界不清 | 记录多种解释，交给人工确认。 |
| 数据与题目不匹配 | 写入风险报告，不强行建模。 |
| 依赖关系不明确 | 保守标记依赖，等待模型路由复核。 |
| 交付要求冲突 | 明确冲突来源并请求人工裁决。 |

## 15. 完成条件

```text
- 每个子问题都有输入、输出、依赖和风险描述。
- problem_model_profile.csv 能支持先验检索和模型路由。
- 后续阶段能读取问题画像。
- 未产生越权模型结论。
- 未触发本阶段禁止动作。
```



## Stage 4: prior_retrieval

Sandbox source: `prompts/training_sandbox/stages/04_prior_retrieval.md`
Formal source: `prompts/stages/04_prior_retrieval.md`

# Training Sandbox Prompt Backup: prior_retrieval

Formal source prompt: `prompts/stages/04_prior_retrieval.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`prior_retrieval` - 先验经验卡片检索

> 中文注释：使用阶段为 `prior_retrieval`；使用场景是在模型路由前，从先验材料中提取经验卡片、图表族提示和评分风险提示，但不复制历史论文文本。

## 1. 阶段身份

```yaml
stage_id: prior_retrieval
stage_name: 先验经验卡片检索
stage_order: 4
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P2
```

## 2. 目标

从先验材料中抽取可复用建模经验卡片，不复制历史论文文本。算力集中在题型匹配、模型族倾向、常见图表族、评分风险和结构缺口上，输出必须保持 advisory_only。

## 3. 必需输入

```text
- config/prior_db_policy.yaml
- 01_task_analysis/problem_model_profile.csv
```

## 4. 可选输入

```text
- 13_prior_db/
- 13_sample_prior/
- 01_task_analysis/task_decomposition.md
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 01_task_analysis/
- 13_prior_db/
- 13_sample_prior/
```

## 6. 允许写入路径

```text
- 13_prior_db/
- 10_ai_logs/
- 11_review/
```

## 7. 禁止动作

```text
- 不得复制历史论文摘要、正文、表格、图注或结论。
- 不得把历史论文当作当前题目的事实答案。
- 不得输出可直接粘贴到论文的段落。
- 不得绕过 prior_db_policy.yaml。
- 不得使用先验材料替代题面、数据、代码或合同证据。
- 不得把低样本类别提示包装成强推荐。
```

## 8. 必需输出

```text
- 13_prior_db/pre_solve_cards.md 或等价经验卡片
- copy-risk 或风险说明
- 与 problem_model_profile.csv 对齐的模型族、图表族、评分风险摘要
- 阶段总结
```

## 9. 合同更新

```text
可更新：无
只读：14_contracts/*.csv
```

## 10. 允许技能

```text
- nature-reader（如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 prior_retrieval 阶段。

输入核验：
1. 检查 config/prior_db_policy.yaml 和 01_task_analysis/problem_model_profile.csv。
2. 若 13_prior_db/cards/prior_cards.jsonl 可读，则优先使用其中 copy_risk_status=abstracted_pass 的抽象卡片。
3. 可参考 13_prior_db/screening/pdf_manifest.csv 的类别、模型族和 source_count；不得读取未授权路径。

阶段目标：
只抽取题型经验、常见模型族、常见图表类型、评分风险和预处理模式；不得生成当前题目的答案。

深度分析：
1. 将每个子问题画像映射到先验卡片的 problem_type、family、model_hints、figure_hints 和 scoring_risks。
2. 对候选模型族给出支持理由和风险理由，区分高样本规律与低样本警告。
3. 对图表族只输出抽象建议，例如权重热力图、Pareto 前沿图、残差诊断组图、机制示意图；不得复用历史图注。
4. 对评分风险输出可行动提醒，例如约束不可追踪、残差诊断缺失、外推边界不清、权重来源弱。
5. 若检索结果与题面或 EDA 冲突，优先题面和数据，先验只记录为风险。

证据绑定：
每张经验卡片必须记录来源卡片 ID、类别、模型族、source_count 或 copy_risk_status；不得引用历史论文正文。

风险清单：
记录拷贝风险、低样本风险、题型不匹配风险、先验与题面冲突风险和技能不可用风险。

自检清单：
1. 输出保持 advisory_only。
2. 没有历史论文可复制文本。
3. 没有当前题目事实答案。
4. 没有把先验卡片写入结果、图表或论文合同。
5. 校验命令已运行或记录 not_run。

人工确认输出：
请人类确认这些先验卡片只作为提示使用，且无复制历史表述或结构。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage prior_retrieval
```

```bash
python scripts/check_prior_copy_risk.py --warn-only
```

## 13. 人工确认问题

```text
这些先验卡片是否只作为提示使用，且没有复制历史表述、图注、表格或结论？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 先验库不存在 | 创建空经验卡片占位，并说明没有可用先验。 |
| 拷贝风险过高 | 丢弃相关文本，只保留抽象经验标签。 |
| 问题画像缺失 | 返回 task_analysis 补齐画像。 |
| 技能不可用 | 记录未运行，使用本地保守模板。 |
| 先验与题面冲突 | 保留题面优先原则，将先验记录为风险而非建议。 |

## 15. 完成条件

```text
- 输出只包含经验卡片和风险提示。
- 没有历史论文可复制文本。
- 每条建议标明 advisory_only。
- 下游模型路由能读取卡片 ID 或提示。
- 未触发本阶段禁止动作。
```



## Stage 5: model_route

Sandbox source: `prompts/training_sandbox/stages/05_model_route.md`
Formal source: `prompts/stages/05_model_route.md`

# Training Sandbox Prompt Backup: model_route

Formal source prompt: `prompts/stages/05_model_route.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`model_route` - 模型族路由

> 中文注释：使用阶段为 `model_route`；使用场景是在任务拆解和数据检查后，为各子问题选择主模型、备选模型、变量、公式路线和验证方案。

## 1. 阶段身份

```yaml
stage_id: model_route
stage_name: 模型族路由
stage_order: 5
gate_type: hard
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. 目标

根据可行性、数据状态和评分风险，为每个子问题选择模型族和备选方案。算力集中在题型-数据-模型适配、可解释性、复现难度、结果可验证性、图表表达潜力和人工确认点上。

## 3. 必需输入

```text
- 01_task_analysis/task_decomposition.md
- 01_task_analysis/problem_model_profile.csv
- 03_data/data_quality_report.md
```

## 4. 可选输入

```text
- 13_prior_db/pre_solve_cards.md
- 04_eda/eda_summary_for_paper.md
- 人工模型偏好或约束
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 00_problem/
- 01_task_analysis/
- 03_data/
- 04_eda/
- 13_prior_db/
- 14_contracts/
```

## 6. 允许写入路径

```text
- 05_model/
- 14_contracts/formula_contract.csv
- 10_ai_logs/
- 11_review/
```

## 7. 禁止动作

```text
- 不得在人工确认前冻结模型路线。
- 不得生成求解代码。
- 不得把先验卡片当作答案。
- 不得选择数据无法支撑的模型而不标风险。
- 不得为追求复杂度选择不可复现或不可解释模型。
- 不得登记尚未定义符号的重要公式。
```

## 8. 必需输出

```text
- 05_model/model_route.md
- 05_model/fallback_plan.md
- 05_model/symbols.md 或等价符号说明
- 每个子问题的主模型、备选模型、验证方案和图表表达建议
- 14_contracts/formula_contract.csv 草稿行（如有重要公式）
- 阶段总结和人工闸门说明
```

## 9. 合同更新

```text
可更新：14_contracts/formula_contract.csv
只读：其他合同
```

## 10. 允许技能

```text
- 无；Prior DB 只能作为已归档经验输入
```

## 11. 代理提示词模板

```text
你正在执行 model_route 阶段。

输入核验：
1. 检查 task_decomposition、problem_model_profile 和 data_quality_report。
2. 若允许读取路径中存在 13_prior_db/pre_solve_cards.md 或 13_prior_db/cards/prior_cards.jsonl，可读取抽象经验；不得读取未授权路径。
3. 确认当前阶段需要人工硬闸门，模型路线不得自动冻结。

阶段目标：
为每个子问题选择主模型和备选模型，说明数据适配性、可解释性、复现性、风险和人工确认点；不得生成代码或论文结果。

深度分析：
1. 对每个子问题建立候选路线矩阵：模型族、输入变量、输出指标、核心假设、公式对象、可验证性、复现成本、失败后备选。
2. 使用题目和 EDA 优先原则：数据不能支撑的模型不得作为主模型；先验卡片只能提醒常见路线和评分风险。
3. 针对模型族做专业判断：
   - 统计评价：指标体系、权重来源、排序稳定性和敏感性。
   - 优化决策：决策变量、目标函数、约束、基线方案和可行性。
   - 预测回归：特征选择、误差指标、残差诊断、外推边界和预测区间。
   - 机理仿真：状态变量、参数来源、情景设定、稳定性和敏感性。
   - 机器学习：训练/验证划分、数据泄漏、解释性、泛化风险和可复现种子。
4. 为每个重要公式登记 formula_contract 草稿：formula_id、question_id、symbols_defined、derivation_source、validation_note。
5. 为 figures 阶段预留图表表达建议，但不生成正式图。

证据绑定：
每个模型选择必须绑定子问题 ID、数据字段、EDA 发现、先验卡片 ID 或人工约束；无法绑定的路线降级为备选或 blocked。

风险清单：
记录数据不匹配、变量缺失、假设过强、模型不可复现、公式符号不清、图表表达不足和人工确认需求。

自检清单：
1. 未生成代码。
2. 未写结果。
3. 未把先验当答案。
4. 每个主模型都有备选模型。
5. 重要公式已登记或说明暂不登记。
6. 校验命令已运行或记录 not_run。

人工确认输出：
请人类批准每个子问题的模型族、备选方案和不可接受风险。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage current --warn-only
```

## 13. 人工确认问题

```text
是否批准每个子问题的模型族、备选方案、核心假设和失败降级路线？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 模型与数据不匹配 | 降级为更稳健的备选方案并说明原因。 |
| 关键变量缺失 | 返回数据或任务分析阶段补齐。 |
| 公式无法解释 | 不写入公式合同，先补模型说明。 |
| 先验提示冲突 | 优先题面和数据，将先验冲突写为风险。 |
| 人工未确认 | 停在 `model_route_gate`。 |

## 15. 完成条件

```text
- 每个子问题有主模型、备选模型、验证方案和风险说明。
- 重要公式已登记或说明暂不登记。
- 模型路线不依赖历史论文答案。
- 等待或完成人工模型路线确认。
- 未触发本阶段禁止动作。
```



## Stage 6: codegen

Sandbox source: `prompts/training_sandbox/stages/06_codegen.md`
Formal source: `prompts/stages/06_codegen.md`

# Training Sandbox Prompt Backup: codegen

Formal source prompt: `prompts/stages/06_codegen.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`codegen` - 分问题代码生成

> 中文注释：使用阶段为 `codegen`；使用场景是在模型路线经人工确认后，按问题逐个生成、运行和记录可复现求解代码。

## 1. 阶段身份

```yaml
stage_id: codegen
stage_name: 分问题代码生成
stage_order: 6
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P4
```

## 2. 目标

一次只为一个问题生成并运行可复现求解代码，产出候选结果文件。算力集中在模型路线忠实实现、数据读取、随机性控制、运行日志、错误处理和结果来源可追踪上。

## 3. 必需输入

```text
- 05_model/model_route.md
- 05_model/fallback_plan.md
- 03_data/ 或已确认数据源
```

## 4. 可选输入

```text
- 14_contracts/formula_contract.csv
- 04_eda/
- 人工实现约束
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 00_problem/
- 01_task_analysis/
- 03_data/
- 04_eda/
- 05_model/
- templates/code/
```

## 6. 允许写入路径

```text
- 06_code/
- 07_results/
- 10_ai_logs/
- 11_review/
```

## 7. 禁止动作

```text
- 不得同时生成多个问题的代码。
- 不得绕过已批准模型路线。
- 不得将未运行代码的输出写成结果。
- 不得写论文结果分析。
- 不得静默替换模型以追求运行成功。
- 不得把调试输出伪装为正式结果。
```

## 8. 必需输出

```text
- 对应问题的代码文件
- 运行日志
- 候选结果文件
- 随机种子、依赖、输入文件和输出文件说明
- 失败或复现风险说明
```

## 9. 合同更新

```text
可更新：建议只生成 result_contract 候选说明，正式冻结在 results_freeze 阶段
只读：formula_contract.csv
```

## 10. 允许技能

```text
- 无
```

## 11. 代理提示词模板

```text
你正在执行 codegen 阶段。

输入核验：
1. 确认模型路线已经人工批准或任务包明确授权。
2. 读取当前指定问题的模型、变量、公式、数据路径和备选方案。
3. 只处理当前问题，不跨问题并行。

阶段目标：
按已批准模型路线生成可复现代码，真实运行并记录候选结果；失败时记录失败原因，不伪造结果。

深度分析：
1. 将模型路线拆成数据读取、预处理、模型计算、验证、输出保存和日志记录步骤。
2. 明确每个输入文件、字段、单位和清洗规则；任何与 EDA 不一致的处理都要记录。
3. 若模型涉及随机性，设置并记录 random_seed；若无随机性，说明 deterministic。
4. 结果文件必须可被 results_freeze 追踪到 source_file、source_row_or_cell、code_file、run_id。
5. 如果代码无法实现主模型，先尝试最小修复；仍失败时按 fallback_plan 降级，不自行发明模型。

证据绑定：
候选结果只绑定代码运行日志和输出文件，不进入论文事实；正式 result_contract 冻结留给 results_freeze。

风险清单：
记录依赖缺失、数据读取失败、模型不收敛、随机性、结果异常、运行时间和复现风险。

自检清单：
1. 只处理一个问题。
2. 代码真实运行或失败已记录。
3. 结果文件来自运行输出。
4. 没有论文结果分析。
5. 没有绕过模型路线。
6. 校验命令已运行或记录 not_run。

人工确认输出：
请人类确认代码是否忠实实现已批准模型，而不是为了方便采用捷径。
```

## 12. 校验命令

```bash
python scripts/run_current_stage.py --question Q1
```

```bash
python scripts/validate_contracts.py --stage current --warn-only
```

## 13. 人工确认问题

```text
生成的代码是否实现了已批准模型，而不是为了运行方便采用了未批准捷径？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 代码运行失败 | 修复最小代码路径并重跑，保留日志。 |
| 模型路线不可实现 | 返回 model_route 记录备选模型。 |
| 数据读取失败 | 返回 eda 或数据准备阶段。 |
| 结果异常 | 标记为候选结果，不进入冻结。 |
| 随机性不可复现 | 固定种子或记录无法复现原因，不冻结。 |

## 15. 完成条件

```text
- 指定问题代码存在并可解释。
- 运行日志和真实候选结果已保存。
- 候选结果可追踪到输入、代码、run_id 和输出文件。
- 没有把候选结果直接写成论文结论。
- 未触发本阶段禁止动作。
```



## Stage 7: results_freeze

Sandbox source: `prompts/training_sandbox/stages/07_results_freeze.md`
Formal source: `prompts/stages/07_results_freeze.md`

# Training Sandbox Prompt Backup: results_freeze

Formal source prompt: `prompts/stages/07_results_freeze.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`results_freeze` - 结果冻结

> 中文注释：使用阶段为 `results_freeze`；使用场景是在代码真实运行后，将可复核结果登记并冻结为论文可用结果来源。

## 1. 阶段身份

```yaml
stage_id: results_freeze
stage_name: 结果冻结
stage_order: 7
gate_type: hard
execution_mode: deep_sequential
roadmap_item: P4
```

## 2. 目标

将已核验代码输出晋升为冻结结果行，使 `result_contract.csv` 成为论文数字的最高结构化来源。算力集中在来源追踪、指标口径、数值一致性、复现证据、人工确认和下游图表/论断可用性上。

## 3. 必需输入

```text
- 07_results/ 中真实模型输出
- 06_code/ 运行日志
- 14_contracts/result_contract.csv
```

## 4. 可选输入

```text
- 05_model/model_route.md
- 14_contracts/formula_contract.csv
- 人工结果复核说明
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 05_model/
- 06_code/
- 07_results/
- 14_contracts/
```

## 6. 允许写入路径

```text
- 07_results/
- 14_contracts/result_contract.csv
- 14_contracts/artifact_freeze_registry.csv
- 10_ai_logs/
- 11_review/
```

## 7. 禁止动作

```text
- 不得冻结未运行或不可复核的结果。
- 不得改变模型输出数值。
- 不得为通过校验而删除结果风险。
- 不得在人工闸门前进入图表或论文阶段。
- 不得把探索性 EDA 数字晋升为模型结果。
- 不得冻结缺少 source_file、metric_name 或 metric_value 的论文可用结果。
```

## 8. 必需输出

```text
- 07_results/result_freeze_report.md
- 14_contracts/result_contract.csv 中冻结或待冻结行
- 14_contracts/artifact_freeze_registry.csv 中相关条目
- 每个结果的 source_file、source_row_or_cell、code_file、run_id、random_seed 和 freeze_status 说明
- 阶段总结和人工闸门说明
```

## 9. 合同更新

```text
可更新：result_contract.csv, artifact_freeze_registry.csv
只读：其他合同
```

## 10. 允许技能

```text
- 无
```

## 11. 代理提示词模板

```text
你正在执行 results_freeze 阶段。

输入核验：
1. 检查 07_results/ 中真实输出、06_code/ 运行日志和 result_contract.csv 表头。
2. 确认每个候选结果都有可定位的源文件、代码文件和运行记录。
3. 确认当前阶段为 hard gate，未获人工确认前不得进入 figures 或 paper_draft。

阶段目标：
逐项核对代码输出、来源文件、指标名称、指标值和可复现性；只有真实运行且可追溯的结果才能写入 result_contract 并标记冻结。

深度分析：
1. 为每个候选结果建立冻结审查表：result_id、question_id、model_id、metric_name、metric_value、unit、source_file、source_row_or_cell、code_file、run_id、random_seed。
2. 对照运行日志和输出文件确认数值没有被手工改写。
3. 检查指标口径：单位、方向、是否越大越好、是否与模型路线一致、是否可被图表或论断使用。
4. 将不确定结果标记 blocked 或 draft，不得冻结。
5. 对可论文使用的结果登记 artifact_freeze_registry，并说明 protected_atoms。

证据绑定：
每个 frozen 结果必须绑定真实文件和代码运行记录；下游图表和论断只能引用 frozen 或 ready 且可复核的结果。

风险清单：
记录结果不可复现、指标含义不明、随机性不稳定、源文件缺失、单位不明、异常值和人工未确认风险。

自检清单：
1. 没有改变结果数值。
2. 没有冻结未运行结果。
3. 每个论文可用结果都有 source_file、metric_name、metric_value。
4. 下游引用字段已预留或说明。
5. 校验命令已运行或记录 not_run。

人工确认输出：
请人类批准将这些数值结果冻结为论文唯一可用结果来源。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage figures
```

## 13. 人工确认问题

```text
是否批准将这些数值结果冻结为论文唯一可用结果来源？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 来源文件缺失 | 不冻结该结果，返回 codegen。 |
| 指标含义不明 | 标记为 blocked，等待人工解释。 |
| 结果不可复现 | 保留候选结果但不进入论文。 |
| 数值与日志不一致 | 停止冻结，重新运行或人工复核。 |
| 人工未确认 | 停在 `results_freeze_gate`。 |

## 15. 完成条件

```text
- 每个论文可用结果都有来源文件、代码文件、指标名称和指标值。
- 冻结状态与人工复核一致。
- 下游图表和论文只能读取冻结结果。
- 不确定结果已标记 blocked 或 draft。
- 未触发本阶段禁止动作。
```



## Stage 8: figures

Sandbox source: `prompts/training_sandbox/stages/08_figures.md`
Formal source: `prompts/stages/08_figures.md`

# Training Sandbox Prompt Backup: figures

Formal source prompt: `prompts/stages/08_figures.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`figures` - 结果绑定图表

> 中文注释：使用阶段为 `figures`；使用场景是在结果冻结后，设计和生成只服务于已登记结果、证据或论断的正式图表。

## 1. 阶段身份

```yaml
stage_id: figures
stage_name: 结果绑定图表
stage_order: 8
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P6
```

## 2. 目标

只在图表能支撑已登记结果、证据或论断时，设计并生成图表。算力集中在图表蓝图、图表类型选择、证据绑定、配色、中文标注、图表去冲突、导出质量和 `figure_contract.csv` 登记上。

## 3. 必需输入

```text
- 14_contracts/result_contract.csv
- 14_contracts/figure_contract.csv
- 07_results/ 中冻结结果来源
```

## 4. 可选输入

```text
- 08_figures/visual_style_guide.md
- 08_figures/chart_type_library.md
- 人工图表偏好
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 07_results/
- 08_figures/
- 14_contracts/
```

## 6. 允许写入路径

```text
- 08_figures/
- 14_contracts/figure_contract.csv
- 10_ai_logs/
- 11_review/
```

## 7. 禁止动作

```text
- 不得引用未冻结结果。
- 不得生成无论断支撑的装饰图。
- 不得在图文件不存在时登记为论文可用。
- 不得伪造图表质量分或标签。
- 不得生成英文标题、英文坐标轴、英文图例或英文注释的正式图表；必要的指标缩写和变量名除外。
- 不得使用默认配色或低辨识度配色作为正式图表风格。
- 不得为了凑数量生成重复、冲突或不服务论证的图。
```

## 8. 必需输出

```text
- 图表文件
- 图表蓝图或图表设计说明
- 14_contracts/figure_contract.csv 更新
- 图表质量或风险说明
- 阶段总结
- 所有正式图表中的标题、坐标轴、图例、注释、节点文字和说明文字必须为中文；图片生成提示词也必须明确要求图中文字为中文。
```

## 9. 合同更新

```text
可更新：figure_contract.csv
只读：result_contract.csv, claim_evidence_map.csv, formula_contract.csv, citation_contract.csv
```

## 10. 允许技能

```text
- nature-figure（如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 figures 阶段。

输入核验：
1. 检查 result_contract.csv、figure_contract.csv 和 07_results/ 中冻结结果来源。
2. 读取 08_figures/figure_template_registry.csv（若存在），优先使用 TPL_001 到 TPL_008 的高级模板。
3. 若需要参考 13_prior_db/cards/prior_cards.jsonl、16_learning/training_data/corpus_features.csv 或 16_learning/reports/training_report.md，只能使用上游阶段已经写入允许路径的摘要；本阶段不得直接读取未授权路径。

阶段目标：
每张图都必须绑定结果、证据或论断，并有真实输出路径。优先生成能解释模型结果、机制、误差、权衡和敏感性的图，避免装饰性图表。

深度分析：
1. 建立图表蓝图矩阵：figure_id、question_id、core_claim、result_id/evidence_source、chart_type、panel_plan、used_in_section、latex_label、review_risk。
2. 按模型族和数据特征选择图表：
   - 统计评价：指标体系层级图、权重热力图、综合得分矩阵图、排序坡度图。
   - 优化决策：目标约束结构图、Pareto 前沿图、路径/网络图、调度甘特图、敏感性热力图。
   - 预测回归：变量关系热力图、预测区间图、残差诊断组图、误差分布或 QQ 图。
   - 机理仿真：机制示意图、状态转移图、仿真轨迹图、参数敏感性图、情景对比图。
   - 机器学习：特征重要性图、混淆矩阵、误差诊断图、嵌入/聚类可视化、消融对比图。
3. 与语料规律对齐但不机械套数：优秀样本图表密度较高，整体图/表/公式提及中位数约 12/8/2；本阶段应保证正式图足以支撑核心论断，但不得凑重复图。
4. 图表去冲突：同一结果不重复画同质图；同一章节图表类型不堆叠；图、表、公式职责清晰。
5. 配色和风格：优先使用 figure_template_registry 的 muted_blue_gold、teal_orange_diverging、deep_blue_vermilion、nature_green_gold 等非默认配色；不得使用 matplotlib 默认蓝橙序列作为最终风格。
6. 导出要求：优先导出 svg/png/pdf 中至少一种真实存在文件，正式图建议保留矢量格式；质量分低于 4.2 的图不得进入正文。
7. 图中文字必须为中文，必要英文缩写、变量名和指标名可保留；图注必须来自合同绑定证据，不得复用历史图注。

证据绑定：
每张正式图必须写入 figure_contract.csv，并至少绑定 result_id 或 evidence_source；进入正文的图必须有 used_in_section 和 latex_label。

风险清单：
记录数据字段不足、图表类型不匹配、配色风险、中文字体风险、导出失败、质量分不足、合同绑定缺失和图表密度不足风险。

自检清单：
1. 图文件真实存在。
2. figure_contract.csv 字段可被 validate_contracts.py 校验。
3. 每张图有结果或证据绑定。
4. 图中文字为中文。
5. 非默认配色。
6. quality_score >= 4.2，或降级为探索性材料。
7. 校验命令已运行或记录 not_run。

人工确认输出：
请人类确认哪些图晋升进入论文，哪些只保留为探索性材料。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage figures
```

```bash
python scripts/check_figure_quality.py
```

## 13. 人工确认问题

```text
哪些图应晋升进入论文，哪些只保留为探索性材料？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 缺少冻结结果 | 返回 results_freeze。 |
| 图文件缺失 | 重新生成或将状态标为 blocked。 |
| 图表质量低 | 改进导出质量或降级为附录/探索图。 |
| 合同绑定缺失 | 补 `figure_contract.csv`，不先引用。 |
| 图表类型与数据不匹配 | 重新选择模板；若无合适图，记录不生成原因。 |
| 中文字体或配色失败 | 修复字体/配色后重导出，或降级为不可用。 |

## 15. 完成条件

```text
- 论文候选图都有真实文件和合同记录。
- 图表与冻结结果或论断绑定。
- 图表类型、数量和章节分布服务论证且不冲突。
- 下游论文可安全引用已登记图。
- 图中文字已检查为中文。
- 未触发本阶段禁止动作。
```



## Stage 9: paper_draft

Sandbox source: `prompts/training_sandbox/stages/09_paper_draft.md`
Formal source: `prompts/stages/09_paper_draft.md`

# Training Sandbox Prompt Backup: paper_draft

Formal source prompt: `prompts/stages/09_paper_draft.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`paper_draft` - 分章节论文草稿

> 中文注释：使用阶段为 `paper_draft`；使用场景是在结果、图表、公式、引用和论断合同齐备后，逐章节生成证据绑定草稿。

## 1. 阶段身份

```yaml
stage_id: paper_draft
stage_name: 分章节论文草稿
stage_order: 9
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P5
```

## 2. 目标

一次只草拟一个章节，内容必须来自已登记论断、结果、公式、图表和引用。算力集中在章节论证链、证据密度、图表密度、公式解释、风险边界和中文表达上，不生成全文、不新增无证据事实。

## 3. 必需输入

```text
- 14_contracts/claim_evidence_map.csv
- 14_contracts/result_contract.csv
- 14_contracts/figure_contract.csv
- 14_contracts/formula_contract.csv
- 14_contracts/citation_contract.csv
```

## 4. 可选输入

```text
- 02_latex_template/sections/
- 09_paper/section_generation_plan.csv
- 人工写作要求
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 00_problem/
- 01_task_analysis/
- 02_latex_template/
- 05_model/
- 07_results/
- 08_figures/
- 09_paper/
- 14_contracts/
```

## 6. 允许写入路径

```text
- 02_latex_template/sections/
- 09_paper/
- 10_ai_logs/
- 11_review/
```

## 7. 禁止动作

```text
- 不得写无证据论断。
- 不得引用未登记图表。
- 不得新增未登记结果数字。
- 不得一次性生成全文。
- 不得生成英文正文作为论文最终内容；必要的英文缩写、变量名、模型名和 LaTeX 命令除外。
- 不得为弥补图表或证据不足而编造解释。
- 不得复制历史论文段落、摘要、图注、表格或结论。
```

## 8. 必需输出

```text
- 指定章节草稿
- 09_paper/missing_evidence_report.md（如有缺口）
- 章节论断记录或更新
- 章节图表/公式/引用使用清单
- 阶段总结
- 指定章节草稿必须为中文；图表标题、图注和正文中对图表的解释必须使用中文。
```

## 9. 合同更新

```text
可更新：claim_evidence_map.csv 草稿行（如流程允许）
只读：result_contract.csv, figure_contract.csv, formula_contract.csv, citation_contract.csv
```

## 10. 允许技能

```text
- nature-writing（如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 paper_draft 阶段。

输入核验：
1. 检查 claim_evidence_map、result_contract、figure_contract、formula_contract、citation_contract。
2. 确认只写当前指定章节，不生成全文。
3. 若需要参考先验资产 13_prior_db/cards/prior_cards.jsonl、16_learning/training_data/corpus_features.csv 或 training_report，只能使用上游已写入允许路径的摘要；不得直接读取未授权路径。

阶段目标：
只写当前章节，只使用合同中可追踪的论断和证据。证据不足时写入缺失证据报告，而不是写强结论。

深度分析：
1. 为本章节列出 claim_id 清单，逐项检查 evidence_type、result_id、figure_id、formula_id、citation_id 和 support_grade。
2. 设计章节论证链：问题背景、方法逻辑、关键公式、结果解释、图表证据、局限边界。
3. 检查图表密度和证据密度：图、表、公式不机械追求数量，但必须足以支撑核心论断；若核心结果没有图表或表格支撑，写入 missing_evidence_report。
4. 对每个结果数字只从 result_contract 引用；不得改写数值、单位和指标含义。
5. 对每张图只从 figure_contract 引用；图题、图注和正文解释必须与 core_claim 和 caption_source 一致。
6. 对公式只使用 formula_contract 中已定义符号；未定义符号不得进入正文。
7. 对引用只用于背景、方法或假设支撑，不得用文献元数据支撑当前数值结果。

证据绑定：
每个段落的核心句必须能追踪到 claim_id 或明确标记为过渡性说明；强结论必须有 result_id、figure_id、formula_id 或 citation_id。

风险清单：
记录无证据论断、图表不足、公式未定义、引用未核验、结果数值缺失、章节逻辑断裂和中文表达风险。

自检清单：
1. 只写当前章节。
2. 没有新增未登记结果。
3. 没有引用未登记图表。
4. 没有复制历史文本。
5. 章节正文、图注和表注为中文。
6. 校验命令已运行或记录 not_run。

人工确认输出：
请人类确认是否有重要论断缺少证据，因此不应写入正文。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage paper_draft
```

## 13. 人工确认问题

```text
是否有重要论断缺少证据，因此不应写入正文或应返回上游补证？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 论断无证据 | 写入缺失证据报告，不写正文强结论。 |
| 图表合同缺失 | 返回 figures 补合同。 |
| 图表密度不足 | 写入缺口报告或返回 figures，不凑装饰图。 |
| 结果合同缺失 | 返回 results_freeze。 |
| 引用未验证 | 降级为背景说明或删除引用句。 |
| 公式符号未定义 | 返回 model_route 或公式合同补齐。 |

## 15. 完成条件

```text
- 章节文本可追踪到合同。
- 缺失证据已显式记录。
- 没有越权写入未证实结论。
- 图表、表格、公式和引用密度足以支撑章节核心论证，或缺口已记录。
- 章节正文、图注和表注为中文。
- 未触发本阶段禁止动作。
```



## Stage 10: paper_full

Sandbox source: `prompts/training_sandbox/stages/10_paper_full.md`
Formal source: `prompts/stages/10_paper_full.md`

# Training Sandbox Prompt Backup: paper_full

Formal source prompt: `prompts/stages/10_paper_full.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`paper_full` - 全文组装

> 中文注释：使用阶段为 `paper_full`；使用场景是在分章节草稿完成后，组装全文并检查跨章节一致性、证据缺口和最终审稿入口。

## 1. 阶段身份

```yaml
stage_id: paper_full
stage_name: 全文组装
stage_order: 10
gate_type: hard
execution_mode: deep_sequential
roadmap_item: P5
```

## 2. 目标

将分章节草稿组装成连贯全文，但不得新增事实或掩盖证据缺口。算力集中在跨章节逻辑、术语一致性、结果一致性、图表/公式/引用一致性、缺口显式暴露和审稿准备上。

## 3. 必需输入

```text
- 02_latex_template/sections/
- 09_paper/missing_evidence_report.md（如存在）
- 14_contracts/claim_evidence_map.csv
```

## 4. 可选输入

```text
- 09_paper/section_generation_plan.csv
- 11_review/阶段总结
- 人工全文结构意见
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 02_latex_template/
- 09_paper/
- 14_contracts/
- 11_review/
```

## 6. 允许写入路径

```text
- 02_latex_template/sections/
- 09_paper/
- 14_contracts/artifact_freeze_registry.csv
- 10_ai_logs/
- 11_review/
```

## 7. 禁止动作

```text
- 不得新增未经合同支撑的事实。
- 不得隐藏缺失证据。
- 不得改变冻结结果含义。
- 不得跳过草稿审阅闸门。
- 不得将中文论文组装成英文正文或混入英文段落；必要的英文缩写、变量名、模型名和 LaTeX 命令除外。
- 不得为了连贯性改写数字、公式、图表标签或引用。
- 不得复制历史论文结构性段落或结论。
```

## 8. 必需输出

```text
- 全文草稿或组装记录
- 全文一致性风险说明
- 需要审稿的问题清单
- 图表/表格/公式/引用一致性检查说明
- 阶段总结和人工闸门说明
- 全文草稿必须为中文；图题、表题、图注、表注和所有面向评审的说明必须为中文。
```

## 9. 合同更新

```text
可更新：artifact_freeze_registry.csv（如冻结全文候选）
只读：其他合同
```

## 10. 允许技能

```text
- nature-writing（如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 paper_full 阶段。

输入核验：
1. 检查各章节草稿、missing_evidence_report 和 claim_evidence_map。
2. 检查 result、figure、formula、citation 合同是否支持全文引用。
3. 若需要参考先验资产，只能使用上游已写入允许路径的摘要；不得直接读取未授权路径。

阶段目标：
整合章节、检查前后逻辑和引用一致性。不得添加新事实；未解决缺口必须单独列出。

深度分析：
1. 检查全文主线：问题提出、模型建立、求解、结果、分析、优缺点和结论是否形成闭环。
2. 检查术语一致性：子问题编号、模型名、变量名、指标名、单位和章节标题。
3. 检查冻结数字一致性：正文、表格、图注和结论不得出现不同版本数值。
4. 检查图表密度和位置：核心结果附近应有相应图/表/公式支撑；不充分时列为审稿前缺口。
5. 检查所有图表引用是否有 latex_label 且在 figure_contract 中登记。
6. 检查公式符号是否定义，引用是否验证，弱证据是否被写成强结论。
7. 只做结构衔接和一致性调整；任何事实新增都应回到 paper_draft 或上游合同阶段。

证据绑定：
全文中的强论断必须可追踪到 claim_evidence_map；全文候选冻结时登记 artifact_freeze_registry 并记录 protected_atoms。

风险清单：
记录章节矛盾、证据缺口、图表不足、标签冲突、引用未核验、结论过强、中文排版和人工闸门风险。

自检清单：
1. 未新增事实。
2. 未隐藏缺口。
3. 未改变冻结结果。
4. 全文和图表说明为中文。
5. 未解决问题已单独列出。
6. 校验命令已运行或记录 not_run。

人工确认输出：
请人类批准这版全文草稿提交审稿，并确认未解决缺口单独列出。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage paper_full
```

```bash
python scripts/check_gates.py
```

## 13. 人工确认问题

```text
是否批准将这版全文草稿提交审稿，并把未解决缺口单独列出？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 章节矛盾 | 返回相关章节修订，不强行润色。 |
| 证据缺口 | 写入缺口清单，等待补证或删除论断。 |
| 图表引用不一致 | 返回 figures 或合同修正。 |
| 数值不一致 | 返回 results_freeze 或相关章节修正。 |
| 人工未确认 | 停在 `draft_review_gate`。 |

## 15. 完成条件

```text
- 全文草稿可审阅。
- 未解决问题已单独列出。
- 全文强论断可追踪到合同。
- 进入 auto_review 前已满足闸门状态。
- 全文和图表说明已检查为中文。
- 未触发本阶段禁止动作。
```



## Stage 11: auto_review

Sandbox source: `prompts/training_sandbox/stages/11_auto_review.md`
Formal source: `prompts/stages/11_auto_review.md`

# Training Sandbox Prompt Backup: auto_review

Formal source prompt: `prompts/stages/11_auto_review.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`auto_review` - 多审稿器自动审稿

> 中文注释：使用阶段为 `auto_review`；使用场景是在全文草稿形成后，生成审稿意见、评分表和可追踪修订任务。

## 1. 阶段身份

```yaml
stage_id: auto_review
stage_name: 多审稿器自动审稿
stage_order: 11
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P3
```

## 2. 目标

生成结构化审稿意见、评分表和修订任务，但不得直接编辑正式交付物。算力集中在多视角批判、合同校验、图表质量、结果可信度、论文说服力、评分风险和可执行修订任务上。

## 3. 必需输入

```text
- 全文草稿
- 14_contracts/claim_evidence_map.csv
- 14_contracts/result_contract.csv
- 14_contracts/figure_contract.csv
```

## 4. 可选输入

```text
- 11_review/历史审稿意见
- 13_prior_db/对标风险卡片（如已允许）
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 02_latex_template/
- 09_paper/
- 11_review/
- 13_prior_db/
- 14_contracts/
```

## 6. 允许写入路径

```text
- 11_review/
- 14_contracts/revision_tasks.csv
- 10_ai_logs/
```

## 7. 禁止动作

```text
- 审稿器不得直接修改论文、代码、结果或图表。
- 不得关闭任务而不提供证据。
- 不得复制先验论文文本。
- 不得把建议伪装成已修复。
- 不得用主观偏好替代合同失败项。
- 不得忽略 fail/major 风险。
```

## 8. 必需输出

```text
- 11_review/*_reviewer_comments.md
- 11_review/review_scorecard.csv
- 14_contracts/revision_tasks.csv
- 多视角问题清单：题目、模型、数据、代码、结果、图表、写作、评委视角
- 阶段总结
```

## 9. 合同更新

```text
可更新：revision_tasks.csv
只读：其他合同
```

## 10. 允许技能

```text
- nature-response（如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 auto_review 阶段。

输入核验：
1. 检查全文草稿和核心合同文件。
2. 若允许读取 13_prior_db/，可参考先验风险卡片和 copy-risk 报告；不得复制历史论文文本。
3. 确认审稿阶段只写评论、评分和修订任务。

阶段目标：
从问题、模型、代码、图表、论文和评委视角审阅草稿。只输出评论、评分和修订任务，不直接修改交付物。

深度分析：
1. 题目视角：是否覆盖所有官方问题、交付物和约束。
2. 数据视角：数据来源、字段解释、缺失异常、可复现性是否支撑模型。
3. 模型视角：假设、变量、公式、验证、备选方案和局限是否充分。
4. 结果视角：冻结结果是否可追踪，数值是否一致，是否有敏感性或误差说明。
5. 图表视角：图表是否高级、非默认配色、中文标注、绑定合同、质量分不低于 4.2，图表密度是否支撑论证。
6. 写作视角：论断是否绑定证据，章节是否连贯，结论是否过强。
7. 评分视角：将问题分为 fail、major、minor、suggestion，并给出可执行 acceptance_check。

证据绑定：
每条修订任务必须指向 source_comment_id、target_artifact、target_location、linked_contract_ids 或明确说明无法定位原因。

风险清单：
记录合同失败、证据缺口、图表质量、结果可信度、复制风险、人工豁免需求和低分风险。

自检清单：
1. 没有修改正式交付物。
2. 所有 fail/major 问题进入 revision_tasks。
3. 每个任务有 required_action 和 acceptance_check。
4. 没有复制先验文本。
5. 校验命令已运行或记录 not_run。

人工确认输出：
请人类决定哪些审稿问题是必修、可选或人工豁免后再开始修订。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage auto_review
```

## 13. 人工确认问题

```text
哪些审稿问题是必修、可选或人工豁免后再开始修订？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 草稿缺失 | 返回 paper_full。 |
| 合同缺失 | 返回相应合同生产阶段。 |
| 审稿意见不可执行 | 改写为具体修订任务。 |
| 分数低于阈值 | 标记 fail/major，进入 revision。 |
| 任务无法定位目标 | 保留评论并要求人工定位，不直接修改。 |

## 15. 完成条件

```text
- 审稿意见和评分表已生成。
- 必需修订已进入 revision_tasks。
- fail/major 风险没有被静默忽略。
- 没有直接修改正式产物。
- 未触发本阶段禁止动作。
```



## Stage 12: revision

Sandbox source: `prompts/training_sandbox/stages/12_revision.md`
Formal source: `prompts/stages/12_revision.md`

# Training Sandbox Prompt Backup: revision

Formal source prompt: `prompts/stages/12_revision.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`revision` - 修订执行与关闭

> 中文注释：使用阶段为 `revision`；使用场景是在审稿任务形成后，逐项执行修订、记录证据并关闭或申请人工豁免。

## 1. 阶段身份

```yaml
stage_id: revision
stage_name: 修订执行与关闭
stage_order: 12
gate_type: hard
execution_mode: deep_sequential
roadmap_item: P3
```

## 2. 目标

执行已批准修订任务，并用证据验证关闭；修复必须保持在任务范围内。算力集中在任务分解、最小必要修改、合同影响分析、重新校验和关闭证据上。

## 3. 必需输入

```text
- 14_contracts/revision_tasks.csv
- 11_review/review_scorecard.csv
- 被修订目标文件
```

## 4. 可选输入

```text
- 15_iteration_memory/task_closure_log.md
- 人工豁免说明
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 02_latex_template/
- 05_model/
- 06_code/
- 07_results/
- 08_figures/
- 09_paper/
- 11_review/
- 14_contracts/
- 15_iteration_memory/
```

## 6. 允许写入路径

```text
- 与修订任务明确对应的目标文件
- 11_review/
- 14_contracts/revision_tasks.csv
- 15_iteration_memory/
- 10_ai_logs/
```

## 7. 禁止动作

```text
- 不得修改任务范围外的事实。
- 不得关闭未验证任务。
- 不得用润色掩盖模型或结果问题。
- 不得绕过人工关闭闸门。
- 不得改变冻结数字、公式、标签、引用或结果含义，除非回到上游并重新冻结。
- 不得把未批准的新模型、新图表或新结果塞入修订。
```

## 8. 必需输出

```text
- 已更新的目标文件（如任务要求）
- revision_tasks.csv 状态更新
- task_closure_log.md
- 重新校验证据
- 受影响合同说明
- 阶段总结和人工闸门说明
```

## 9. 合同更新

```text
可更新：revision_tasks.csv；必要时更新相关合同并说明原因
```

## 10. 允许技能

```text
- nature-response（如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 revision 阶段。

输入核验：
1. 读取 revision_tasks.csv 和 review_scorecard.csv。
2. 只处理已批准、未关闭且范围明确的任务。
3. 确认目标文件在任务允许范围内。

阶段目标：
逐项处理已批准修订任务，记录修改、证据、重跑命令和关闭依据。任务外内容保持不动。

深度分析：
1. 按 severity、scope、target_artifact、acceptance_check 排序处理任务。
2. 对每项任务先判断修订类型：事实修正、合同补齐、图表重做、结构调整、语言修正或人工豁免。
3. 修改前评估是否影响冻结结果、公式、引用、图表标签或模型路线；若影响，停止并返回上游阶段。
4. 对可修任务执行最小必要修改，并记录修改位置和理由。
5. 对每个关闭任务写入 closure_note：完成动作、验收证据、重跑命令、剩余风险。
6. 对无法关闭任务保持 open/blocked，不得伪造验收。

证据绑定：
任务关闭必须绑定 acceptance_check、校验命令结果、合同 ID 或人工豁免说明。

风险清单：
记录修订范围不清、影响冻结事实、验证失败、人工豁免、合同冲突和下游连锁影响。

自检清单：
1. 只改任务范围内目标。
2. 未关闭未验证任务。
3. 未用润色掩盖事实问题。
4. fail/major 任务关闭或明确 blocked/waived。
5. 校验命令已运行或记录 not_run。

人工确认输出：
请人类批准关闭或豁免所有剩余必需修订任务。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage revision
```

```bash
python scripts/check_gates.py
```

## 13. 人工确认问题

```text
是否批准关闭或豁免所有剩余必需修订任务？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 修订影响冻结事实 | 停止并请求人工决定是否回到上游阶段。 |
| 修订无法验证 | 保持任务未关闭。 |
| 任务范围不清 | 请求人工澄清，不擅自扩大范围。 |
| 需要新增模型或结果 | 返回 model_route/codegen/results_freeze，不在 revision 偷改。 |
| 人工未确认 | 停在 `revision_closure_gate`。 |

## 15. 完成条件

```text
- fail/major 任务已关闭或人工豁免。
- 每个关闭任务都有证据。
- 与合同相关的修改已同步或明确返回上游。
- 下游 polish 可以只做事实保持润色。
- 未触发本阶段禁止动作。
```



## Stage 13: polish

Sandbox source: `prompts/training_sandbox/stages/13_polish.md`
Formal source: `prompts/stages/13_polish.md`

# Training Sandbox Prompt Backup: polish

Formal source prompt: `prompts/stages/13_polish.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`polish` - 事实保持润色

> 中文注释：使用阶段为 `polish`；使用场景是在修订关闭后，仅改进语言表达并保护数字、单位、公式、标签、引用、模型名和结果含义。

## 1. 阶段身份

```yaml
stage_id: polish
stage_name: 事实保持润色
stage_order: 13
gate_type: soft
execution_mode: deep_sequential
roadmap_item: P5
```

## 2. 目标

在保留所有受保护事实原子和结果含义的前提下改进表达。算力集中在句式清晰、段落衔接、中文学术表达、冗余压缩和逐项差异核验上。

## 3. 必需输入

```text
- 已确认草稿章节
- 14_contracts/artifact_freeze_registry.csv
- 14_contracts/polish_diff_check.csv
```

## 4. 可选输入

```text
- 10_polish/polish_rules.md
- 人工语言风格偏好
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 02_latex_template/
- 09_paper/
- 10_polish/
- 14_contracts/
```

## 6. 允许写入路径

```text
- 02_latex_template/sections/
- 09_paper/
- 10_polish/
- 14_contracts/polish_diff_check.csv
- 10_ai_logs/
- 11_review/
```

## 7. 禁止动作

```text
- 不得改变数字、公式、标签、引用、文献、模型名或结果含义。
- 不得强化弱结论。
- 不得删除图表或公式引用。
- 不得把润色当作事实修订。
- 不得把中文论文润色成英文，或引入英文段落；必要的英文缩写、变量名、模型名和 LaTeX 命令除外。
- 不得改动单位、随机种子、指标名称、图表编号、表格编号或 citation key。
- 不得让 protected_atom_delta_count 大于 0。
```

## 8. 必需输出

```text
- 润色后的章节
- polish_diff_check.csv
- 受保护事实原子检查说明
- 润色差异说明
- 阶段总结
- 润色后的正文、图注、表注和面向评审说明必须保持中文。
```

## 9. 合同更新

```text
可更新：polish_diff_check.csv
只读：其他合同和冻结登记
```

## 10. 允许技能

```text
- nature-polishing（如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 polish 阶段。

输入核验：
1. 检查 artifact_freeze_registry.csv 和 polish_diff_check.csv。
2. 确认 revision 阶段已关闭 fail/major 问题或有人类豁免。
3. 确认只做语言润色，不新增事实。

阶段目标：
只改进语言流畅度、逻辑衔接和中文表达，不改变任何受保护事实。

深度分析：
1. 提取受保护事实原子：数字、单位、公式、标签、引用、citation key、文献、模型名、结果含义、图表编号、表格编号。
2. 逐段润色：压缩冗余、增强中文学术表达、消除歧义、改善段落衔接。
3. 对每个润色片段执行前后比对：changed_numbers、changed_units、changed_formulas、changed_labels、changed_refs、changed_citations、changed_model_names、changed_result_meanings。
4. 若任何保护原子变化，回滚该片段或转为 revision 任务，不在 polish 阶段强行处理。
5. 弱证据句只能更谨慎，不得润色成强结论。

证据绑定：
polish_diff_check.csv 必须记录 check_id、artifact_id、original_path、polished_path、protected_atom_delta_count、decision 和 review_note；默认 protected_atom_delta_count=0。

风险清单：
记录事实原子变化、LaTeX 破坏、中文表达歧义、弱结论强化、引用丢失和差异检查不可用风险。

自检清单：
1. protected_atom_delta_count 为 0。
2. changed_numbers/changed_formulas/changed_labels/changed_refs 均为否或空。
3. 没有新增事实。
4. 润色后仍为中文。
5. LaTeX 结构未破坏。
6. 校验命令已运行或记录 not_run。

人工确认输出：
请人类确认润色后的章节是否在提升可读性的同时保留了全部事实。
```

## 12. 校验命令

```bash
python scripts/validate_contracts.py --stage polish
```

## 13. 人工确认问题

```text
润色后的章节是否在提升可读性的同时保留了全部数字、单位、公式、标签、引用、模型名和结果含义？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 受保护事实变化 | 回滚该润色片段，记录 fail。 |
| LaTeX 被破坏 | 修复语法，不改变内容事实。 |
| 润色需要新增解释 | 转为 revision 任务，不在本阶段新增事实。 |
| 弱结论被强化 | 改回谨慎表达，并记录风险。 |
| 差异检查不可用 | 标记未运行，不声称通过。 |

## 15. 完成条件

```text
- polish_diff_check 没有受保护事实变化。
- protected_atom_delta_count 默认且实际为 0。
- LaTeX 结构保持可编译。
- 润色只改善表达。
- 润色后仍为中文论文文本。
- 未触发本阶段禁止动作。
```



## Stage 14: compile

Sandbox source: `prompts/training_sandbox/stages/14_compile.md`
Formal source: `prompts/stages/14_compile.md`

# Training Sandbox Prompt Backup: compile

Formal source prompt: `prompts/stages/14_compile.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`compile` - 编译与提交检查

> 中文注释：使用阶段为 `compile`；使用场景是在润色通过后，编译论文包并运行最终结构门禁。

## 1. 阶段身份

```yaml
stage_id: compile
stage_name: 编译与提交检查
stage_order: 14
gate_type: hard
execution_mode: deep_sequential
roadmap_item: P0
```

## 2. 目标

编译论文包，并在最终导出前运行结构性门禁。算力集中在编译日志、合同一致性、图表文件、引用标签、未关闭修订、提交格式和最终人工确认风险上。

## 3. 必需输入

```text
- 02_latex_template/main.tex
- 02_latex_template/sections/
- 14_contracts/polish_diff_check.csv
- 14_contracts/revision_tasks.csv
```

## 4. 可选输入

```text
- 12_submission/submission_checklist.md
- 人工提交格式说明
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 02_latex_template/
- 08_figures/
- 09_paper/
- 11_review/
- 12_submission/
- 14_contracts/
```

## 6. 允许写入路径

```text
- 12_submission/
- 11_review/
- 10_ai_logs/
```

## 7. 禁止动作

```text
- 不得改写论文事实来修复编译。
- 不得删除引用或图表来掩盖合同问题。
- 不得跳过最终提交闸门。
- 不得创建未经人工确认的最终交付。
- 不得为通过编译改变数字、公式、标签、引用、模型名或结果含义。
```

## 8. 必需输出

```text
- 编译日志
- 最终提交检查清单
- 门禁报告
- 图表、引用、标签和合同一致性说明
- 阶段总结和人工闸门说明
```

## 9. 合同更新

```text
可更新：无
只读并校验所有必需合同
```

## 10. 允许技能

```text
- 无
```

## 11. 代理提示词模板

```text
你正在执行 compile 阶段。

输入核验：
1. 检查 main.tex、sections、polish_diff_check.csv、revision_tasks.csv。
2. 检查所有正文引用的图表文件、latex_label、公式标签和 citation key。
3. 确认 polish 阶段没有保护原子变化，revision 没有未关闭 fail/major 任务。

阶段目标：
编译论文包并运行最终结构检查。如发现事实、合同或引用问题，报告并返回上游，不通过删除内容掩盖问题。

深度分析：
1. 运行 LaTeX 编译并保存日志，区分语法/路径问题和事实/合同问题。
2. 检查重复 label、缺失 ref、未登记图表引用、图文件缺失和 TODO/占位文本。
3. 运行合同校验和 gate 检查，汇总 fail/warn。
4. 检查最终提交候选是否仍为中文，图题、表题、图注、表注和可见图中文字是否为中文。
5. 对每个失败项给出返回阶段：figures、paper_draft、revision、polish 或 results_freeze。

证据绑定：
编译通过只说明结构和文件可用，不代表人工最终确认；最终包必须等待 final_submission_gate。

风险清单：
记录编译失败、合同失败、未关闭修订、缺失图表、引用错误、中文字体、提交格式和人工未确认风险。

自检清单：
1. 没有改写事实。
2. 没有删除引用或图表掩盖问题。
3. 编译日志和门禁报告已保存。
4. fail 项已指向上游恢复路径。
5. 校验命令已运行或记录 not_run。

人工确认输出：
请人类批准该编译论文包作为最终提交候选。
```

## 12. 校验命令

```bash
python scripts/compile_latex.py
```

```bash
python scripts/check_gates.py
```

```bash
python scripts/validate_contracts.py --stage final_export
```

## 13. 人工确认问题

```text
是否批准该编译论文包作为最终提交候选？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| LaTeX 编译失败 | 只修复格式或路径问题；事实问题返回上游。 |
| 合同校验失败 | 回到相应合同生产阶段。 |
| 未关闭修订任务 | 返回 revision。 |
| 图表或引用缺失 | 返回 figures、paper_draft 或合同修正。 |
| 人工未确认 | 停在 `final_submission_gate`。 |

## 15. 完成条件

```text
- 编译和门禁结果已记录。
- 终稿候选没有 fail 级结构问题，或 fail 已明确返回上游。
- 未通过删除事实、引用或图表掩盖问题。
- 等待或完成最终人工确认。
- 未触发本阶段禁止动作。
```



## Stage 15: final_export

Sandbox source: `prompts/training_sandbox/stages/15_final_export.md`
Formal source: `prompts/stages/15_final_export.md`

# Training Sandbox Prompt Backup: final_export

Formal source prompt: `prompts/stages/15_final_export.md`

This is a sandbox-specific backup/fine-tuned prompt derived from the formal prompt system. It must not modify the formal prompt files.

Sandbox overlay rules:
- Work only inside the sandbox workspace and reply through JSON file actions.
- Treat formal human gates as simulated sandbox gates; write evidence to `11_review/simulated_human_gate_log.csv` with `formal_effect=none`.
- Preserve formal contract hierarchy: contracts before paper claims, figures registered before citation, results frozen before analysis.
- Training enhancement points are candidate workflow improvements only. Write them to `reports/training_enhancement_points.csv` and `.md`; do not apply them to formal prompts here.
- Any later promotion into formal workflow must be suggestion-only and pass validation, copy-risk, no open fail/major queue, contract checks, and human gate.

## Formal Prompt Body

# 阶段提示词：`final_export` - 最终导出与可选 PPT

> 中文注释：使用阶段为 `final_export`；使用场景是在最终人工闸门确认后，打包提交材料并可选生成展示材料。

## 1. 阶段身份

```yaml
stage_id: final_export
stage_name: 最终导出与可选 PPT
stage_order: 15
gate_type: final
execution_mode: deep_sequential
roadmap_item: P7
```

## 2. 目标

打包最终批准的交付物，并可选地只从已批准论文生成展示材料。算力集中在最终来源核验、包完整性、展示材料不越界、中文可见文字和最终审计记录上。

## 3. 必需输入

```text
- 已人工确认的最终论文包
- 11_review/final_submission_checklist.md
- 14_contracts/ 全部最终校验通过
```

## 4. 可选输入

```text
- 人工确认的展示材料需求
- 12_export/pptx/
```

## 5. 允许读取路径

```text
- AGENTS.md
- workflow_state.yaml
- config/
- 02_latex_template/
- 09_paper/
- 11_review/
- 12_submission/
- 12_export/
- 14_contracts/
```

## 6. 允许写入路径

```text
- 12_submission/
- 12_export/
- 10_ai_logs/
- 11_review/
```

## 7. 禁止动作

```text
- 未经最终人工确认不得导出。
- 不得在导出阶段新增论文事实。
- PPT 不得包含论文外结果。
- 不得跳过最终门禁失败项。
- 不得导出英文正文、英文展示说明或英文图中文字作为最终面向评审材料；必要英文缩写和变量名除外。
- 不得修改已批准论文来适配展示材料。
```

## 8. 必需输出

```text
- 最终提交包说明
- 可选 PPT 导出目录
- 最终阶段总结
- 最终来源清单和人工确认记录
- 最终提交包说明、PPT 文本、图片中文字、图表标题、图例、注释和节点文字必须为中文。
```

## 9. 合同更新

```text
可更新：无
只读：全部最终合同
```

## 10. 允许技能

```text
- nature-paper2ppt（仅终稿后且如技能路由允许）
```

## 11. 代理提示词模板

```text
你正在执行 final_export 阶段。

输入核验：
1. 确认最终人工闸门已记录。
2. 检查 final_submission_checklist、最终合同和提交包来源。
3. 若生成展示材料，确认人工明确需要 PPT 或展示材料。

阶段目标：
只打包已批准的最终产物。如果生成展示材料，必须只来源于已批准论文，且不得新增模型结果或结论。

深度分析：
1. 建立最终来源清单：论文 PDF、LaTeX 源、图表文件、提交说明、AI 使用说明、可选 PPT。
2. 检查所有文件是否来自 compile 阶段批准产物或终稿后允许派生产物。
3. 生成 PPT 时只压缩和重组论文已有内容：问题、模型、结果、图表、结论和局限，不新增结果数字或图表论断。
4. 检查所有最终可见文字为中文；必要英文缩写、变量名、文件名和指标名可保留。
5. 记录导出命令、输出路径、缺失文件和人工确认状态。

证据绑定：
最终导出说明必须绑定最终人工确认、门禁报告和合同校验状态；展示材料必须能追溯到最终论文章节或图表。

风险清单：
记录最终闸门未确认、合同失败、PPT 越界、文件缺失、中文文字不合规、提交格式不明和导出失败风险。

自检清单：
1. 最终人工确认已存在。
2. 没有新增论文事实。
3. PPT 不含论文外结果。
4. 最终导出物可见文字为中文。
5. 校验命令已运行或记录 not_run。

人工确认输出：
请人类确认是否只基于已批准论文生成终稿后的展示材料。
```

## 12. 校验命令

```bash
python scripts/check_gates.py
```

```bash
python scripts/validate_contracts.py --stage final_export
```

## 13. 人工确认问题

```text
是否只基于已批准论文生成终稿后的展示材料？
```

## 14. 失败恢复

| 失败模式 | 安全恢复 |
|---|---|
| 最终闸门未确认 | 停止导出，等待人工确认。 |
| 合同校验失败 | 返回相应上游阶段。 |
| PPT 需求不清 | 只打包论文，不生成展示材料。 |
| 展示材料引入新事实 | 删除新事实，改为引用已批准论文内容。 |
| 导出文件缺失 | 重新运行编译或打包步骤，不改事实。 |

## 15. 完成条件

```text
- 最终提交包来源明确。
- 可选展示材料不超出已批准论文。
- 所有最终检查和人工确认已记录。
- 最终导出物及其中图片/图表文字已检查为中文。
- 未触发本阶段禁止动作。
```


