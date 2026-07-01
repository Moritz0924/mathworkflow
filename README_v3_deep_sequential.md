# 数学建模国赛全流程工作流 v3.0 使用说明

## 1. 系统定位

本系统用于辅助数学建模国赛论文的全流程生产，目标是把赛题、附件数据、建模代码、图表、论文正文和终稿检查整合成一套可复核、可追踪、可分段推进的工作流。

系统不是“一键生成获奖论文”的黑箱，而是一个质量优先的建模生产驾驶舱：

```text
题目与数据输入
→ 数据分析
→ 分问拆解
→ 模型路由
→ 分问代码生成
→ 模型求解
→ 图表生成
→ LaTeX 论文初稿
→ 分段式完整正文
→ 学术润色
→ 人工审核
→ 终稿导出
```

核心原则：

```text
只基于真实题目、真实数据、真实代码输出写论文。
不虚构结果。
不虚构图表。
不虚构参考文献。
不为了速度牺牲建模逻辑与论文一致性。
```

---

## 2. 全局执行策略：单环节深度模式

v3.0 默认采用 **单环节深度模式**。

这意味着系统在任何时候只集中处理当前一个流程节点，不并行推进多个阶段，不为了快速完成全流程而降低每个节点的质量。

### 2.1 执行原则

```text
一轮只处理一个节点。
一个节点只处理一个核心任务。
当前节点未通过自动检查，不进入下一节点。
当前节点未通过人工确认，不进入下一节点。
后续节点只能读取已确认产物。
发现不确定性时，优先标记风险，不强行继续。
```

### 2.2 禁止行为

```text
禁止一边分析数据，一边生成论文正文。
禁止模型未确认就生成建模代码。
禁止代码未运行就写结果分析。
禁止图表未生成或未登记就引用图表。
禁止一次性粗糙生成完整论文。
禁止一次性粗糙润色全文。
禁止使用并行模式用质量换速度。
```

### 2.3 推荐启动方式

默认启动当前节点：

```bash
python scripts/run_current_stage.py
```

或：

```bash
python scripts/start_full_pipeline.py --mode deep
```

不推荐默认使用：

```bash
python scripts/start_full_pipeline.py --stage all
```

`--stage all` 仅保留为开发调试命令，不作为正式比赛流程入口。

---

## 3. 快速开始

### 3.1 放入题目和数据

把赛题文件放入：

```text
00_problem/inbox/
```

把数据附件放入：

```text
03_data/raw/
```

推荐输入：

```text
题目 PDF
题目 txt 或 md 文字版
附件 csv / xlsx / json / geojson
```

注意：

```text
扫描版 PDF 或图片题目需要 OCR，v3.0 基础版不保证可靠识别。
```

### 3.2 初始化项目

```bash
python scripts/start_full_pipeline.py --mode deep
```

系统会读取 `workflow_state.yaml`，自动判断当前应该执行哪个节点。

---

## 4. 流程状态文件

系统通过 `workflow_state.yaml` 锁定当前阶段，防止跳步。

示例：

```yaml
execution_mode: deep_sequential
allow_parallel: false
speed_priority: low
quality_priority: highest

current_stage: intake

completed_stages: []

locked_stages:
  - eda
  - task_analysis
  - model_route
  - codegen
  - figures
  - paper_draft
  - paper_full
  - polish
  - compile

human_gate_required: true
last_confirmed_gate: null
```

字段含义：

```text
execution_mode：执行模式，默认 deep_sequential。
allow_parallel：是否允许并行，默认 false。
current_stage：当前允许执行的节点。
completed_stages：已完成节点。
locked_stages：暂时锁定的后续节点。
human_gate_required：是否需要人工确认。
last_confirmed_gate：最后通过的人工闸门。
```

---

## 5. 全流程节点

## Node 0：项目初始化与 LaTeX 模板生成

### 目标

在流程最开始生成可编译的 LaTeX 论文骨架。后续正文、图表引用、公式编号全部写入 LaTeX，不再先写 Markdown 再迁移。

### 输入

```text
比赛类型
题号
队伍信息
是否启用附录
是否启用 AI 使用说明
```

### 产出

```text
02_latex_template/main.tex
02_latex_template/preamble.tex
02_latex_template/cn_math_style.sty
02_latex_template/references.bib
02_latex_template/sections/*.tex
```

### 人工检查

```text
章节结构是否符合国赛论文习惯
题号和队伍信息是否正确
是否存在不允许提交的信息
LaTeX 是否能编译
```

---

## Node 1：赛题与数据投喂解析

### 目标

自动读取题目和附件，生成基础说明。

### 输入目录

```text
00_problem/inbox/
03_data/raw/
```

### 产出

```text
00_problem/problem_statement.md
00_problem/problem_statement.tex
00_problem/attachments_overview.md
01_task_analysis/auto_start_summary.md
```

### 人工检查

```text
题目是否读取完整
附件是否全部识别
是否遗漏题目中的关键限制
扫描件是否需要人工补录
```

---

## Node 2：数据分析与数据质量诊断

### 目标

对数据进行体检，生成数据字典、质量报告和初步可视化。

### 产出代码

```text
04_eda_code/generate_data_dictionary.py
04_eda_code/run_data_quality_check.py
04_eda_code/run_eda_pipeline.py
04_eda_code/eda_visuals.py
```

### 产出文件

```text
03_data/data_dictionary.csv
03_data/data_quality_report.md
03_data/data_quality_report.tex
03_data/eda_summary.tex
08_figures/output/eda_*.png
```

### 检查内容

```text
字段类型
缺失值
异常值
重复值
时间字段
类别字段
连续变量分布
变量相关性
单位与量纲风险
```

### 人工检查

```text
字段含义是否理解正确
单位是否正确
缺失值处理是否合理
异常值是真异常还是重要样本
数据口径是否与题意一致
```

---

## Node 3：分问拆解与任务画像

### 目标

把赛题拆成多个可建模子任务，确定每一问的输入、输出和任务类型。

### 产出

```text
01_task_analysis/task_decomposition.md
01_task_analysis/task_decomposition.tex
01_task_analysis/problem_model_profile.csv
01_task_analysis/question_dependency_graph.md
```

### `problem_model_profile.csv` 推荐字段

```csv
question_id,problem_type,model_family,data_feature,output_goal,input_data,core_variables,evaluation_metric,risk_level,human_confirmed
Q1,评价决策型,熵权-TOPSIS,多指标截面数据,综合评价排序,附件1,指标A/指标B,综合得分,中,否
Q2,预测分析型,回归/时间序列,历史观测数据,预测未来趋势,附件2,时间/目标变量,RMSE/MAE,中,否
Q3,优化决策型,规划模型,约束条件明确,输出最优方案,附件3,决策变量/约束变量,目标函数值,高,否
```

### 人工检查

```text
每一问是否拆得合理
问题之间是否有依赖关系
是否遗漏隐含约束
题型判断是否错误
模型族是否过度复杂
```

---

## Node 4：模型路由与方案选择

### 目标

根据题型、数据特征和输出目标，推荐主模型、备选模型和不推荐模型。

### 产出

```text
05_model/model_route.md
05_model/model_route.tex
05_model/model_candidate_score.csv
05_model/model_selection_reasoning.md
09_paper/active_weight_config.csv
08_figures/active_figure_plan.csv
08_figures/active_visual_profile.md
```

### 模型评分维度

```text
题意匹配度
数据适配度
可解释性
实现难度
结果稳定性
论文表现力
图表表现力
时间成本
国赛适配度
```

### 人工检查

```text
模型是否过度炫技
模型是否支撑题目输出
模型是否能被论文解释清楚
数据是否足以支撑模型
是否需要更稳的备选模型
```

---

## Node 5：分问建模代码生成

### 目标

根据模型路线，为每一问生成数据处理、建模、评估和结果导出代码。

### 单环节深度要求

一次只处理一个问题：

```bash
python scripts/generate_model_code.py --question Q1 --mode deep
```

不推荐：

```bash
python scripts/generate_model_code.py --question all
```

### 产出目录

```text
06_solution_code/Q1/
06_solution_code/Q2/
06_solution_code/Q3/
```

每问默认包含：

```text
q*_data_prepare.py
q*_model.py
q*_evaluate.py
q*_export_results.py
README_Q*.md
```

### 结果产出

```text
07_results/tables/q*_result_table.csv
07_results/metrics/q*_metrics.json
07_results/logs/q*_run_log.txt
```

### 人工检查

```text
变量是否对应题意
目标函数是否正确
约束是否完整
评价指标是否合理
结果是否可复现
```

---

## Node 6：图表生成与图文配置

### 目标

根据真实结果生成高质量中文图表，并登记到图表注册表。

### 产出

```text
08_figures/active_figure_plan.csv
08_figures/figure_registry.csv
08_figures/figure_quality_check.csv
08_figures/output/*.png
08_figures/output/*.pdf
```

### 图表要求

```text
中文标题
中文坐标轴
中文图例
非默认配色
字号清晰
图表必须服务正文结论
同篇论文禁止图类单一
低价值图转入附录或删除
```

### 高优先级图类

```text
热力图
雷达图
桑基图
Pareto 前沿图
机制路径图
预测区间图
残差诊断组图
特征重要性图
敏感性分析热力图
空间分布图
网络结构图
方案对比矩阵图
```

---

## Node 7：LaTeX 论文初稿生成

### 目标

根据已确认的题目、数据、模型和结果，生成结构完整的 LaTeX 初稿。

### 产出

```text
09_paper/paper_draft_v1.tex
02_latex_template/sections/*.tex
```

### 初稿原则

```text
先保证事实和结构。
不虚构数据结果。
不虚构显著性。
不虚构参考文献。
所有图表必须来自 figure_registry.csv。
所有结果必须来自 07_results/。
模型公式必须能对应代码逻辑。
```

---

## Node 8：完整论文分段式生成

### 目标

在初稿基础上，按照国赛论文框架分段生成完整正文。

### 推荐生成顺序

```text
1. 问题重述与问题分析
2. 数据预处理与数据分析
3. 模型假设与符号说明
4. 问题一模型建立、求解、结果分析
5. 问题二模型建立、求解、结果分析
6. 问题三模型建立、求解、结果分析
7. 灵敏度分析与误差分析
8. 模型评价
9. 摘要
10. 结论
```

摘要必须最后生成。

### 人工检查

```text
是否符合题意
是否引用真实结果
是否图文一致
公式是否和代码一致
章节之间是否连贯
摘要是否与正文一致
```

---

## Node 9：正文润色与终稿审核

### 目标

对 AI 初步生成的 LaTeX 正文进行自然化学术润色，提升中文学术表达的自然度和可读性，同时不改变事实、数据、模型和结论强度。

注意：系统可以减少模板化表达，但不承诺规避任何检测，也不以规避检测作为目标。

### 产出

```text
10_polish/polished_sections/*.tex
10_polish/polish_log.csv
09_paper/paper_polished_v1.tex
```

### 润色保护规则

```text
不得破坏 LaTeX 命令。
不得改动 \label{}。
不得改动 \ref{}。
不得改动 \cite{}。
不得改动公式环境。
不得改动公式内部变量。
不得改动表格和图表编号。
不得删除图表引用。
不得强化弱结论。
```

### 人工检查

```text
润色是否改变结论强度
是否改错变量名
是否破坏 LaTeX 编译
是否误删图表引用
是否新造解释
```

---

## 6. 人工审核闸门

系统设置 5 个强制人工闸门。

### Gate 1：题目与数据审核

位置：Node 2 后。

```text
题目是否读取完整
数据文件是否全部识别
字段含义是否正确
缺失值处理是否合理
单位是否误判
```

### Gate 2：题型与模型审核

位置：Node 4 后。

```text
每一问题型是否正确
模型族是否合理
是否过度复杂
是否模型太简单
是否有备选方案
```

### Gate 3：代码与结果审核

位置：Node 5 后。

```text
代码是否能运行
结果是否可复现
指标是否合理
约束是否完整
图表是否真实来自结果
```

### Gate 4：论文初稿审核

位置：Node 7 / Node 8 后。

```text
论文结构是否完整
段落是否连贯
公式是否对应代码
图表是否支撑结论
摘要是否与正文一致
```

### Gate 5：润色与终稿审核

位置：Node 9 后。

```text
润色是否改动事实
语言是否自然
LaTeX 是否能编译
参考文献是否真实
图表编号是否一致
提交格式是否满足要求
```

---

## 7. 核心数据契约

为防止论文内容和代码结果脱节，系统必须建立数据契约。

### 7.1 结果契约

论文只能引用以下目录中的真实结果：

```text
07_results/result_summary.tex
07_results/tables/*.csv
07_results/metrics/*.json
```

### 7.2 图表契约

所有图表必须登记到：

```text
08_figures/figure_registry.csv
```

字段示例：

```csv
figure_id,path,title,question_id,section,data_source,main_message,used_in_paper,quality_score
F1,08_figures/output/q1_weight_heatmap.png,指标权重热力图,Q1,问题一结果分析,q1_result.csv,展示核心指标权重分布,是,4.6
```

论文中只能引用已登记图表。

### 7.3 公式契约

建议新增：

```text
05_model/formula_registry.csv
```

字段示例：

```csv
formula_id,question_id,latex,meaning,variables,source_code_file
EQ1,Q1,"S_i=\sum_j w_j z_{ij}",综合评价得分,权重w_j/标准化指标z_ij,06_solution_code/Q1/q1_model.py
```

论文公式必须能对应模型代码。

---

## 8. 终稿检查

终稿前运行：

```bash
python scripts/check_gates.py
python scripts/compile_latex.py
```

检查内容：

```text
LaTeX 是否可编译
所有 \ref 是否存在
所有 \label 是否唯一
所有图片路径是否存在
所有 figure_id 是否登记
所有结果是否来自 07_results/
是否存在英文图题
是否存在 TODO
是否存在未确认节点提前产出后续文件
是否存在并行模式痕迹
```

---

## 9. 推荐三人队分工

### 队员 A：数据与代码

```text
负责数据清洗
负责 EDA
负责建模代码
负责结果导出
```

### 队员 B：模型与图表

```text
负责模型路线审核
负责图表规划
负责图表质量检查
负责公式与代码一致性检查
```

### 队员 C：论文与排版

```text
负责 LaTeX 结构
负责正文分段生成
负责润色审核
负责终稿编译和提交检查
```

---

## 10. 最小可用流程

比赛时最稳的执行顺序：

```bash
python scripts/start_full_pipeline.py --mode deep
python scripts/check_gates.py
```

每通过一个人工闸门，再进入下一阶段。

不要急着生成完整论文。先把数据、模型、代码、结果跑稳，再写正文。国赛论文像搭桥，桥墩歪了，桥面再漂亮也只是一条横着的幻觉。
