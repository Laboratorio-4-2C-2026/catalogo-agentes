---
name: g09-zervi-exploratory-qc
description: "Invocación explícita: explora la coherencia de Zervi en sesiones de hasta 20 minutos y consolida hallazgos sin inventar ejecución ni cierres."
license: MIT
metadata:
  author: "Bruno Iacovone"
  github: "BrunoIacovone"
  version: "1.0.0"
  tipo: skill
  area: [qa]
  fase: [testing]
  tecnologias: [agnostico]
  metodologia: [agnostico]
  herramientas: [otra]
  requiere: []
  grupo: "09"
  autor:
    nombre: Bruno Iacovone
    github: BrunoIacovone
  responsables: [BrunoIacovone]
  madurez: usado-en-proyecto
  relacionados: ["g09-jira-qa-validation", "g09-zervi-directed-qa"]
---

## Activation Contract

- Activate only on explicit `g09-zervi-exploratory-qc`, `zervi-exploratory-qc` or unambiguous named equivalent; never organically during QA/implementation/review/debugging/discussion.
- Explore user goals independently of Jira criteria; tickets are context, not truth.

## Hard Rules

- Read mandatory references below and the full existing supplied/authorized register. Establish authorized `OUTPUT_BASE`/`findings.md`; never infer repo paths. Initialize only within that base; empty templates prove no testing.
- Absolute maximum: 20 minutes per invocation, no override. Stop earlier on completion/safety/tool blocker; reserve final 3 minutes for reporting when possible. Broader work needs separately authorized sessions.
- Default read-only. Mutations need explicit authorization and disposable data. Report/register writes need authorized base; reject escaping paths and unrelated overwrites. Never edit app source or Git files/state/branches/refs, stage or commit.
- Use approved origins only; protect secrets, tokens, cookies, authorization data and localStorage.
- No unevidenced execution. Pasted inputs support planning without integrations; exploration requires browser tools and authorized environment. Without tools: charter/plan, `NOT TESTED` probes, Environment/Tooling Blocker, no observed findings.
- Judge goals, invariants, consistency, safety/trust, data meaning, feedback and navigation. Keep one narrow mission; record untested/blocked areas.

## Decision Gates

| Condition | Action |
|---|---|
| Missing/oversized mission | Define/narrow charter; remainder untested, later sessions need explicit authorization. |
| Mutation/first login/upload/destruction | Require authorization and disposable data; otherwise record boundary. |
| Same normalized finding key | Update last seen/evidence/occurrences, no new ID. |
| Similar, different root behavior | Keep separate. |
| Writes unauthorized/unavailable | Propose both documents in chat. |
| Closure proposed | Apply register closure rules; otherwise preserve status. |

## Execution Steps

1. Record charter, scope, environment, actors, origins, tools, start/deadline (≤20 min), base/register and permissions.
2. With tools, reconnoiter breadth-first then test risk hypotheses within this charter. Otherwise follow the planning fallback.
3. Probe contradictions, unnecessary data, dead ends/CTAs, roles, persistence/stale state, mobile/desktop, accessibility, recovery/destruction and privacy/security.
4. Capture sanitized evidence; classify Clear Defect, Improvement Opportunity, Product Question, Environment/Tooling Blocker or Resolved/Closed candidate.
5. Deduplicate by normalized route/module + actor + trigger + behavior + impact. Assign next `ZQC-###` only to distinct findings.
6. When authorized, use the session template for `OUTPUT_BASE/sessions/YYYY-MM-DD-HHmm-<scope>.md`; update `OUTPUT_BASE/findings.md`.
7. Preserve history and template statuses/closure rules: defects need explicit retest, other categories need their specified decision/implementation/restoration evidence. Blocker closure leaves probes `NOT TESTED` for separately authorized sessions, never PASS.

Related: `g09-jira-qa-validation` generates cases; `g09-zervi-directed-qa` also accepts human/other cases. No dependency/activation implied; each needs explicit invocation/authorization. Regression proposals need a user decision, never automatic requirements.

## Output Contract

- In the user's language, summarize mission, actual budget, paths, categories, register changes, blockers and untested areas.
- Cite written report path/changed IDs, or provide complete proposed report/register content in chat when writes unavailable.

## References

- [Product context](references/zervi-product-context.md) — mandatory product/identity/safety baseline.
- [Session template](assets/session-report-template.md) — mandatory report shape.
- [Register/closure rules](assets/findings-register-template.md) — mandatory; existing register is operator input.

## Ejemplo de uso

Ejemplo sintético ilustrativo; no representa ejecución realizada.

**Pedido:** Invoca g09-zervi-exploratory-qc para planificar una sesión de coherencia entre listado y detalle de servicios. No hay navegador, registro previo ni autorización de escritura; entrega la propuesta en chat.

**Resultado:** Propone charter de hasta 20 minutos para comparar título y precio entre listado y detalle; sondas `NOT TESTED`, sin hallazgos observados ni duración ejecutada. Entrega informe/registro propuestos en chat con bloqueo de herramientas y sin cierres; solicita entorno y sesión autorizados para explorar.
