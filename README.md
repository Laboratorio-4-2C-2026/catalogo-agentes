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
| `area` | `frontend` (119), `backend` (156), `mobile` (21), `datos` (34), `ia` (18), `qa` (215), `devops` (68), `seguridad` (38), `gestion` (287), `diseno` (53), `documentacion` (99) |
| `fase` | `planificacion` (151), `analisis` (100), `diseno` (68), `desarrollo` (108), `testing` (120), `revision` (321), `despliegue` (35), `mantenimiento` (78), `integracion` (5) |
| `tecnologias` | `agnostico` (357), `express` (23), `flutter` (18), `prisma` (40), `dart` (17), `docker` (25), `figma` (5), `javascript` (3), `postgresql` (49), `riverpod` (1), `supertest` (4), `typescript` (127), `vitest` (9), `zod` (1), `n8n` (10), `supabase` (41), `firebase` (15), `firestore` (3), `git` (37), `jest` (9), `nodejs` (15), `react` (86), `python` (46), `nextjs` (21), `playwright` (24), `nestjs` (47), `tanstack-query` (1), `auth0` (4), `flyway` (7), `junit` (2), `kotlin` (13), `postman` (1), `spring-boot` (23), `testcontainers` (1), `tailwindcss` (9), `vite` (8), `github-actions` (19), `k6` (2), `turborepo` (1), `cypress` (1), `terraform` (1), `foundry` (6), `solidity` (7) |
| `metodologia` | `scrum` (458), `kanban` (10), `agnostico` (82) |
| `herramientas` | `claude-code` (527), `cursor` (54), `codex` (213), `otra` (128) |
| `requiere` | `jira` (72), `github` (194), `figma` (5), `google-sheets` (12), `slack` (0), `dart-mcp` (2), `chrome` (20), `discord` (14), `google-drive` (15), `engram` (70), `linear` (113), `playwright` (9), `talksmith` (2), `openrouter` (13), `multica` (51), `supabase` (1), `platformance` (1), `cloudflare` (1), `neon` (5), `render` (1), `agentation` (5), `codegraph` (28), `stitch` (8), `canva` (1), `gemini` (2), `vertex-ai` (2), `vercel` (1) |
| `madurez` | `experimental` (299), `probado` (29), `usado-en-proyecto` (328), `prototipo` (3) |
<!-- LISTAS:FIN -->
