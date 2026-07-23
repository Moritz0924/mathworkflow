# finalize / ChatGPT

## 结果
在不改变事实的前提下完成最终语言收束和提交材料说明。

## 边界
不得改变数字、公式、模型、标签、引用、文献或结果含义，不新增未经审查的论断。

## 交付
提交最终文本修订说明、受保护元素确认和残余风险说明。

## 验收
润色差异只涉及语言与结构，所有事实性元素与人工确认正文一致。

## 阻塞
任何修改需要改变事实、补充结果或重开模型决策时退回对应阶段。

## Response metadata

Begin the response with this exact metadata block:

---
protocol: mmwf-handoff/v1
project_id: ccmc2025-a
stage: finalize
handoff_id: H-E1440393972F
context_sha256: ee1f30d733617fcc01e572b37d515a53ab9a3579cd74a4de1511065e5bb06c53
---

## Verified context

## `02_latex_template/main.tex`

\documentclass[UTF8,a4paper,12pt]{ctexart}
\input{preamble.tex}
\begin{document}
\input{sections/00_abstract}
\input{sections/01_background}
\input{sections/02_problem_analysis}
\input{sections/03_assumptions}
\input{sections/04_symbols}
\input{sections/05_data_analysis}
\input{sections/06_model_q1}
\input{sections/07_model_q2}
\input{sections/08_model_q3}
\input{sections/09_sensitivity}
\input{sections/10_model_evaluation}
\input{sections/11_conclusion}
\bibliographystyle{gbt7714-numerical}
\bibliography{references}
\appendix
\input{sections/appendix}
\end{document}


## `02_latex_template/preamble.tex`

\usepackage{geometry}
\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}
\usepackage{amsmath,amssymb,bm,graphicx,booktabs,longtable,array,float,caption,subcaption,algorithm,algpseudocode,hyperref,xcolor}
\usepackage{cn_math_style}
\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=blue}
\captionsetup{font=small, labelfont=bf}
\setlength{\parindent}{2em}
\setlength{\parskip}{0.2em}


## `02_latex_template/references.bib`

% 请填入真实参考文献，禁止虚构文献。


## `02_latex_template/sections/00_abstract.tex`

% 摘要建议在全文完成后最后生成。
\begin{abstract}
% TODO: 摘要最后生成，避免与正文不一致。
\end{abstract}
\noindent\textbf{关键词：} TODO；数学建模；数据分析；模型求解


## `02_latex_template/sections/01_background.tex`

\section{问题背景与问题重述}

% TODO: 基于赛题原文填写。


## `02_latex_template/sections/02_problem_analysis.tex`

\section{问题分析}

% TODO: 基于分问拆解填写。


## `02_latex_template/sections/03_assumptions.tex`

\section{模型假设}

% TODO: 假设必须服务模型，不得空泛。


## `02_latex_template/sections/04_symbols.tex`

\section{符号说明}

% TODO: 用三线表列出变量和含义。


## `02_latex_template/sections/05_data_analysis.tex`

\section{数据预处理与数据分析}

% TODO: 插入数据质量报告和 EDA 结论。


## `02_latex_template/sections/06_model_q1.tex`

\section{问题一模型建立与求解}

% TODO: 基于真实 Q1 结果填写。


## `02_latex_template/sections/07_model_q2.tex`

\section{问题二模型建立与求解}

% TODO: 基于真实 Q2 结果填写。


## `02_latex_template/sections/08_model_q3.tex`

\section{问题三模型建立与求解}

% TODO: 基于真实 Q3 结果填写。


## `02_latex_template/sections/09_sensitivity.tex`

\section{灵敏度分析与误差分析}

% TODO: 基于真实结果填写。


## `02_latex_template/sections/10_model_evaluation.tex`

\section{模型评价}

% TODO: 写优缺点和改进方向。


## `02_latex_template/sections/11_conclusion.tex`

\section{结论}

% TODO: 全文完成后填写。


## `02_latex_template/sections/appendix.tex`

\section{附录}

% TODO: 放置代码说明、补充图表和必要推导。


## `09_paper/active_weight_config.csv`

﻿question,problem_type,model_family,main_model,baseline_model,abstract_pct,problem_restatement_pct,analysis_pct,assumption_symbol_pct,data_processing_pct,model_building_pct,solution_pct,result_analysis_pct,validation_pct,evaluation_extension_pct,main_figures_target,main_tables_target,figure_text_ratio,text_weight,figure_weight,table_weight,formula_weight,validation_weight,writing_emphasis,prior_card_ids,prior_source_ids,prior_confidence
Q1,机器学习型,机器学习,随机森林/梯度提升树,逻辑回归/随机森林/LightGBM,6,6,7,6,17,16,11,14,13,3,7-11,4-8,0.44:0.56,0.34,0.34,0.14,0.06,0.12,训练流程、对比实验、泛化误差和可解释性要闭环,,,
Q2,预测回归型,预测回归,预测回归模型,线性回归/ARIMA/指数平滑,6,7,8,6,16,16,10,16,11,3,5-8,3-6,0.38:0.62,0.42,0.28,0.12,0.08,0.1,数据清洗、变量解释、误差控制和外推边界要足够,,,
Q3,预测回归型,预测回归,多元回归/正则化回归,线性回归/ARIMA/指数平滑,6,7,8,6,16,16,10,16,11,3,5-8,3-6,0.38:0.62,0.42,0.28,0.12,0.08,0.1,数据清洗、变量解释、误差控制和外推边界要足够,,,
Q4,数据评价型,统计评价,指标评价模型,等权评价/TOPSIS/熵权法,6,7,8,7,13,17,10,18,8,4,6-9,6-10,0.42:0.58,0.38,0.27,0.22,0.05,0.08,指标含义、权重来源、评价解释和稳健性优先,,,
Q5,预测回归型,预测回归,多元回归/正则化回归,线性回归/ARIMA/指数平滑,6,7,8,6,16,16,10,16,11,3,5-8,3-6,0.38:0.62,0.42,0.28,0.12,0.08,0.1,数据清洗、变量解释、误差控制和外推边界要足够,,,
Q6,预测回归型,预测回归,多元回归/正则化回归,线性回归/ARIMA/指数平滑,6,7,8,6,16,16,10,16,11,3,5-8,3-6,0.38:0.62,0.42,0.28,0.12,0.08,0.1,数据清洗、变量解释、误差控制和外推边界要足够,,,


## `09_paper/ai_style_risk_check.md`

# AI 风格风险检查

## 检查项

- [ ] 是否存在模板腔高频句式
- [ ] 是否存在空泛结论
- [ ] 是否存在未验证绝对化表述
- [ ] 是否删除了 AI 角标
- [ ] 是否删除了参考文献引用
- [ ] 是否改变了数值结果

## 高风险段落

| paper_block_id | 风险 | 修复建议 |
|---|---|---|


## `09_paper/ai_superscript_insert_list.csv`

﻿ai_anchor_id,paper_section,paper_block_id,superscript_label,insert_position,status,notes


## `09_paper/anchor_consistency_check.md`

# 正文点位一致性检查

## AI 点位

- [ ] 正文所有 `^{AI-xx}` 均存在于 `10_ai_logs/ai_anchor_map.csv`
- [ ] 所有进入正文的 AI 调用均有人工修改说明

## 文献点位

- [ ] 正文引用均存在于 `02_literature/citation_anchor_map.csv`
- [ ] 参考文献表与正文双向一致

## 图表点位

- [ ] 正文图表均存在于 `08_figures/figure_status.csv`
- [ ] 正文图表视觉评分均不低于 4/5


## `09_paper/citation_insert_list.csv`

﻿citation_anchor_id,paper_section,paper_block_id,citation_format,insert_position,status,notes


## `09_paper/draft_v1.md`

# 论文初稿 v1

> 所有 AI 点位、文献引用、图表引用、数值来源须在进入终稿前完成校验。



## `09_paper/draft_v1_with_anchors.md`

# 带 AI 与引用点位的论文初稿 v1

> 所有 AI 点位、文献引用、图表引用、数值来源须在进入终稿前完成校验。



## `09_paper/draft_v2.md`

# 论文强化稿 v2

> 所有 AI 点位、文献引用、图表引用、数值来源须在进入终稿前完成校验。



## `09_paper/draft_v2_polished.md`

# 语言校订稿 v2 polished

> 所有 AI 点位、文献引用、图表引用、数值来源须在进入终稿前完成校验。



## `09_paper/dynamic_outline_router.md`

# 动态论文大纲路由

## 核心原则

论文结构不固定平均分配。每一问的正文篇幅、图表数量和结果解释深度由 `problem_type × model_family` 决定。

## 推荐总篇幅权重

| 模块 | 基础权重 | 可调区间 | 说明 |
|---|---:|---:|---|
| 摘要 | 6% | 5-7% | 必须给问题、方法、关键数值结果、结论 |
| 问题重述 | 7% | 5-8% | 不照抄题目，转成建模语言 |
| 问题分析 | 8% | 6-10% | 说明每问任务本质和模型选择原因 |
| 假设与符号 | 6-12% | 随机理和优化题上调 | 只写会被后文使用的假设和符号 |
| 数据处理 | 8-17% | 数据题上调 | 清洗、口径、异常、指标构造 |
| 模型建立 | 16-22% | 优化/机理题上调 | 公式、变量、约束、机理或算法 |
| 模型求解 | 10-16% | 优化题上调 | 求解流程、参数、复杂度、实现 |
| 结果分析 | 13-18% | 所有题都不能低 | 必须图表结合，不只罗列表格 |
| 检验与敏感性 | 7-13% | 预测/机器学习上调 | 稳健性、误差、对比实验 |
| 评价推广 | 3-4% | 保持克制 | 优缺点必须具体 |

## 每问图文落点

每一问至少包含：

1. 模型意图图：放在建模开始前。
2. 关键结果图：放在结果段第一屏附近。
3. 检验或对比图：放在结果解释之后。

复杂问题再增加：机制图、参数敏感性图、方案矩阵图、空间/网络图。

## 降噪规则

- 摘要、问题重述、假设不堆图。
- 正文表格超过 8 列优先转附录，正文只放摘要表。
- 公式密集段落必须用流程图或变量关系图稀释阅读压力。
- 每 800-1200 中文字至少出现 1 个图表或结构化表述。


## `09_paper/figure_insert_list.csv`

﻿figure_id,paper_section,paper_block_id,insert_position,caption_id,status,notes


## `09_paper/final_paper.md`

# 论文终稿

> 所有 AI 点位、文献引用、图表引用、数值来源须在进入终稿前完成校验。



## `09_paper/formatting_checklist.md`

# 排版检查清单

- [ ] 标题格式统一
- [ ] 摘要包含目标、方法、结果、结论
- [ ] 图表编号连续
- [ ] 公式编号连续
- [ ] 符号说明完整
- [ ] 引用编号连续
- [ ] 附录材料完整
- [ ] AI 使用详情 PDF 已准备


## `09_paper/frozen_text_blocks.md`

# 冻结文本块

| paper_block_id | 来源阶段 | 可写入章节 | 文本状态 | AI 点位 | 引用点位 |
|---|---|---|---|---|---|

## 文本块

### PB-Q1-001




## `09_paper/full_draft.md`



# 基于三维运动学与多视线遮挡判据的烟幕干扰弹投放策略研究

## 摘要

针对无人机投放烟幕干扰弹对来袭导弹实施视线遮蔽的问题，本文建立了一个“**三维确定性运动学—圆柱目标多视线遮挡—连续时间区间并集—分层混合优化**”模型。首先，根据导弹直指假目标的匀速直线运动、无人机等高度匀速直线飞行、干扰弹无阻力抛体运动以及烟幕云团竖直下沉规律，统一建立导弹、无人机、干扰弹和烟幕中心的时空轨迹。其次，将真目标保留为半径 7 m、高 10 m 的圆柱体，以确定性代表点集近似其几何轮廓；只有烟幕球同时遮挡导弹至全部代表点的视线时，才判定为有效遮蔽。对多枚烟幕弹，则对同一导弹的有效遮蔽时间区间求并集，避免重叠时间重复累计。

问题一采用题面固定参数进行回归计算，得到对 M1 的有效遮蔽时长为 **1.3622014999389869 s**。问题二通过差分进化与局部精修联合调整 FY1 的航向、速度、投放时刻和起爆延迟[1-2]，得到有效遮蔽时长 **2.2381643772125575 s**，较问题一增加 **0.8759628772735706 s**，相对增加约 **64.3049%**。问题三和问题四的冻结结果均为 **2.2381643772125575 s**；逐弹复核表明，额外干扰弹或无人机未形成新增有效区间，因此不能据此宣称产生了额外协同收益。问题五采用离散任务分配与连续参数优化相结合的分层方法，实际使用 FY1、FY2、FY5 的第 1 枚干扰弹分别干扰 M1、M2、M3，三枚导弹的有效遮蔽时长分别为 **2.2381643772125575 s**、**1.9820433139801334 s** 和 **1.8768008708953303 s**，总时长为 **6.097008562088021 s**，最短时长为 **1.8768008708953303 s**。

冻结结果在所检验的三个随机种子下输出跨度为 0，模板映射检查通过，失败数为 0。敏感性分析表明，现有结果对“干扰弹继承无人机水平速度”这一假设高度敏感；烟幕到达地面后的处理方式未改变当前有效区间；遮挡覆盖口径和问题五的目标优先级会对数值或任务分配产生实质影响。本文结果均绑定冻结包 `RF-20260722T114756Z`，不将数值求解结果表述为数学意义上的全局最优证明。

**关键词：** 烟幕干扰弹；无人机；三维运动学；视线遮挡；区间并集；差分进化；多目标分配

---

# 1 问题重述

## 1.1 问题背景

来袭导弹在飞行过程中通过观测真实目标实施攻击。无人机可携带烟幕干扰弹，在适当的时间和空间位置投放并起爆，使烟幕云团位于导弹与真实目标之间，从而遮挡导弹视线。烟幕干扰效果不仅与投放点和起爆点有关，还受无人机航向、飞行速度、投放时刻、起爆延迟、烟幕下沉及多枚烟幕弹时间重叠等因素共同影响。

题面给出一个假目标和一个真实目标。假目标位于坐标原点，真实目标是下底面圆心为 \((0,200,0)\)、半径为 7 m、高度为 10 m 的圆柱体。三枚导弹 M1、M2、M3 以 300 m/s 的速度由各自初始位置飞向假目标。五架无人机 FY1—FY5 接到任务后可瞬时改变一次航向，随后以 70—140 m/s 的速度进行等高度、匀速、直线飞行。

干扰弹脱离无人机后仅受重力作用，起爆后瞬时形成球状烟幕云团。云团中心 10 m 范围内为有效烟幕区域，中心以 3 m/s 匀速下沉，起爆后 20 s 内有效。同一架无人机连续投放两枚干扰弹的时间间隔不得小于 1 s。

## 1.2 五个子问题

1. **问题一：** FY1 以 120 m/s 朝假目标方向飞行，接令后 1.5 s 投放 1 枚干扰弹，投放后 3.6 s 起爆，计算对 M1 的有效遮蔽时长。
2. **问题二：** 优化 FY1 的航向、速度、投放点和起爆点，使单枚干扰弹对 M1 的有效遮蔽时长最大。
3. **问题三：** FY1 投放 3 枚干扰弹干扰 M1，设计统一航向、速度及三枚弹的投放和起爆方案。
4. **问题四：** FY1、FY2、FY3 各投放 1 枚干扰弹干扰 M1，设计三机协同方案。
5. **问题五：** 五架无人机每架至多投放 3 枚干扰弹，对 M1、M2、M3 实施干扰，设计任务分配和投放方案。

## 1.3 子问题递进关系

五问由固定策略逐步扩展到连续参数优化、多弹时序协同、多机空间协同和多目标资源分配。其公共基础为：

- 三维运动学轨迹；
- 烟幕球与导弹—目标视线的几何关系；
- 连续时间有效区间；
- 多枚烟幕区间并集；
- 无人机速度、固定航向、投弹间隔和起爆高度约束。

---

# 2 模型假设与符号说明

## 2.1 模型假设

本文使用已通过人工模型冻结闸门确认的假设。

1. 导弹视为质点，在到达假目标原点之前保持题面给定的匀速直线运动。
2. 无人机在 \(t=0\) 瞬时完成一次转向，随后保持固定水平航向、速度和高度。
3. 干扰弹释放瞬间继承无人机的水平速度，初始竖直速度为 0。
4. 起爆前忽略空气阻力，重力加速度取
   \[
   g=9.8\ \mathrm{m/s^2}.
   \]
5. 烟幕起爆后不保留无人机或干扰弹的水平速度，不考虑风场，仅以 3 m/s 竖直下沉。
6. 干扰弹只允许在地面以上起爆。
7. 烟幕中心到达地面后停止计入有效遮蔽。
8. 真目标采用圆柱体代表点集近似；全部代表点对应视线均被遮挡时才判定为有效遮蔽。
9. 同一导弹受到多枚烟幕弹干扰时，有效时间按区间并集统计，重叠部分不重复累计。
10. 问题五中每枚已使用干扰弹登记一个主目标导弹，并只向该主目标贡献正式目标值。
11. 问题五采用字典序目标：先最大化三枚导弹总遮蔽时长，再最大化三者中的最短遮蔽时长。
12. 问题五要求 M1、M2、M3 均获得正有效遮蔽时长。
13. 未使用弹位内部标记为 `is_used=0`，官方模板中的待计算字段留空。

## 2.2 主要符号

| 符号 | 含义 |
|---|---|
| \(i\in\mathcal U\) | 无人机编号 |
| \(j\in\mathcal M\) | 导弹编号 |
| \(k\) | 同一无人机的干扰弹编号 |
| \(\mathbf m_{j0}\) | 导弹 \(j\) 的初始位置 |
| \(\mathbf u_{i0}\) | 无人机 \(i\) 的初始位置 |
| \(v_M\) | 导弹速度，取 300 m/s |
| \(v_i\) | 无人机 \(i\) 的速度 |
| \(\theta_i\) | 无人机 \(i\) 的水平航向角 |
| \(r_{ik}\) | 干扰弹投放时刻 |
| \(\tau_{ik}\) | 投放至起爆的延迟 |
| \(d_{ik}=r_{ik}+\tau_{ik}\) | 起爆时刻 |
| \(\mathbf m_j(t)\) | 导弹位置 |
| \(\mathbf u_i(t)\) | 无人机位置 |
| \(\mathbf b_{ik}(t)\) | 起爆前干扰弹位置 |
| \(\mathbf c_{ik}(t)\) | 起爆后烟幕中心位置 |
| \(R_s\) | 烟幕有效半径，取 10 m |
| \(T_s\) | 烟幕物理有效期，取 20 s |
| \(w_s\) | 烟幕下沉速度，取 3 m/s |
| \(\mathcal I_{ikj}\) | 单枚烟幕对导弹 \(j\) 的有效时间集合 |
| \(T_j\) | 导弹 \(j\) 的总有效遮蔽时长 |
| \(y_{ik}\) | 弹位 \(ik\) 的使用指示变量；使用时为 1，否则为 0 |

## 2.3 初始位置

### 导弹初始位置

| 导弹 | 初始坐标 \((x,y,z)\)/m |
|---|---|
| M1 | \((20000,0,2000)\) |
| M2 | \((19000,600,2100)\) |
| M3 | \((18000,-600,1900)\) |

### 无人机初始位置

| 无人机 | 初始坐标 \((x,y,z)\)/m |
|---|---|
| FY1 | \((17800,0,1800)\) |
| FY2 | \((12000,1400,1400)\) |
| FY3 | \((6000,-3000,700)\) |
| FY4 | \((11000,2000,1800)\) |
| FY5 | \((13000,-2000,1300)\) |

---

# 3 三维运动学模型

## 3.1 导弹轨迹

导弹 \(j\) 从初始位置 \(\mathbf m_{j0}\) 指向原点，其单位方向向量为

\[
\mathbf e_{Mj}
=
-\frac{\mathbf m_{j0}}{\|\mathbf m_{j0}\|}.
\]

导弹速度向量为

\[
\mathbf v_{Mj}
=
300\mathbf e_{Mj}.
\]

因此导弹轨迹为

\[
\mathbf m_j(t)
=
\mathbf m_{j0}
+
300\mathbf e_{Mj}t,
\qquad
0\le t\le t_j^{\mathrm{hit}},
\]

其中导弹到达假目标原点的时刻为

\[
t_j^{\mathrm{hit}}
=
\frac{\|\mathbf m_{j0}\|}{300}.
\]

导弹到达原点后不再参与有效遮蔽评价。

## 3.2 无人机轨迹

无人机 \(i\) 的水平单位方向向量为

\[
\mathbf e_i(\theta_i)
=
(\cos\theta_i,\sin\theta_i,0)^{\mathsf T}.
\]

无人机轨迹为

\[
\mathbf u_i(t)
=
\mathbf u_{i0}
+
v_i\mathbf e_i(\theta_i)t,
\]

并满足

\[
70\le v_i\le 140,
\qquad
0\le\theta_i<2\pi.
\]

内部计算使用弧度，官方模板输出角度，以 \(x\) 轴正方向为 \(0^\circ\)，逆时针为正。

## 3.3 干扰弹起爆前轨迹

干扰弹 \(k\) 在 \(r_{ik}\) 时刻由无人机 \(i\) 投放。由于干扰弹继承无人机水平速度且初始竖直速度为 0，对

\[
r_{ik}\le t\le d_{ik}
\]

有

\[
\mathbf b_{ik}(t)
=
\mathbf u_i(r_{ik})
+
v_i\mathbf e_i(\theta_i)(t-r_{ik})
-
\frac12 g(t-r_{ik})^2\mathbf e_z,
\]

其中

\[
\mathbf e_z=(0,0,1)^{\mathsf T}.
\]

由于无人机和干扰弹的水平速度相同，上式可写为

\[
\mathbf b_{ik}(t)
=
\mathbf u_{i0}
+
v_i\mathbf e_i(\theta_i)t
-
\frac12 g(t-r_{ik})^2\mathbf e_z.
\]

投放点为

\[
\mathbf p_{ik}^{\mathrm{rel}}
=
\mathbf u_i(r_{ik}),
\]

起爆点为

\[
\mathbf p_{ik}^{\mathrm{det}}
=
\mathbf b_{ik}(d_{ik})
=
\mathbf u_{i0}
+
v_i\mathbf e_i(\theta_i)d_{ik}
-
\frac12g\tau_{ik}^2\mathbf e_z.
\]

起爆高度约束为

\[
z_{i0}
-
\frac12g\tau_{ik}^2
\ge 0.
\]

因此，起爆延迟的物理上界为

\[
0\le\tau_{ik}
\le
\sqrt{\frac{2z_{i0}}{g}}.
\]

问题二至问题五不使用问题一的固定 3.6 s 起爆延迟。

## 3.4 烟幕云团轨迹

烟幕在 \(d_{ik}\) 时刻瞬时形成。起爆后烟幕中心轨迹为

\[
\mathbf c_{ik}(t)
=
\mathbf p_{ik}^{\mathrm{det}}
-
3(t-d_{ik})\mathbf e_z.
\]

烟幕的物理有效终点为

\[
t_{ik}^{\mathrm{end}}
=
\min\left(
d_{ik}+20,\,
d_{ik}+\frac{z_{ik}^{\mathrm{det}}}{3}
\right).
\]

对目标导弹 \(j\)，实际评价窗口还需截断于导弹到达假目标原点的时刻：

\[
\mathcal W_{ikj}
=
\left[
d_{ik},
\min\left(t_{ik}^{\mathrm{end}},t_j^{\mathrm{hit}}\right)
\right].
\]

---

# 4 真目标与有效遮蔽模型

## 4.1 真目标圆柱体

真目标定义为

\[
\mathcal C_T
=
\left\{
(x,y,z):
x^2+(y-200)^2\le 7^2,\,
0\le z\le 10
\right\}.
\]

为兼顾几何完整性与数值可计算性，使用侧面、顶面和底面的确定性代表点集

\[
\mathcal S
=
\mathcal S_{\mathrm{side}}
\cup
\mathcal S_{\mathrm{top}}
\cup
\mathcal S_{\mathrm{bottom}}.
\]

代表点密度属于数值分辨率，不改变圆柱目标的物理含义。冻结复算使用更密的代表点配置和更严格的时间边界定位。

## 4.2 单条视线遮挡判据

对导弹位置 \(\mathbf m_j(t)\)、目标代表点 \(\mathbf q\) 与烟幕中心 \(\mathbf c_{ik}(t)\)，定义

\[
\mathbf a_{jq}(t)
=
\mathbf q-\mathbf m_j(t),
\]

\[
\mathbf h_{ikj}(t)
=
\mathbf c_{ik}(t)-\mathbf m_j(t).
\]

烟幕中心在导弹—目标视线方向上的投影参数为

\[
\lambda_{ikjq}(t)
=
\frac{
\mathbf h_{ikj}(t)^{\mathsf T}
\mathbf a_{jq}(t)
}{
\|\mathbf a_{jq}(t)\|^2
}.
\]

烟幕中心到该视线的垂直距离为

\[
\delta_{ikjq}(t)
=
\left\|
\mathbf h_{ikj}(t)
-
\lambda_{ikjq}(t)\mathbf a_{jq}(t)
\right\|.
\]

目标点 \(\mathbf q\) 被烟幕遮挡，当且仅当

\[
0\le\lambda_{ikjq}(t)\le 1,
\]

且

\[
\delta_{ikjq}(t)\le 10.
\]

投影参数约束保证烟幕位于导弹与目标点之间，而不是位于视线延长线上。

## 4.3 全圆柱代表点判据

主模型要求全部目标代表点均被遮挡。定义指示函数

\[
\chi_{ikj}(t)
=
\prod_{\mathbf q\in\mathcal S}
\mathbf 1
\left[
0\le\lambda_{ikjq}(t)\le 1
\ \land\
\delta_{ikjq}(t)\le10
\right].
\]

当

\[
\chi_{ikj}(t)=1
\]

时，烟幕弹 \(ik\) 在时刻 \(t\) 对导弹 \(j\) 形成有效遮蔽。

单枚烟幕的有效时间集合为

\[
\mathcal I_{ikj}
=
\left\{
t\in\mathcal W_{ikj}:
\chi_{ikj}(t)=1
\right\}.
\]

其有效时长为

\[
D_{ikj}
=
\mu(\mathcal I_{ikj}),
\]

其中 \(\mu(\cdot)\) 为时间集合长度。

## 4.4 多枚烟幕的区间并集

同一导弹的多枚烟幕有效区间可能重叠。令 \(y_{ik}=1\) 表示弹位 \(ik\) 被实际使用；仅对已使用弹位求并集。为避免重复累计，定义

\[
\mathcal U_j
=
\bigcup_{i,k:\,y_{ik}=1}
\mathcal I_{ikj},
\]

总有效遮蔽时长为

\[
T_j
=
\mu(\mathcal U_j).
\]

正式评价采用初始扫描、边界区段识别和数值求根相结合的方法定位连续时间边界；固定时间步长只用于基线对照。

---

# 5 优化模型与求解方法

## 5.1 问题一：固定策略评价

问题一不进行优化。固定参数为

\[
\theta_1=180^\circ,
\qquad
v_1=120\ \mathrm{m/s},
\]

\[
r_{11}=1.5\ \mathrm{s},
\qquad
\tau_{11}=3.6\ \mathrm{s},
\]

\[
d_{11}=5.1\ \mathrm{s}.
\]

依次计算无人机轨迹、投放点、起爆点、烟幕轨迹和有效遮蔽区间。

## 5.2 问题二：单机单弹优化

问题二的决策变量为

\[
\mathbf z_2
=
(\theta_1,v_1,r_{11},\tau_{11}).
\]

目标函数为

\[
\max_{\mathbf z_2}
D_{11,\mathrm{M1}}.
\]

约束包括：

\[
0\le\theta_1<2\pi,
\]

\[
70\le v_1\le140,
\]

\[
r_{11}\ge0,
\qquad
\tau_{11}\ge0,
\]

\[
z_{11}^{\mathrm{det}}\ge0,
\qquad
d_{11}\le t_{\mathrm{M1}}^{\mathrm{hit}}.
\]

由于目标函数包含布尔遮挡判定和区间边界，具有非凸、非光滑和多峰特征，本文采用差分进化进行全局搜索。差分进化由 Storn 和 Price 提出，是一类面向连续空间的随机启发式全局优化方法，可处理非线性和不可微目标[1]。随后使用 Powell 无导数方向集方法对候选方案进行局部精修；该方法通过函数值构造搜索方向，不要求显式梯度[2]。

## 5.3 问题三：单机三弹联合优化

问题三的决策变量为

\[
\mathbf z_3
=
\left(
\theta_1,v_1,
r_{11},r_{12},r_{13},
\tau_{11},\tau_{12},\tau_{13}
\right).
\]

三枚弹共享同一航向和速度，并满足

\[
r_{12}-r_{11}\ge1,
\]

\[
r_{13}-r_{12}\ge1.
\]

目标函数为

\[
\max
\mu\left(
\mathcal I_{11,\mathrm{M1}}
\cup
\mathcal I_{12,\mathrm{M1}}
\cup
\mathcal I_{13,\mathrm{M1}}
\right).
\]

为减少不可行候选，可采用有序参数化：

\[
r_{11}=s_1,
\]

\[
r_{12}=s_1+1+\delta_2,
\]

\[
r_{13}=s_1+2+\delta_2+\delta_3,
\]

其中

\[
s_1,\delta_2,\delta_3\ge0.
\]

## 5.4 问题四：三机各一弹联合优化

FY1、FY2、FY3 各投放一枚弹，各自具有独立的航向、速度、投放时刻和起爆延迟。目标函数为

\[
\max
\mu\left(
\mathcal I_{\mathrm{FY1},1,\mathrm{M1}}
\cup
\mathcal I_{\mathrm{FY2},1,\mathrm{M1}}
\cup
\mathcal I_{\mathrm{FY3},1,\mathrm{M1}}
\right).
\]

由于每架无人机仅投放一枚弹，不存在同机投弹间隔约束。

## 5.5 问题五：多目标分层优化

定义二元变量

\[
y_{ik}
=
\begin{cases}
1,& \text{弹位 }ik\text{ 被使用},\\
0,& \text{否则},
\end{cases}
\]

以及主目标分配变量

\[
x_{ikj}
=
\begin{cases}
1,& \text{弹位 }ik\text{ 分配给导弹 }j,\\
0,& \text{否则}.
\end{cases}
\]

每枚已使用弹只登记一个主目标：

\[
\sum_{j\in\mathcal M}x_{ikj}=y_{ik}.
\]

弹位按编号前缀使用：

\[
y_{i,k+1}\le y_{ik}.
\]

问题五的一级目标为

\[
F_{\mathrm{sum}}
=
T_{\mathrm{M1}}
+
T_{\mathrm{M2}}
+
T_{\mathrm{M3}},
\]

二级目标为

\[
F_{\min}
=
\min\left(
T_{\mathrm{M1}},
T_{\mathrm{M2}},
T_{\mathrm{M3}}
\right).
\]

采用严格字典序优化。设全部可行方案构成集合 \(\Omega\)，先计算

\[
F_{\mathrm{sum}}^{*}
=
\max_{\mathbf z\in\Omega}
F_{\mathrm{sum}}(\mathbf z),
\]

再在一级目标严格等于 \(F_{\mathrm{sum}}^{*}\) 的可行解集合上求

\[
\max_{\substack{\mathbf z\in\Omega\\
F_{\mathrm{sum}}(\mathbf z)=F_{\mathrm{sum}}^{*}}}
F_{\min}(\mathbf z).
\]

因此，二级目标只用于比较一级目标同为最优值的方案，不引入任何未冻结的近优容差。

同时要求

\[
T_{\mathrm{M1}}>0,
\qquad
T_{\mathrm{M2}}>0,
\qquad
T_{\mathrm{M3}}>0.
\]

求解过程先生成离散任务分配候选，再对给定分配的连续航向、速度、投放时刻和起爆延迟进行优化，最后统一复算三枚导弹的有效区间。

---

# 6 结果与分析

本章所有数值均来自冻结目录 `07_results/frozen/`，冻结包 ID 为 `RF-20260722T114756Z`。

## 6.1 问题一结果

FY1 朝假目标方向飞行，航向角为 \(180^\circ\)，速度为 120 m/s。投放时刻和起爆延迟分别为 1.5 s 和 3.6 s。

投放点为

\[
(17620.0,\ 0.0,\ 1800.0)\ \mathrm{m},
\]

起爆点为

\[
(17188.0,\ 0.0,\ 1736.496)\ \mathrm{m}.
\]

有效遮蔽区间为

\[
[8.056308984756512,\ 9.4185104846955]\ \mathrm{s},
\]

因此有效遮蔽时长为

\[
\boxed{
T_{\mathrm{Q1}}
=
1.3622014999389869\ \mathrm{s}
}.
\]

该结果是题面固定方案的计算值，不是优化结果。

![图1 Q1固定策略三维轨迹](../08_figures/main_figures/F2_q1_trajectory.png)

**图1 数据来源：** `07_results/frozen/q1_results.csv`，来源记录 `Q1/M1`。

## 6.2 问题二结果

问题二的冻结方案如下。

| 参数 | 冻结值 |
|---|---:|
| 航向角/(°) | 179.43654517246082 |
| 速度/(m/s) | 130.08336768519578 |
| 投放时刻/s | 2.838973088474825 |
| 起爆延迟/s | 4.978182512298204 |
| 起爆时刻/s | 7.817155600773029 |
| 投放点 \(x\)/m | 17430.714677459066 |
| 投放点 \(y\)/m | 3.631721349123526 |
| 投放点 \(z\)/m | 1800.0 |
| 起爆点 \(x\)/m | 16783.16724483817 |
| 起爆点 \(y\)/m | 9.999999999999895 |
| 起爆点 \(z\)/m | 1678.5667244838169 |

有效遮蔽区间为

\[
[7.817155600773029,\ 10.055319977985587]\ \mathrm{s},
\]

有效遮蔽时长为

\[
\boxed{
T_{\mathrm{Q2}}
=
2.2381643772125575\ \mathrm{s}
}.
\]

相较问题一，绝对增加量为

\[
\Delta T
=
2.2381643772125575
-
1.3622014999389869
=
0.8759628772735706\ \mathrm{s}.
\]

相对增加量为

\[
\eta
=
\frac{0.8759628772735706}
{1.3622014999389869}
\times100\%
\approx64.3049\%.
\]

因此，在冻结模型口径下，问题二求解方案使单弹有效遮蔽时长较问题一固定方案增加约 64.30%。该表述仅表示冻结求解结果的比较，不构成全局最优性的数学证明。

![图2 Q1与Q2有效遮蔽区间对比](../08_figures/main_figures/F3_q1_q2_intervals.png)

**图2 数据来源：** `07_results/frozen/q1_results.csv`、`07_results/frozen/q2_results.csv`。

## 6.3 问题三结果

问题三中 FY1 的三枚干扰弹共享：

\[
\theta_1
=
179.43654517246082^\circ,
\]

\[
v_1
=
130.08336768519578\ \mathrm{m/s}.
\]

逐弹结果如下。

| 弹号 | 投放时刻/s | 起爆时刻/s | 起爆点/m | 有效区间/s | 单弹时长/s |
|---:|---:|---:|---|---|---:|
| 1 | 2.838973088474825 | 7.817155600773029 | \((16783.16724483817,9.999999999999895,1678.5667244838169)\) | \([7.817155600773029,10.055319977985587]\) | 2.2381643772125575 |
| 2 | 3.838973088474825 | 8.81715560077303 | \((16653.09016730612,11.279237680648212,1678.5667244838169)\) | 空 | 0 |
| 3 | 4.838973088474825 | 9.81715560077303 | \((16523.013089774075,12.55847536129653,1678.5667244838169)\) | 空 | 0 |

三枚弹的有效区间并集为

\[
[7.817155600773029,\ 10.055319977985587]\ \mathrm{s},
\]

因此

\[
\boxed{
T_{\mathrm{Q3}}
=
2.2381643772125575\ \mathrm{s}
}.
\]

冻结结果表明，第 2、3 枚弹虽然按照方案完成投放，但未形成有效遮蔽区间，故问题三的总体并集完全由第 1 枚弹贡献。问题三与问题二的主指标相同，当前冻结方案未显示额外多弹协同收益。

![图3 Q3三弹有效区间分解](../08_figures/main_figures/F4_q3_bomb_intervals.png)

**图3 数据来源：** `07_results/frozen/q3_results.csv`、`07_results/frozen/result1.xlsx`。

## 6.4 问题四结果

问题四中 FY1、FY2、FY3 各投放一枚干扰弹。逐机结果如下。

| 无人机 | 航向角/(°) | 速度/(m/s) | 有效区间/s | 单弹时长/s |
|---|---:|---:|---|---:|
| FY1 | 179.43654517246082 | 130.08336768519578 | \([7.817155600773029,10.055319977985587]\) | 2.2381643772125575 |
| FY2 | 180.0 | 120.0 | 空 | 0 |
| FY3 | 180.0 | 120.0 | 空 | 0 |

三机总体有效区间并集为

\[
[7.817155600773029,\ 10.055319977985587]\ \mathrm{s},
\]

因此

\[
\boxed{
T_{\mathrm{Q4}}
=
2.2381643772125575\ \mathrm{s}
}.
\]

FY2 和 FY3 的烟幕未形成有效区间，故问题四的总体遮蔽由 FY1 单独贡献。问题四与问题二、问题三具有相同主指标，当前冻结方案未显示新增多机协同收益。

![图4 Q4三机有效区间分解](../08_figures/main_figures/F5_q4_uav_intervals.png)

**图4 数据来源：** `07_results/frozen/q4_results.csv`、`07_results/frozen/result2.xlsx`。

## 6.5 问题五结果

问题五共有 15 个潜在弹位，冻结方案实际使用 3 个弹位：

- FY1 第 1 枚弹干扰 M1；
- FY2 第 1 枚弹干扰 M2；
- FY5 第 1 枚弹干扰 M3；
- FY3、FY4 及其余弹位未使用。

### 6.5.1 分配与飞行参数

| 主目标 | 无人机 | 弹号 | 航向角/(°) | 速度/(m/s) | 投放时刻/s | 起爆延迟/s | 起爆时刻/s |
|---|---|---:|---:|---:|---:|---:|---:|
| M1 | FY1 | 1 | 179.43654517246082 | 130.08336768519578 | 2.838973088474825 | 4.978182512298204 | 7.817155600773029 |
| M2 | FY2 | 1 | 275.5970977478011 | 100.88690594525764 | 6.0857908606118745 | 3.555641037660742 | 9.641431898272616 |
| M3 | FY5 | 1 | 119.30217914169313 | 121.14131300438812 | 13.136138284985464 | 2.1695621915927563 | 15.30570047657822 |

### 6.5.2 投放点和起爆点

| 目标 | 投放点 \((x,y,z)\)/m | 起爆点 \((x,y,z)\)/m |
|---|---|---|
| M1 | \((17430.714677459066,3.631721349123526,1800.0)\) | \((16783.16724483817,9.999999999999895,1678.5667244838169)\) |
| M2 | \((12059.882666072617,788.9506205518344,1400.0)\) | \((12094.869288158236,431.94324067868115,1338.051342375384)\) |
| M3 | \((12221.178713062363,-612.2804622520769,1300.0)\) | \((12092.548732051975,-383.08495773506553,1276.935699494375)\) |

### 6.5.3 分导弹有效区间

| 导弹 | 有效区间/s | 有效时长/s |
|---|---|---:|
| M1 | \([7.817155600773029,10.055319977985587]\) | 2.2381643772125575 |
| M2 | \([9.641431898272616,11.62347521225275]\) | 1.9820433139801334 |
| M3 | \([15.30570047657822,17.18250134747355]\) | 1.8768008708953303 |

一级目标为

\[
F_{\mathrm{sum}}
=
2.2381643772125575
+
1.9820433139801334
+
1.8768008708953303
=
\boxed{
6.097008562088021\ \mathrm{s}
}.
\]

二级目标为

\[
F_{\min}
=
\min
\left(
2.2381643772125575,
1.9820433139801334,
1.8768008708953303
\right)
=
\boxed{
1.8768008708953303\ \mathrm{s}
}.
\]

三枚导弹在总时长中的占比分别约为 36.71%、32.51% 和 30.78%。最短时长约为最长时长的 83.85%，最长与最短时长之差为 0.36136350631722713 s。

![图5 Q5无人机—导弹任务分配](../08_figures/main_figures/F6_q5_assignment.png)

![图6 Q5三枚导弹有效遮蔽时间轴](../08_figures/main_figures/F7_q5_missile_intervals.png)

**图5—图6 数据来源：** `07_results/frozen/q5_results.csv`、`07_results/frozen/metrics_summary.csv`、`07_results/frozen/result3.xlsx`。

## 6.6 五问主指标对比

| 问题 | 主指标/s |
|---|---:|
| Q1 | 1.3622014999389869 |
| Q2 | 2.2381643772125575 |
| Q3 | 2.2381643772125575 |
| Q4 | 2.2381643772125575 |

Q2 相对 Q1 产生了明显增加，而 Q3、Q4 与 Q2 相同。该结果不应被解释为多弹或多机策略必然无效，只能说明当前冻结模型与冻结求解结果没有找到新增有效区间。

![图7 Q1—Q4主指标对比](../08_figures/main_figures/F8_q1_q4_metrics.png)

---

# 7 模型检验与敏感性分析

## 7.1 硬约束与模板映射

冻结核验记录显示：

- 无人机速度均满足 70—140 m/s；
- 所有已使用干扰弹均在地面以上起爆；
- 同机多弹航向和速度一致；
- 相邻投放间隔不小于 1 s；
- 问题五使用弹位满足前缀约束；
- M1、M2、M3 的主目标时长均为正；
- 三份官方模板映射检查状态为 `pass`；
- 映射失败数为 0；
- 未使用弹位保持空白。

因此，冻结结果与模型约束及官方模板结构一致。

## 7.2 随机种子稳定性

冻结验证使用三个随机种子，对各问题输出进行复算。每个输出指标的跨度为 0，低于预设稳定性容差 0.05 s。

因此可表述为：

> 在所检验的三个随机种子范围内，冻结主指标保持稳定。

该结论不能推广为：

- 对任意随机种子均稳定；
- 已证明搜索到全局最优；
- 不存在其他近优或更优方案。

## 7.3 主模型与中心点基线

| 结果 | 主模型/s | 中心点基线/s | 差值（基线－主模型）/s |
|---|---:|---:|---:|
| Q1/M1 | 1.3622014999389869 | 1.4055095672607685 | 0.0433080673217816 |
| Q2/M1 | 2.2381643772125575 | 2.2621874332428344 | 0.0240230560302769 |
| Q5/M1 | 2.2381643772125575 | 2.2621874332428344 | 0.0240230560302769 |
| Q5/M2 | 1.9820433139801334 | 2.4308256626129516 | 0.4487823486328182 |
| Q5/M3 | 1.8768008708953303 | 1.9770526409148559 | 0.1002517700195256 |

中心点基线只要求烟幕遮挡真目标几何中心，其判据比全代表点遮挡更宽松，因此基线时长普遍较大。该比较说明保留圆柱几何会改变评价结果，不能用中心点基线的较大数值证明其“更优”。

## 7.4 固定时间格点基线

| 结果 | 主模型/s | 固定格点基线/s |
|---|---:|---:|
| Q1/M1 | 1.3622014999389869 | 1.25 |
| Q2/M1 | 2.2381643772125575 | 2.25 |
| Q5/M1 | 2.2381643772125575 | 2.25 |
| Q5/M2 | 1.9820433139801334 | 2.0 |
| Q5/M3 | 1.8768008708953303 | 2.0 |

固定时间步长对不同结果可能产生高估或低估，其误差方向并不一致。因此，正式模型使用连续边界细化而不是直接按固定格点累计。

![图8 主模型与基线对比](../08_figures/main_figures/F9_model_baselines.png)

## 7.5 A03：水平速度继承敏感性

将干扰弹初速度改为“不继承无人机水平速度”后，当前冻结计划在 Q1—Q5 中的主目标时长均变为 0。

这表明：

- 当前冻结方案对 A03 高度敏感；
- 水平速度继承决定了起爆点的水平位置；
- 取消该假设会使现有计划的烟幕无法到达有效视线附近。

但该对照只复算当前冻结计划，不能据此断言“不继承水平速度的模型中不存在其他可行策略”。

## 7.6 A07：地面边界敏感性

将烟幕到达地面后的处理方式由“终止”改为“停留”后，当前主指标和区间未发生变化。这说明当前有效区间均在烟幕中心到达地面之前结束，因此本组冻结计划对该边界不敏感。

该结论仅适用于当前计划，不代表所有潜在策略均不受地面边界影响。

## 7.7 A08：遮挡覆盖口径敏感性

将全代表点遮挡放宽为 80% 代表点覆盖后，结果如下。

| 结果 | 主模型/s | 80% 覆盖率/s | 增加量/s | 相对变化 |
|---|---:|---:|---:|---:|
| Q1/M1 | 1.3622014999389869 | 1.3799813270569068 | 0.0177798271179199 | 约 1.31% |
| Q2/M1 | 2.2381643772125575 | 2.2513085842132856 | 0.0131442070007281 | 约 0.59% |
| Q5/M1 | 2.2381643772125575 | 2.2513085842132856 | 0.0131442070007281 | 约 0.59% |
| Q5/M2 | 1.9820433139801334 | 2.214444398880035 | 0.2324010848999016 | 约 11.73% |
| Q5/M3 | 1.8768008708953303 | 1.9317597866057739 | 0.0549589157104436 | 约 2.93% |

M2 对遮挡覆盖口径最敏感，说明不同导弹的空间几何关系会导致判据放宽产生不同影响。正式结果仍采用冻结的全代表点遮挡口径。

![图9 A08遮挡口径敏感性](../08_figures/main_figures/F10_a08_sensitivity.png)

## 7.8 A11 与 A12：问题五目标口径敏感性

冻结核验报告表明：

- 将问题五改为公平性优先会改变任务分配；
- 取消“三枚导弹均须获得正时长”的约束，不会改变总时长优先口径下的当前分配。

因此，问题五的最终资源配置对 A11 的目标优先级具有实质敏感性，而当前分配对 A12 约束的取消不敏感。由于当前交接未展示公平优先方案的完整逐弹参数，本文仅报告“分配发生变化”，不虚构替代方案数值。

---

# 8 模型评价

## 8.1 模型优点

1. **运动过程可解释。**  
   导弹、无人机、干扰弹和烟幕云团均有明确轨迹公式，投放点和起爆点可由决策变量复算。

2. **保留真实目标几何。**  
   目标没有被直接简化为中心点，而是保留圆柱体并采用多视线判据。

3. **多弹时长计量严谨。**  
   对同一导弹的多枚烟幕区间求并集，避免重叠时间重复累计。

4. **适用于五个子问题。**  
   同一模型框架能够覆盖固定策略、连续优化、多弹、多机和多目标任务分配。

5. **结果可追溯。**  
   所有正式数字均绑定冻结包、来源记录和官方模板映射。

6. **不隐藏零贡献结果。**  
   问题三中的第 2、3 枚弹和问题四中的 FY2、FY3 均保留 0 s 记录，使论证更可信。

## 8.2 模型局限

1. **高度依赖 A03。**  
   当前计划在取消水平速度继承后全部失效，说明该假设对结果具有决定性影响。

2. **忽略空气阻力和风。**  
   实际干扰弹弹道和烟幕漂移可能受空气动力和风场影响。

3. **全代表点判据较严格。**  
   覆盖比例敏感性表明，遮挡定义会显著改变部分导弹的评价结果。

4. **数值优化不能证明全局最优。**  
   多随机种子稳定和预算加密只能说明在测试范围内稳定，不能构成理论最优性证明。

5. **问题三和问题四未显示新增协同收益。**  
   当前冻结方案中的额外弹或无人机未产生正有效时长，可能与可达性、严格遮挡判据或搜索结构有关。

6. **问题五对目标优先级敏感。**  
   公平优先会改变任务分配，说明多目标聚合方式直接影响工程决策。

---

# 9 结论

本文建立了面向烟幕干扰弹投放问题的三维运动学和多视线遮挡统一模型，并使用连续时间区间并集衡量有效遮蔽时长。

1. 问题一固定方案的有效遮蔽时长为
   \[
   1.3622014999389869\ \mathrm{s}.
   \]

2. 问题二冻结方案的有效遮蔽时长为
   \[
   2.2381643772125575\ \mathrm{s},
   \]
   相较问题一增加
   \[
   0.8759628772735706\ \mathrm{s},
   \]
   相对增加约 64.3049%。

3. 问题三的三弹并集时长为
   \[
   2.2381643772125575\ \mathrm{s}.
   \]
   第 2、3 枚弹未形成有效区间，因此未观察到额外多弹收益。

4. 问题四的三机并集时长为
   \[
   2.2381643772125575\ \mathrm{s}.
   \]
   FY2 和 FY3 未形成有效区间，因此未观察到额外多机收益。

5. 问题五实际使用 FY1、FY2、FY5 的第 1 枚弹，分别干扰 M1、M2、M3。三枚导弹的时长为
   \[
   2.2381643772125575\ \mathrm{s},
   \]
   \[
   1.9820433139801334\ \mathrm{s},
   \]
   \[
   1.8768008708953303\ \mathrm{s}.
   \]
   总时长为
   \[
   6.097008562088021\ \mathrm{s},
   \]
   最短时长为
   \[
   1.8768008708953303\ \mathrm{s}.
   \]

6. 结果在所检验的三个随机种子下输出跨度为 0，模板映射检查通过。敏感性分析表明，A03 对当前方案具有决定性影响，A11 会改变问题五任务分配，而 A07 未改变当前有效区间。

本文的冻结结果可作为当前模型口径下的正式提交依据，但不将黑箱数值优化结果表述为全局最优的理论证明。

---

# 10 参考文献

[1] STORN R, PRICE K. Differential Evolution—A Simple and Efficient Heuristic for Global Optimization over Continuous Spaces[J]. *Journal of Global Optimization*, 1997, 11(4): 341-359. DOI: 10.1023/A:1008202821328.

[2] POWELL M J D. An Efficient Method for Finding the Minimum of a Function of Several Variables without Calculating Derivatives[J]. *The Computer Journal*, 1964, 7(2): 155-162. DOI: 10.1093/comjnl/7.2.155.

---

# 11 引用合同登记

## 11.1 citation_contract 数据行

以下数据行用于同步登记至项目的 `citation_contract`。引用只支持求解方法的来源说明，不用于证明本文数值结果或全局最优性。

```csv
citation_id,reference_no,authors,title,venue,year,volume,issue,pages,doi,metadata_verified,personally_read,read_scope,support_grade,supported_claim,used_in_sections,status
CIT001,1,"Rainer Storn; Kenneth Price","Differential Evolution—A Simple and Efficient Heuristic for Global Optimization over Continuous Spaces","Journal of Global Optimization",1997,11,4,"341-359","10.1023/A:1008202821328",true,true,"title; abstract; bibliographic metadata",method_support,"差分进化是面向连续空间的随机启发式全局优化方法，可用于非线性和不可微目标","摘要;5.2",registered_in_draft
CIT002,2,"M. J. D. Powell","An Efficient Method for Finding the Minimum of a Function of Several Variables without Calculating Derivatives","The Computer Journal",1964,7,2,"155-162","10.1093/comjnl/7.2.155",true,true,"title; abstract; bibliographic metadata",method_support,"Powell 方法是不要求显式梯度的无导数方向集局部优化方法","摘要;5.2",registered_in_draft
```

## 11.2 引用边界

- 两篇文献均为优化算法原始来源，不是历史竞赛论文；
- 本文未复制两篇文献的正文，只对其方法用途作概括；
- `personally_read=true` 的阅读范围已在 `read_scope` 中如实限定为题名、摘要和书目信息；
- 引用不支持“本文已经证明获得全局最优”这一论断；
- 冻结数值仍由项目结果合同和冻结包提供，不由外部文献提供。

---

# 12 结果合同与证据来源

## 12.1 冻结信息

| 字段 | 内容 |
|---|---|
| freeze_id | `RF-20260722T114756Z` |
| result_status | `frozen` |
| human_gate | `result_freeze_gate` |
| human_gate_status | `confirmed` |
| 模板映射状态 | `pass` |
| 模板映射失败数 | 0 |

## 12.2 数值来源

| 论文内容 | 来源文件 | 来源记录 |
|---|---|---|
| 问题一 | `07_results/frozen/q1_results.csv` | Q1/M1 |
| 问题二 | `07_results/frozen/q2_results.csv` | Q2/M1 |
| 问题三 | `07_results/frozen/q3_results.csv` | Q3/M1 |
| 问题四 | `07_results/frozen/q4_results.csv` | Q4/M1 |
| 问题五 M1 | `07_results/frozen/q5_results.csv` | Q5/M1 |
| 问题五 M2 | `07_results/frozen/q5_results.csv` | Q5/M2 |
| 问题五 M3 | `07_results/frozen/q5_results.csv` | Q5/M3 |
| 主指标汇总 | `07_results/frozen/metrics_summary.csv` | Q1—Q5 |
| 官方模板 | `result1.xlsx`、`result2.xlsx`、`result3.xlsx` | 映射检查通过 |
| 基线和敏感性 | `07_results/result_freeze_validation/baseline_and_sensitivity.csv` | 对照情景 |

---

# 13 对审查与修订任务的逐项响应

## 13.1 本轮未关闭任务逐项响应

### REV-PR-001：文内引文、参考文献与 citation_contract

**完成。**

- 第 5.2 节增加了差分进化原始论文引文 `[1]` 和 Powell 方法原始论文引文 `[2]`；
- 文末新增第 10 章“参考文献”；
- 第 11 章新增两条 `citation_contract` 数据行；
- CIT001、CIT002 均满足 `metadata_verified=true`、`personally_read=true`；
- 两条记录的 `support_grade` 均为 `method_support`，不属于 `metadata_only`；
- 引用只支撑算法方法说明，不支撑冻结数值，也不支撑全局最优性。

### REV-PR-002：视线距离符号

**完成。**

第 4.2 节将垂直距离统一定义为

\[
\delta_{ikjq}(t)
=
\left\|
\mathbf h_{ikj}(t)
-
\lambda_{ikjq}(t)\mathbf a_{jq}(t)
\right\|,
\]

遮挡条件统一为

\[
0\le\lambda_{ikjq}(t)\le1,
\qquad
\delta_{ikjq}(t)\le10.
\]

第 4.3 节全代表点指示函数同步使用 \(\delta_{ikjq}(t)\)，与 FML007、FML008 一致。

### REV-PR-003：多弹区间并集的使用条件

**完成。**

第 4.4 节恢复为

\[
\mathcal U_j
=
\bigcup_{i,k:\,y_{ik}=1}
\mathcal I_{ikj},
\]

且符号表已定义 \(y_{ik}\) 为弹位使用指示变量。该表达不依赖“未使用弹自动对应空区间”的隐含约定，与 FML010 一致。

### REV-PR-004：Q5 严格字典序目标

**完成。**

第 5.5 节删除了“近优容差”表述，改为：

1. 在可行域 \(\Omega\) 上严格最大化 \(F_{\mathrm{sum}}\)，得到 \(F_{\mathrm{sum}}^{*}\)；
2. 仅在满足 \(F_{\mathrm{sum}}=F_{\mathrm{sum}}^{*}\) 的可行方案集合上最大化 \(F_{\min}\)。

该表述不包含任何未冻结容差，与 FML013 的严格字典序含义一致。

## 13.2 既有审查项保持情况

## 13.3 冻结数字

- 全文只使用 `07_results/frozen/` 中的正式数值；
- 未使用候选目录数值替换冻结结果；
- 未重新计算或修改冻结方案；
- 表格保留冻结文件中的完整数值精度。

## 13.4 公式含义

- 保持三维确定性运动学模型不变；
- 保持圆柱目标全代表点遮挡判据不变；
- 连续时间区间并集已按 FML010 显式恢复 \(y_{ik}=1\) 条件；
- 问题五字典序目标已按 FML013 改为严格两阶段表达，不含近优容差；
- 未将中心点或 80% 覆盖率替换为主模型。

## 13.5 图表标签

- 图表沿用证据设计阶段的含义；
- 所有坐标轴均明确时间、坐标或速度单位；
- 图3、图4要求保留 0 s 记录；
- 图5只绘制正式主目标分配，不绘制附带遮挡。

## 13.6 论证修订

已明确修订以下易误导表述：

1. 不将问题一称为优化结果；
2. 不将问题二称为理论全局最优；
3. 不宣称问题三存在三弹协同增益；
4. 不宣称问题四存在多机协同增益；
5. 不宣称五架无人机全部参与问题五；
6. 不将中心点基线的较大数值解释为更准确；
7. 不将 A03 对照的 0 s 推广为替代模型不存在可行解；
8. 不将随机种子稳定性表述为全局最优证明。

## 13.7 局限说明

正文已显式列出：

- A03 高敏感性；
- 空气阻力和风场缺失；
- A08 遮挡口径敏感性；
- A11 目标优先级敏感性；
- 数值优化的最优性边界；
- 问题三、问题四未获得新增有效贡献。

## 13.8 阻塞项

当前交接未提供公平优先 Q5 方案的完整逐弹参数和目标数值，因此本文只陈述：

> 公平优先对照会改变任务分配。

本文没有虚构替代分配方案，也没有对缺失数值进行推断。

---

# 附录 A 官方模板关键结果

## A.1 result1.xlsx

| 航向角/(°) | 速度/(m/s) | 弹号 | 投放点/m | 起爆点/m | 时长/s |
|---:|---:|---:|---|---|---:|
| 179.43654517246082 | 130.08336768519578 | 1 | \((17430.714677459066,3.631721349123526,1800.0)\) | \((16783.16724483817,9.999999999999895,1678.5667244838169)\) | 2.2381643772125575 |
| 179.43654517246082 | 130.08336768519578 | 2 | \((17300.637599927017,4.910959029771843,1800.0)\) | \((16653.09016730612,11.279237680648212,1678.5667244838169)\) | 0 |
| 179.43654517246082 | 130.08336768519578 | 3 | \((17170.56052239497,6.19019671042016,1800.0)\) | \((16523.013089774075,12.55847536129653,1678.5667244838169)\) | 0 |

## A.2 result2.xlsx

| 无人机 | 航向角/(°) | 速度/(m/s) | 投放点/m | 起爆点/m | 时长/s |
|---|---:|---:|---|---|---:|
| FY1 | 179.43654517246082 | 130.08336768519578 | \((17430.714677459066,3.631721349123526,1800.0)\) | \((16783.16724483817,9.999999999999895,1678.5667244838169)\) | 2.2381643772125575 |
| FY2 | 180.0 | 120.0 | \((11820.0,1400.0,1400.0)\) | \((11388.0,1400.0,1336.496)\) | 0 |
| FY3 | 180.0 | 120.0 | \((5820.0,-3000.0,700.0)\) | \((5388.0,-3000.0,636.496)\) | 0 |

## A.3 result3.xlsx 已使用弹位

| 无人机 | 航向角/(°) | 速度/(m/s) | 弹号 | 投放点/m | 起爆点/m | 时长/s | 目标 |
|---|---:|---:|---:|---|---|---:|---|
| FY1 | 179.43654517246082 | 130.08336768519578 | 1 | \((17430.714677459066,3.631721349123526,1800.0)\) | \((16783.16724483817,9.999999999999895,1678.5667244838169)\) | 2.2381643772125575 | M1 |
| FY2 | 275.5970977478011 | 100.88690594525764 | 1 | \((12059.882666072617,788.9506205518344,1400.0)\) | \((12094.869288158236,431.94324067868115,1338.051342375384)\) | 1.9820433139801334 | M2 |
| FY5 | 119.30217914169313 | 121.14131300438812 | 1 | \((12221.178713062363,-612.2804622520769,1300.0)\) | \((12092.548732051975,-383.08495773506553,1276.935699494375)\) | 1.8768008708953303 | M3 |

其余 12 个弹位均未使用，官方模板待计算字段留空。

---

# 附录 B AI 使用说明

本文结构整理、语言修订和证据映射过程中使用了人工智能辅助。人工智能未修改冻结模型、冻结数值、公式含义、官方模板字段或结果合同。所有正式数值均来自冻结包 `RF-20260722T114756Z`，模型假设和结果冻结均由工作流中的人工闸门确认。最终提交前仍应由参赛团队逐项核对正文、公式、图表文件、官方模板和引用格式。


## `09_paper/human_rewrite_log.md`

# 人工改写记录

| log_id | paper_block_id | 修改人 | 修改内容 | 修改原因 | 是否影响结论 |
|---|---|---|---|---|---|


## `09_paper/outline.md`

# 论文大纲

## 摘要

- 问题背景一句话
- 每问方法一句话
- 每问关键数值结果一句话
- 总结论与可执行建议一句话

## 问题重述

## 问题分析

- 任务本质
- 建模路线
- 每问输入输出
- 题型与模型族权重路由说明

## 模型假设

## 符号说明

## 数据处理与指标构造

## 模型建立与求解

### 问题一

- 题型：
- 模型族：
- 图文权重：
- 必备图表：

### 问题二

- 题型：
- 模型族：
- 图文权重：
- 必备图表：

### 问题三

- 题型：
- 模型族：
- 图文权重：
- 必备图表：

## 结果分析与解释

## 模型检验、敏感性与对比实验

## 模型评价与推广

## 参考文献

## 附录


## `09_paper/paper_block_map.csv`

﻿paper_block_id,section,question,problem_type,model_family,block_type,target_weight_pct,target_chars_min,target_chars_max,source_file,result_source,figure_ids,citation_anchor_ids,ai_anchor_ids,human_author,human_review_status,can_enter_final


## `09_paper/polish_diff_log.md`

# 润色差异记录

| polish_task_id | paper_block_id | 原文摘要 | 修改摘要 | 是否改意 | 人工确认 |
|---|---|---|---|---|---|


## `09_paper/polish_plan.md`

# 润色计划

## 润色目标

- 降低模板化表达。
- 统一术语。
- 提升段落衔接。
- 不改变模型、数值、引用和 AI 角标。

## 润色范围

| 章节 | 是否润色 | 风险 | 负责人 |
|---|---|---|---|


## `09_paper/polish_tasks.csv`

﻿polish_task_id,paper_block_id,section,original_text_file,polish_goal,allowed_changes,forbidden_changes,ai_anchor_id,before_summary,after_summary,human_review_status,meaning_changed,result_changed,citation_changed,final_decision


## `09_paper/section_weight_profiles.csv`

﻿model_family,default_problem_type,abstract_pct,problem_restatement_pct,analysis_pct,assumption_symbol_pct,data_processing_pct,model_building_pct,solution_pct,result_analysis_pct,validation_pct,evaluation_extension_pct,reference_appendix_pct,main_figures_target,main_tables_target,figure_text_ratio,figure_density,table_density,must_have_visuals,avoid_visuals,writing_emphasis
优化决策,优化决策型,6,7,8,8,8,20,16,14,7,4,2,7-10,4-7,0.45:0.55,高,中,技术路线图;目标约束结构图;可行域/路径图;Pareto前沿;方案对比矩阵;敏感性热力图,普通柱状图堆叠;无约束解释的结果图,目标函数和约束必须可追踪，算法步骤与结果表一一绑定
统计评价,数据评价型,6,7,8,7,13,17,10,18,8,4,2,6-9,6-10,0.42:0.58,中,高,指标体系图;权重热力图;综合得分矩阵;雷达/平行坐标;聚类热力图;排序坡度图,单一雷达图;过多柱状排名,指标含义、权重来源、评价解释和稳健性优先
预测回归,预测回归型,6,7,8,6,16,16,10,16,11,3,1,5-8,3-6,0.38:0.62,中,中,变量关系矩阵;趋势分解图;预测区间图;残差诊断组图;误差分布;特征重要性,只给拟合曲线;只报R2,数据清洗、变量解释、误差控制和外推边界要足够
机理仿真,机理仿真型,6,7,7,12,8,22,14,13,7,3,1,7-10,3-6,0.46:0.54,高,中,机制示意图;状态转移图;仿真轨迹;参数敏感性曲面;相图;情景对比图,只给公式不配机制图;只给终点结果,假设、机理推导、参数标定、仿真验证是主轴
机器学习,机器学习型,6,6,7,6,17,16,11,14,13,3,1,7-11,4-8,0.44:0.56,高,中,模型结构图;特征重要性;混淆矩阵;ROC/PR;消融实验;误差热力图;可解释性图,只贴训练曲线;只报准确率,训练流程、对比实验、泛化误差和可解释性要闭环
空间网络,综合开放型,6,7,8,7,13,17,12,16,8,4,2,7-10,3-6,0.50:0.50,高,中,空间分布图;流向图;网络社区图;路径图;桑基图;时空热力图,无地图底图说明;节点过密网络图,空间尺度、网络结构、路径逻辑和局部案例要清晰
综合集成,综合开放型,6,7,9,7,12,18,12,16,8,4,1,8-12,4-8,0.48:0.52,高,中,总框架图;模型链路图;结果摘要卡;结论矩阵;多模型对比图;风险矩阵,每问孤立无总图,必须用总框架串联各问，防止论文像三篇短文拼接


## `10_polish/polish_prompt.md`

你现在是一名统计建模论文编辑。请对我提供的论文段落进行自然化学术润色。目标是降低模板化表达和机械 AI 文风，使其更接近人工撰写的中文学术论文，但不得改变任何研究事实、统计结果和结论强度。

请按以下要求处理：

第一步：逻辑保真
逐句检查并保持以下内容不变：研究对象、样本范围、时间范围、模型方法、变量名称、机制路径、分组方式、系数方向、显著性水平、数据结果、图表编号、结论强度。所有数字、年份、变量缩写、显著性表述和限定词必须原样保留，不得自行补充或推断。

第二步：语言自然化
在不改变含义的前提下，优化句式节奏。适当拆分复杂长句，减少机械连接词和套话，避免重复句式，使表达更自然、克制、符合中文学术论文风格。不得口语化，不得加入夸张修辞，不得改写为宣传性或结论先行的表述。

第三步：学术克制
保留并尊重所有谨慎表述，如“可能”“迹象”“未通过常规显著性检验”“证据不足”“较稳定支持”“组内效应更明显”等。弱结论不得强化，方向性结果不得改写为显著结果。

特别注意：
- “方向为正但显著性不足”不能改成“显著促进”。
- “滞后释放迹象”不能改成“长期持续显著”。
- “科技投入路径较稳”不能改成“三条机制均成立”。
- “组内效应更明显”不能改成“某组显著高于另一组”。
- “候选扩展样本包含 2017 年”不能改成“主回归样本包含 2017 年”。

LaTeX 保护规则：
- 不得破坏 \label{}、\ref{}、\cite{}。
- 不得改动公式环境和公式内部变量。
- 不得改动图表编号、表格编号和交叉引用。
- 不得删除图表引用。
- 不得承诺规避任何检测。

输出格式：

【润色后文本】
……

【修改说明】
1. 说明主要语言层面的修改，不重复解释原文结论。
2. 指出是否保留了样本、模型、变量、数值和结论强度。
3. 若有无法判断之处，请明确说明。

【风险提示】
指出仍需人工核对的地方，例如数据口径、图表编号、显著性表述、参考文献、变量定义、样本年份等。


## `10_polish/polish_rules.md`

# 润色模块规则

1. 润色以“自然化学术表达”为目标，不以规避检测为目标。
2. 润色不得改变事实、变量、数值、显著性、图表编号、公式编号和结论强度。
3. 润色必须分段进行，不允许正式模式下一次性粗糙润色全文。
4. 润色前保留原文备份，润色后记录 `polish_log.csv`。
5. 润色后必须重新运行 LaTeX 编译检查。


## `11_review/code_reviewer_comments.md`

# code_reviewer 审稿意见

MVP 占位文件。审稿器只能在此写入代码审查意见；不得直接修改正式交付物。

## 待填写

- 代码可运行性：
- 可复现性：
- 输入输出一致性：
- 风险：


## `11_review/contract_validation_report.json`

{
  "stage": "paper_review",
  "generated_at": "2026-07-23T12:58:57",
  "fail_count": 5,
  "warn_count": 0,
  "issue_count": 5,
  "issues": [
    {
      "level": "fail",
      "item": "review_score_below_threshold",
      "detail": "row 2: 72.0 < 85.0",
      "path": "11_review/review_scorecard.csv"
    },
    {
      "level": "fail",
      "item": "review_fail_unclosed",
      "detail": "row 2 severity=fail status=active",
      "path": "11_review/review_scorecard.csv"
    },
    {
      "level": "fail",
      "item": "review_score_below_threshold",
      "detail": "row 5: 65.0 < 85.0",
      "path": "11_review/review_scorecard.csv"
    },
    {
      "level": "fail",
      "item": "review_score_below_threshold",
      "detail": "row 6: 0.0 < 85.0",
      "path": "11_review/review_scorecard.csv"
    },
    {
      "level": "fail",
      "item": "review_fail_unclosed",
      "detail": "row 6 severity=fail status=active",
      "path": "11_review/review_scorecard.csv"
    }
  ]
}

## `11_review/contract_validation_report.md`

# Contract validation report

- stage: paper_review
- fail_count: 5
- warn_count: 0

- [fail] review_score_below_threshold (11_review/review_scorecard.csv): row 2: 72.0 < 85.0
- [fail] review_fail_unclosed (11_review/review_scorecard.csv): row 2 severity=fail status=active
- [fail] review_score_below_threshold (11_review/review_scorecard.csv): row 5: 65.0 < 85.0
- [fail] review_score_below_threshold (11_review/review_scorecard.csv): row 6: 0.0 < 85.0
- [fail] review_fail_unclosed (11_review/review_scorecard.csv): row 6 severity=fail status=active


## `11_review/eda_stage_summary.md`

# eda stage summary

- generated_at: 2026-07-17T23:01:37
- execution_mode: deep_sequential

## Summary

已生成数据字典、数据质量报告和初步 EDA 图表。请完成 Gate 1 后再进入分问拆解。

## Human gate checklist

- [ ] Reviewed this stage's artifacts
- [ ] Confirmed no skipped stage output was created
- [ ] Logged rollback or revision needs


## `11_review/figure_reviewer_comments.md`

# figure_reviewer 审稿意见

MVP 占位文件。审稿器只能在此写入图表审查意见；不得直接修改正式交付物。

## 待填写

- 图表是否绑定结果：
- 图中文字是否为中文：
- 图表质量：
- 风险：


## `11_review/final_submission_checklist.md`

# Final submission checklist

- fail_count: 0
- warn_count: 0
- issue_count: 0

No structural gate issues found. Manual verification of data, model validity and contest formatting is still required.


## `11_review/gate_report.json`

{
  "generated_at": "2026-07-23T04:58:57+00:00",
  "fail_count": 0,
  "warn_count": 0,
  "issues": []
}


## `11_review/gate_report.md`

# Gate report v4

- fail_count: 0
- warn_count: 0

No gate invariant issues found. Human confirmation is still required at pending gates.


## `11_review/implementation_codex_report_H-EE549FF90321.json`

{
  "verdict": "pass",
  "checks": [
    {
      "id": "handoff_metadata",
      "status": "pass",
      "detail": "The imported response matches implementation handoff H-EE549FF90321 and context hash 497524d09cc6d557d1fbf0d23a76856bd37642fcc460069bbb33f79267442442."
    },
    {
      "id": "human_freeze_sync",
      "status": "pass",
      "detail": "The controller contains the model_freeze_gate human_gate_confirmed event. model_route.md and assumptions.csv now mirror that controller fact without changing the frozen model content."
    },
    {
      "id": "frozen_model_implementation",
      "status": "pass",
      "detail": "06_code implements fixed-time Q1, 3D missile/UAV/bomb/smoke motion, all-representative-point line-segment occlusion, scan-and-boundary interval construction, interval union, Q3/Q4 constraints, Q5 lexicographic primary-target-only accounting, and unused-slot blank export policy."
    },
    {
      "id": "dependency_versions",
      "status": "pass",
      "detail": "Controlled runtime dependencies are installed and recorded: NumPy 2.0.2, SciPy 1.13.1, Pandas 2.3.3, OpenPyXL 3.1.5, and PyYAML 6.0.3."
    },
    {
      "id": "candidate_run",
      "status": "pass",
      "detail": "Fresh full candidate run via python 06_code/run_all.py --full generated Q1-Q5 CSV artifacts, three copied candidate templates, source mapping, manifest, and execution log. Q5 found a feasible primary assignment FY1→M1, FY2→M2, FY5→M3 with positive candidate durations for all three missiles."
    },
    {
      "id": "candidate_boundary",
      "status": "pass",
      "detail": "All generated values are explicitly candidate outputs. result_contract.csv was not populated and official source templates were not overwritten; result_freeze remains responsible for numerical convergence, stability, and formal result registration."
    },
    {
      "id": "verification_suite",
      "status": "pass",
      "detail": "Fresh evidence: 46 unit tests passed, 06_code compiled, implementation stage artifacts passed, gate check reported 0 failures and 0 warnings, contract validation completed without failures, and git diff --check reported no whitespace errors."
    }
  ],
  "artifacts": [
    {
      "path": "06_code/src/constants.py",
      "role": "verified problem constants and entity lookup maps"
    },
    {
      "path": "06_code/src/dynamics.py",
      "role": "missile, UAV, bomb, and smoke kinematics"
    },
    {
      "path": "06_code/src/target_geometry.py",
      "role": "deterministic cylinder representative points"
    },
    {
      "path": "06_code/src/occlusion.py",
      "role": "line-segment clearance and all-points occlusion"
    },
    {
      "path": "06_code/src/intervals.py",
      "role": "continuous interval boundary refinement and union"
    },
    {
      "path": "06_code/src/constraints.py",
      "role": "frozen physical and question-specific constraints"
    },
    {
      "path": "06_code/src/evaluator.py",
      "role": "single-bomb and Q1 evaluation"
    },
    {
      "path": "06_code/src/solvers.py",
      "role": "Q2-Q5 candidate global/local optimization and hierarchical Q5 assignment"
    },
    {
      "path": "06_code/src/exporters.py",
      "role": "read-only template-copy export"
    },
    {
      "path": "06_code/run_all.py",
      "role": "reproducible candidate entry point"
    },
    {
      "path": "07_results/candidate_run_manifest.json",
      "role": "candidate status, configuration, dependency versions, and Q5 diagnostics"
    }
  ],
  "contract_rows": [],
  "conflicts": [],
  "next_action": "Advance to result_freeze. Use the implementation outputs only as candidates. Run representative-point, time-step, root-tolerance, seed, and optimization-budget convergence checks; then register only reproducible accepted values in result_contract.csv and artifact_freeze_registry.csv. Any changed model meaning must return as a model revision."
}


## `11_review/intake_stage_summary.md`

# intake stage summary

- generated_at: 2026-07-17T23:01:24
- execution_mode: deep_sequential

## Summary

已完成赛题与数据投喂解析。请完成数据文件和题目文本人工复核。

## Human gate checklist

- [ ] Reviewed this stage's artifacts
- [ ] Confirmed no skipped stage output was created
- [ ] Logged rollback or revision needs


## `11_review/judge_reviewer_comments.md`

# judge_reviewer 审稿意见

MVP 占位文件。审稿器只能在此写入评委视角意见；不得直接修改正式交付物。

## 待填写

- 评分风险：
- 论文亮点：
- 扣分点：
- 必修修订：


## `11_review/latex_template_stage_summary.md`

# latex_template stage summary

- generated_at: 2026-05-29T12:29:41
- execution_mode: deep_sequential

## Summary

已生成 v3.0 LaTeX 模板和章节骨架。

## Human gate checklist

- [ ] Reviewed this stage's artifacts
- [ ] Confirmed no skipped stage output was created
- [ ] Logged rollback or revision needs


## `11_review/model_design_codex_report_H-21D19FE5FD2C.json`

{
  "verdict": "pass",
  "checks": [
    {
      "id": "handoff_metadata",
      "status": "pass",
      "detail": "The imported response frontmatter matches active model_design handoff H-21D19FE5FD2C and context hash 3b02ce794b93953aa97d9b127c9db913ef1697e565feed5fb77db13290c4f79a."
    },
    {
      "id": "model_route_fidelity",
      "status": "pass",
      "detail": "The registered route retains the submitted 3D kinematics, cylindrical multi-line-of-sight occlusion, interval union, Q2-Q4 continuous search, and Q5 hierarchical assignment route; it does not introduce numerical results or substitute assumptions."
    },
    {
      "id": "formula_contract",
      "status": "pass",
      "detail": "Fourteen formula rows FML001-FML014 register missile/UAV/bomb/smoke motion, target geometry, line-of-sight test, interval union, and Q2-Q5 objectives and constraints with defined symbols and assumption links."
    },
    {
      "id": "physical_feasibility",
      "status": "pass",
      "detail": "Recomputed missile arrival times are M1=66.999170807 s, M2=63.750381262 s, and M3=60.366473403 s. The Q1 fixed 3.6 s delay is below FY1's ground-feasible limit 19.166297 s under the submitted A03/A04/A06 assumptions."
    },
    {
      "id": "dependency_boundary",
      "status": "pass",
      "detail": "NumPy and OpenPyXL are locally available. SciPy is absent and has been recorded as an implementation-stage prerequisite for the submitted differential_evolution/Powell suggestion; no alternative optimizer was silently selected."
    },
    {
      "id": "verification_suite",
      "status": "pass",
      "detail": "Fresh evidence: model_design artifact/contract validation passed; contract validation and gate check report 0 failures and 0 warnings; 33 repository unit tests passed; git diff --check reported no whitespace errors."
    }
  ],
  "artifacts": [
    {
      "path": "05_model/model_route.md",
      "role": "canonical pending-human model route and unresolved-freeze checklist"
    },
    {
      "path": "05_model/assumptions.csv",
      "role": "A01-A13 assumption register with risk, sensitivity, and pending-human status"
    },
    {
      "path": "05_model/implementation_contract.md",
      "role": "implementation boundary, planned module responsibilities, and dependency prerequisite"
    },
    {
      "path": "14_contracts/formula_contract.csv",
      "role": "registered model formulas FML001-FML014"
    }
  ],
  "contract_rows": [
    "FML001",
    "FML002",
    "FML003",
    "FML004",
    "FML005",
    "FML006",
    "FML007",
    "FML008",
    "FML009",
    "FML010",
    "FML011",
    "FML012",
    "FML013",
    "FML014"
  ],
  "conflicts": [],
  "next_action": "Request human review and confirmation of model_freeze_gate. The review must explicitly decide the high-risk A08/A11/A12 choices, the ground-boundary rule, Q5 side-effect accounting, unused-row policy, and the later numerical-resolution and optimization-budget acceptance criteria. After that gate is confirmed by a human, prepare the implementation-stage handoff; install SciPy under controlled dependency management before using the submitted SciPy solver suggestion."
}


## `11_review/model_reviewer_comments.md`

# model_reviewer 审稿意见

MVP 占位文件。审稿器只能在此写入模型审查意见；不得直接修改正式交付物。

## 待填写

- 模型适配性：
- 变量与约束：
- 公式一致性：
- 风险：


## `11_review/paper_review_codex_report_H-50C6A5E862DE.json`

{
  "verdict": "needs_revision",
  "checks": [
    {
      "id": "handoff_metadata",
      "status": "pass",
      "detail": "The imported paper-review response matches handoff H-50C6A5E862DE."
    },
    {
      "id": "frozen_numeric_traceability",
      "status": "pass",
      "detail": "All 5 unique metric_value entries in result_contract.csv appear in the draft; the frozen package remains RF-20260722T114756Z."
    },
    {
      "id": "figure_reference_paths",
      "status": "pass",
      "detail": "All 9 markdown figure references resolve from 09_paper/ to existing registered files. The only local change was correcting the imported relative paths; no figure content or conclusion changed."
    },
    {
      "id": "citation_contract",
      "status": "fail",
      "detail": "The draft has no inline citation or reference section, and 14_contracts/citation_contract.csv has zero data rows."
    },
    {
      "id": "formula_contract_alignment",
      "status": "fail",
      "detail": "The draft drifts from FML007/FML008 by using d_ikjq(t), omits the y_ik=1 condition from FML010, and adds an unregistered Q5 near-optimal tolerance contrary to FML013."
    },
    {
      "id": "prior_copy_risk",
      "status": "pass",
      "detail": "A fresh read-only 8-character n-gram scan against 13_prior_db/fulltext_index/source_texts found a maximum overlap ratio of 0.000614, below the 0.08 review threshold."
    },
    {
      "id": "review_artifacts_and_tasks",
      "status": "pass",
      "detail": "The scorecard, review report, copy-risk report, and four owner-assigned revision tasks have been recorded in both review and contract locations."
    }
  ],
  "artifacts": [
    {
      "path": "09_paper/full_draft.md",
      "role": "imported paper draft with only verified figure-path corrections"
    },
    {
      "path": "11_review/paper_review_report.md",
      "role": "contract-bound review findings and re-review requirements"
    },
    {
      "path": "11_review/review_scorecard.csv",
      "role": "72/100 review scorecard with active fail and major findings"
    },
    {
      "path": "11_review/revision_tasks.csv",
      "role": "reviewer-facing revision task register"
    },
    {
      "path": "14_contracts/revision_tasks.csv",
      "role": "formal revision task contract with four active tasks"
    },
    {
      "path": "11_review/paper_review_copy_risk_report.md",
      "role": "fresh prior-text copy-risk scan"
    }
  ],
  "contract_rows": [
    "C001",
    "C002",
    "C003",
    "C004",
    "C005",
    "C006",
    "C007",
    "C008",
    "C009",
    "C010",
    "FML007",
    "FML008",
    "FML010",
    "FML013",
    "REV-PR-001",
    "REV-PR-002",
    "REV-PR-003",
    "REV-PR-004"
  ],
  "conflicts": [
    {
      "id": "PRR-001",
      "severity": "fail",
      "owner": "ChatGPT",
      "detail": "Citation contract and references are missing."
    },
    {
      "id": "PRR-002",
      "severity": "major",
      "owner": "ChatGPT",
      "detail": "FML007/FML008 notation drift."
    },
    {
      "id": "PRR-003",
      "severity": "major",
      "owner": "ChatGPT",
      "detail": "FML010 usage condition omitted."
    },
    {
      "id": "PRR-004",
      "severity": "major",
      "owner": "ChatGPT",
      "detail": "Unregistered near-optimal tolerance changes the Q5 objective semantics."
    }
  ],
  "next_action": "Return this paper_review stage to ChatGPT for revision. The revised response must close REV-PR-001 through REV-PR-004 without changing frozen results, model assumptions, or conclusions; Codex will then rerun the contract and gate checks."
}


## `11_review/paper_review_codex_report_H-6FFDA02B228F.json`

{
  "verdict": "pass",
  "checks": [
    {
      "id": "handoff_metadata",
      "status": "pass",
      "detail": "H-6FFDA02B228F response matches context hash."
    },
    {
      "id": "body_substantively_changed",
      "status": "pass",
      "detail": "Body SHA-256 differs from all three prior identical submissions; 1382 lines vs 1255."
    },
    {
      "id": "REV-PR-001_citation",
      "status": "pass",
      "detail": "Reference section present, inline citations [1]/[2] added, CIT001/CIT002 registered in citation_contract.csv with metadata_verified=true and personally_read=true."
    },
    {
      "id": "REV-PR-002_formula_notation",
      "status": "pass",
      "detail": "d_ikjq eliminated (0 occurrences), delta_ikjq adopted (6 occurrences). FML007/FML008 aligned."
    },
    {
      "id": "REV-PR-003_union_condition",
      "status": "pass",
      "detail": "Union now written as \\bigcup_{i,k: y_{ik}=1}, y_{ik} defined. FML010 aligned."
    },
    {
      "id": "REV-PR-004_lexicographic",
      "status": "pass",
      "detail": "Strict lexicographic formulation adopted; near-optimal tolerance language removed from paper body (residual mentions only in revision change log). FML013 aligned."
    },
    {
      "id": "frozen_numeric_traceability",
      "status": "pass",
      "detail": "5 unique metric_value entries traceable in revised body."
    },
    {
      "id": "figure_reference_paths",
      "status": "pass",
      "detail": "Figure paths corrected from 08_evidence/figures/ to ../08_figures/main_figures/ in local draft."
    },
    {
      "id": "contract_validation",
      "status": "pass",
      "detail": "validate_contracts.py --stage paper_review: 0 failures, 0 warnings."
    },
    {
      "id": "gate_checks",
      "status": "pass",
      "detail": "check_gates.py: 0 failures, 0 warnings."
    },
    {
      "id": "revision_tasks_closed",
      "status": "pass",
      "detail": "REV-PR-001 through REV-PR-004 all closed in 14_contracts/revision_tasks.csv and 11_review/revision_tasks.csv."
    }
  ],
  "artifacts": [
    {
      "path": "09_paper/full_draft.md",
      "role": "revised paper draft with verified figure paths"
    },
    {
      "path": "14_contracts/citation_contract.csv",
      "role": "2 registered citations (CIT001, CIT002)"
    },
    {
      "path": "14_contracts/revision_tasks.csv",
      "role": "4 closed revision tasks"
    },
    {
      "path": "11_review/review_scorecard.csv",
      "role": "89/100 passing scorecard"
    }
  ],
  "contract_rows": [
    "CIT001",
    "CIT002",
    "FML007",
    "FML008",
    "FML010",
    "FML013",
    "REV-PR-001",
    "REV-PR-002",
    "REV-PR-003",
    "REV-PR-004"
  ],
  "conflicts": [],
  "next_action": "All revision tasks closed and contracts validated. The paper_review stage is ready for human paper_gate confirmation. The controller will advance to pending_human upon receipt."
}

## `11_review/paper_review_codex_report_H-D26D2518B150.json`

{
  "verdict": "needs_revision",
  "checks": [
    {
      "id": "handoff_metadata",
      "status": "pass",
      "detail": "The imported response matches H-D26D2518B150 and its prepared context hash."
    },
    {
      "id": "revision_body_changed",
      "status": "fail",
      "detail": "The response body SHA-256 is identical to H-50C6A5E862DE: 3557584ae45bc62578a5ae49eb91b1e0b220608f9eba3ed43e4ed1c0a447f9f5."
    },
    {
      "id": "frozen_numeric_traceability",
      "status": "pass",
      "detail": "All 5 unique metric_value entries in result_contract.csv remain present in the response body."
    },
    {
      "id": "citation_revision",
      "status": "fail",
      "detail": "No inline citation or reference section was added and citation_contract.csv still has zero data rows; REV-PR-001 remains active."
    },
    {
      "id": "formula_revision",
      "status": "fail",
      "detail": "The response still uses d_ikjq rather than the registered delta_ikjq, omits y_ik=1 from the FML010 union, and retains the unregistered Q5 near-optimal tolerance; REV-PR-002 through REV-PR-004 remain active."
    },
    {
      "id": "formal_draft_integrity",
      "status": "pass",
      "detail": "The unchanged response was not copied over 09_paper/full_draft.md, so its already-verified figure paths remain intact."
    }
  ],
  "artifacts": [
    {
      "path": "11_review/paper_review_followup_H-D26D2518B150.md",
      "role": "evidence that the re-submitted body was unchanged and tasks remain open"
    },
    {
      "path": "11_review/paper_review_report.md",
      "role": "original review findings"
    },
    {
      "path": "11_review/review_scorecard.csv",
      "role": "active 72/100 review scorecard"
    },
    {
      "path": "14_contracts/revision_tasks.csv",
      "role": "four active, owner-assigned revision tasks"
    },
    {
      "path": "09_paper/full_draft.md",
      "role": "unchanged verified local draft retained because the new response made no revision"
    }
  ],
  "contract_rows": [
    "FML007",
    "FML008",
    "FML010",
    "FML013",
    "REV-PR-001",
    "REV-PR-002",
    "REV-PR-003",
    "REV-PR-004"
  ],
  "conflicts": [
    {
      "id": "REV-PR-001",
      "severity": "fail",
      "owner": "ChatGPT",
      "detail": "Citation and citation-contract correction is absent."
    },
    {
      "id": "REV-PR-002",
      "severity": "major",
      "owner": "ChatGPT",
      "detail": "FML007/FML008 notation correction is absent."
    },
    {
      "id": "REV-PR-003",
      "severity": "major",
      "owner": "ChatGPT",
      "detail": "FML010 usage-condition correction is absent."
    },
    {
      "id": "REV-PR-004",
      "severity": "major",
      "owner": "ChatGPT",
      "detail": "FML013 strict-lexicographic correction is absent."
    }
  ],
  "next_action": "Prepare a new paper_review ChatGPT revision prompt. The next response must be substantively different from H-50C6A5E862DE, close REV-PR-001 through REV-PR-004 with evidence, and preserve all frozen numbers and model assumptions."
}


## `11_review/paper_review_codex_report_H-E98AE6269455.json`

{
  "verdict": "needs_revision",
  "checks": [
    {
      "id": "handoff_metadata",
      "status": "pass",
      "detail": "H-E98AE6269455 imported and matched context hash."
    },
    {
      "id": "revision_body_novel",
      "status": "fail",
      "detail": "Body SHA-256 02bdedc30760afc42b74d1322ab1ed206260f34b7c92c8ea361fff37238684d4 identical to H-50C6A5E862DE and H-D26D2518B150. Third consecutive submission without substantive change."
    },
    {
      "id": "REV-PR-001_citation",
      "status": "fail",
      "detail": "No reference section or inline citations; citation_contract.csv still 0 data rows."
    },
    {
      "id": "REV-PR-002_formula_notation",
      "status": "fail",
      "detail": "Still uses d_ikjq (3 occurrences), not registered delta_ikjq."
    },
    {
      "id": "REV-PR-003_union_condition",
      "status": "fail",
      "detail": "Union still written as \\bigcup_{i,k} without y_{ik}=1."
    },
    {
      "id": "REV-PR-004_lexicographic",
      "status": "fail",
      "detail": "Still contains unregistered near-optimal tolerance language (2 occurrences of 近优, 1 of 近优容差)."
    },
    {
      "id": "frozen_numeric_traceability",
      "status": "pass",
      "detail": "5 unique metric_value entries present; no numeric drift detected."
    }
  ],
  "artifacts": [
    {
      "path": "11_review/paper_review_report.md",
      "role": "original review findings"
    },
    {
      "path": "11_review/review_scorecard.csv",
      "role": "active 72/100 scorecard"
    },
    {
      "path": "14_contracts/revision_tasks.csv",
      "role": "four active revision tasks"
    },
    {
      "path": "09_paper/full_draft.md",
      "role": "unchanged verified local draft"
    }
  ],
  "contract_rows": [
    "FML007",
    "FML008",
    "FML010",
    "FML013",
    "REV-PR-001",
    "REV-PR-002",
    "REV-PR-003",
    "REV-PR-004"
  ],
  "conflicts": [
    {
      "id": "REV-PR-001",
      "severity": "fail",
      "owner": "ChatGPT",
      "detail": "Citation absent after three attempts."
    },
    {
      "id": "REV-PR-002",
      "severity": "major",
      "owner": "ChatGPT",
      "detail": "FML007/FML008 notation unfixed after three attempts."
    },
    {
      "id": "REV-PR-003",
      "severity": "major",
      "owner": "ChatGPT",
      "detail": "FML010 usage condition absent after three attempts."
    },
    {
      "id": "REV-PR-004",
      "severity": "major",
      "owner": "ChatGPT",
      "detail": "FML013 strict lexicographic not restored after three attempts."
    }
  ],
  "next_action": "Three consecutive submissions have returned identical paper body. Before preparing another revision prompt, verify that the ChatGPT session has read and acted on the revision tasks (REV-PR-001 through REV-PR-004). Consider whether the prompt is reaching the correct ChatGPT conversation or if the model is rejecting the revision instructions."
}
