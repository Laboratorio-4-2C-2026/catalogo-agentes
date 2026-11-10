# Google Sheets Gantt integration

Read the canonical Gantt and supporting-sheet URLs from `management/links.md`, the shared project link registry. Register new user-authorized links there before using them; do not duplicate URLs in workflow instructions.

Use the Google Drive/Sheets connector only after the workspace administrator has connected it. Portfolio Planner owns schedule edits; Linear Tracker owns reconciliation. Linear remains the execution truth; Google Sheets remains the schedule and forecast view. Every Gantt row must include its Linear project/issue key.

Reconcile weekly and before milestones: status comes from Linear/GitHub, while dates, dependencies and forecast live in the Gantt. Report mismatches before changing dates, scope or ownership.
