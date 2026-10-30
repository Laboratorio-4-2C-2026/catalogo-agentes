# Catálogo Común de Agentes

Skills, agentes y comandos de IA hechos por todos los grupos de la materia.

- **Explorar el catálogo y ver el avance por alumno:** https://laboratorio-4-2c-2026.github.io/catalogo-agentes/ (se actualiza solo después de cada merge). También se puede abrir `sitio/index.html` con doble clic.
- **Guía del catálogo (reglas, cómo subir piezas y cómo funciona):** https://claude.ai/artifact/A2mYu33xi9r7XdX4duFiD8
- **Acceso:** la cátedra invita a cada integrante a la organización y a este repo. Llegan dos mails de GitHub: hay que aceptar los dos.
- **Subir o actualizar piezas:** seguí los pasos de [CONTRIBUTING.md](CONTRIBUTING.md).
- **Prompts para preparar las piezas:** carpeta [prompts/](prompts/).

## Estructura

| Carpeta | Contenido |
|---|---|
| `skills/` | Una carpeta `gNN-nombre/` por skill, con su `SKILL.md` |
| `agentes/` | Una carpeta `gNN-nombre/` por agente |
| `comandos/` | Una carpeta `gNN-nombre/` por comando |
| `sitio/` | Explorador de piezas y avance por alumno, conectados (se genera solo) |
| `scripts/` | Controles y generadores que usan los workflows |

## Categorías disponibles

Esta tabla se actualiza sola cada vez que se acepta un PR.

<!-- LISTAS:INICIO -->
| Campo | Valores (cantidad de piezas que lo usan) |
|---|---|
| `area` | `frontend` (18), `backend` (33), `mobile` (19), `datos` (3), `ia` (6), `qa` (38), `devops` (9), `seguridad` (9), `gestion` (30), `diseno` (7), `documentacion` (13) |
| `fase` | `planificacion` (20), `analisis` (14), `diseno` (12), `desarrollo` (38), `testing` (21), `revision` (36), `despliegue` (8), `mantenimiento` (7) |
| `tecnologias` | `agnostico` (34), `express` (18), `flutter` (18), `prisma` (4), `dart` (17), `docker` (3), `figma` (2), `javascript` (1), `postgresql` (3), `riverpod` (1), `supertest` (3), `typescript` (43), `vitest` (3), `zod` (1), `n8n` (1), `supabase` (1), `firebase` (10), `firestore` (3), `git` (1), `jest` (4), `nodejs` (3), `react` (13), `python` (1) |
| `metodologia` | `scrum` (68), `kanban` (0), `agnostico` (1) |
| `herramientas` | `claude-code` (104), `cursor` (53), `codex` (38), `otra` (2) |
| `requiere` | `jira` (14), `github` (20), `figma` (1), `google-sheets` (3), `slack` (0), `dart-mcp` (2), `chrome` (2), `discord` (4), `google-drive` (1) |
| `madurez` | `experimental` (2), `probado` (0), `usado-en-proyecto` (102) |
<!-- LISTAS:FIN -->
