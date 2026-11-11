# NutrIA harness catalog submission

This submission includes every skill and native bundle agent from [https://github.com/nutria-lab/ai-harness](https://github.com/nutria-lab/ai-harness/tree/4e3652d4dbf38d8746626401126aa0e1b4139c89) at commit `4e3652d4dbf38d8746626401126aa0e1b4139c89` (package version 1.0.4). It contains **26 skills and 31 agents**, with the source instructions preserved. It intentionally excludes the harness installer, tool bootstrapper, npm publication workflow and local state.

## Team ownership

Ownership follows the requested team roles for this submission. It does not claim that the assignee originally authored every upstream instruction. Original source metadata, native TOML, source revision and SHA-256 hashes remain available in [the manifest](harness/manifest.json). Product Design workflows were vendored into the source harness from OpenAI; this submission preserves their source content and provenance.

| Team member | Role | Focus | Agents | Skills | Total |
| --- | --- | --- | ---: | ---: | ---: |
| Felipe Fernandez Cronenbold (`sonpipe0`) | PM | Delivery, planning, reporting and operational continuity | 9 | 8 | 17 |
| Tomás Alcázar (`tomasalcazar`) | PO | Product discovery, backlog and design validation | 3 | 11 | 14 |
| Camila Catalini (`CCatalini`) | TL | Architecture, implementation and technical integration | 11 | 5 | 16 |
| Tais Marambio (`TaisMarambio`) | QA | Testing, quality evidence and change review | 8 | 2 | 10 |

## Shared context and dependencies

These are catalog adaptations, not independent self-contained runtimes. Use the original runtime names from `metadata.source_name` when working with the native profiles. The `g06-` names identify catalog records.

- Read `harness/AGENTS.md` and `harness/.ai/index.md`, then only the relevant knowledge module. Submission ownership does not change runtime role gates or human approval authority: Felipe maintains the management review/release workflows, while their native TL/QA approval requirements remain in force.
- Shared bundle policies and library mappings are in `harness/bundles/`. Native TOML profiles are adjacent to each catalog agent card; the manifest maps each original path to its catalog location.
- Skill-local support files remain adjacent to their skill card. Shared Product Design references and prototype assets are in `harness/references/` and `harness/product-design/`.
- Original project-relative paths in instructions assume the source harness layout. For manual integration, assemble the original paths from the manifest: use native TOML files for `bundles/*/agents/`, skill cards and their local support for `skills/<source_name>/`, and shared support relative to `harness/`. Review tool discovery and role policies in the target project. No automatic installation is included.
- Product Design instructions are preserved, including upstream references to optional Figma inputs. NutrIA-specific rules in the shared critical overrides keep Stitch as the design source; do not introduce a Figma workflow for NutrIA.
- MCP definitions are reference configurations. Authenticate services in the target environment. Replace `__NUTRIA_ENGRAM_COMMAND__` and `__NUTRIA_CODEGRAPH_COMMAND__` in templates with actual local executable paths when configuring those tools manually.
- Agentation is required by the frontend checker workflows. The source profiles differ in how they describe Agentation availability; follow the selected native profile and report missing capabilities rather than inventing endpoints.
- The management role/task gate belongs to the primary management entrypoint. Non-interactive review handoffs use their supplied role and task as defined in the native profiles.
- Maturity defaults to `experimental` because per-piece real-project use has not been confirmed. Listed tools reflect source-supported targets, not proof that every piece has been executed in all of them.

New dependency taxonomy values used by this submission are `neon`, `stitch`, `codegraph` and `agentation`; these name real dependencies declared by the source harness. Catalog taxonomies and generated site files are left to the catalog workflows.

## Validation evidence

- Source `npm run validate`: passed. The source validator prints a stale count of 25 skills; the inventory and manifest include the additional `review` skill for a total of 26.
- Source `npm test`: 17 passed, 3 failed at the unchanged source commit. The failures are management guidance assertions in `tests/installer-idempotency.test.mjs` expecting prefixed native names such as `nutria_management_portfolio_planner`, `nutria_management_linear_tracker` and `nutria_management_quality_strategist` in the generated guidance.
- Catalog checks, source-preservation checks and dry-run evidence are recorded in the PR description.

## Full inventory

### Felipe Fernandez Cronenbold — PM

| Type | Catalog entry | Original source |
| --- | --- | --- |
| skill | [g06-documentation-evidence](../../skills/g06-documentation-evidence/SKILL.md) | `skills/documentation-evidence/SKILL.md` |
| skill | [g06-engram-memory-protocol](../../skills/g06-engram-memory-protocol/SKILL.md) | `skills/engram-memory-protocol/SKILL.md` |
| skill | [g06-gentle-ai-engram](../../skills/g06-gentle-ai-engram/SKILL.md) | `skills/gentle-ai-engram/SKILL.md` |
| skill | [g06-linear-delivery-ops](../../skills/g06-linear-delivery-ops/SKILL.md) | `skills/linear-delivery-ops/SKILL.md` |
| skill | [g06-nutria-project-context](../../skills/g06-nutria-project-context/SKILL.md) | `skills/nutria-project-context/SKILL.md` |
| skill | [g06-pr-release-guardrails](../../skills/g06-pr-release-guardrails/SKILL.md) | `skills/pr-release-guardrails/SKILL.md` |
| skill | [g06-review](../../skills/g06-review/SKILL.md) | `skills/review/SKILL.md` |
| skill | [g06-time-reporting](../../skills/g06-time-reporting/SKILL.md) | `skills/time-reporting/SKILL.md` |
| agente | [g06-development-linear-time-registration](../../agentes/g06-development-linear-time-registration/g06-development-linear-time-registration.md) | `bundles/development/agents/linear-time-registration.toml` |
| agente | [g06-management-evidence-reporter](../../agentes/g06-management-evidence-reporter/g06-management-evidence-reporter.md) | `bundles/management/agents/evidence-reporter.toml` |
| agente | [g06-management-linear-tracker](../../agentes/g06-management-linear-tracker/g06-management-linear-tracker.md) | `bundles/management/agents/linear-tracker.toml` |
| agente | [g06-management-portfolio-planner](../../agentes/g06-management-portfolio-planner/g06-management-portfolio-planner.md) | `bundles/management/agents/portfolio-planner.toml` |
| agente | [g06-management-review-readability](../../agentes/g06-management-review-readability/g06-management-review-readability.md) | `bundles/management/agents/review-readability.toml` |
| agente | [g06-management-review-reliability](../../agentes/g06-management-review-reliability/g06-management-review-reliability.md) | `bundles/management/agents/review-reliability.toml` |
| agente | [g06-management-review-resilience](../../agentes/g06-management-review-resilience/g06-management-review-resilience.md) | `bundles/management/agents/review-resilience.toml` |
| agente | [g06-management-review-risk](../../agentes/g06-management-review-risk/g06-management-review-risk.md) | `bundles/management/agents/review-risk.toml` |
| agente | [g06-management-risk-dependency-manager](../../agentes/g06-management-risk-dependency-manager/g06-management-risk-dependency-manager.md) | `bundles/management/agents/risk-dependency-manager.toml` |

### Tomás Alcázar — PO

| Type | Catalog entry | Original source |
| --- | --- | --- |
| skill | [g06-audit](../../skills/g06-audit/SKILL.md) | `skills/audit/SKILL.md` |
| skill | [g06-get-context](../../skills/g06-get-context/SKILL.md) | `skills/get-context/SKILL.md` |
| skill | [g06-ideate](../../skills/g06-ideate/SKILL.md) | `skills/ideate/SKILL.md` |
| skill | [g06-image-to-code](../../skills/g06-image-to-code/SKILL.md) | `skills/image-to-code/SKILL.md` |
| skill | [g06-index](../../skills/g06-index/SKILL.md) | `skills/index/SKILL.md` |
| skill | [g06-product-backlog](../../skills/g06-product-backlog/SKILL.md) | `skills/product-backlog/SKILL.md` |
| skill | [g06-research](../../skills/g06-research/SKILL.md) | `skills/research/SKILL.md` |
| skill | [g06-share](../../skills/g06-share/SKILL.md) | `skills/share/SKILL.md` |
| skill | [g06-stitch-ui-workflow](../../skills/g06-stitch-ui-workflow/SKILL.md) | `skills/stitch-ui-workflow/SKILL.md` |
| skill | [g06-url-to-code](../../skills/g06-url-to-code/SKILL.md) | `skills/url-to-code/SKILL.md` |
| skill | [g06-user-context](../../skills/g06-user-context/SKILL.md) | `skills/user-context/SKILL.md` |
| agente | [g06-management-backlog-steward](../../agentes/g06-management-backlog-steward/g06-management-backlog-steward.md) | `bundles/management/agents/backlog-steward.toml` |
| agente | [g06-management-frontend-checker](../../agentes/g06-management-frontend-checker/g06-management-frontend-checker.md) | `bundles/management/agents/frontend-checker.toml` |
| agente | [g06-management-product-discovery](../../agentes/g06-management-product-discovery/g06-management-product-discovery.md) | `bundles/management/agents/product-discovery.toml` |

### Camila Catalini — TL

| Type | Catalog entry | Original source |
| --- | --- | --- |
| skill | [g06-architecture-adr](../../skills/g06-architecture-adr/SKILL.md) | `skills/architecture-adr/SKILL.md` |
| skill | [g06-codegraph-guidance](../../skills/g06-codegraph-guidance/SKILL.md) | `skills/codegraph-guidance/SKILL.md` |
| skill | [g06-google-modern-web-guidance](../../skills/g06-google-modern-web-guidance/SKILL.md) | `skills/google-modern-web-guidance/SKILL.md` |
| skill | [g06-meal-plan-ai-safety](../../skills/g06-meal-plan-ai-safety/SKILL.md) | `skills/meal-plan-ai-safety/SKILL.md` |
| skill | [g06-neon-prisma-safety](../../skills/g06-neon-prisma-safety/SKILL.md) | `skills/neon-prisma-safety/SKILL.md` |
| agente | [g06-development-backend-designer](../../agentes/g06-development-backend-designer/g06-development-backend-designer.md) | `bundles/development/agents/backend-designer.toml` |
| agente | [g06-development-backend-explorer](../../agentes/g06-development-backend-explorer/g06-development-backend-explorer.md) | `bundles/development/agents/backend-explorer.toml` |
| agente | [g06-development-backend-implementer](../../agentes/g06-development-backend-implementer/g06-development-backend-implementer.md) | `bundles/development/agents/backend-implementer.toml` |
| agente | [g06-development-backend-review-readability](../../agentes/g06-development-backend-review-readability/g06-development-backend-review-readability.md) | `bundles/development/agents/backend-review-readability.toml` |
| agente | [g06-development-backend-review-reliability](../../agentes/g06-development-backend-review-reliability/g06-development-backend-review-reliability.md) | `bundles/development/agents/backend-review-reliability.toml` |
| agente | [g06-development-backend-review-resilience](../../agentes/g06-development-backend-review-resilience/g06-development-backend-review-resilience.md) | `bundles/development/agents/backend-review-resilience.toml` |
| agente | [g06-development-backend-review-risk](../../agentes/g06-development-backend-review-risk/g06-development-backend-review-risk.md) | `bundles/development/agents/backend-review-risk.toml` |
| agente | [g06-development-frontend-designer](../../agentes/g06-development-frontend-designer/g06-development-frontend-designer.md) | `bundles/development/agents/frontend-designer.toml` |
| agente | [g06-development-frontend-explorer](../../agentes/g06-development-frontend-explorer/g06-development-frontend-explorer.md) | `bundles/development/agents/frontend-explorer.toml` |
| agente | [g06-development-frontend-implementer](../../agentes/g06-development-frontend-implementer/g06-development-frontend-implementer.md) | `bundles/development/agents/frontend-implementer.toml` |
| agente | [g06-management-architecture-governor](../../agentes/g06-management-architecture-governor/g06-management-architecture-governor.md) | `bundles/management/agents/architecture-governor.toml` |

### Tais Marambio — QA

| Type | Catalog entry | Original source |
| --- | --- | --- |
| skill | [g06-design-qa](../../skills/g06-design-qa/SKILL.md) | `skills/design-qa/SKILL.md` |
| skill | [g06-qa-playwright-evidence](../../skills/g06-qa-playwright-evidence/SKILL.md) | `skills/qa-playwright-evidence/SKILL.md` |
| agente | [g06-development-backend-tester](../../agentes/g06-development-backend-tester/g06-development-backend-tester.md) | `bundles/development/agents/backend-tester.toml` |
| agente | [g06-development-frontend-checker-lite](../../agentes/g06-development-frontend-checker-lite/g06-development-frontend-checker-lite.md) | `bundles/development/agents/frontend-checker-lite.toml` |
| agente | [g06-development-frontend-review-readability](../../agentes/g06-development-frontend-review-readability/g06-development-frontend-review-readability.md) | `bundles/development/agents/frontend-review-readability.toml` |
| agente | [g06-development-frontend-review-reliability](../../agentes/g06-development-frontend-review-reliability/g06-development-frontend-review-reliability.md) | `bundles/development/agents/frontend-review-reliability.toml` |
| agente | [g06-development-frontend-review-resilience](../../agentes/g06-development-frontend-review-resilience/g06-development-frontend-review-resilience.md) | `bundles/development/agents/frontend-review-resilience.toml` |
| agente | [g06-development-frontend-review-risk](../../agentes/g06-development-frontend-review-risk/g06-development-frontend-review-risk.md) | `bundles/development/agents/frontend-review-risk.toml` |
| agente | [g06-development-frontend-tester](../../agentes/g06-development-frontend-tester/g06-development-frontend-tester.md) | `bundles/development/agents/frontend-tester.toml` |
| agente | [g06-management-quality-strategist](../../agentes/g06-management-quality-strategist/g06-management-quality-strategist.md) | `bundles/management/agents/quality-strategist.toml` |
