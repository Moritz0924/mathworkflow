{
  "status": "blocked",
  "summary": "Auto-review blocked: required full paper draft and contracts are missing from workspace.",
  "files": [
    {
      "path": "11_review/initial_reviewer_comments.md",
      "operation": "write",
      "content": "# Prerequisite Check: Auto Review Blocked\n\n## Summary\nAuto-review stage cannot proceed because the full paper draft is missing from `09_paper/`. Additionally, required contract files (`claim_evidence_map.csv`, `result_contract.csv`, `figure_contract.csv`) have not been verified.\n\n## Expected Inputs\n- Full paper draft (likely `09_paper/full_draft.tex` or similar)\n- `14_contracts/claim_evidence_map.csv`\n- `14_contracts/result_contract.csv`\n- `14_contracts/figure_contract.csv`\n\n## Current Status\nNone of the above inputs were found in the workspace at the time of this review attempt. Without the draft and contracts, the multi-perspective review (problem, model, data, results, figures, writing, scoring) cannot be performed.\n\n## Recommended Action\n- Execute `paper_full` stage to generate the full paper draft and update all contracts.\n- Then re-run `auto_review` stage.\n\n## Blocker Severity: Fail\n"
    },
    {
      "path": "11_review/review_scorecard.csv",
      "operation": "write",
      "content": "item_id,category,aspect,score,max_score,status,comments\nREV-001,prerequisites,all required inputs,0,10,fail,\"Missing full paper draft and contracts; auto-review cannot proceed\"\n"
    },
    {
      "path": "14_contracts/revision_tasks.csv",
      "operation": "write",
      "content": "task_id,stage,source_comment,target_artifact,required_action,acceptance_check,priority,status\nREV-001,paper_full,auto-review prerequisite check,\"full paper draft, contracts\",\"Generate the full paper draft and update all contracts (claim_evidence_map.csv, result_contract.csv, figure_contract.csv) before retrying auto_review.\",\"Existence of 09_paper/full_draft.tex and 14_contracts/ files with valid content.\",blocker,open\n"
    },
    {
      "path": "11_review/simulated_human_gate_log.csv",
      "operation": "write",
      "content": "stage_id,gate_id,agent_decision,evidence,residual_risk,formal_effect\nauto_review,review_prerequisites_check,block; auto_review cannot run,\"Missing full paper draft and contracts; no files in 09_paper/ or 14_contracts/ (unverified).\",High,none\n"
    }
  ],
  "unresolved": [
    {
      "issue": "Full paper draft and contract files missing",
      "blocker": "Execute paper_full stage before auto_review; current workspace appears empty or incomplete."
    }
  ]
}
