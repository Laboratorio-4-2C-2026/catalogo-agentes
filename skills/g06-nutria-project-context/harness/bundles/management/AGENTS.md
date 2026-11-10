# NutrIA Management Bundle

At the primary management-task entrypoint, before interpreting any user prompt, ask exactly: **"¿Qué rol tenés: PM, PO, TL o QA?"** Wait for the answer. Then ask exactly: **"¿Qué querés hacer?"** and show only the options for that role:

- **PM:** Actualizar Gantt/forecast; reconciliar Linear y Gantt; revisar riesgos/dependencias; preparar reporte de avance.
- **PO:** Investigar problema; preparar/refinar backlog; definir criterios de aceptación; preparar evidencia de producto; revisar fidelidad visual con Stitch.
- **TL:** Preparar ADR/decisión técnica; revisar arquitectura o migración; analizar riesgo/dependencias; revisar PR o frontend con evidencia técnica.
- **QA:** Diseñar estrategia de calidad; revisar cobertura/evidencia; analizar riesgo de calidad; revisar PR/release.

Wait for the selected option before loading the matching task agent. Do this even when the initial prompt appears unambiguous.

This role/task gate belongs only to the primary management task. Task-specialized subagents are non-interactive handoffs: when the parent has already supplied the resolved role and task, they must not ask either gate again. They must start their assigned bounded work immediately; if the handoff is missing the resolved role or task, report a handoff error instead of asking the user.

PM owns delivery health and capacity; PO owns scope, priority and acceptance criteria; TL owns architecture and technical risk; QA owns quality evidence and release recommendation. All use the minimum required skills/MCPs, preserve human approval gates, and never deploy, merge, alter production data, or update a development issue status unless explicitly authorized.

## Task-specialized subagents

Use `portfolio_planner` for Gantt and forecast; `risk_dependency_manager` for RAID; `linear_tracker` for traceability; `product_discovery` and `backlog_steward` for PO work; `architecture_governor` for TL decisions; `quality_strategist` for QA strategy; `evidence_reporter` for reports; the project `review` skill for TL PR review; and `frontend_checker` for full Stitch/Agentation frontend fidelity checks. Spawn only independent bounded work and wait for results.


`frontend_checker` is the only profile that requires Agentation as a runtime tool. If Agentation is unavailable, report a blocker instead of substituting another endpoint. `frontend_checker` recommends only; PO, TL and QA keep approval authority. The `review` skill reports readiness evidence but never merges, deploys or approves.

## Gantt and Linear

Use `google-sheets-workflow.md`. Portfolio Planner updates the Gantt; Linear Tracker reconciles it with Linear. Links are read from `management/links.md`. Never let Sheets overwrite Linear workflow status.

## Project links

All agents and workflows read project resource URLs from `management/links.md`, including Google Sheets and Stitch. Add new user-authorized project links there and reference that file instead of duplicating URLs in instructions. If a required link is missing, ask for it and register it there. Never store credentials in this file.

## Inventory and context

Read `.ai/index.md` first. Use `.ai/delivery-and-linear.md` and `google-sheets-workflow.md` for planning; `.ai/architecture.md` for TL work; `.ai/quality-and-testing.md` for QA; `.ai/release-and-evidence.md` for reporting and PR/release review; and `.ai/frontend-and-stitch.md` for full frontend fidelity checks. The complete task-agent inventory and minimum MCP libraries are in `bundles/agent-libraries.json`.

## Required connector

Management requires the Google Drive connector described in `.nutria/connectors.json` after installation. It is relevant only to `portfolio_planner` and `linear_tracker`; authenticate it through the workspace, never through repository credentials.

## Persistent memory with Engram

Engram is mandatory persistent project memory. At session start call `mem_context`; before architecture-sensitive work call `mem_review` with `action: list` when available. For past-work questions, call `mem_context`, then `mem_search`, then `mem_get_observation`; treat memories marked `needs_review` as stale until verified and never mark them reviewed automatically.

Immediately call `mem_save` after an architecture or design decision, workflow or convention change, bug fix, configuration change, non-obvious discovery, established pattern, significant artifact update, or confirmed user direction. Save a short verb-first title, the appropriate type, `project` scope by default, a stable `topic_key` for evolving topics, and structured **What / Why / Where / Learned** content. Call `mem_save_prompt` before derived saves when the original prompt is observable. Do not overwrite unrelated topics and never store credentials, tokens, connection strings, PII, raw production data, or unreviewed transcripts.

Before declaring the session complete, call `mem_session_summary` with Goal, Instructions, Discoveries, Accomplished, Next Steps, and Relevant Files. After compaction, persist that summary first, recover context with `mem_context`, and only then continue.
