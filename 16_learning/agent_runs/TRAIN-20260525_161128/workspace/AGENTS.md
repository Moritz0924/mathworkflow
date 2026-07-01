# Math Modeling Workflow v3.2-MVP Agent Rules

This repository uses a controlled, deep-sequential math modeling workflow.
The workflow controller owns state. Codex executes tasks. nature-skills are specialist tools. The prior database is a coach, not an answer source. Reviewers create review artifacts only.

## Authority Order

1. Human final gate
2. Workflow controller and stage state
3. Contract bus and validation scripts
4. Codex executor
5. nature-skills specialist guidance
6. Prior DB retrieval notes

If two rules conflict, follow the higher authority.

## Hard Constraints

- Use `deep_sequential` mode only.
- Do not run stages in parallel.
- Do not skip human gates.
- Do not generate the full paper before result contracts exist.
- Do not write result analysis without model outputs and `result_contract.csv` entries.
- Do not cite a figure unless it is registered in `figure_contract.csv` and the file exists.
- Do not polish by changing numbers, formulas, labels, references, citations, model names, or result meanings.
- Do not copy text from prior papers, including abstracts, body paragraphs, captions, tables, and conclusions.
- Do not allow reviewer agents to directly edit deliverables.
- Do not treat nature-skills as the workflow controller.

## Stage-to-Skill Routing

| Stage | Allowed skills | Role | Required contract before use |
|---|---|---|---|
| literature | nature-academic-search, nature-citation | Search and citation verification | `citation_contract.csv` scaffold |
| data | nature-data | Data source and reproducibility statement | `data_contract.yaml` if present |
| prior_retrieval | nature-reader | Extract experience cards only | `prior_db_policy.yaml` |
| figures | nature-figure | Figure argument design and export quality | `result_contract.csv`, `figure_contract.csv` |
| paper_draft | nature-writing | Section-level argument drafting | `claim_evidence_map.csv`, `result_contract.csv`, `figure_contract.csv` |
| paper_full | nature-writing | Cross-section coherence | Same as paper_draft |
| auto_review | nature-response style logic | Comment triage and traceability | Draft paper and contracts |
| polish | nature-polishing | Fact-preserving language polish | `artifact_freeze_registry.csv` |
| final_export | nature-paper2ppt | Post-final presentation deck | Human-confirmed final paper |

## Contract Bus Rules

All formal claims must be represented in `14_contracts/claim_evidence_map.csv`.
All numerical results used in the paper must be represented in `14_contracts/result_contract.csv`.
All paper figures must be represented in `14_contracts/figure_contract.csv`.
All important formulas must be represented in `14_contracts/formula_contract.csv`.
All citations must be represented in `14_contracts/citation_contract.csv`.
All frozen artifacts must be represented in `14_contracts/artifact_freeze_registry.csv`.
All polish changes must pass `14_contracts/polish_diff_check.csv`.
All reviewer issues must be represented in `14_contracts/revision_tasks.csv`.

## Reviewer Permissions

Reviewer agents may write:

- `11_review/*_reviewer_comments.md`
- `11_review/review_scorecard.csv`
- `11_review/revision_tasks.csv`
- `14_contracts/revision_tasks.csv`

Reviewer agents may not modify:

- `02_latex_template/`
- `05_model/`
- `06_code/`
- `07_results/`
- `08_figures/`
- `09_paper/`
- `12_submission/`

## Prior DB Rules

Before solving, prior DB retrieval may output only:

- problem type experience
- common model families
- common figure types
- common scoring risks

After a first complete draft exists, prior DB retrieval may additionally output:

- structure comparison
- argument gap comparison
- figure density comparison
- scoring risk comparison

Forbidden:

- copying prior paper text
- reusing prior captions
- reusing prior abstracts or conclusions
- directly copying historical tables
- treating prior papers as ground-truth answers

## nature-skills Integration Rules

- Copy whole `skills/nature-*` directories, not just `SKILL.md`.
- Keep project-vendored skills under `vendor/nature-skills/skills/`.
- Sync to `~/.codex/skills/` only when running Codex locally.
- Pin the nature-skills commit in `vendor/nature-skills/VERSION.txt` when possible.
- Treat skills as stage-local specialists. Their outputs must still pass contract validation.

## Final Gate

A final deliverable is allowed only when:

- `scripts/check_gates.py` passes.
- `scripts/validate_contracts.py` passes.
- no fail-level item exists in `11_review/review_scorecard.csv`.
- all required revision tasks are closed or explicitly waived by a human.
- the human final gate is confirmed.
