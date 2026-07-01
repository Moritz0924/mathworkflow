{
  "status": "blocked",
  "summary": "auto_review blocked: missing required paper draft and contracts. Generated blocker artifacts and simulated gate log.",
  "files": [
    {
      "path": "11_review/simulated_human_gate_log.csv",
      "operation": "write",
      "content": "stage_id,gate_id,agent_decision,evidence,residual_risk,formal_effect\nauto_review,stage_start,blocked,Missing draft in 09_paper/; cannot perform review,High,none\n"
    },
    {
      "path": "11_review/review_scorecard.csv",
      "operation": "write",
      "content": "reviewer_id,perspective,item,severity,description,recommendation\nblocker,all,missing_draft,critical,Required paper draft not found in 09_paper/; all perspectives unable to review,Execute paper_full stage to generate draft before retrying auto_review\n"
    },
    {
      "path": "14_contracts/revision_tasks.csv",
      "operation": "write",
      "content": "task_id,source_comment_id,target_artifact,target_location,required_action,acceptance_check,status,linked_contract_ids,notes\nREV-001,auto_review_missing_draft,09_paper/,/,Execute paper_full stage to generate a complete draft matching the problem statement,Draft exists in 09_paper/ and passes preliminary structure checks,blocked,N/A,auto_review cannot proceed without draft\n"
    },
    {
      "path": "11_review/blocker_reviewer_comments.md",
      "operation": "write",
      "content": "# Reviewer Comments: Blocker\n\n## Summary\nThe auto_review stage cannot proceed because the required full paper draft is missing from the expected location (09_paper/). Additionally, core contracts (claim_evidence_map.csv, result_contract.csv, figure_contract.csv) have not been verified. Without these inputs, no meaningful review can be conducted.\n\n## Required Pre-conditions\n1. Complete paper_full stage to produce a draft in 09_paper/.\n2. Ensure 14_contracts/ contains claim_evidence_map.csv, result_contract.csv, and figure_contract.csv.\n3. Validate contracts using `scripts/validate_contracts.py`.\n\n## Recommended Action\nStop auto_review and roll back to paper_full stage. Update workflow state accordingly.\n"
    },
    {
      "path": "reports/training_enhancement_points.csv",
      "operation": "write",
      "content": "id,stage,finding,impact,suggestion\nTE-001,auto_review,Missing full draft input in sandbox environment prevents review execution,Blocks auto_review stage from completing; may require workflow adjustments,Consider adding a minimal draft fixture or ensuring prior stages complete before calling auto_review in training sandboxes.\n"
    },
    {
      "path": "reports/training_enhancement_points.md",
      "operation": "write",
      "content": "# Training Enhancement Points\n\n- **TE-001** (auto_review): Missing full draft input in sandbox environment prevents review execution. Impact: Blocks auto_review stage. Suggestion: Add minimal draft fixture or ensure prior stages complete before auto_review.\n"
    }
  ],
  "unresolved": [
    {
      "issue": "Missing paper draft and potentially required contracts",
      "blocker": "Cannot execute auto_review without complete paper draft (09_paper/) and required contracts (claim_evidence_map.csv, etc.)."
    }
  ]
}
