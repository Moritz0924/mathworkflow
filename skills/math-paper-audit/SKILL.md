---
name: math-paper-audit
description: Use when auditing a Chinese mathematical-modeling paper for contest readiness, evidence traceability, figures, tables, formulas, validation, or academic-writing risks; use before a paper-review or final-submission gate, or when judging whether a draft is submission-ready rather than merely well-formatted.
---

# Math Paper Audit

## Overview

Audit the argument and evidence chain, not visual polish alone. Treat the active `AGENTS.md`, workflow state, contracts, and contest rules as authoritative. Internal scores are benchmarks, never award predictions.

Read [references/audit-rubric.md](references/audit-rubric.md) before scoring or issuing a verdict.

## Workflow

1. Identify the target: draft, final source, PDF, or submission package. Read `AGENTS.md`, `workflow_state.yaml`, `14_contracts/`, and `11_review/`.
2. Select the audit mode.

   | Condition | Mode | Result |
   |---|---|---|
   | Before `paper_review` | readiness | Evidence gaps only; no score |
   | `paper_review` or `finalize` | full audit | Scorecard and revisions |
   | Human gate pending | pre-gate | Verdict plus the remaining human action |

3. Pin one canonical source. Compare its date/hash and IDs with every draft, PDF, export manifest, and freeze record. Report version mismatch; never combine editions.
4. Run read-only checks when available:

   ```powershell
   python -B scripts/check_gates.py --no-write --json
   python -B -c "import sys; sys.path.insert(0,'scripts'); import validate_contracts as v; print(v.run_validation('current', write=False))"
   ```

   Record `not_run` and the reason if unavailable.
5. Trace each core conclusion: `claim_id → result/source → figure/table/formula/citation → canonical-paper location`. Match final numbers, units, names, figure labels, equation labels, and citations directly; a pass on an old draft is insufficient.
6. Score only after the source and evidence chain are complete. State `internal benchmark`, denominator, and unavailable measures.
7. Write only review artifacts and revision tasks when persistence is authorized by the active stage. Do not edit frozen papers, results, figures, models, or workflow state.

## Required report

```markdown
# 数学建模论文审计

- 审计对象：<canonical source + hash/date>
- 阶段与待确认闸门：<stage / gate>
- 审计模式：<readiness / full / pre-gate>
- 结论：<可提交候选 / 需修订 / 不可提交；不预测奖项>
- 内部评分：<x/100 或 未评分，理由>

## 硬闸门
| 检查 | 状态 | 证据 | 必要动作 |
|---|---|---|---|

## 论断与证据
| 论断/位置 | 结果与来源 | 图表/公式/引用 | 一致性 | 风险 |
|---|---|---|---|---|

## 量化质量
| 维度 | 得分 | 满分 | 依据与缺口 |
|---|---:|---:|---|

## 修订任务
| 严重级 | 目标位置 | 必须动作 | 验收方式 |
|---|---|---|---|

## 边界
<无法支持的结论、待人工确认事项、分数不等于奖项>
```

## Quick reference

| Check | Pass condition |
|---|---|
| Results | Frozen/usable contract entry and source file |
| Claims | Registered, matching evidence and bounded wording |
| Figures | Existing registered file, clear claim/source, final label matches |
| Formulas | Defined symbols and final label/meaning matches |
| Citations | Verified metadata; supports method/background, not invented results |
| Final artifact | Source, PDF, page count, review, export, and freeze describe one edition |

Use `fail`, `major`, `minor`, and `suggestion` consistently. `fail` blocks readiness; `major` needs closure or an explicit human waiver before “submission-ready.”

## Common mistakes

- Score an old draft while inspecting a newer TeX/PDF. Pin the canonical source first.
- Treat contract validation as semantic proof of final figure/equation labels. Compare final identifiers.
- Add decorative figures, tables, or formulas to meet a count. Require a distinct conclusion.
- Call an internal 85/90 benchmark an award prediction, or rewrite formal artifacts during an audit.

## Example

“内部审计为 88/100，达到可提交候选的数量基准；但最终 TeX 的 `fig:PF003` 未与 `figure_contract.csv` 的论断记录对应，因此结论为‘需修订’，不建议确认最终人工闸门。”
