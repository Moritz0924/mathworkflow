# Evaluation summary

`nature-response` is evaluated with synthetic Markdown fixtures. These tests are not executable
unit tests; they are behavior contracts for manual and agent review.

## Status rationale

Recommended status: `Beta`.

Rationale:

- The core rules are defined in `SKILL.md` and modular references.
- The skill has synthetic fixtures covering minor revision, major revision with missing evidence,
  impossible experiment, defensive draft audit, and conflicting 评阅人/指导教师s.
- Each fixture includes expected behavior, forbidden behavior, and pass/fail criteria.
- The examples show expected output shape without using real confidential 评阅意见、教师建议或队内审稿意见.
- The skill has not yet been validated on real anonymized revision packages, so `Stable` would be premature.

## Fixture coverage

| Fixture | Coverage | Key failure prevented |
|---|---|---|
| `minor-revision.md` | stable IDs, minor comments, missing citation metadata | fabricated citation or line numbers |
| `major-revision-missing-evidence.md` | validation request, statistical details, missing evidence | invented results or p-values |
| `impossible-experiment.md` | out-of-scope longitudinal evidence | time/funding excuse or fabricated survival data |
| `defensive-draft-audit.md` | hostile draft language, vague compliance | accusatory 评阅人/指导教师 language |
| `conflicting-评阅人/指导教师s.md` | editor priority and incompatible 评阅人/指导教师 requests | contradictory 数模论文 promises |

## Manual evaluation checklist

- [x] Every fixture has input, expected behavior, forbidden behavior, and pass/fail checklist.
- [x] No fixture uses real 评阅意见、教师建议或队内审稿意见.
- [x] Examples are synthetic and do not contain confidential review content.
- [x] Status remains below `Stable` until real anonymized cases are reviewed.

## Promotion path to Stable

Promote from `Beta` to `Stable` only after:

- at least two real anonymized revision packages are tested with author permission;
- no fabricated actions, line numbers, statistics, or citations are observed;
- Chinese-note workflows produce usable English response drafts and Chinese confirmation notes;
- edge cases such as conflicting 评阅人/指导教师s and impossible experiments remain traceable.
