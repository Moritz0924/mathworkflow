{
  "status": "blocked",
  "summary": "Full paper draft missing. Review blocked. Generated reviewer comments (fail), scorecard (0/10), and revision tasks for missing draft + open figure contract failures.",
  "files": [
    {
      "path": "11_review/auto_reviewer_comments.md",
      "operation": "write",
      "content": "# 多审稿器自动审稿意见\n\n## 1. 题目视角\n- **状态**: FAIL – 缺少全文草稿。无法验证题目覆盖度、子问题回答和交付物完整性。\n- **风险**: 可能缺失官方问题要求。\n\n## 2. 数据视角\n- **状态**: FAIL – 无草稿因此无数据描述，无法评估数据来源、字段解释、缺失值处理或可复现性。\n\n## 3. 模型视角\n- **状态**: FAIL – 模型假设、变量定义、公式、验证和局限均未呈现，无法评估合理性。\n\n## 4. 结果视角\n- **状态**: FAIL – 无冻结结果；图表文件仅为 11 字节占位（见 MCP 观察），无法核对数值一致性、敏感性分析或误差估计。\n\n## 5. 图表视角\n- **状态**: FAIL – 4 张图表均为无效占位（11 字节），无法评估设计质量、中文标注或论证支撑。图像合同存在合规失败（缺少 evidence_source 和有效输出文件）。\n\n## 6. 写作视角\n- **状态**: FAIL – 草稿缺失，无法评估论断-证据绑定、章节连贯性和结论强度。\n\n## 7. 评委视角\n- **状态**: FAIL – 因缺少草稿和结果，无法生成综合评分。建议立即返回 `paper_full` 阶段。\n\n## 总结\n所有视角均因缺少全文草稿而阻断。必须首先执行 `paper_full` 阶段并生成有效的图表和合同，然后重新进行审稿。当前所有指标评分为 0。"
    },
    {
      "path": "11_review/review_scorecard.csv",
      "operation": "write",
      "content": "metric,score,max_score,status,notes\nproblem_coverage,0,10,fail,missing paper draft\ndata_quality,0,10,fail,draft missing\nmodel_validity,0,10,fail,draft missing\nresult_reliability,0,10,fail,draft missing\nfigure_quality,0,10,fail,placeholder figures (11B)\nwriting_clarity,0,10,fail,draft missing\noverall,0,10,fail,stage blocked"
    },
    {
      "path": "14_contracts/revision_tasks.csv",
      "operation": "write",
      "content": "task_id,title,severity,status,source_comment_id,target_artifact,target_location,required_action,acceptance_check\nREV-001,Generate full paper draft (paper_full stage),fail,open,AUTO-REVIEW-001,09_paper/paper.tex,paper_full output,Execute paper_full stage to produce a complete draft.,Full draft exists at 09_paper/paper.tex with all sections.\nREV-002,Add evidence_source for fig1 in figure_contract,major,open,VAL-001,14_contracts/figure_contract.csv,fig1 row,Add result_id or evidence_source for fig1_scatter.png.,figure_contract.csv row has valid result_id or evidence_source.\nREV-003,Ensure valid output file for fig1 exists,major,open,VAL-002,14_contracts/figure_contract.csv / 08_figures/,fig1 row and file,Replace placeholder with actual chart and update figure_contract output path.,fig1_scatter.png is > 1KB and registered.\nREV-004,Add evidence_source for fig2,major,open,VAL-003,14_contracts/figure_contract.csv,fig2 row,Same as REV-002.,fig2 row has evidence_source.\nREV-005,Ensure valid output file for fig2 exists,major,open,VAL-004,14_contracts/figure_contract.csv / 08_figures/,fig2 row and file,Replace placeholder with actual chart.,fig2_residuals.png > 1KB.\nREV-006,Add evidence_source for fig3,major,open,VAL-005,14_contracts/figure_contract.csv,fig3 row,Same as REV-002.,fig3 row has evidence_source.\nREV-007,Ensure valid output file for fig3 exists,major,open,VAL-006,14_contracts/figure_contract.csv / 08_figures/,fig3 row and file,Replace placeholder.,fig3_coefficients.png > 1KB.\nREV-008,Add evidence_source for fig4,major,open,VAL-007,14_contracts/figure_contract.csv,fig4 row,Same as REV-002.,fig4 row has evidence_source.\nREV-009,Ensure valid output file for fig4 exists,major,open,VAL-008,14_contracts/figure_contract.csv / 08_figures/,fig4 row and file,Replace placeholder.,fig4_pred_vs_actual.png > 1KB.\nREV-010,Resolve legacy open major/fail revision tasks,major,open,VAL-009+,,,Review and close/waive pre-existing major/fail tasks after fixes are applied.,All major/fail tasks in revision_tasks.csv are closed or waived."
    },
    {
      "path": "11_review/simulated_human_gate_log.csv",
      "operation": "write",
      "content": "stage_id,gate_id,agent_decision,evidence,residual_risk,formal_effect\nauto_review,human_gate_auto_review,hold,Missing full paper draft. Stage cannot proceed. Review comments and scorecard generated as fail.,Review cannot produce meaningful assessment. Risk of proceeding with incomplete validation.,none"
    }
  ],
  "unresolved": [
    {
      "issue": "Full paper draft missing (09_paper/paper.tex not found or empty).",
      "blocker": "paper_full stage must be executed first. Cannot review without draft."
    },
    {
      "issue": "All four figure files are 11-byte placeholders and figure_contract rows lack evidence_source and valid output paths.",
      "blocker": "Figures and figure_contract must be fixed before quality review can pass."
    },
    {
      "issue": "Legacy major/fail revision tasks remain open (VAL-009 to VAL-012).",
      "blocker": "Previous revision tasks must be addressed; review cannot close them without artifact fixes."
    }
  ]
}
