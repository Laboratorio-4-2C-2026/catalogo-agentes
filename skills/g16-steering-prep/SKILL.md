---
name: g16-steering-prep
description: 'Arma el borrador del reporte mensual de steering de Laboratorio IV con la evidencia que ya deja el repo (reportes semanales, blockers, riesgos, PRs mergeados con su resumen y su DoD, issues de post-deploy), con un link a la fuente de cada afirmación. Usar unos días antes del steering mensual.'
metadata:
  tipo: skill
  area:
  - gestion
  - documentacion
  fase:
  - planificacion
  tecnologias:
  - agnostico
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: "16"
  autor:
    nombre: Valentino Gianuzzo
    github: ValentinoGianuzzo
  responsables:
  - ValentinoGianuzzo
  madurez: usado-en-proyecto
  relacionados:
  - g16-eureka-progreso-semanal
  - g16-eureka-blockers
  - g16-cronograma
  - g13-preparador-de-steering
---

# Steering prep

Once a month the team presents a steering to the course: progress against the
plan, a demo, metrics, risks and the decisions it needs from the professors.
The evidence is already in the repo, spread across issues and PR comments that
the agents write every week. This skill gathers it into one draft for the PM.

Talk to the user in Spanish (rioplatense). The draft is in Spanish.

## The rule that matters

**Every claim in the draft links to its source** (an issue, a PR, a comment).
If something cannot be backed by a link, it does not go in the draft, or it goes
in a "Para completar por el PM" list. A thin month must look thin: the course
compares steerings month to month, and an inflated one does more damage than a
poor one. This is the same principle as the weekly Progreso report.

**"No data" and "no source" are different things, and the draft must say
which.** A label with no issues can mean "nothing went wrong" or "that agent
does not exist yet". Before reading a source, check that it exists (step 2), and
when it doesn't, write "fuente no disponible" for that item — never "cero" or
"ninguno".

## Step 1 — Scope (one message to the PM)

Ask everything in a single message:

- Which month (default: the current one, or the previous one if today is in the
  first week of the month).
- What the team committed to for that month (sprint goals, the plan presented
  at the previous steering). Without it, "progress against the plan" cannot be
  written: if the PM does not have it, the section says so.
- Where the risk register lives (another team member maintains a risks agent;
  it may be an issue label, a document or something outside the repo).
- Anything they already have in mind for the demo, and the team's
  recommendation on any decision they want to bring to the professors.

If `docs/steering/` has the previous month's draft, read it: its "Decisiones
requeridas" are the follow-up items of this month. If there is none, the
"Seguimiento" section says "No hay steering anterior."

## Step 2 — Gather the evidence

Use `gh` against this repository. Dates are in Argentina time (UTC-3): the month
runs from `YYYY-MM-01T03:00:00Z` to `YYYY-(MM+1)-01T03:00:00Z`. Use those
timestamps in GitHub searches (`merged:FROM..TO`), which are in UTC.

First check which sources exist. An agent's output only exists if its workflow
is on the default branch:
`gh api repos/{owner}/{repo}/contents/.github/workflows --jq '.[].name'`.
`eureka-progreso.yml`, `eureka-blockers.yml`, `eureka-resumen-pr.yml`,
`eureka-dod.yml` and `eureka-post-deploy.yml` back the sources below; note in the
draft which ones were missing, and for those that were added during the month,
from which date they cover.

- **Weekly progress** (`reporte-semanal` label). Reports cover Friday to Friday,
  so filter by the window in the title or the table, not by creation date:
  take every report whose window overlaps the month, and say in the draft which
  windows were used and that the first and last can include days of the
  neighbouring months. Do not prorate. A report that opens with "El agente no
  dejó reporte" has a correct table but no narrative: use the table and list the
  week in "Para completar".
- **Blockers** (`blockers-report` label). The issue body is only the current
  state. For the month, read its edit history:
  `gh api graphql -f query='query{repository(owner:"OWNER",name:"REPO"){issue(number:N){userContentEdits(first:100){nodes{editedAt diff}}}}}'`.
  Report the blockers that appeared in the month and how long they lasted.
- **Risks**: wherever the PM said in step 1. If they did not know, it goes to
  "Para completar". Do not build a risk list yourself from PR bodies.
- **Merged PRs**: `gh pr list --state merged --search "merged:FROM..TO" --limit 100 --json number,title,url,author,createdAt,mergedAt,body`.
  A PR opened in a previous month and merged in this one counts.
  For each one, read its comments (`gh api repos/{owner}/{repo}/issues/<n>/comments`)
  and pick the ones that start with `<!-- eureka-resumen-pr -->` (business
  summary) and `<!-- eureka-dod -->` (Definition of Done table), if those
  agents existed when the PR was open.
- **Reviews**: for each merged PR, both `gh api repos/{owner}/{repo}/pulls/<n>/reviews`
  and the issue comments above. In this team a review is often left as a PR
  comment instead of a formal review, so both count. Human means `user.type`
  is not `Bot` **and** the user is not the PR author (authors replying to
  threads are not reviewing).
- **Post-deploy** (`post-deploy` label): issues opened or closed in the month.
  Only meaningful if `eureka-post-deploy.yml` existed; otherwise "fuente no
  disponible".
- **Jira**: if a Jira/Atlassian tool is available in this session, list the
  tickets closed in the month. If not, the item goes to "Para completar".

## Step 3 — Metrics

Compute only what the data supports, and show how each one was computed in a
footnote line:

- PRs merged, and median time from open to merge.
- Median time from open to first human review (as defined above). Report how
  many PRs had one; PRs without any human review are listed separately, not
  dropped silently from the median.
- Definition of Done: share of rows marked ✅ across the DoD tables of the
  merged PRs, and how many PRs had a table. If no PR had one (the agent did not
  exist yet), "fuente no disponible". Do not compute it from the checkboxes in
  the PR body: ticking a box is not evidence.
- Agent findings by severity: sum of the "Hallazgos de los agentes" rows of the
  weekly reports used, with "sin severidad" as its own column. If a report's
  narrative and its table disagree, use the table and note the mismatch.
- Deploys with configuration errors (post-deploy issues), or "fuente no
  disponible".

## Step 4 — Write the draft

Write `docs/steering/<YYYY-MM>.md` with exactly these sections:

1. **Resumen** — three sentences: where the project is, what moved this month,
   what is at risk.
2. **Avance contra lo planificado** — one row per committed item: done / in
   progress / not started, with links. Items done that were not planned go in a
   separate short list. Without a plan, say so and list what was done, grouped
   by area.
3. **Demo** — what can be shown working end to end, with the PR that backs each
   item and the order to show it in. Evidence of "end to end": the "Qué probar"
   of the business summary, an E2E test (`cypress/e2e/`) added or changed in the
   PR, or a manual test described in the PR body. Code with only unit tests is
   not demo material: list it apart as "mergeado, sin prueba de punta a punta".
   Prefer flows a user would do (register a patent, share it, buy credits).
4. **Métricas** — the table from step 3.
5. **Riesgos** — the top risks from the risk register, with owner and mitigation
   as they appear there, plus the blockers of the month.
6. **Decisiones requeridas** — only decisions the team cannot take alone (scope
   changes, priorities, external dependencies), each with the options and the
   team's recommendation as the PM gave it. A decision you see in the evidence
   without a recommendation goes to "Para completar". If there are none, write
   "Ninguna" here only.
7. **Seguimiento** — what happened with the decisions requested at the previous
   steering, or "No hay steering anterior."
8. **Para completar por el PM** — everything that could not be backed with
   evidence, and every "fuente no disponible" from step 2.

Short sentences, no filler, no adjectives the data does not support.

## Step 5 — Hand it over

Show the PM a short summary of the draft and the "Para completar" list. Do not
commit, push or publish anything: the PM reviews and edits the draft first. If
they want slides, offer to turn the reviewed draft into a deck.

## Ejemplo de uso

**Pedido:** «Armá el borrador del steering de noviembre.»

**Resultado:** Pregunta el alcance en un solo mensaje y escribe `docs/steering/<AAAA-MM>.md` con cada afirmación respaldada por un link; lo que no puede respaldar queda en «Para completar por el PM». No publica nada.
