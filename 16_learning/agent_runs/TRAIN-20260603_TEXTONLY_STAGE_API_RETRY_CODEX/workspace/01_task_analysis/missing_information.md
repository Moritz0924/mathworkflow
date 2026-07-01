# Missing Information – Intake Blocker

- **Issue**: The problem statement, attachments, and any data files are absent from or unreadable in the workspace. No content was found in `00_problem/inbox/` or `03_data/raw/` (empty or inaccessible).
- **Impact**: Cannot extract problem facts such as objects, variables, units, spatial/temporal scope, objectives, constraints, or deliverables.
- **Required action**: Human must place the official contest problem description and all accompanying files (PDF, CSV, images, etc.) into `00_problem/inbox/` or `03_data/raw/` and re-trigger the intake stage.
- **Risk**: Without input, no downstream stage (EDA, task analysis, modeling) can proceed.
