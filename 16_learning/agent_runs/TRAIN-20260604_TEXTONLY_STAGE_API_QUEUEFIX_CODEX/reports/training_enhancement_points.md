# Training Enhancement Points (final_export)

## System
- SYS-001: Workflow controller should enforce stage lockout more strictly when preconditions not met. Currently, the controller may allow final_export despite open fail items. A stricter gate would prevent wasting compute on incomplete workflows.

## Prompt
- PROMPT-001: The final_export stage prompt should include fallback instructions when `09_paper/full_draft.md` is not accessible for copying. It could direct the agent to generate a placeholder and raise a blocker.
- PROMPT-002: The agent currently lacks a mechanism to read files from allowed paths. Adding a `read` operation to the file-action protocol would enable stages like final_export to access required upstream artifacts.

## Gate
- GATE-001: The simulated human gate logging could be automated. Every stage gate should log a row with `formal_effect=none` automatically, reducing manual overhead.
