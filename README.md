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
| `area` | `frontend` (99), `backend` (126), `mobile` (21), `datos` (23), `ia` (12), `qa` (161), `devops` (48), `seguridad` (25), `gestion` (226), `diseno` (43), `documentacion` (67) |
| `fase` | `planificacion` (128), `analisis` (80), `diseno` (59), `desarrollo` (97), `testing` (95), `revision` (246), `despliegue` (24), `mantenimiento` (54), `integracion` (5) |
| `tecnologias` | `agnostico` (283), `express` (22), `flutter` (18), `prisma` (38), `dart` (17), `docker` (21), `figma` (3), `javascript` (3), `postgresql` (40), `riverpod` (1), `supertest` (4), `typescript` (110), `vitest` (8), `zod` (1), `n8n` (2), `supabase` (22), `firebase` (15), `firestore` (3), `git` (29), `jest` (8), `nodejs` (13), `react` (68), `python` (28), `nextjs` (15), `playwright` (19), `nestjs` (44), `tanstack-query` (1), `auth0` (3), `flyway` (7), `junit` (2), `kotlin` (12), `postman` (1), `spring-boot` (16), `testcontainers` (1), `tailwindcss` (8), `vite` (6), `github-actions` (6), `k6` (2), `turborepo` (1), `cypress` (1), `terraform` (1) |
| `metodologia` | `scrum` (386), `kanban` (10), `agnostico` (50) |
| `herramientas` | `claude-code` (437), `cursor` (53), `codex` (181), `otra` (116) |
| `requiere` | `jira` (55), `github` (151), `figma` (3), `google-sheets` (11), `slack` (0), `dart-mcp` (2), `chrome` (19), `discord` (14), `google-drive` (15), `engram` (70), `linear` (113), `playwright` (8), `talksmith` (2), `openrouter` (10), `multica` (43), `supabase` (1), `platformance` (1), `cloudflare` (1), `neon` (5), `render` (1), `agentation` (5), `codegraph` (28), `stitch` (8) |
| `madurez` | `experimental` (238), `probado` (17), `usado-en-proyecto` (269), `prototipo` (3) |
<!-- LISTAS:FIN -->
