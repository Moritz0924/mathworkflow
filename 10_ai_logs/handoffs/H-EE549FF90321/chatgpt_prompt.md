# implementation / ChatGPT

## 结果
对实现期间出现的建模歧义给出决策，保持已冻结模型路线的一致性。

## 边界
不直接声明本地代码已经运行，不修改Codex测得的错误、性能或数值结果。

## 交付
仅回答影响模型含义的决策点，并说明对公式、约束、参数或评价的影响。

## 验收
决策与冻结模型合同一致，且Codex能够转化为明确的实现和测试。

## 阻塞
需要改变冻结假设、目标函数或主模型时标记为模型修订，不得当作实现细节处理。

## Response metadata

Begin the response with this exact metadata block:

---
protocol: mmwf-handoff/v1
project_id: ccmc2025-a
stage: implementation
handoff_id: H-EE549FF90321
context_sha256: 497524d09cc6d557d1fbf0d23a76856bd37642fcc460069bbb33f79267442442
---

## Verified context

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


## `05_model/assumptions.csv`

assumption_id,content,source,applies_to,risk_level,validation_or_sensitivity,confirmation_status,notes
A01,导弹视为质点并在到达假目标原点前保持题面给定的匀速直线运动,ChatGPT模型设计 H-21D19FE5FD2C,Q1-Q5,低,与题面初始位置和到达时刻核对,pending_human,题面未给出机动信息
A02,无人机在t=0瞬时完成一次转向后保持固定水平航向和恒定高度飞行,ChatGPT模型设计 H-21D19FE5FD2C,Q1-Q5,低,检查航向速度在同机各弹记录中一致,pending_human,对应题面飞行规则
A03,干扰弹释放瞬间继承无人机水平速度且初始竖直速度为0,ChatGPT模型设计 H-21D19FE5FD2C,Q1-Q5,中,与不继承水平速度的替代口径比较,pending_human,题面未明确初速度继承方式
A04,起爆前忽略空气阻力并取重力加速度g=9.8 m/s²,ChatGPT模型设计 H-21D19FE5FD2C,Q1-Q5,中,比较g=9.8与g=9.81并记录差异,pending_human,题面未提供空气动力数据
A05,起爆后烟幕不保留水平速度且不受风影响，仅以3 m/s竖直下沉,ChatGPT模型设计 H-21D19FE5FD2C,Q1-Q5,中,检查烟幕中心轨迹和风场缺失的影响,pending_human,题面只给出匀速下沉
A06,干扰弹只允许在地面以上起爆，即起爆高度z≥0,ChatGPT模型设计 H-21D19FE5FD2C,Q1-Q5,中,验证延迟不超过由高度导出的物理上界,pending_human,排除地下起爆
A07,烟幕中心到达地面后停止计入有效遮蔽,ChatGPT模型设计 H-21D19FE5FD2C,Q1-Q5,中,与中心停留地面的替代口径比较,pending_human,保守地面边界处理
A08,主模型以全部圆柱代表点均被遮挡作为有效遮蔽判据,ChatGPT模型设计 H-21D19FE5FD2C,Q1-Q5,高,与中心点和覆盖比例口径作敏感性分析,pending_human,代表点密度须做收敛试验
A09,同一导弹受到多枚烟幕的有效时长按时间区间并集计算且不重复累计,ChatGPT模型设计 H-21D19FE5FD2C,Q3-Q5,中,构造重叠区间单元测试,pending_human,与有效遮蔽时长的计量含义一致
A10,Q5中每一枚已使用干扰弹登记一个主目标导弹编号,ChatGPT模型设计 H-21D19FE5FD2C,Q5,中,检查结果3模板的目标编号字段,pending_human,不排除物理上附带遮蔽其他导弹
A11,Q5按先总遮蔽时长后最短导弹遮蔽时长的字典序目标优化,ChatGPT模型设计 H-21D19FE5FD2C,Q5,高,与公平性优先的备选目标比较,pending_human,题面未显式规定多目标聚合方式
A12,Q5要求M1/M2/M3均至少分配一枚产生正有效时长的已使用干扰弹,ChatGPT模型设计 H-21D19FE5FD2C,Q5,高,检查每枚导弹的T_j>0并做取消约束对照,pending_human,题面对覆盖均衡的解释需人工确认
A13,未使用弹位在内部数据中标记is_used=0且最终模板默认留空,ChatGPT模型设计 H-21D19FE5FD2C,Q5,中,检查未使用行不输出伪坐标或负值,pending_human,需与最终模板填报口径一致


## `05_model/implementation_contract.md`

# 实现交接合同（模型冻结前）

## 边界

本文件把已导入的模型设计映射到仓库目录，不创建求解器，也不产生数值结果。`05_model/` 保存冻结前的模型工件；正式实现只能在人工确认 `model_freeze_gate` 后写入 `06_code/`。

## 计划模块

| 模块 | 职责 | 关键验收 |
|---|---|---|
| `constants.py` / `entities.py` | 题面常数、导弹、无人机、炸弹计划数据结构 | 单位和 ID 与题面、模板一致 |
| `dynamics.py` | 导弹、无人机、干扰弹、烟幕中心位置 | Q1 固定参数回归；起爆高度和时间边界 |
| `target_geometry.py` | 圆柱体代表点集及加密方案 | 代表点数和加密结果可复现 |
| `occlusion.py` | 视线投影参数、垂距、全代表点判据 | 视线前后、相切、越界的单元测试 |
| `intervals.py` | 有效区间定位、合并及长度计算 | 重叠、相邻、空区间的单元测试 |
| `constraints.py` / `validators.py` | 速度、起爆高度、投放间隔、Q5 分配和空行规则 | 每条约束均有拒绝用例 |
| `q1_evaluator.py` 至 `q5_solver.py` | 分问评估与优化入口 | Q1 无优化；Q2–Q5 先给可行解再作收敛与稳定性检查 |
| `exporters.py` | 内部结果合同与三份 Excel 模板映射 | 写入前从结果合同复算字段 |

## 数值配置的冻结规则

- 初始时间扫描步长、根求解容差、代表点密度、随机种子和最大评估次数均暂不设正式数值。
- 实施阶段须记录加密/收敛试验，再将通过验证的数值写入配置；不得凭经验在本阶段伪造。
- 主模型要同中心点、固定时间步和逐弹贪心基线比较，但基线不替代主模型结论。

## 本地依赖检查（2026-07-22）

- 可用：Python、NumPy、OpenPyXL。
- 缺失：SciPy。若执行 GPT 建议的 `differential_evolution` 与 `Powell`，implementation 阶段应将 `scipy` 加入受控依赖并记录版本；若提出替代优化器，则先返回 ChatGPT 重新确认。



## `05_model/model_route.md`

# 模型路线登记（待人工冻结）

## 来源与状态

- 决策来源：`10_ai_logs/handoffs/H-21D19FE5FD2C/chatgpt_response.md`。
- 本文件仅将 ChatGPT 的模型设计转写为本地可审计工件；不代表任何数值结果，也不构成人工确认。
- 当前状态：待 Codex 核验后进入 `model_freeze_gate` 人工确认。冻结前不得执行正式优化、填充结果模板或冻结结论。

## 主路线

采用“**三维确定性运动学—圆柱目标多视线遮挡—连续时间区间并集—分层混合优化**”路线：

1. 以三维匀速直线运动描述导弹和无人机，以无阻力抛体运动描述起爆前干扰弹，以竖直下沉描述起爆后烟幕中心；
2. 将半径 7 m、高 10 m 的真目标保留为圆柱体，并用确定性代表点集近似其几何；
3. 只有烟幕球同时遮挡全部代表点对应的导弹—目标视线时，才计为有效遮蔽；
4. 对同一导弹的多枚烟幕遮蔽区间求并集，重叠部分不重复累计；
5. Q2–Q4 使用连续黑箱全局搜索加局部精修；Q5 先做离散任务分配，再优化连续飞行和投放参数。

## 各问目标与输出边界

| 问题 | 决策/计算 | 评价目标 |
|---|---|---|
| Q1 | 使用题面给定 FY1 航向、120 m/s、投放时刻 1.5 s、起爆延迟 3.6 s | 计算对 M1 的实际有效遮蔽时长，不优化 |
| Q2 | FY1 的航向、速度、投放时刻和起爆延迟 | 最大化单弹对 M1 的有效遮蔽时长 |
| Q3 | FY1 的固定航向/速度及 3 枚弹的时序 | 最大化 M1 的遮蔽区间并集长度 |
| Q4 | FY1–FY3 各自的航向、速度、投放时刻和起爆延迟 | 最大化 M1 的遮蔽区间并集长度 |
| Q5 | FY1–FY5 每架至多 3 枚弹的使用、主目标分配和连续参数 | 先最大化 M1–M3 总遮蔽时长，再最大化三者最短遮蔽时长 |

## 约束与待冻结假设

- 题面硬约束：无人机速度为 70–140 m/s；飞行高度不变；同机相邻投放间隔至少 1 s；烟幕半径 10 m、物理有效期 20 s、中心下沉速度 3 m/s。
- 公式登记见 `14_contracts/formula_contract.csv`；全部假设及其风险见 `05_model/assumptions.csv`。
- A08（全代表点遮挡）、A11（Q5 字典序目标）和 A12（三枚导弹均须获得正遮蔽）为高风险建模口径，均尚未获得人工冻结。

## 人工冻结前必须确定的事项

1. 是否采用干扰弹继承无人机水平速度、忽略空气阻力并取 `g=9.8 m/s²`；
2. 烟幕中心到达地面后是否立即失效；
3. 遮蔽使用“全代表点”“中心点”还是“覆盖比例”口径；
4. 多弹遮蔽是否按时间并集统计；
5. Q5 是否要求 M1–M3 均有正有效遮蔽，以及总时长/公平性的优先级；
6. 一枚烟幕对非主目标的附带遮蔽是否计入 Q5 总目标；
7. 未使用弹位在最终模板中是否留空；
8. 代表点密度、时间扫描步长、求根容差和优化预算须在收敛试验后确定，不能现在虚填。

## 备选路线与触发条件

- 若全代表点口径下所有可行策略均为 0，则仅在人工批准后启用覆盖比例敏感性分析；
- 若代表点加密不收敛，则改用精确投影视锥几何方案；
- 若 Q5 总时长目标过度集中资源，比较公平性优先的备选目标；
- 以上均为已登记备选，不得由实现阶段自行切换。

## 实现可行性结论

运动学、视线距离、区间合并和模板映射均可由本地 Python 实现。建议的 `differential_evolution` 与 `Powell` 求解器通常依赖 SciPy；当前环境有 NumPy 和 OpenPyXL，但未安装 SciPy，故在 implementation 阶段开始前必须以受控依赖方式补齐 SciPy 或把等价求解器提交给 ChatGPT 重新确认。该依赖缺口不改变当前模型路线。


## `06_code/README.md`

# 代码说明

## 运行方式

```bash
pip install -r requirements.txt
python run_all.py
```

## 目录说明

- `src/`: 主模型、数据处理、绘图函数。
- `notebooks/`: 探索性分析笔记本，可选。
- `execution_log.md`: 每次运行记录。

## 结果输出约定

- 每问结果输出到 `07_results/q*_results.csv`。
- 总指标输出到 `07_results/metrics_summary.csv`。
- 结果来源映射输出到 `07_results/result_source_map.csv`。


## `06_code/execution_log.md`

# 代码执行日志

| run_id | 时间 | 命令 | 状态 | 输出文件 | 报错 | 修复 |
|---|---|---|---|---|---|---|
| RUN001 |  |  | 未运行 |  |  |  |


## `06_code/requirements.txt`

numpy
pandas
matplotlib
seaborn
plotly
networkx
pyyaml
scipy
scikit-learn
reportlab
openpyxl
pypdf
PyPDF2


## `06_code/run_all.py`

from pathlib import Path
from datetime import datetime
import pandas as pd

ROOT = Path(__file__).resolve().parents[0].parent
RESULT_DIR = ROOT / "07_results"
RESULT_DIR.mkdir(exist_ok=True)


def write_placeholder_results():
    for q in ["q1", "q2", "q3"]:
        df = pd.DataFrame([
            {"question": q.upper(), "metric": "placeholder", "value": "", "source": "manual_or_model_output"}
        ])
        df.to_csv(RESULT_DIR / f"{q}_results.csv", index=False, encoding="utf-8-sig")

    pd.DataFrame([
        {"metric_id": "M001", "question": "Q1", "metric_name": "", "value": "", "unit": "", "source_file": ""}
    ]).to_csv(RESULT_DIR / "metrics_summary.csv", index=False, encoding="utf-8-sig")

    pd.DataFrame([
        {"result_id": "R001", "question": "Q1", "result_file": "07_results/q1_results.csv", "generated_by": "run_all.py", "timestamp": datetime.now().isoformat(), "verified": False}
    ]).to_csv(RESULT_DIR / "result_source_map.csv", index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    write_placeholder_results()
    print("[OK] placeholder result files written to 07_results/")


## `06_code/src/__init__.py`



## `06_code/src/io_utils.py`

from pathlib import Path
import pandas as pd


def read_csv(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)


def write_csv(df: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
