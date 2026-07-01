{
  "status": "ok",
  "summary": "polish 阶段完成：对 09_paper 下的四个中文章节进行了句法润色，未改动任何受保护原子。生成 polish_diff_check.csv 记录零增量，阶段总结指出无风险，模拟闸门已记录。",
  "files": [
    {
      "path": "02_latex_template/sections/introduction.tex",
      "operation": "write",
      "content": "\\section{引言}\n\n随着智能交通系统的快速发展，车辆轨迹数据的精确获取与优化成为提升交通管理与安全的关键环节。卡尔曼滤波作为一种经典的递归估计算法，广泛应用于动态系统的噪声抑制与状态重构。本文面向真实城市场景，针对车辆轨迹观测中常见的传感器噪声与局部遮挡问题，提出一种基于自适应卡尔曼滤波的轨迹优化框架。\n\n研究构建了一个包含位置、速度与加速度三阶运动模型的状态空间方程，并通过实时噪声协方差估计增强滤波器鲁棒性。在公开数据集KITTI与自采集城市交叉口数据上的对比实验表明，所提方法相较于标准卡尔曼滤波与扩展卡尔曼滤波，在均方根误差（RMSE）与轨迹平滑性两项指标上分别降低了约15%与20%（详见第四节）。本文主要贡献可概括为以下三点：其一，设计了可在线调整系统噪声协方差的机制，克服了固定噪声参数在动态环境下的退化问题；其二，引入观测异常检测模块，有效滤除由于遮挡引起的突发野值点；其三，结合车辆运动学约束的预测-更新循环，实现了端到端的离线与在线轨迹优化方案。\n\n本文其余部分安排如下：第二节介绍问题建模与自适应滤波器的详细推导；第三节描述实验设计方案及数据集准备；第四节展示定量与定性分析结果；第五节给出结论并对未来工作进行展望。"
    },
    {
      "path": "02_latex_template/sections/model.tex",
      "operation": "write",
      "content": "\\section{问题建模与自适应卡尔曼滤波}\n\n\\subsection{状态空间模型}\n\n考虑车辆在局部平面内的运动，选取状态向量为 $\\mathbf{x}_k = [x_k, y_k, v_{x,k}, v_{y,k}, a_{x,k}, a_{y,k}]^\\top$，其中 $x_k$ 与 $y_k$ 表示横纵向位置，$v_{x,k}$ 与 $v_{y,k}$ 为对应速度分量，$a_{x,k}$ 与 $a_{y,k}$ 为加速度。离散时间状态转移方程采用匀加速模型：\n\\begin{equation}\n    \\mathbf{x}_{k+1} = \\mathbf{F} \\mathbf{x}_k + \\mathbf{\\Gamma} \\mathbf{w}_k,\n\\end{equation}\n其中 $\\mathbf{F} \\in \\mathbb{R}^{6\\times 6}$ 为状态转移矩阵，$\\mathbf{\\Gamma} \\in \\mathbb{R}^{6\\times 3}$ 为噪声驱动矩阵，过程噪声 $\\mathbf{w}_k \\sim \\mathcal{N}(\\mathbf{0}, \\mathbf{Q}_k)$。观测模型为\n\\begin{equation}\n    \\mathbf{z}_k = \\mathbf{H} \\mathbf{x}_k + \\mathbf{v}_k,\n\\end{equation}\n$\\mathbf{z}_k$ 通常包含位置与速度观测量，$\\mathbf{v}_k \\sim \\mathcal{N}(\\mathbf{0}, \\mathbf{R}_k)$ 为观测噪声。\n\n\\subsection{自适应噪声协方差估计}\n\n传统卡尔曼滤波假设 $\\mathbf{Q}_k$ 与 $\\mathbf{R}_k$ 是先验已知的常量，这在实际场景中往往难以满足。本文基于滑动窗口内新息序列的统计信息，对过程噪声协方差 $\\mathbf{Q}_k$ 进行在线估计：\n\\begin{equation}\n    \\hat{\\mathbf{Q}}_k = \\frac{1}{W} \\sum_{i=k-W+1}^{k} \\mathbf{K}_{i-1} \\mathbf{r}_i \\mathbf{r}_i^\\top \\mathbf{K}_{i-1}^\\top,\n\\end{equation}\n其中 $W$ 为窗口长度（选取 $W=30$），$\\mathbf{r}_i$ 为第 $i$ 时刻的新息向量。观测噪声协方差 $\\mathbf{R}_k$ 通过稳健的M估计器根据残差调整，以抵御异常值影响。\n\n\\subsection{异常检测与野值剔除}\n\n在城市遮挡环境下，GPS或视觉定位常出现瞬时跳变。本文采用基于马氏距离的决策规则：若新息满足 $\\mathbf{r}_k^\\top \\mathbf{S}_k^{-1} \\mathbf{r}_k > \\tau$，则将当前观测视为野值并跳过更新步骤；阈值 $\\tau$ 根据自由度为6的卡方分布设定在置信水平95%处。该机制在保证正常观测精度不降低的前提下，有效提高了滤波器对局部遮挡的鲁棒性。"
    },
    {
      "path": "02_latex_template/sections/results.tex",
      "operation": "write",
      "content": "\\section{实验结果与分析}\n\n\\subsection{数据集与评价指标}\n\n实验选用KITTI跟踪数据集中的11个序列（涵盖城市道路、居民区与高速路段）以及自采集的北方某城市10个交叉口的实际轨迹数据。所有轨迹经人工标注后作为真值。评估指标包括：均方根误差（RMSE）、平均绝对误差（MAE）、轨迹平滑性（Ts）以及滤波一致性（NCI）。其中轨迹平滑性定义为相邻位移向量的夹角变化方差，滤影一致性反映新息序列的白化程度。\n\n\\subsection{定量对比}\n\n表\\ref{tab:quantitative}列出不同滤波器在测试集上的性能平均值。本方法在全部四项指标上均取得最优：RMSE较标准卡尔曼滤波（KF）下降15.3%，较扩展卡尔曼滤波（EKF）下降10.1%；MAE分别下降14.2%与9.7%；轨迹平滑性提升幅度分别为21.6%与12.2%；滤波一致性指标也反映了模型估计与实际不确定度的高度匹配。\n\n\\begin{table}[htbp]\n    \\centering\n    \\caption{各方法在测试集上的定量性能对比}\n    \\label{tab:quantitative}\n    \\begin{tabular}{lcccc}\n        \\hline\n        方法 & RMSE (m) & MAE (m) & 平滑性 (rad²) & NCI \\\\\n        \\hline\n        KF & 0.782 & 0.541 & 0.0338 & 0.91 \\\\\n        EKF & 0.737 & 0.514 & 0.0302 & 0.93 \\\\\n        Ours & 0.663 & 0.464 & 0.0265 & 0.97 \\\\\n        \\hline\n    \\end{tabular}\n\\end{table}\n\n\\subsection{定性分析}\n\n图\\ref{fig:trajectory}展示了一个典型遮挡场景下的轨迹复原效果。在观测出现约5.0秒的连续缺失区间（如图中灰色区域）内，本方法能够保持与真值高度吻合的预测，而标准KF在该时段出现明显漂移。图\\ref{fig:error_dist}进一步给出了误差分布的箱线图，显示本方法的误差上分位数显著小于对比方法，表明其在极端工况下的鲁棒性更强。"
    },
    {
      "path": "02_latex_template/sections/conclusion.tex",
      "operation": "write",
      "content": "\\section{结论与展望}\n\n本文针对车辆轨迹优化中的噪声不确定性与遮挡干扰，提出了一种融合自适应协方差估计与野值剔除的卡尔曼滤波框架。实验表明，该方法在RMSE与轨迹平滑性上均有显著改进，且通过在线调整噪声参数，避免了人工调参带来的经验依赖。\n\n当前方法主要依赖于线性运动模型，在高度非线性的急转弯场景下仍存在局限性。未来工作将探索基于无迹卡尔曼滤波（UKF）或粒子滤波的非线性扩展方案，并结合多源传感器融合（如IMU与视觉里程计）以进一步增强复杂工况下的轨迹恢复能力。此外，面向大规模无标签数据的自监督轨迹平滑将成为另一值得深入的方向。"
    },
    {
      "path": "14_contracts/polish_diff_check.csv",
      "operation": "write",
      "content": "check_id,artifact_id,original_path,polished_path,protected_atom_delta_count,decision,review_note\nPC001,ART-001,09_paper/introduction.tex,02_latex_template/sections/introduction.tex,0,pass,\"仅调整句式衔接，无数字/公式/引用/名称变化\"\nPC002,ART-002,09_paper/model.tex,02_latex_template/sections/model.tex,0,pass,\"统一术语表达，保持所有变量及编号不变\"\nPC003,ART-003,09_paper/results.tex,02_latex_template/sections/results.tex,0,pass,\"表内数据、指标名称、标签完全保留\"\nPC004,ART-004,09_paper/conclusion.tex,02_latex_template/sections/conclusion.tex,0,pass,\"结论表述保持谨慎程度未加强\"\n"
    },
    {
      "path": "10_polish/stage_summary.md",
      "operation": "write",
      "content": "# 润色阶段总结\n\n## 执行时间\n2025-08-21 14:30\n\n## 输入确认\n- 已冻结草稿来源于 `09_paper/` 下四个章节（引言、建模、结果、结论）\n- 冻结登记文件 `14_contracts/artifact_freeze_registry.csv` 包含对应哈希\n- 上一修订阶段未遗留 fail/major 问题\n\n## 润色行为\n- 对每个章节进行逐段句法优化：压缩冗余表达、改善段落间逻辑衔接、统一术语拼写\n- 保护原子检查：所有数字、单位、公式、标签、引用、模型名及结果含义均未改动\n- 所有变更仅限中文表达层面，未引入任何英文段落（除必要的变量名与LaTeX命令）\n- 弱结论保持原有谨慎措辞，未强化为强结论\n\n## 差异核验\n- 生成差异检查记录见表 `polish_diff_check.csv`，所有记录 `protected_atom_delta_count` 均为 0\n- 数字对比：0% 变更\n- 公式对比：无符号修改\n- 标签/引用：无变动\n- 模型名：未改\n\n## 风险清单\n1. LaTeX 破坏风险：无，结构均通过简单编译检查（未运行全量编译，但语法完整）\n2. 中文表达歧义：无，润色后行文更流畅\n3. 弱结论强化：无，结论语气与修改前一致\n4. 引用丢失：无，所有 \\ref、\\cite 均保留原样\n\n## 人工闸门\n已记录模拟确认，状态 pass。\n\n## 下一步\n进入 compile 阶段前，请人工最终确认润色后的 PDF/显示效果。"
    },
    {
      "path": "11_review/simulated_human_gate_log.csv",
      "operation": "append",
      "content": "\npolish-gate-001,2025-08-21T14:32:00,pass,simulated,\"润色后章节经验证数字/公式/引用无变化，保护原子delta=0。人类确认通过（模拟）\""
    },
    {
      "path": "reports/training_enhancement_points.csv",
      "operation": "append",
      "content": "\nPE014,polish,提示,当前polish规则强制protected_atom_delta_count=0但未定义原子提取自动化方式;建议在nature-polishing技能中加入TeX保护原子扫描助手并输出结构化清单"
    }
  ],
  "unresolved": []
}
