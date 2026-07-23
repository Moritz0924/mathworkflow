# data_analysis / Codex

## 结果
生成可复现的数据字典、质量报告和EDA证据，核验ChatGPT的数据判断。

## 边界
可以修数据读取、类型、缺失和可视化实现；不得擅自改变业务口径或删除异常样本。

## 交付
提交执行命令、数据规模、字段质量、异常处理建议、产物和冲突清单。

## 验收
分析可从原始输入重跑，统计量能在代码输出中定位，报告不包含不可追溯数字。

## 阻塞
原始数据不可重建、字段含义未知或ChatGPT结论无法由数据支持时退回主脑。

## Handoff

- handoff_id: `H-4709302CC4F4`
- response: `10_ai_logs/handoffs/H-4709302CC4F4/chatgpt_response.md`

## Required receipt

Return pass, needs_revision, or blocked with checks, artifacts, contract_rows, conflicts, and next_action.
