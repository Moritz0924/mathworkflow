# nature-response test rubric

Use this rubric to manually evaluate `nature-response` outputs against the Markdown fixtures.

## Completeness

Pass when:

- Every 评阅人/指导教师 comment receives a stable ID.
- Every ID appears in the tracker and response letter.
- Repeated concerns are cross-referenced rather than ignored.
- Ambiguous 评阅人/指导教师 boundaries are flagged.

Fail when:

- A comment is skipped.
- Two concerns are merged without traceability.
- A major concern receives only a polite acknowledgement.

## Traceability

Pass when:

- Every claimed 数模论文 change has a section, page, line, figure, table, supplement, or explicit placeholder.
- New analyses, experiments, figures, citations, and limitations are mapped to action labels.
- Missing locations are flagged rather than invented.

Fail when:

- The response claims a change without location or evidence.
- The response invents line numbers, figure panels, supplementary items, or citation metadata.

## Factuality

Pass when:

- Missing evidence is marked `AUTHOR_INPUT_NEEDED`.
- Quantitative details are used only when supplied by the author.
- Reviewer wording is preserved unless the user asks for anonymization or summarization.

Fail when:

- The response invents data, p-values, confidence intervals, sample sizes, accession details, 评阅人/指导教师 identities, or editor instructions.
- The response overstates unsupported causal or clinical claims.

## Tone

Pass when:

- The response is cooperative, concise, and evidence-forward.
- Disagreement is respectful and scientifically justified.
- Reviewer misunderstanding is framed as 数模论文 clarification when appropriate.

Fail when:

- The response accuses the 评阅人/指导教师 of error, incompetence, or misunderstanding.
- The response is excessively apologetic, defensive, or repetitive.
- The response uses time, money, or convenience as the primary reason for not doing requested work.

## Actionability

Pass when:

- The author can see what to change in the 数模论文.
- Missing information is listed as concrete author questions.
- Blocking or high-risk issues are visible before the draft letter.

Fail when:

- The output only produces prose and no action checklist.
- The author cannot identify what evidence is still needed.

## 数模论文-fit

Pass when:

- The output is organized as editor-readable point-by-point response material.
- All referee criticisms are seriously addressed, justified, or flagged.
- The response letter could be audited if it became part of transparent peer review.

Fail when:

- The output reads like generic language polishing.
- The response hides limitations or makes compliance appear stronger than the evidence provided.
