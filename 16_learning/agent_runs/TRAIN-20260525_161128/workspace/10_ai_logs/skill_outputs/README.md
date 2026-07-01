# Skill Output Archive

This directory is the P1 archive layer for specialist skill calls.

Specialist skills are not allowed to write directly into workflow contracts,
frozen artifacts, final paper files, scripts, or workflow state. Every skill
call must first be archived here, then promoted only after validation and, when
required, human confirmation.

## Canonical archive path

```text
10_ai_logs/skill_outputs/<stage_id>/<skill_id>/<call_id>/
```

Each call directory must contain:

```text
input_manifest.yaml
raw_output.md
promotion_notes.md
```

Recommended optional files:

```text
policy_snapshot.yaml
contract_snapshot_refs.md
validation_stdout.txt
validation_stderr.txt
human_decision.md
```

## Call directory naming

Use a stable call id:

```text
SKILL-<stage_id>-<skill_id>-<YYYYMMDDTHHMMSSZ>
```

Example:

```text
10_ai_logs/skill_outputs/figures/nature-figure/SKILL-figures-nature-figure-20260523T132000Z/
```

## Promotion rule

Raw skill output is advisory. It becomes usable only after a promotion note
records:

1. the output type,
2. the target file,
3. contract bindings,
4. validation status,
5. human decision when required.

No promotion note means no downstream use.
