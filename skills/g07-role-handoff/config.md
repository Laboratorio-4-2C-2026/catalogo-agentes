# Configuración — g07-role-handoff

Datos del proyecto. No hay secretos acá.

- **Proyecto**: `<nombre del proyecto>`
- **Site de Jira**: `<tuequipo>.atlassian.net`
- **Project key**: `<KEY>`
- **Repo de GitHub**: `<org>/<repo>` — branch base `main`
- **Estado "en curso"**: `In Progress`
- **Estado "en revisión"**: `In Review`
- **Convención de branches/PRs**: `<KEY>-<n>-<slug-del-ticket>`
- **Día de entrega**: `jueves` (ciclo semanal, por el campo Due date)
- **Variable de entorno del webhook** (solo si se pide mandar a Discord): `DISCORD_WEBHOOK_URL`

## Herramientas y rutinas de cada rol

Lo que se le cuenta a quien llega en la sección "Herramientas del rol". Si el equipo suma una herramienta, agregala acá en el rol que corresponda.

- **PM**
  - `g07-sprint-status-report` — estado del sprint con bloqueos y recomendaciones, a pedido. Se envía a Discord.
  - `g07-sprint-retro` — retro de un sprint cerrado. Se envía a Discord.
  - `g07-delivery-digest` — rutinas automáticas: aviso de entrega los jueves 10am y chequeo de mitad de ciclo los lunes 10am.
  - `g07-weekly-process-checklist` — documento de proceso para la cátedra en Google Drive, una entrada por semana.
- **TL**
  - `g07-code-review-tl` — code review fullstack de un PR, con prueba en Chrome.
  - `g07-pr-jira-sync` — cruce de PRs con Jira para detectar el board desactualizado.
- **QA**
  - `g07-qa-acceptance` (agente) — valida un ticket In Review contra sus criterios de aceptación.
  - `g07-ready-check` — antes del planning, revisa que los tickets de la próxima entrega estén listos para empezar.
- **PO**
  - `g07-release-notes` — notas de la entrega en lenguaje de usuario.
  - `g07-ready-check` — antes del planning, revisa que los tickets de la próxima entrega estén listos para empezar.
- **Todos**
  - `g07-role-handoff` — esta skill.
