{
  "status": "blocked",
  "summary": "Auto-review blocked: paper draft and required contracts are missing. Revision tasks created to unblock.",
  "files": [
    {
      "path": "11_review/simulated_human_gate_log.csv",
      "operation": "write",
      "content": "stage_id,gate_id,agent_decision,evidence,residual_risk,formal_effect\nauto_review,gate-001,blocked,No paper draft or contracts found in workspace; unable to perform review.,Review cannot start; must return to paper_full.,none\n"
    },
    {
      "path": "11_review/blocker_reviewer_comments.md",
      "operation": "write",
      "content": "# Blocker Review Comments\n\n## Summary\n\nThe auto-review stage cannot proceed because the required inputs are not available in the workspace:\n- Full paper draft (`09_paper/`)\n- `14_contracts/claim_evidence_map.csv`\n- `14_contracts/result_contract.csv`\n- `14_contracts/figure_contract.csv`\n\n## Recommended Action\nReturn to the `paper_full` stage to generate a complete draft and populate the required contracts. Once these are available, re-run the `auto_review` stage.\n\n## Review Perspectives (Placeholder)\n- Problem: Not assessed\n- Data: Not assessed\n- Model: Not assessed\n- Results: Not assessed\n- Figures: Not assessed\n- Writing: Not assessed\n- Scoring: Not assessed\n"
    },
    {
      "path": "11_review/review_scorecard.csv",
      "operation": "write",
      "content": "aspect,score,max_score,risk_level,fail_level,comment\ndraft_presence,0,1,critical,fail,Full paper draft is missing.\nclaim_evidence_map,0,1,critical,fail,Contract file missing.\nresult_contract,0,1,critical,fail,Contract file missing.\nfigure_contract,0,1,critical,fail,Contract file missing.\noverall,0,4,critical,fail,Review blocked until all inputs are provided.\n"
    },
    {
      "path": "14_contracts/revision_tasks.csv",
      "operation": "write",
      "content": "task_id,source_comment_id,target_artifact,target_location,required_action,acceptance_check,linked_contract_ids,status,risk_level\ntask-001,blocker-001,09_paper/paper_draft.tex,Entire draft,Generate complete paper draft with all sections and register claims/figures/results in respective contracts.,Presence of draft and all required contracts verified; all contracts pass validation.,claim_evidence_map.csv|result_contract.csv|figure_contract.csv,open,critical\n"
    },
    {
      "path": "10_ai_logs/auto_review_stage_summary.md",
      "operation": "write",
      "content": "# Auto Review Stage Summary\n\n- Status: Blocked\n- Reason: Missing paper draft and contracts.\n- Next step: Execute paper_full stage.\n"
    }
  ],
  "unresolved": [
    {
      "issue": "Missing paper draft and required contracts for review.",
      "blocker": "Cannot proceed with review without full draft and contracts."
    }
  ]
}
