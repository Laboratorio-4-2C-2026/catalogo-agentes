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
| `area` | `frontend` (20), `backend` (37), `mobile` (19), `datos` (3), `ia` (8), `qa` (50), `devops` (9), `seguridad` (9), `gestion` (54), `diseno` (9), `documentacion` (21) |
| `fase` | `planificacion` (31), `analisis` (22), `diseno` (15), `desarrollo` (41), `testing` (28), `revision` (53), `despliegue` (9), `mantenimiento` (10) |
| `tecnologias` | `agnostico` (64), `express` (18), `flutter` (18), `prisma` (4), `dart` (17), `docker` (3), `figma` (2), `javascript` (1), `postgresql` (4), `riverpod` (1), `supertest` (3), `typescript` (44), `vitest` (3), `zod` (1), `n8n` (1), `supabase` (9), `firebase` (10), `firestore` (3), `git` (1), `jest` (4), `nodejs` (4), `react` (13), `python` (1), `nextjs` (6), `playwright` (1) |
| `metodologia` | `scrum` (108), `kanban` (0), `agnostico` (1) |
| `herramientas` | `claude-code` (144), `cursor` (53), `codex` (38), `otra` (2) |
| `requiere` | `jira` (14), `github` (27), `figma` (1), `google-sheets` (3), `slack` (0), `dart-mcp` (2), `chrome` (4), `discord` (4), `google-drive` (1), `engram` (33), `linear` (22), `playwright` (1), `talksmith` (2) |
| `madurez` | `experimental` (2), `probado` (0), `usado-en-proyecto` (142) |
<!-- LISTAS:FIN -->
