# Contexto de Zest — resumen base

> Resumen inicial armado el 30/10/26 a partir del repo `proyecto-zest/zest`, el repo `zest-support`,
> el Tablero de Estado del Proyecto y la configuración de Multica. Lo que diga una fuente más nueva
> (repo, docs, Multica, planilla) **le gana** a este archivo. Actualizarlo cuando cambie algo importante.

## Qué es Zest
Una app de recetas: los usuarios crean recetas (ingredientes, pasos e imágenes), las guardan, las organizan en colecciones y planifican qué cocinar cada día. Es el proyecto del **Equipo 02** de la materia Dirección de Proyectos (Universidad Austral, 2026), desarrollado en conjunto con Lab IV.

## Equipo
- **Roles actuales** (confirmados por Ines Gassiebayle, Tech Lead, el 09/11/26): Luz Laura, PM; Maria Clara Lopez, PO; Ines Gassiebayle, Tech Lead; Agus Alma, QA.
- Ojo: documentos anteriores (los PDFs de Steering 1 y 2 y la pestaña "Inscripción catálogo" del Tablero, 30/10/26) muestran otras asignaciones porque los roles fueron rotando. Para los roles de hoy **gana la lista de arriba**; si preguntan por los roles en una fecha pasada, citar el documento de esa fecha.
- **Desarrolladores:** Dev 1 (`usuario-dev1`, GitHub `github-dev1`) y Dev 2 (`usuario-dev2`, GitHub `github-dev2`).
- **Catálogo Común de Agentes de la materia:** https://laboratorio-4-2c-2026.github.io/catalogo-agentes/ (Zest es el grupo 02, prefijo `g02-`). Cada integrante tiene que llegar a 10 piezas como autora.

## Herramientas
| Para qué | Herramienta | Dónde |
|---|---|---|
| Tickets | Multica, workspace `zest` | https://multica.ai/zest — board "Zest" |
| Código | GitHub | `proyecto-zest/zest` (app) y `inesgassiebayle/zest-support` (docs, diseño y convenciones, como submódulo `support/`) |
| Comunicación | Grupo de WhatsApp del equipo | — |
| Seguimiento para la cátedra | Tablero de Estado del Proyecto (Google Sheets), pestaña "Equipo 02" | Semáforo semanal, Cronograma e Incidentes; se carga los jueves |
| KPIs de Lab IV | Panel de cumplimiento | https://lab4-kpis.github.io/kpis/#/cumplimiento (Zest es el equipo 2) |

## Stack
- **Frontend:** React + TypeScript + Vite + Tailwind (`frontend/`).
- **Backend:** Node.js + TypeScript + NestJS + Prisma (`backend/`).
- **Base de datos:** PostgreSQL. Esquema en `backend/prisma/schema.prisma`; la fuente de verdad es `support/docs/db.md`.
- **Autenticación:** Auth0 (no hay contraseñas en la base).
- **Imágenes:** S3, con URLs prefirmadas.
- **Infraestructura:** hay dos versiones documentadas que no coinciden: `.claude/skills/zest-infra` habla de EC2 + RDS, y `zest-support/AGENTS.md` y los `.env.example` hablan de Render + Vercel + Neon. Antes de responder sobre deploy, revisar `support/skills/infra.md` y el estado actual.

## Modelo de datos (resumen)
Usuarios, recetas (con categoría, tiempo, dificultad y porciones), pasos, ingredientes (catálogo fijo en inglés), imágenes de recetas, colecciones y la relación colección-receta. En el modelo de `db.md` también figuran `saved_recipes` y `planner_entries`. **No existen** etiquetas, seguidores ni planes semanales: si un documento viejo los menciona, está desactualizado.

## Pantallas
Feed (`/`), detalle de receta, crear y editar receta, colecciones y su detalle, perfil propio y perfil público, login y registro. Todo requiere sesión salvo login y registro.

## Cómo se trabaja
- **Tickets:** viven en Multica con el formato `ZEST-<número>`. Cada uno tiene responsable y fecha de vencimiento (normalmente los jueves).
- **Branches:** una por ticket, con el nombre del ticket (por ejemplo `ZEST-114`). La guía de `zest-support` sugiere `feature/`, `fix/` y `chore/`, pero en la práctica se usa el ID.
- **PRs:** chicos, con descripción y ticket vinculado. Al menos una revisión antes de mergear y nunca commits directos a `main`. El CI corre en GitHub Actions.
- **Ceremonias:** clase y reunión interna los jueves; el status se carga los jueves a las 10.
- **Hito próximo:** despliegue del MVP, con fecha estimada el 12/11/26 según el Cronograma.

## Agentes del equipo
Cada integrante armó 10 agentes en Multica: revisión de PRs, tickets, tests E2E, chequeo responsive, status report, KPIs, recordatorios, estimaciones, limpieza de branches, datos de demo, entre otros. La lista completa y actualizada está en la documentación de agentes de `zest-support`.

## Dónde buscar cada cosa
| Pregunta | Dónde |
|---|---|
| ¿Cómo está el proyecto esta semana? | Tablero de Estado (semáforo e incidentes) y Multica |
| ¿Qué hace tal pantalla o endpoint? | `frontend/src/features/`, `backend/src/` |
| ¿Qué campos tiene tal entidad? | `support/docs/db.md` |
| ¿Por qué se eligió tal tecnología? | `support/docs/tech-stack.md` |
| ¿Cómo se ve tal pantalla? | `support/design/` |
| ¿Qué se decidió en tal reunión o entrega? | Carpeta de conocimiento (actas, presentaciones) |
| ¿Quién hace qué? | Multica (asignaciones) y documentos del equipo |
