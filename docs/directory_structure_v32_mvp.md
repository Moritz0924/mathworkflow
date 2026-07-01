# v3.2-MVP 目录结构

这是在 v3.0 之上的增量补丁，不是完整重写。

```text
project_root/
├── AGENTS.md
├── config/
│   ├── execution_policy.yaml
│   ├── skill_enhancement.yaml
│   ├── contract_policy.yaml
│   ├── iteration_policy.yaml
│   └── prior_db_policy.yaml
├── 11_review/
│   ├── problem_reviewer_comments.md
│   ├── model_reviewer_comments.md
│   ├── code_reviewer_comments.md
│   ├── figure_reviewer_comments.md
│   ├── paper_reviewer_comments.md
│   ├── judge_reviewer_comments.md
│   ├── review_scorecard.csv
│   └── revision_tasks.csv
├── 13_prior_db/
│   ├── cards/
│   ├── fulltext_index/
│   └── screening/
├── 14_contracts/
│   ├── README.md
│   ├── claim_evidence_map.csv
│   ├── result_contract.csv
│   ├── figure_contract.csv
│   ├── formula_contract.csv
│   ├── citation_contract.csv
│   ├── artifact_freeze_registry.csv
│   ├── polish_diff_check.csv
│   ├── revision_tasks.csv
│   └── data_contract.yaml
├── 15_iteration_memory/
│   ├── round_01_summary.md
│   ├── round_02_summary.md
│   ├── decision_log.md
│   └── task_closure_log.md
├── 12_export/
│   └── pptx/
├── vendor/
│   └── nature-skills/
│       ├── VERSION.txt
│       └── skills/
│           ├── nature-figure/
│           ├── nature-writing/
│           ├── nature-polishing/
│           ├── nature-citation/
│           ├── nature-data/
│           ├── nature-reader/
│           ├── nature-response/
│           ├── nature-paper2ppt/
│           └── nature-academic-search/
└── scripts/
    ├── validate_contracts.py
    ├── retrieve_prior_cards.py
    ├── check_prior_copy_risk.py
    ├── auto_review.py
    ├── build_revision_tasks.py
    ├── apply_revision_tasks.py
    ├── check_revision_closure.py
    └── polish_diff_check.py
```

## 保留 v3.0 内容

除非迁移脚本明确处理，否则保留现有文件夹和文件：

- `00_problem/`
- `01_task_analysis/`
- `02_literature/`
- `02_latex_template/`
- `03_data/`
- `04_eda/`
- `05_model/`
- `06_code/`
- `07_results/`
- `08_figures/`
- `09_paper/`
- `10_ai_logs/`
- `11_dashboard/`
- `12_submission/`
- `13_sample_prior/`

## 重命名或桥接

不要删除 `13_sample_prior/`。它是遗留来源，后续可桥接到 `13_prior_db/`。
