{
  "status": "blocked",
  "summary": "Cannot execute codegen: required model route and data inputs missing; earlier stages must be completed first.",
  "files": [
    {
      "path": "11_review/stage_codegen_blocker.md",
      "operation": "write",
      "content": "# Stage Blocker: codegen\n\n- **Simulated stage**: codegen\n- **Date**: 2025-01-01 (simulated)\n- **Status**: blocked\n\n## Missing Prerequisites\n\n- `05_model/model_route.md` – not generated yet\n- `05_model/fallback_plan.md` – not generated yet\n- `03_data/` – data sources not confirmed\n\n## Workflow state\n\n- `current_stage`: intake\n- `codegen` is locked until prior stages (`task_analysis`, `eda`, `prior_retrieval`, `model_route`) are completed and gates passed.\n\n## Required action\n\nComplete the missing stages in order. Do not skip to codegen.\n"
    }
  ],
  "unresolved": [
    {
      "issue": "Pre-stage dependencies not satisfied for codegen",
      "blocker": "Missing model_route.md and confirmed data"
    }
  ]
}
