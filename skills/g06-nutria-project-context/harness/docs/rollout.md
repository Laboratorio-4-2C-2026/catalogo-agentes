# NutrIA controlled rollout

The team decides when each capability becomes active. Installation makes the assets available; it does not grant approval to change scope, data, priorities, or production.

## Order

1. **Foundation**: `nutria-project-context`, `engram-memory-protocol`, Linear MCP, and `delivery-manager`.
2. **Product delivery**: `product-owner`, `product-backlog`, `linear-delivery-ops`, and `time-reporting`.
3. **Architecture and data**: `technical-lead`, `architecture-adr`, `backend-engineer`, `neon-prisma-safety`.
4. **Design and frontend**: Stitch MCP, `stitch-ui-workflow`, `frontend-engineer`.
5. **AI feature**: `meal-plan-ai-engineer`, `meal-plan-ai-safety`.
6. **Quality and release**: `qa-automation`, `qa-playwright-evidence`, `pr-release-guardian`, `pr-release-guardrails`.
7. **Final evidence**: `documentation-evidence` agent and skill.

## Authorization model

| Change | Required human approval |
|---|---|
| Scope, priority, dates, assignee | PM or PO |
| ADR, API contract, migration, release | TL |
| Test pass, defect severity, release evidence | QA |
| Linear mutation by an agent | Responsible role explicitly approves it |
| Neon query or schema change | TL, development branch only |
| Stitch artifact becomes implementation target | PO |

## Linear data model

Create one initiative: **NutrIA MVP 2026**. Use projects for Foundation & Identity, Nutritional Profile & Preferences, Meal Plans with AI, Recipes/Shopping/Adherence, and Quality/Release/Documentation. Use weekly cycles and the statuses `Backlog`, `Ready`, `In Progress`, `In Review`, `QA`, `Done`, `Blocked`.

Track **estimate** in Linear for capacity/complexity. Track **actual hours** in a linked tracker such as Harvest. Report both, but never treat hours as a performance score.
