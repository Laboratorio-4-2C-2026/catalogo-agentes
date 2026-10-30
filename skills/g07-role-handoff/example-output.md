# Ejemplo de output — Role Handoff

> Generado sobre un board y un repo reales; los nombres de las personas y los acuerdos son ficticios.

🔁 **Handoff de TL — de Marco a Denise — 30/10**

## ⚡ Lo primero que tenés que hacer
1. Antes del jueves 05/11, confirmá con Julia si los PRs [#92](https://github.com/tu-org/study-arena/pull/92) y [#93](https://github.com/tu-org/study-arena/pull/93) salen de draft: [STUDY-107](https://tuequipo.atlassian.net/browse/STUDY-107) y [STUDY-108](https://tuequipo.atlassian.net/browse/STUDY-108) figuran In Review en Jira, pero el código todavía no está para revisar.
2. Asignate como reviewer de #92, #93 y #95: ninguno tiene reviewer.
3. Revisá [#96](https://github.com/tu-org/study-arena/pull/96) ([STUDY-98](https://tuequipo.atlassian.net/browse/STUDY-98)) con `g07-code-review-tl`: es el único PR listo y vence el jueves.
4. Hablá con el PO por [STUDY-79](https://tuequipo.atlassian.net/browse/STUDY-79): sigue en To Do y bloquea a STUDY-105, que vence el 05/11.

## 📅 Próximas entregas
**Jueves 05/11**
- **Julia**
  - STUDY-107 Endpoint de historial de estudio — In Review (PR #92 en draft) ⚠️
  - STUDY-108 Sección "Tu historial" en el perfil — In Review (PR #93 en draft) ⚠️
  - STUDY-109 Rediseño de filtros en Materiales — In Review (PR #95 en draft) ⚠️
- **Marco**
  - STUDY-98 Cuestionarios en los materiales de grupos — In Review (PR #96 con reviewer) ✅
  - STUDY-105 Cuestionarios con IA desde un archivo del grupo — In Progress, bloqueado 🚫
  - STUDY-106 Preguntas con IA en el modal de cuestionario — To Do, bloqueado 🚫

**Jueves 12/11**
- Todavía no hay nada asignado.

## 🚧 Riesgos y bloqueos vivos
- **STUDY-105 ← STUDY-79** (To Do): la generación de cuestionarios desde archivo depende de la generación de tarjetas desde archivo, que no arrancó. Según Marco, se puede destrabar reusando el parser de STUDY-99; falta que alguien lo confirme.
- **STUDY-106 ← STUDY-105** (In Progress): en cadena con el anterior. Si STUDY-105 no llega, STUDY-106 tampoco.
- **STUDY-108 ← STUDY-107** (In Review, PR en draft): el front espera al endpoint.

## 🔀 PRs y revisión
- #96 (STUDY-98): listo, con reviewer. Te toca revisarlo.
- #92, #93, #95: draft y sin reviewer. Le toca moverse a Julia (sacarlos de draft), y después a vos (asignarte).

## 🛠️ Lo propio del TL
- **Branches y PRs**: `STUDY-<n>-<slug>`, base `main`. Un PR por ticket; si un ticket tiene back y front, van en dos PRs.
- **CI**: `ci-check-gradle.yml` y `frontend-ci.yml` corren en cada PR. Según Marco, el de frontend falla de forma intermitente por el cache de npm: si falla, se re-corre antes de investigar.
- **Decisiones técnicas recientes** (según Marco): la generación con IA va por un servicio aparte con timeout de 30 s; no se suman llamadas síncronas a la IA en los controllers.

## 🤝 Acuerdos, personas y accesos
- **Acuerdo** (según Marco): con el PO quedó que STUDY-106 puede pasar a la entrega del 12/11 si STUDY-105 se atrasa. No está escrito en Jira.
- **Personas**: Julia conoce el módulo de perfil y métricas. Las dudas de la cátedra sobre la entrega, al canal #consultas.
- **Accesos que necesitás**: MCP de Atlassian conectado a Claude Code, permiso de reviewer en `tu-org/study-arena` y `gh` autenticado. Pedile a Marco que te sume como admin del repo.

## 🧰 Herramientas del rol
- `g07-code-review-tl`: code review fullstack de un PR, con prueba de la UI en Chrome.
- `g07-pr-jira-sync`: muestra dónde el board de Jira y los PRs dicen cosas distintas. Corrélo antes de cada jueves.

## ❓ Lo que no se pudo verificar
- El estado del CI de cada PR: el snapshot de GitHub no lo trae.
- Marco no pasó consejos para quien llega (pregunta 5).
