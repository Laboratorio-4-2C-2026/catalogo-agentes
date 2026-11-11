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
| `area` | `frontend` (92), `backend` (111), `mobile` (20), `datos` (20), `ia` (11), `qa` (156), `devops` (46), `seguridad` (20), `gestion` (221), `diseno` (41), `documentacion` (62) |
| `fase` | `planificacion` (125), `analisis` (80), `diseno` (53), `desarrollo` (94), `testing` (88), `revision` (224), `despliegue` (22), `mantenimiento` (48), `integracion` (5) |
| `tecnologias` | `agnostico` (278), `express` (22), `flutter` (18), `prisma` (31), `dart` (17), `docker` (20), `figma` (3), `javascript` (3), `postgresql` (34), `riverpod` (1), `supertest` (4), `typescript` (95), `vitest` (7), `zod` (1), `n8n` (2), `supabase` (17), `firebase` (14), `firestore` (3), `git` (25), `jest` (7), `nodejs` (12), `react` (60), `python` (25), `nextjs` (15), `playwright` (18), `nestjs` (30), `tanstack-query` (1), `auth0` (3), `flyway` (7), `junit` (2), `kotlin` (12), `postman` (1), `spring-boot` (16), `testcontainers` (1), `tailwindcss` (7), `vite` (5), `github-actions` (5), `k6` (2), `turborepo` (1), `cypress` (1), `terraform` (1) |
| `metodologia` | `scrum` (371), `kanban` (10), `agnostico` (35) |
| `herramientas` | `claude-code` (407), `cursor` (53), `codex` (181), `otra` (106) |
| `requiere` | `jira` (55), `github` (143), `figma` (3), `google-sheets` (11), `slack` (0), `dart-mcp` (2), `chrome` (19), `discord` (14), `google-drive` (15), `engram` (70), `linear` (112), `playwright` (8), `talksmith` (2), `openrouter` (10), `multica` (38), `supabase` (1), `platformance` (1), `cloudflare` (1), `neon` (5), `render` (1), `agentation` (5), `codegraph` (28), `stitch` (8) |
| `madurez` | `experimental` (208), `probado` (17), `usado-en-proyecto` (269), `prototipo` (3) |
<!-- LISTAS:FIN -->
