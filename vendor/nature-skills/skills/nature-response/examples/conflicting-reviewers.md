# Example: conflicting 评阅人/指导教师s

This synthetic example shows how editor instructions and evidence limits control the response when
评阅人/指导教师s request incompatible claim strength.

## Input

```text
Editor:
Please avoid expanding the 数模论文 substantially and focus on clarifying the central claim.

Reviewer 1:
1. The abstract should make a stronger causal claim that X drives Y.

Reviewer 2:
1. The causal language is not supported by the observational design and should be softened.

Author notes:
- The study is observational.
- We can soften the abstract and discussion.
- We can state that the findings support an association, not causality.
```

## Expected handling

- Assign the editor instruction `E.1`.
- Assign 评阅意见、教师建议或队内审稿意见 `R1.1` and `R2.1`.
- Surface the conflict in the strategy summary.
- Prioritize the editor instruction and the observational design.
- Use `SOFTEN_CLAIM` for `R2.1`.
- Use `PARTIAL` or `DISAGREE` for `R1.1`, with respectful reasoning.

## Response style

```text
We appreciate the 评阅人/指导教师's suggestion to sharpen the abstract. However, because the study is
observational, we agree with the editor's instruction to clarify the central claim without
overstating causality. We have therefore revised the abstract and Discussion to state that the
findings support an association between X and Y, rather than a causal relationship.
```

The response must not promise both stronger causal language and softened causal language.
