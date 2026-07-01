# Contract Bus Templates

The contract bus is the shared truth layer for v3.2-MVP. Every stage may create draft rows, but formal paper output can use only rows that are ready or frozen.

## Files

| File | Purpose | Primary producer | Primary consumer |
|---|---|---|---|
| `claim_evidence_map.csv` | Maps paper claims to result, citation, figure, or formula evidence | paper_draft | nature-writing, check_gates |
| `result_contract.csv` | Freezes numerical and qualitative results used by figures and paper | results_freeze | figures, paper_draft, polish |
| `figure_contract.csv` | Defines figure claims, evidence source, output paths, and paper usage | figures | nature-figure, LaTeX, check_gates |
| `formula_contract.csv` | Tracks formulas, symbols, assumptions, and section usage | model_route | paper_draft, polish |
| `citation_contract.csv` | Tracks citation support grade and metadata verification | literature | nature-citation, paper_draft |
| `artifact_freeze_registry.csv` | Records artifacts whose facts must not change after freeze | results_freeze, paper_full | polish, final gate |
| `polish_diff_check.csv` | Records protected atom changes after polishing | polish | check_gates |
| `revision_tasks.csv` | Converts reviewer comments into traceable tasks | auto_review | revision, final gate |
| `data_contract.yaml` | Optional data source and reproducibility contract | data | nature-data, submission |

## Status Values

Use one of:

- `draft`
- `ready`
- `frozen`
- `blocked`
- `closed`
- `waived`

## Severity Values

Use one of:

- `fail`
- `major`
- `minor`
- `suggestion`

## Support Grades

Use one of:

- `strong`
- `partial`
- `background`
- `limiting`
- `metadata_only`
- `none`
