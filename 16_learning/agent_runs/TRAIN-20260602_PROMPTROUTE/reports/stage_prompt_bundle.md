# Formal Stage Prompt Bundle For Full-Agent Training

This file is assembled from the same prompt files used by normal competition mode. The training wrapper may define sandbox execution, but stage behavior comes from the sections below.

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

Source: `prompts/stages/latex_template.md`

[missing stage prompt]

## Stage 1: intake

Source: `prompts/stages/intake.md`

[missing stage prompt]

## Stage 2: eda

Source: `prompts/stages/eda.md`

[missing stage prompt]

## Stage 3: task_analysis

Source: `prompts/stages/task_analysis.md`

[missing stage prompt]

## Stage 4: prior_retrieval

Source: `prompts/stages/prior_retrieval.md`

[missing stage prompt]

## Stage 5: model_route

Source: `prompts/stages/model_route.md`

[missing stage prompt]

## Stage 6: codegen

Source: `prompts/stages/codegen.md`

[missing stage prompt]

## Stage 7: results_freeze

Source: `prompts/stages/results_freeze.md`

[missing stage prompt]

## Stage 8: figures

Source: `prompts/stages/figures.md`

[missing stage prompt]

## Stage 9: paper_draft

Source: `prompts/stages/paper_draft.md`

[missing stage prompt]

## Stage 10: paper_full

Source: `prompts/stages/paper_full.md`

[missing stage prompt]

## Stage 11: auto_review

Source: `prompts/stages/auto_review.md`

[missing stage prompt]

## Stage 12: revision

Source: `prompts/stages/revision.md`

[missing stage prompt]

## Stage 13: polish

Source: `prompts/stages/polish.md`

[missing stage prompt]

## Stage 14: compile

Source: `prompts/stages/compile.md`

[missing stage prompt]

## Stage 15: final_export

Source: `prompts/stages/final_export.md`

[missing stage prompt]
