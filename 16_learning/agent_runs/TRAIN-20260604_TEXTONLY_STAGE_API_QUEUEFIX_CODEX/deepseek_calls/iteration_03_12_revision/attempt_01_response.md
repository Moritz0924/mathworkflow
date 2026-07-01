{
  "status": "blocked",
  "summary": "Blocked on missing current workspace files needed to execute revision tasks accurately. Requesting current content of key artifacts to avoid data loss and ensure contract validity.",
  "files": [],
  "unresolved": [
    {
      "issue": "Unable to view current figure_contract.csv content, cannot safely add result_id/evidence_source per task VAL-003/005/007/009 without risk of corrupting existing rows or violating schema.",
      "blocker": "Need read access to 14_contracts/figure_contract.csv (full content) and any existing figure files mapping."
    },
    {
      "issue": "Cannot refresh final_submit_paper.md from a topic-aligned full_draft (VAL-002) without knowing current paper/full_draft state and the expected 'required section signal' definition.",
      "blocker": "Need read access to 09_paper/final_submit_paper.md, 09_paper/full_draft.md (if exists), and the validation rule for training_final_paper_missing_section_signal."
    },
    {
      "issue": "Cannot update revision_tasks.csv to mark tasks closed without knowing the current task schema, IDs, and existing statuses.",
      "blocker": "Need read access to 14_contracts/revision_tasks.csv and 11_review/review_scorecard.csv."
    },
    {
      "issue": "Cannot generate missing figure files (VAL-004/006/008/010) without knowing the exact figure IDs, expected file formats, and whether they should be derived from actual results.",
      "blocker": "Need the current figure_contract.csv rows specifying figure_id and file_path so that placeholder files match the contract exactly."
    },
    {
      "issue": "Cannot align paper figure references with figure_contract ids (VAL-011/012/013) without the current paper text and contract ids, risking mismatched or broken references.",
      "blocker": "Need full text of 09_paper/final_submit_paper.md and the complete list of figure_id from figure_contract.csv."
    }
  ]
}
