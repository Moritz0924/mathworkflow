# 数学建模工作流 v3.2 架构设计与调整方案

nature-skills 增强 + 本地优秀论文数据库 + Codex 自审稿迭代闭环

日期：2026-05-20

## 1. 执行摘要

v3.2 不应推翻 v3.0，而应在 v3.0 的单环节深度模式上增加三层增强：nature-skills 质量层、本地优秀论文数据库经验层、Codex 自动审稿与复盘迭代层。工作流仍然是裁判，Codex 是执行代理，数据库是教练，skills 是专业工具。

## 2. 现状识别

- v3.0 已具备 deep_sequential、禁止并行、人工闸门、阶段状态锁定。
- check_gates.py 当前检查深度模式、LaTeX label/ref、图表注册表和 result_summary。
- 08_figures、09_paper、10_ai_logs、13_sample_prior 已有良好雏形。
- 短板是缺 claim-evidence 契约总线、图表论证契约、润色事实保护 diff、prior 数据库可控检索层。

## 3. 总体架构

```text
用户/赛题输入
    ↓
Workflow Controller
    ↓
Contract Bus ←→ Codex Executor ←→ Agent Skills
    ↓              ↑
Auto Reviewer ←→ Prior DB Retriever
    ↓
Iteration Memory
    ↓
Human Final Gate
```

## 4. 三层闭环

### 做题闭环
题目输入 → 题型识别 → prior 经验卡片 → 建模计划 → 代码求解 → 结果冻结 → 图表 → 论文初稿

### 审稿闭环
初稿产物 → check_gates → 多 reviewer 审稿 → 优秀论文对标 → review_scorecard → revision_tasks

### 迭代闭环
revision_tasks → Codex 逐项修订 → 重新运行局部脚本 → 重新审稿 → 达标冻结 → 人工确认

## 5. 目录架构

```text
project_root/
├── AGENTS.md
├── config/
│   ├── execution_policy.yaml
│   ├── skill_enhancement.yaml
│   ├── iteration_policy.yaml
│   └── prior_db_policy.yaml
├── 13_prior_db/
├── 14_contracts/
├── 11_review/
└── 15_iteration_memory/
```

## 6. nature-skills 接入

- nature-figure：图表论证和导出质量。
- nature-writing：论文结构与 claim 组织。
- nature-polishing：润色但不改事实。
- nature-academic-search / nature-citation：文献检索与支撑等级。
- nature-data：数据来源与复现说明。
- nature-paper2ppt：终稿后的展示材料。

## 7. 本地 Prior DB

解题前只输出题型经验、常用模型、常见图表、常见扣分点。初稿后才允许进行优秀论文全文对标。禁止复制历史论文的摘要、正文、图注和结论。

## 8. 自动审稿

建议拆为 problem_reviewer、model_reviewer、code_reviewer、figure_reviewer、paper_reviewer、judge_reviewer。审稿器只输出 reviewer_comments、review_scorecard、revision_tasks，不直接修改产物。

## 9. 契约总线

核心文件：claim_evidence_map、result_contract、figure_contract、formula_contract、citation_contract、artifact_freeze_registry、polish_diff_check、revision_tasks。

## 10. 调整路线

1. 架构冻结，不动代码。
2. 接入 Codex 规则。
3. 接入契约总线。
4. 接入 nature-skills 增强。
5. 接入 Prior DB。
6. 接入自动审稿闭环。
7. 接入迭代记忆。

## 11. 防失控规则

数据库不是答案库；Codex 不是自由写手；nature-skills 不是总控；Reviewer 只提任务；最终提交必须人工确认。
