# v3.0 开发任务清单

## 1. 开发目标

将现有 v2.5 投喂式启动工作流升级为 v3.0 全流程系统。

v3.0 必须支持：

```text
LaTeX 模板初始化
题目与数据投喂解析
数据分析
分问拆解
模型路由
分问建模代码生成
图表生成与登记
LaTeX 初稿生成
完整论文分段式生成
正文润色
人工闸门
终稿检查
单环节深度模式
```

默认执行策略：

```text
deep_sequential
禁止并行推进
质量优先
人工闸门优先
结果契约优先
```

---

## 2. 开发阶段划分

## Phase 0：基础架构与状态控制

目标：建立项目骨架、配置文件和单环节深度执行机制。

### P0-1：目录结构初始化

创建目录：

```text
00_problem/
01_task_analysis/
02_latex_template/
03_data/
04_eda_code/
05_model/
06_solution_code/
07_results/
08_figures/
09_paper/
10_polish/
11_review/
12_export/
config/
scripts/
templates/
```

验收标准：

```text
目录完整
空目录保留 .gitkeep
README 能解释每个目录用途
```

---

### P0-2：新增执行策略配置

创建：

```text
config/execution_policy.yaml
```

内容必须包含：

```yaml
mode: deep_sequential

parallel_execution:
  enabled: false
  allow_multi_stage: false
  allow_multi_question_codegen: false
  allow_full_paper_one_shot: false

quality_policy:
  priority: highest
  require_stage_summary: true
  require_risk_report: true
  require_human_gate: true
  require_source_trace: true

generation_policy:
  paper_generation: section_by_section
  model_codegen: question_by_question
  polish: section_by_section
  figure_generation: result_bound_only

forbidden_actions:
  - generate_full_paper_before_results
  - write_result_without_model_output
  - cite_unregistered_figure
  - skip_human_gate
  - parallel_stage_execution
  - use_fast_mode
```

验收标准：

```text
配置文件可被 Python 读取
默认不允许并行
默认不允许全文一次性生成
```

---

### P0-3：新增流程状态文件

创建：

```text
workflow_state.yaml
```

初始内容：

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

验收标准：

```text
系统可读取 current_stage
后续节点默认 locked
状态更新函数可写回 YAML
```

---

### P0-4：实现当前节点启动器

新增：

```text
scripts/run_current_stage.py
```

功能：

```text
读取 workflow_state.yaml
读取 config/execution_policy.yaml
判断当前允许执行节点
调用对应节点脚本
禁止执行 locked_stages
执行完成后生成 stage_summary
等待人工确认
```

验收标准：

```text
运行 python scripts/run_current_stage.py 可启动 current_stage
locked 节点不可执行
若检测 allow_parallel=true 则报错
```

---

### P0-5：实现全流程入口

新增或升级：

```text
scripts/start_full_pipeline.py
```

支持参数：

```bash
--mode deep
--stage current
--stage intake
--stage eda
--stage task_analysis
--stage model_route
--stage codegen
--stage figures
--stage paper_draft
--stage paper_full
--stage polish
--stage compile
```

限制：

```text
默认 --mode deep
--stage all 仅允许在 --dev-debug 下使用
正式模式禁止 all
```

验收标准：

```text
默认只执行当前节点
--stage all 在正式模式下会被拒绝
日志写入 07_results/logs/
```

---

## Phase 1：LaTeX 模板与投喂式启动

## P1-1：LaTeX 模板生成器

新增：

```text
scripts/generate_latex_template.py
```

生成：

```text
02_latex_template/main.tex
02_latex_template/preamble.tex
02_latex_template/cn_math_style.sty
02_latex_template/references.bib
02_latex_template/sections/00_abstract.tex
02_latex_template/sections/01_background.tex
02_latex_template/sections/02_problem_analysis.tex
02_latex_template/sections/03_assumptions.tex
02_latex_template/sections/04_symbols.tex
02_latex_template/sections/05_data_analysis.tex
02_latex_template/sections/06_model_q1.tex
02_latex_template/sections/07_model_q2.tex
02_latex_template/sections/08_model_q3.tex
02_latex_template/sections/09_sensitivity.tex
02_latex_template/sections/10_model_evaluation.tex
02_latex_template/sections/11_conclusion.tex
02_latex_template/sections/appendix.tex
```

LaTeX 要求：

```text
使用 ctexart
支持 XeLaTeX
支持中文
支持数学公式
支持三线表
支持图片
支持算法
支持参考文献
支持附录
```

验收标准：

```text
空模板可被 XeLaTeX 编译
所有 section 文件可被 main.tex 正确 input
无中文乱码
```

---

## P1-2：投喂式解析器升级

升级：

```text
scripts/start_from_inputs.py
```

输入：

```text
00_problem/inbox/
03_data/raw/
```

输出：

```text
00_problem/problem_statement.md
00_problem/problem_statement.tex
00_problem/attachments_overview.md
01_task_analysis/auto_start_summary.md
```

支持：

```text
txt
md
csv
xlsx
json
普通文本型 PDF
```

边界：

```text
扫描版 PDF 只登记，不做高置信解析
```

验收标准：

```text
能识别题目文件
能识别数据文件
能生成附件说明
能标记无法解析文件
```

---

## Phase 2：数据分析与质量诊断

## P2-1：数据字典生成

新增：

```text
04_eda_code/generate_data_dictionary.py
```

输出：

```text
03_data/data_dictionary.csv
```

字段：

```csv
file_name,column_name,inferred_type,missing_rate,unique_count,sample_values,possible_meaning,risk_note
```

验收标准：

```text
支持 csv/xlsx
能处理中文列名
能统计缺失率和样例值
```

---

## P2-2：数据质量检查

新增：

```text
04_eda_code/run_data_quality_check.py
```

输出：

```text
03_data/data_quality_report.md
03_data/data_quality_report.tex
```

检查：

```text
缺失值
重复值
异常值
时间范围
类别分布
数值范围
单位风险
字段命名风险
```

验收标准：

```text
每个数据文件都有质量摘要
LaTeX 版可直接插入论文
```

---

## P2-3：EDA 可视化

新增：

```text
04_eda_code/eda_visuals.py
```

输出：

```text
08_figures/output/eda_*.png
08_figures/figure_registry.csv
```

图表优先级：

```text
相关性热力图
缺失值矩阵图
箱线图
小提琴图
散点矩阵
时间密度趋势图
类别占比矩阵图
```

图表规范：

```text
中文标题
中文坐标轴
非默认配色
字号清晰
登记到 figure_registry.csv
```

验收标准：

```text
每张图都有 figure_id
每张图有 main_message
质量评分低于阈值时标记为附录或重画
```

---

## Phase 3：分问拆解与模型路由

## P3-1：分问拆解模块

新增：

```text
scripts/decompose_problem.py
```

输出：

```text
01_task_analysis/task_decomposition.md
01_task_analysis/task_decomposition.tex
01_task_analysis/question_dependency_graph.md
```

功能：

```text
识别问题数量
提取每问目标
提取输入数据
提取输出要求
识别隐含约束
识别问题依赖关系
```

验收标准：

```text
每一问都有 input/output/method_hint/risk_note
不确定处明确标记
```

---

## P3-2：任务画像表生成

生成或升级：

```text
01_task_analysis/problem_model_profile.csv
```

字段：

```csv
question_id,problem_type,model_family,data_feature,output_goal,input_data,core_variables,evaluation_metric,risk_level,human_confirmed
```

验收标准：

```text
每一问一行
human_confirmed 默认为 否
人工确认后才能进入模型代码生成
```

---

## P3-3：模型路由模块

升级：

```text
scripts/route_weight_config.py
```

新增或输出：

```text
05_model/model_route.md
05_model/model_route.tex
05_model/model_candidate_score.csv
05_model/model_selection_reasoning.md
09_paper/active_weight_config.csv
08_figures/active_figure_plan.csv
08_figures/active_visual_profile.md
```

候选模型评分维度：

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

验收标准：

```text
每问有主模型、备选模型、不推荐模型
不推荐模型必须说明原因
权重配置随题型和模型族变化
```

---

## Phase 4：建模代码生成与运行

## P4-1：代码模板库

创建：

```text
templates/code/evaluation/
templates/code/prediction/
templates/code/optimization/
templates/code/clustering/
templates/code/simulation/
templates/code/machine_learning/
templates/code/network/
```

每类模板至少包含：

```text
data_prepare.py.tpl
model.py.tpl
evaluate.py.tpl
export_results.py.tpl
README.md.tpl
```

验收标准：

```text
模板可渲染
变量占位符清晰
中文注释不乱码
```

---

## P4-2：分问代码生成器

新增：

```text
scripts/generate_model_code.py
```

命令：

```bash
python scripts/generate_model_code.py --question Q1 --mode deep
```

禁止：

```bash
python scripts/generate_model_code.py --question all
```

除非：

```bash
--dev-debug
```

输出：

```text
06_solution_code/Q*/q*_data_prepare.py
06_solution_code/Q*/q*_model.py
06_solution_code/Q*/q*_evaluate.py
06_solution_code/Q*/q*_export_results.py
06_solution_code/Q*/README_Q*.md
```

验收标准：

```text
一次只生成一个问题的代码
未通过 Gate 2 不允许生成代码
生成代码固定 random_state
结果导出到 07_results/
```

---

## P4-3：结果导出契约

所有模型必须输出：

```text
07_results/tables/q*_result_table.csv
07_results/metrics/q*_metrics.json
07_results/logs/q*_run_log.txt
07_results/result_summary.tex
```

验收标准：

```text
结果文件存在
论文生成器只读取这些结果
未生成结果时禁止写结果分析
```

---

## Phase 5：图表生成与注册

## P5-1：图表注册表

创建：

```text
08_figures/figure_registry.csv
```

字段：

```csv
figure_id,path,title,question_id,section,data_source,main_message,used_in_paper,quality_score
```

验收标准：

```text
所有图表都登记
未登记图表不得被论文引用
图表路径必须存在
```

---

## P5-2：图表质量检查

新增：

```text
scripts/check_figure_quality.py
```

输出：

```text
08_figures/figure_quality_check.csv
```

检查：

```text
中文标题
中文坐标轴
中文图例
非默认配色
字号
图像分辨率
图表类型多样性
是否有 main_message
是否服务正文结论
```

验收标准：

```text
正文图 quality_score >= 4.2
低于阈值的图不得进入正文
```

---

## Phase 6：论文生成

## P6-1：论文分段生成计划

新增：

```text
09_paper/section_generation_plan.csv
```

字段：

```csv
section_id,section_file,depends_on,required_sources,status,human_confirmed
```

验收标准：

```text
每个 section 有依赖源
摘要依赖所有正文
未满足依赖不得生成
```

---

## P6-2：LaTeX 初稿生成器

新增：

```text
scripts/generate_paper_sections.py
```

支持：

```bash
python scripts/generate_paper_sections.py --section 06_model_q1 --mode deep
```

禁止正式模式下：

```bash
python scripts/generate_paper_sections.py --section all
```

输入：

```text
problem_statement.tex
task_decomposition.tex
data_quality_report.tex
eda_summary.tex
model_route.tex
result_summary.tex
figure_registry.csv
formula_registry.csv
active_weight_config.csv
```

输出：

```text
02_latex_template/sections/*.tex
09_paper/paper_draft_v1.tex
```

验收标准：

```text
所有正文为 LaTeX
不破坏命令
不引用未登记图表
不写未生成结果
```

---

## P6-3：完整正文分段生成

规则：

```text
先数据与模型，后摘要与结论。
每段生成后需要人工确认。
上一段未确认，不生成下一段。
```

推荐顺序：

```text
01_background
02_problem_analysis
05_data_analysis
03_assumptions
04_symbols
06_model_q1
07_model_q2
08_model_q3
09_sensitivity
10_model_evaluation
11_conclusion
00_abstract
```

验收标准：

```text
section_generation_plan.csv 中状态正确流转
摘要最后生成
章节风格基本一致
```

---

## Phase 7：润色模块

## P7-1：润色提示词文件

创建：

```text
10_polish/polish_prompt.md
10_polish/polish_rules.md
```

必须包含用户提供的润色规则，并额外加入 LaTeX 保护规则：

```text
不得破坏 \label{}
不得破坏 \ref{}
不得破坏 \cite{}
不得破坏 equation/table/figure 环境
不得改动公式变量
不得改动图表编号
不得强化弱结论
```

验收标准：

```text
提示词完整
LaTeX 保护规则明确
不承诺规避检测
```

---

## P7-2：分段润色器

新增：

```text
scripts/polish_latex_sections.py
```

命令：

```bash
python scripts/polish_latex_sections.py --section 06_model_q1 --mode deep
```

禁止正式模式下：

```bash
python scripts/polish_latex_sections.py --section all --fast
```

输出：

```text
10_polish/polished_sections/*.tex
10_polish/polish_log.csv
09_paper/paper_polished_v1.tex
```

验收标准：

```text
一次只润色一个 section
保留原文备份
记录修改说明
记录风险提示
润色后 LaTeX 可编译
```

---

## Phase 8：质量检查与终稿导出

## P8-1：闸门检查器升级

升级：

```text
scripts/check_gates.py
```

检查：

```text
当前节点是否允许执行
是否跳过人工闸门
是否有未确认节点提前生成后续产物
是否引用未登记图表
是否写入未生成结果
LaTeX 是否可编译
\ref 是否存在
\label 是否唯一
图片路径是否存在
是否存在 TODO
是否存在默认图题
是否存在英文图题
是否存在 --fast 或 --parallel 痕迹
```

输出：

```text
11_review/gate_report.json
11_review/final_submission_checklist.md
```

验收标准：

```text
发现违规直接失败
错误信息能指出回退节点
```

---

## P8-2：LaTeX 编译器

新增：

```text
scripts/compile_latex.py
```

功能：

```text
调用 XeLaTeX
调用 BibTeX 或 biber
再次调用 XeLaTeX
输出 PDF
保存编译日志
```

输出：

```text
12_export/final_paper.pdf
12_export/compile_log.txt
```

验收标准：

```text
能编译空模板
能编译包含中文、公式、图片、参考文献的模板
错误日志可读
```

---

## 3. 开发优先级

## 必须先做

```text
P0-1 目录结构初始化
P0-2 execution_policy.yaml
P0-3 workflow_state.yaml
P0-4 run_current_stage.py
P1-1 generate_latex_template.py
P1-2 start_from_inputs.py
P2-1 generate_data_dictionary.py
P2-2 run_data_quality_check.py
P3-1 decompose_problem.py
P3-3 route_weight_config.py
```

原因：

```text
这些是流程地基。
没有状态控制，单环节深度模式无法落地。
没有 LaTeX 骨架，后续正文会失控。
没有数据和模型路由，论文生成会变成空写。
```

---

## 第二批做

```text
P4-1 代码模板库
P4-2 generate_model_code.py
P4-3 结果导出契约
P5-1 figure_registry.csv
P5-2 check_figure_quality.py
P6-1 section_generation_plan.csv
```

---

## 第三批做

```text
P6-2 generate_paper_sections.py
P6-3 完整正文分段生成
P7-1 polish_prompt.md
P7-2 polish_latex_sections.py
P8-1 check_gates.py
P8-2 compile_latex.py
```

---

## 4. MVP 验收标准

v3.0 MVP 不要求所有模型自动完美运行，但必须做到：

```text
1. 能初始化完整目录。
2. 能生成可编译 LaTeX 空模板。
3. 能读取题目与数据文件清单。
4. 能生成数据字典。
5. 能生成数据质量报告。
6. 能拆分问题并生成任务画像表。
7. 能生成模型路线和图文权重配置。
8. 能按单个问题生成代码骨架。
9. 能登记图表。
10. 能生成一个 LaTeX 章节初稿。
11. 能按 section 润色。
12. 能通过检查器发现跳步、未登记图表、未确认模型等问题。
13. 默认禁止并行和全文一次性生成。
```

---

## 5. 风险清单

## R1：OCR 不稳定

风险：

```text
扫描版题目无法可靠解析。
```

处理：

```text
只登记扫描件。
要求人工补录题目文字。
后续可加入 OCR 模块。
```

---

## R2：模型误判

风险：

```text
系统可能把评价题误判为优化题。
```

处理：

```text
模型路由必须输出备选模型和不推荐模型。
Gate 2 必须人工确认。
human_confirmed=false 时禁止代码生成。
```

---

## R3：代码和论文不一致

风险：

```text
代码跑的是一种模型，论文写的是另一种模型。
```

处理：

```text
建立 formula_registry.csv。
建立 result_summary.tex。
论文只能引用登记结果。
```

---

## R4：图表漂亮但无意义

风险：

```text
高级图表与正文结论无关。
```

处理：

```text
每张图必须有 main_message。
正文图必须 quality_score >= 4.2。
未服务正文结论的图转附录或删除。
```

---

## R5：润色改变结论

风险：

```text
弱结论被改成强结论。
```

处理：

```text
保留原文。
记录 polish_log.csv。
禁止改数字、变量、显著性、图表编号。
人工审核润色后文本。
```

---

## R6：并行推进导致质量下降

风险：

```text
数据未确认就生成模型，代码未运行就写论文。
```

处理：

```text
workflow_state.yaml 锁定节点。
execution_policy.yaml 禁止并行。
check_gates.py 发现跳步直接失败。
```

---

## 6. 开发完成后的建议命令

正式使用：

```bash
python scripts/start_full_pipeline.py --mode deep
```

执行当前节点：

```bash
python scripts/run_current_stage.py
```

生成 LaTeX 模板：

```bash
python scripts/generate_latex_template.py
```

运行数据分析：

```bash
python 04_eda_code/run_eda_pipeline.py
```

生成单问代码：

```bash
python scripts/generate_model_code.py --question Q1 --mode deep
```

生成单个论文章节：

```bash
python scripts/generate_paper_sections.py --section 06_model_q1 --mode deep
```

润色单个章节：

```bash
python scripts/polish_latex_sections.py --section 06_model_q1 --mode deep
```

终稿检查：

```bash
python scripts/check_gates.py
python scripts/compile_latex.py
```

---

## 7. 不做清单

v3.0 MVP 暂不做：

```text
自动 OCR 扫描题目
自动保证所有题型最优模型
自动生成无人工审核的终稿
自动虚构参考文献
自动绕过检测
多节点并行生成
全文一键粗糙润色
```

这些功能不是能力问题，而是质量和风险控制问题。比赛流程里，最贵的不是慢半小时，是错一层楼。
