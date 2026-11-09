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
| `area` | `frontend` (43), `backend` (64), `mobile` (19), `datos` (8), `ia` (10), `qa` (80), `devops` (15), `seguridad` (14), `gestion` (85), `diseno` (14), `documentacion` (32) |
| `fase` | `planificacion` (45), `analisis` (32), `diseno` (16), `desarrollo` (52), `testing` (43), `revision` (103), `despliegue` (12), `mantenimiento` (20), `integracion` (3) |
| `tecnologias` | `agnostico` (106), `express` (21), `flutter` (18), `prisma` (14), `dart` (17), `docker` (7), `figma` (2), `javascript` (1), `postgresql` (15), `riverpod` (1), `supertest` (4), `typescript` (67), `vitest` (6), `zod` (1), `n8n` (1), `supabase` (17), `firebase` (12), `firestore` (3), `git` (4), `jest` (5), `nodejs` (7), `react` (29), `python` (2), `nextjs` (11), `playwright` (7), `nestjs` (10), `tanstack-query` (1), `auth0` (3), `flyway` (3), `junit` (1), `kotlin` (8), `postman` (1), `spring-boot` (8), `testcontainers` (1), `tailwindcss` (1), `vite` (1) |
| `metodologia` | `scrum` (136), `kanban` (0), `agnostico` (11) |
| `herramientas` | `claude-code` (187), `cursor` (53), `codex` (69), `otra` (17) |
| `requiere` | `jira` (25), `github` (72), `figma` (1), `google-sheets` (4), `slack` (0), `dart-mcp` (2), `chrome` (5), `discord` (14), `google-drive` (1), `engram` (33), `linear` (37), `playwright` (7), `talksmith` (2), `openrouter` (9), `multica` (6) |
| `madurez` | `experimental` (46), `probado` (6), `usado-en-proyecto` (173), `prototipo` (3) |
<!-- LISTAS:FIN -->
