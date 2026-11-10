# Agent catalog

It enumerates the 31 installed profiles from the management and development bundles: 13 management profiles and 18 development profiles. Bundle files and workflow guides remain authoritative.

## Management bundle

These profiles are role-gated: management work starts by identifying PM, PO, TL or QA, and the named owner retains approval authority.

| Profile | Workflow | Human owner / approval boundary | Library |
|---|---|---|---|
| `architecture-governor` | Management role-gated | TL; approves architecture and release decisions | Technical lead |
| `backlog-steward` | Management role-gated | PO; approves priority and scope | Product owner |
| `evidence-reporter` | Management role-gated | PM / TL / QA; verify claims before publication | Evidence fallback* |
| `linear-tracker` | Management delivery | PM; approves delivery-field and workflow mutations | Linear tracker |
| `portfolio-planner` | Management delivery | PM; approves scope, dates and capacity decisions | Portfolio planner |
| `product-discovery` | Management role-gated | PO; approves product direction and scope | Product owner |
| `quality-strategist` | Management role-gated | QA; owns the recommendation and does not self-close work | QA manager |
| `risk-dependency-manager` | Management role-gated | TL; approves technical-risk decisions and escalations | Technical lead |
| `frontend-checker` | Management full frontend fidelity | PO / TL; PO validates visual fidelity and TL validates implementation correctness | Frontend checker; auto-provisioned local Agentation MCP, human-approved |
| `review-risk`, `review-resilience`, `review-readability`, `review-reliability` | Management /review TL gate for any PR scope | TL/QA; evidence only, never approve, merge or deploy | Management review |

## Development bundle

The workflow is designer → explorer → tester → implementer → `/review` with four parallel review lenses → frontend checker-lite when applicable → time registration. `/review` selects backend/frontend variants from changed scope and reports actionable evidence; PO validates product/visual fidelity, TL validates implementation correctness, and QA/TL approve merge and release. Full `frontend-checker` remains a management handoff stage, not a development profile.

| Profile(s) | Source / stage | Human owner / approval boundary | Library |
|---|---|---|---|
| `backend-designer`, `backend-explorer`, `backend-tester`, `backend-implementer` | Development / bounded change | Rotating developer; human owners approve scope, architecture, quality evidence and release | Backend |
| `frontend-designer`, `frontend-explorer`, `frontend-tester`, `frontend-implementer` | Development / bounded change | Rotating developer; human owners approve scope, architecture, quality evidence and release | Frontend |
| `backend-review-readability`, `backend-review-reliability`, `backend-review-resilience`, `backend-review-risk` | Development / parallel review | TL / QA; approve merge and release | Review |
| `frontend-review-readability`, `frontend-review-reliability`, `frontend-review-resilience`, `frontend-review-risk` | Development / parallel review | TL / QA; approve merge and release | Review |
| `frontend-checker-lite` | Development / narrow, fast frontend developer workflow check | Rotating developer; reports evidence only and does not approve product fidelity, merge or release | Frontend checker lite; auto-provisioned local Agentation MCP |
| `linear-time-registration` | Development / final stage | PM; records time and completed work but never changes issue status | Linear time registration |

## Review skill

The project `review` skill (`skills/review/SKILL.md`) is the `/review` workflow. Management/TL gates run exactly four generic management lenses for any PR scope; development workflow review selects backend/frontend variants from changed scope. Both use only the diff plus directly relevant context, run all four lenses, deduplicate findings with lens attribution, and report unavailable lenses as blockers. Neither workflow approves, merges or deploys.

## Library mapping

Skills and MCPs below mirror `bundles/agent-libraries.json`; the catalog contains the same arrays per profile.

| Library | Skills | MCPs / runtime |
|---|---|---|
| Technical lead | ADR, Neon/Prisma safety, PR guardrails, CodeGraph guidance | Linear, Neon, Engram, CodeGraph |
| Product owner | Product backlog, NutrIA context, Stitch UI workflow | Linear, Stitch, Engram |
| QA manager | Playwright evidence, product backlog | Linear, Stitch, Engram |
| Linear tracker / Portfolio planner | Linear delivery ops, time reporting, documentation evidence | Linear, Google Drive, Engram |
| Backend | ADR, Neon/Prisma safety, Playwright evidence, CodeGraph guidance, Engram | Linear, Neon, Engram, CodeGraph |
| Frontend | Modern Web Guidance, Stitch UI workflow, Playwright evidence, CodeGraph guidance, Engram | Linear, Stitch, Engram, CodeGraph |
| Management review | Four generic management reviewer lenses for any PR scope | Linear, Engram, CodeGraph |
| Review | Existing backend/frontend reviewer variants for risk, resilience, readability and reliability | Development reviewer TOMLs; no new reviewer agent |
| Frontend checker | Modern Web Guidance, Stitch UI workflow, Playwright evidence, CodeGraph guidance, Engram | Linear, Stitch, Engram, CodeGraph, Agentation; auto-provisioned locally with no remote endpoint and human approval required |
| Frontend checker lite | Modern Web Guidance, Stitch UI workflow, Playwright evidence, CodeGraph guidance, Engram | Linear, Stitch, Engram, CodeGraph, Agentation; narrower and faster than the full checker, with local auto-provisioning and human approval required |
| Linear time registration | Linear delivery ops, time reporting | Linear, Engram |

\* `evidence-reporter` has no dedicated key in `bundles/agent-libraries.json`; its catalog entry preserves the existing documentation/evidence + Engram minimum until that library is defined.

## Global MCP policy

- **Linear:** read first; no priority, status, assignee or scope changes without human approval.
- **Neon:** development branches only; never use production connections, secrets or PII.
- **Stitch:** human-approved; generated artifacts are proposals until PO approval.
- **Agentation:** required by both management `frontend-checker` and development `frontend-checker-lite`; it is auto-provisioned as a local MCP with no remote endpoint, and annotations remain human-approved. Lite is the narrower, faster check.
- **Engram:** save curated project knowledge proactively; never store secrets, tokens, PII or raw production data.
- **CodeGraph:** explore first; do not use administrative lifecycle commands during normal work.

No profile may merge, deploy, access production data or change work scope on its own.
