# model_design / ChatGPT

## 结果
选择能回答全部子问题的模型路线，并定义假设、公式、变量、评价和备选方案。

## 边界
只能使用已验证题意和数据能力；不得以复杂度代替适配性，不得引用尚未运行的结果。

## 交付
给出主模型、基线、公式含义、参数估计、验证方案、失败条件和路线取舍。

## 验收
路线可由Codex实现，公式和假设可登记，评价指标能区分模型优劣并覆盖题目目标。

## 阻塞
数据无法识别关键参数、假设不可检验或多个路线缺少选择依据时请求补证据。

## Response metadata

Begin the response with this exact metadata block:

---
protocol: mmwf-handoff/v1
project_id: ccmc2025-a
stage: model_design
handoff_id: H-21D19FE5FD2C
context_sha256: 3b02ce794b93953aa97d9b127c9db913ef1697e565feed5fb77db13290c4f79a
---

## Verified context

## `00_problem/attachments_overview.md`

# 附件总览（经原始文件核验）

## 题目文件

| 文件 | 类型 | 状态 | 说明 |
|---|---|---|---|
| A题.pdf | .pdf | 已验证可读（PDF-1.7，286,520 bytes） | 赛题原文；可提取 1 页文本 |

## 数据文件

| 文件 | 类型 | 路径 | 说明 |
|---|---|---|---|
| result1.xlsx | .xlsx | 03_data/raw/result1.xlsx | 问题三结果模板：FY1 三枚干扰弹参数（运动方向、速度、投放点坐标、起爆点坐标、有效干扰时长） |
| result2.xlsx | .xlsx | 03_data/raw/result2.xlsx | 问题四结果模板：FY1/FY2/FY3 协同干扰参数 |
| result3.xlsx | .xlsx | 03_data/raw/result3.xlsx | 问题五结果模板：全编队五机三弹协同分配参数（含所干扰导弹编号） |

## 先验数据库

| 目录 | 说明 |
|---|---|
| 13_prior_db/ | 已构建结构化先验数据库（含 TF-IDF 全文索引、检索结果、论文卡片） |
| 论文数据集/ | 原始论文 PDF 集合（按建模方法分类：线性规划、神经网络等38类） |


## `00_problem/contest_info.yaml`

contest:
  name: "高教社杯全国大学生数学建模竞赛"
  year: 2025
  problem_id: "A"
  problem_title: "烟幕干扰弹的投放策略"
  source_file: "00_problem/inbox/A题.pdf"
  start_time: ""
  end_time: ""
  total_hours: 72
  current_time: ""

team:
  team_id: ""
  members:
    - name: ""
      role: ""
      responsibility: []

ai_policy:
  require_ai_log: true
  require_paper_anchor: true
  require_ai_usage_detail_pdf: true
  ai_superscript_format: "^{AI-xx}"


## `00_problem/problem_statement.md`

# 赛题原文摘要（经 A题.pdf 核验）

## 来源与适用范围

- 来源：`00_problem/inbox/A题.pdf`，2025 年高教社杯全国大学生数学建模竞赛 A 题。
- 题名：**烟幕干扰弹的投放策略**。
- 本文件是用于工作流交接的事实摘要；以原始 PDF 为最高优先级，不替代 PDF。

## 背景与目标

无人机受领任务后投放烟幕干扰弹，在来袭空地导弹与真目标之间形成烟幕遮蔽。需针对五种场景设计无人机航向、速度、烟幕弹投放点和起爆点，使对真目标的有效遮蔽时间尽可能长；不同烟幕弹形成的遮蔽区间可以不连续。

## 空间与运动参数

### 坐标与目标

- 假目标为坐标原点，水平面为 x-y 平面，z 轴表示高度。
- 真目标是半径 7 m、高 10 m 的圆柱体；其下底面圆心为 `(0, 200, 0)`。
- 三枚来袭导弹均以 300 m/s 匀速直线飞向假目标（原点）。

| 导弹 | 初始坐标 (m) |
|---|---|
| M1 | (20000, 0, 2000) |
| M2 | (19000, 600, 2100) |
| M3 | (18000, -600, 1900) |

| 无人机 | 初始坐标 (m) |
|---|---|
| FY1 | (17800, 0, 1800) |
| FY2 | (12000, 1400, 1400) |
| FY3 | (6000, -3000, 700) |
| FY4 | (11000, 2000, 1800) |
| FY5 | (13000, -2000, 1300) |

### 无人机约束

- 受领任务后可瞬时调整一次飞行方向。
- 以 70–140 m/s 的速度等高度、匀速、直线飞行。
- 各机航向与速度可以不同，但一旦确定不得再次调整。
- 结果模板中航向角以 x 轴正向为 0°，逆时针为正，取值范围为 `[0°, 360°)`。

### 烟幕干扰弹与烟幕云团

- 同一无人机任意两枚干扰弹的投放时间间隔不得小于 1 s。
- 干扰弹脱离无人机后仅受重力作用运动；其初始速度继承方式、重力常数及起爆时序范围需在建模阶段显式登记。
- 起爆后瞬时形成球状烟幕云团，云团中心以 3 m/s 匀速下沉。
- 起爆后 20 s 内，云团中心 10 m 范围为有效烟幕区域。

## 五个问题

### 问题 1：固定单机单弹情形

FY1 以 120 m/s 朝假目标方向飞行；受领任务 1.5 s 后投放一枚烟幕干扰弹，投放后 3.6 s 起爆。计算其对 M1 的有效遮蔽时长。

### 问题 2：单机单弹优化

利用 FY1 对 M1 投放一枚烟幕干扰弹，确定 FY1 飞行方向、飞行速度、投放点和起爆点，使遮蔽时间尽可能长。

### 问题 3：单机三弹协同

利用 FY1 投放三枚烟幕干扰弹对 M1 实施干扰，给出投放策略，并将结果填写到 `03_data/raw/result1.xlsx`。

### 问题 4：三机各一弹协同

利用 FY1、FY2、FY3 三架无人机，各投放一枚烟幕干扰弹对 M1 实施干扰，给出策略，并将结果填写到 `03_data/raw/result2.xlsx`。

### 问题 5：五机多弹多目标协同

利用 FY1–FY5 五架无人机，每架至多投放三枚烟幕干扰弹，对 M1–M3 实施干扰；给出策略，并将结果填写到 `03_data/raw/result3.xlsx`。

## 待在后续阶段明确的建模口径

题面给出了烟幕云团和真目标的几何参数，但未用公式定义“有效遮蔽”判据。后续须明确：

1. 导弹—真目标视线与烟幕球相交的判定，以及真目标圆柱体的几何表示；
2. 干扰弹释放瞬间的初速度继承、重力常数、起爆是否受地面边界限制；
3. 多枚干扰弹对同一导弹的遮蔽时长是否按时间并集计量；
4. 问题 5 多导弹遮蔽时间的聚合目标。

## 结果与审计要求

- Q3、Q4、Q5 分别使用 `result1.xlsx`、`result2.xlsx`、`result3.xlsx` 模板。
- 所有后续数值结果必须登记到 `14_contracts/result_contract.csv`；公式、图表和论断也必须先登记对应合同。


## `01_task_analysis/task_decomposition.md`

# 问题拆解与数据边界

## 事实来源优先级

1. `00_problem/inbox/A题.pdf`；
2. `03_data/raw/result1.xlsx`、`result2.xlsx`、`result3.xlsx`；
3. 本地题面摘要与由模板检查器生成的数据工件；
4. 已导入的 data_analysis 阶段回复（`H-4709302CC4F4`）。

自动生成的数据工件与原始 PDF 冲突时，以 PDF 为准。

## 子问题依赖

| 问题 | 场景 | 输出 | 与前问关系 |
|---|---|---|---|
| Q1 | FY1 一机一弹干扰 M1；航向、120 m/s、投放时刻和起爆间隔固定 | 单弹实际有效遮蔽时长 | 验证运动学与遮蔽判据的基础算例 |
| Q2 | FY1 一机一弹干扰 M1 | 航向、速度、投放点、起爆点和最大遮蔽时长 | 将 Q1 的固定参数变为决策变量 |
| Q3 | FY1 三弹干扰 M1 | `result1.xlsx` | 在 Q2 基础上加入同机投放间隔和多弹时间区间 |
| Q4 | FY1/FY2/FY3 各一弹干扰 M1 | `result2.xlsx` | 在单弹计算基础上加入跨机协同 |
| Q5 | 五机、每机至多三弹干扰 M1/M2/M3 | `result3.xlsx` | 加入多目标分配、资源配置和总体评价 |

## 变量角色

- 题面常量：导弹和无人机初始位置、导弹速度、无人机速度范围、真目标几何、烟幕半径/下沉速度/有效期、最小投放间隔。
- 状态变量：导弹、无人机、未起爆干扰弹和烟幕云团的位置；有效遮蔽是否成立。
- 后续决策变量：航向、速度、投放时刻、起爆时刻/延迟和 Q5 目标分配。
- 派生结果：投放点、起爆点、遮蔽时间区间、并集时长和模板填写值。

## 数据边界

三份 Excel 是官方结果填写模板，而非历史或观测样本。模板中的空白表示“结果待计算”，不能用于相关性、回归、异常值分布或特征筛选。

模板结构核验结果：

- `result1.xlsx`：3 个结果行，对应 FY1 的三枚干扰弹；
- `result2.xlsx`：3 个结果行，对应 FY1、FY2、FY3 各一枚干扰弹；
- `result3.xlsx`：15 个结果行，对应 5 架无人机各 3 个潜在弹位；
- 三份文件均无合并单元格、公式、隐藏行列、保护或数据验证；详细记录见 `03_data/template_structure_report.md`。

## 已修正的本地事实

- Q1 的 `1.5 s` 是接令后的投放时刻，`3.6 s` 是投放至起爆的间隔；二者均不适用于 Q2–Q5。
- 起爆后烟幕瞬时形成；20 s 是物理有效期上限，而非每枚弹必然获得的遮蔽时长。
- EDA 入口只做模板结构核验；在至少两列真实数值观测出现前，不生成相关性图。

## 进入模型设计前需登记的假设

以下事项不是题面已给定事实，必须在模型设计中显式登记并由人工在 `model_freeze_gate` 前确认：

1. 有效遮蔽的几何判据，以及真目标圆柱体的表示方式；
2. 干扰弹的初始速度、重力常数、空气阻力和地面边界；
3. Q2–Q5 的起爆时序范围；
4. 同一导弹的多弹遮蔽时间是否按区间并集统计；
5. Q5 对 M1/M2/M3 的聚合目标与公平性口径；
6. 未使用弹位在最终模板中的填写规则。


## `03_data/cleaning_rules.md`

# 数据清洗与结果一致性规则

这些规则用于校验后续计算结果；`03_data/raw/` 中的官方模板不作覆盖修改。

| 规则编号 | 字段或对象 | 判定 | 处理方式 | 是否影响正式结果 | 记录文件 |
|---|---|---|---|---|---|
| CR001 | 无人机运动速度 (m/s) | 不在 70~140 m/s | 标记为硬约束违例，阻止结果冻结 | 是 | processed/cleaning_log.csv |
| CR002 | 无人机运动方向 | 不在 `[0, 360)` | 仅对等价角度归一化；保留原值与归一化记录 | 否 | processed/cleaning_log.csv |
| CR003 | 有效干扰时长 (s) | 已使用弹的时长 `<= 0`，或任意记录的时长 `< 0` | 已使用弹的非正时长和任何负值均为错误；未使用弹按最终模板规则留空或填 0，并显式标记未使用 | 是 | processed/cleaning_log.csv |
| CR004 | 投放点、起爆点坐标 | 已使用弹存在非有限数值 | 标记异常，回退到弹道复核 | 是 | processed/cleaning_log.csv |
| CR005 | 同一无人机多弹记录 | 航向或速度不一致 | 标记为硬约束违例；同一无人机一经确定航向和速度不得再调整 | 是 | processed/cleaning_log.csv |
| CR006 | 同一无人机多次投放 | 相邻投放时间间隔小于 1 s | 标记为硬约束违例 | 是 | processed/cleaning_log.csv |
| CR007 | 干扰目标导弹编号 | 不属于 `M1`、`M2`、`M3` | 标记异常，回退到任务分配复核 | 是 | processed/cleaning_log.csv |

## 原始数据保留原则

- 原始模板 `03_data/raw/` 不得覆盖。
- 派生数据和校验日志写入 `03_data/processed/`。
- 清洗或归一化前后的差异必须可追溯。


## `03_data/data_dictionary.csv`

﻿file_name,column_name,inferred_type,missing_rate,unique_count,sample_values,possible_meaning,risk_note
result1.xlsx,无人机运动方向,numeric,not_applicable_template,0,,无人机运动方向,结果待计算；空白单元格不是观测数据缺失
result1.xlsx,无人机运动速度 (m/s),numeric,not_applicable_template,0,,无人机运动速度 (m/s),结果待计算；空白单元格不是观测数据缺失
result1.xlsx,烟幕干扰弹编号,integer,not_applicable_template,3,1 | 2 | 3,烟幕干扰弹编号,结果待计算；空白单元格不是观测数据缺失
result1.xlsx,烟幕干扰弹投放点的x坐标 (m),numeric,not_applicable_template,0,,烟幕干扰弹投放点的x坐标 (m),结果待计算；空白单元格不是观测数据缺失
result1.xlsx,烟幕干扰弹投放点的y坐标 (m),numeric,not_applicable_template,0,,烟幕干扰弹投放点的y坐标 (m),结果待计算；空白单元格不是观测数据缺失
result1.xlsx,烟幕干扰弹投放点的z坐标 (m),numeric,not_applicable_template,0,,烟幕干扰弹投放点的z坐标 (m),结果待计算；空白单元格不是观测数据缺失
result1.xlsx,烟幕干扰弹起爆点的x坐标 (m),numeric,not_applicable_template,0,,烟幕干扰弹起爆点的x坐标 (m),结果待计算；空白单元格不是观测数据缺失
result1.xlsx,烟幕干扰弹起爆点的y坐标 (m),numeric,not_applicable_template,0,,烟幕干扰弹起爆点的y坐标 (m),结果待计算；空白单元格不是观测数据缺失
result1.xlsx,烟幕干扰弹起爆点的z坐标 (m),numeric,not_applicable_template,0,,烟幕干扰弹起爆点的z坐标 (m),结果待计算；空白单元格不是观测数据缺失
result1.xlsx,有效干扰时长 (s),numeric,not_applicable_template,0,,有效干扰时长 (s),结果待计算；空白单元格不是观测数据缺失
result2.xlsx,无人机编号,categorical,not_applicable_template,3,FY1 | FY2 | FY3,无人机编号,结果待计算；空白单元格不是观测数据缺失
result2.xlsx,无人机运动方向,numeric,not_applicable_template,0,,无人机运动方向,结果待计算；空白单元格不是观测数据缺失
result2.xlsx,无人机运动速度 (m/s),numeric,not_applicable_template,0,,无人机运动速度 (m/s),结果待计算；空白单元格不是观测数据缺失
result2.xlsx,烟幕干扰弹投放点的x坐标 (m),numeric,not_applicable_template,0,,烟幕干扰弹投放点的x坐标 (m),结果待计算；空白单元格不是观测数据缺失
result2.xlsx,烟幕干扰弹投放点的y坐标 (m),numeric,not_applicable_template,0,,烟幕干扰弹投放点的y坐标 (m),结果待计算；空白单元格不是观测数据缺失
result2.xlsx,烟幕干扰弹投放点的z坐标 (m),numeric,not_applicable_template,0,,烟幕干扰弹投放点的z坐标 (m),结果待计算；空白单元格不是观测数据缺失
result2.xlsx,烟幕干扰弹起爆点的x坐标 (m),numeric,not_applicable_template,0,,烟幕干扰弹起爆点的x坐标 (m),结果待计算；空白单元格不是观测数据缺失
result2.xlsx,烟幕干扰弹起爆点的y坐标 (m),numeric,not_applicable_template,0,,烟幕干扰弹起爆点的y坐标 (m),结果待计算；空白单元格不是观测数据缺失
result2.xlsx,烟幕干扰弹起爆点的z坐标 (m),numeric,not_applicable_template,0,,烟幕干扰弹起爆点的z坐标 (m),结果待计算；空白单元格不是观测数据缺失
result2.xlsx,有效干扰时长 (s),numeric,not_applicable_template,0,,有效干扰时长 (s),结果待计算；空白单元格不是观测数据缺失
result3.xlsx,无人机编号,categorical,not_applicable_template,5,FY1 | FY1 | FY1 | FY2 | FY2 | FY2 | FY3 | FY3 | FY3 | FY4 | FY4 | FY4 | FY5 | FY5 | FY5,无人机编号,结果待计算；空白单元格不是观测数据缺失
result3.xlsx,无人机运动方向,numeric,not_applicable_template,0,,无人机运动方向,结果待计算；空白单元格不是观测数据缺失
result3.xlsx,无人机运动速度 (m/s),numeric,not_applicable_template,0,,无人机运动速度 (m/s),结果待计算；空白单元格不是观测数据缺失
result3.xlsx,烟幕干扰弹编号,integer,not_applicable_template,3,1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 | 3,烟幕干扰弹编号,结果待计算；空白单元格不是观测数据缺失
result3.xlsx,烟幕干扰弹投放点的x坐标 (m),numeric,not_applicable_template,0,,烟幕干扰弹投放点的x坐标 (m),结果待计算；空白单元格不是观测数据缺失
result3.xlsx,烟幕干扰弹投放点的y坐标 (m),numeric,not_applicable_template,0,,烟幕干扰弹投放点的y坐标 (m),结果待计算；空白单元格不是观测数据缺失
result3.xlsx,烟幕干扰弹投放点的z坐标 (m),numeric,not_applicable_template,0,,烟幕干扰弹投放点的z坐标 (m),结果待计算；空白单元格不是观测数据缺失
result3.xlsx,烟幕干扰弹起爆点的x坐标 (m),numeric,not_applicable_template,0,,烟幕干扰弹起爆点的x坐标 (m),结果待计算；空白单元格不是观测数据缺失
result3.xlsx,烟幕干扰弹起爆点的y坐标 (m),numeric,not_applicable_template,0,,烟幕干扰弹起爆点的y坐标 (m),结果待计算；空白单元格不是观测数据缺失
result3.xlsx,烟幕干扰弹起爆点的z坐标 (m),numeric,not_applicable_template,0,,烟幕干扰弹起爆点的z坐标 (m),结果待计算；空白单元格不是观测数据缺失
result3.xlsx,有效干扰时长 (s),numeric,not_applicable_template,0,,有效干扰时长 (s),结果待计算；空白单元格不是观测数据缺失
result3.xlsx,干扰的导弹编号,categorical,not_applicable_template,0,,干扰的导弹编号,结果待计算；空白单元格不是观测数据缺失


## `03_data/data_quality_report.md`

# 数据质量报告

## 结论

三份 Excel 文件均为官方结果填写模板。其空白数值单元格表示结果尚未计算，不能按观测数据缺失处理，也不能用于相关性、回归或异常值分布分析。

## 模板核验

| 文件 | 工作表 | 可填写结果行 | 结构状态 |
|---|---|---|---|
| result1.xlsx | Sheet1 | 2, 3, 4 | 无合并、无公式、无隐藏行列、未保护 |
| result2.xlsx | Sheet1 | 2, 3, 4 | 无合并、无公式、无隐藏行列、未保护 |
| result3.xlsx | Sheet1 | 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16 | 无合并、无公式、无隐藏行列、未保护 |

## 后续结果校验规则

- 已使用弹的投放点、起爆点和有效干扰时长必须为可复核数值。
- 未使用弹位由最终模型设计明确留空或填 0；无论何种表示，负的有效时长均非法。
- 同一无人机的多弹记录必须共享同一航向与速度，并满足相邻投放间隔不少于 1 s。
- 相关性 EDA 在没有至少两列真实数值观测前必须跳过。


## `03_data/data_quality_report.tex`

\section{数据预处理与数据质量诊断}

本节由自动数据质量检查生成，字段含义和异常处理仍需人工确认。



## `03_data/input_decision_table.csv`

input_id,field_name,source_file,question,model,decision,reason,risk_level,fallback,notes
IN01,导弹初始位置,00_problem/inbox/A题.pdf,Q1-Q5,全问,采用题面给定坐标,题面硬数据不可改,低,,M1/M2/M3 坐标
IN02,无人机初始位置,00_problem/inbox/A题.pdf,Q1-Q5,全问,采用题面给定坐标,题面硬数据不可改,低,,FY1~FY5 坐标
IN03,导弹速度,00_problem/inbox/A题.pdf,Q1-Q5,全问,300 m/s 匀速,题面给定,低,,导弹指向假目标原点
IN04,无人机速度范围,00_problem/inbox/A题.pdf,Q1-Q5,全问,70~140 m/s 约束,题面给定,低,,等高度匀速直线飞行
IN05,Q1投放时刻,00_problem/inbox/A题.pdf,Q1,固定情景,接令后1.5 s,Q1题面给定的投放时刻,低,,不适用于Q2-Q5
IN06,Q1投放至起爆间隔,00_problem/inbox/A题.pdf,Q1,固定情景,3.6 s,Q1题面给定的投放至起爆间隔,低,,起爆后烟幕瞬时形成；不适用于Q2-Q5
IN07,烟幕物理有效期,00_problem/inbox/A题.pdf,Q1-Q5,全问,起爆后20 s,题面给定,低,,实际遮蔽时长不超过该上限
IN08,Q2-Q5起爆时序,00_problem/inbox/A题.pdf,Q2-Q5,待建模口径,题面未规定,不得将Q1时序外推到Q2-Q5,高,模型设计阶段登记假设,需与地面边界和弹道可行性共同处理


## `03_data/template_structure_report.md`

# 官方结果模板结构核验

- 检查方式：openpyxl 只读结构检查。
- 结论：三份文件均为待填写的结果模板，不是统计样本数据。

## result1.xlsx

- 工作表：`Sheet1`（共 1 张）
- 维度：6 行 × 10 列
- 可填写结果行：2, 3, 4
- 合并单元格：无
- 隐藏行/列：无 / 无
- 保护：否；公式：0；数据验证：0
- 单元格数字格式：General
- 表头：无人机运动方向；无人机运动速度 (m/s)；烟幕干扰弹编号；烟幕干扰弹投放点的x坐标 (m)；烟幕干扰弹投放点的y坐标 (m)；烟幕干扰弹投放点的z坐标 (m)；烟幕干扰弹起爆点的x坐标 (m)；烟幕干扰弹起爆点的y坐标 (m)；烟幕干扰弹起爆点的z坐标 (m)；有效干扰时长 (s)

## result2.xlsx

- 工作表：`Sheet1`（共 1 张）
- 维度：6 行 × 10 列
- 可填写结果行：2, 3, 4
- 合并单元格：无
- 隐藏行/列：无 / 无
- 保护：否；公式：0；数据验证：0
- 单元格数字格式：General
- 表头：无人机编号；无人机运动方向；无人机运动速度 (m/s)；烟幕干扰弹投放点的x坐标 (m)；烟幕干扰弹投放点的y坐标 (m)；烟幕干扰弹投放点的z坐标 (m)；烟幕干扰弹起爆点的x坐标 (m)；烟幕干扰弹起爆点的y坐标 (m)；烟幕干扰弹起爆点的z坐标 (m)；有效干扰时长 (s)

## result3.xlsx

- 工作表：`Sheet1`（共 1 张）
- 维度：18 行 × 12 列
- 可填写结果行：2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16
- 合并单元格：无
- 隐藏行/列：无 / 无
- 保护：否；公式：0；数据验证：0
- 单元格数字格式：General
- 表头：无人机编号；无人机运动方向；无人机运动速度 (m/s)；烟幕干扰弹编号；烟幕干扰弹投放点的x坐标 (m)；烟幕干扰弹投放点的y坐标 (m)；烟幕干扰弹投放点的z坐标 (m)；烟幕干扰弹起爆点的x坐标 (m)；烟幕干扰弹起爆点的y坐标 (m)；烟幕干扰弹起爆点的z坐标 (m)；有效干扰时长 (s)；干扰的导弹编号


## `04_eda/eda_report.md`

# 数据分析与 EDA 报告

## 数据性质

result1.xlsx、result2.xlsx、result3.xlsx 是结果模板而非观测样本。预填的仅为无人机或烟幕弹编号；方向、速度、坐标与时长均待后续计算产生。

## 可执行分析

- 已完成模板字段、行结构、工作表与格式核验，详见 `03_data/template_structure_report.md`。
- 已完成题面参数、模板输出字段和硬约束的结构化映射。
- 当前不生成相关性热力图、回归、描述统计或特征筛选图：这些方法对空结果模板没有统计意义。

## 已发现的本地事实冲突

- `input_decision_table.csv` 中的 Q1 时序已按原题修正为“接令后 1.5 s 投放”和“投放后 3.6 s 起爆”，且不外推到 Q2–Q5。
- EDA 脚本现在要求至少两列具有真实数值观测才生成相关性图。

## 进入模型设计前仍需登记的假设

- 有效遮蔽的几何判据；
- 干扰弹初始速度、重力常数、地面边界和 Q2–Q5 起爆时序；
- 多弹重叠时间的统计规则及 Q5 的目标聚合方式。


## `14_contracts/formula_contract.csv`

formula_id,question_id,section_id,formula_latex,symbols_defined,assumption_ids,derivation_source,used_in_section,latex_label,depends_on_formula_ids,validation_note,status,owner,last_checked
