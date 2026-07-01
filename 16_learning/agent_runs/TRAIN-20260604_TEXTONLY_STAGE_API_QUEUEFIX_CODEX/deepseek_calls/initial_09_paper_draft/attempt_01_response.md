{
  "status": "blocked",
  "summary": "paper_draft 无法启动：必需的合同文件（claim_evidence_map, result_contract, figure_contract, formula_contract, citation_contract）缺失。请先完成上游阶段以生成合同。",
  "files": [
    {
      "path": "09_paper/missing_evidence_report.md",
      "operation": "write",
      "content": "# 缺失证据报告\n\n## 阶段\npaper_draft\n\n## 阻塞原因\n未找到以下必需的合同文件：\n- `14_contracts/claim_evidence_map.csv`\n- `14_contracts/result_contract.csv`\n- `14_contracts/figure_contract.csv`\n- `14_contracts/formula_contract.csv`\n- `14_contracts/citation_contract.csv`\n\n## 影响\n在合同就绪前，无法生成任何有证据支持的章节草稿。所有正式论断、结果、图表、公式和引用必须先在合同中登记。\n\n## 建议操作\n1. 检查工作流状态，确认 `results_freeze`、`figures` 等上游阶段已完成。\n2. 补齐缺失的合同文件。\n3. 重新调用 `paper_draft` 阶段。\n"
    }
  ],
  "unresolved": [
    {
      "issue": "合同文件缺失",
      "blocker": "缺失 claim_evidence_map.csv, result_contract.csv, figure_contract.csv, formula_contract.csv, citation_contract.csv"
    }
  ]
}
