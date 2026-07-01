# final_export 阶段阻塞记录

## 阻塞时间
2025-06-04T13:15:00Z

## 阻塞原因
1. TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-002~004: 图表引用与合同不匹配，且图片文件缺失。
2. TRAIN-20260604_TEXTONLY_STAGE_API_QUEUEFIX_CODEX-VAL-011~013: 审阅分数低于阈值，不能提交。
3. 缺少最终人工闸门确认。

## 影响
无法生成有效最终提交包及 PPT，所有导出动作挂起。

## 建议
返回 upstream 阶段修复图表和论文质量，重新通过 auto_review，然后重新执行 final_export。
