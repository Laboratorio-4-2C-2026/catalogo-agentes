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
| `area` | `frontend` (106), `backend` (133), `mobile` (21), `datos` (25), `ia` (18), `qa` (183), `devops` (58), `seguridad` (28), `gestion` (253), `diseno` (46), `documentacion` (83) |
| `fase` | `planificacion` (140), `analisis` (89), `diseno` (63), `desarrollo` (99), `testing` (106), `revision` (271), `despliegue` (29), `mantenimiento` (62), `integracion` (5) |
| `tecnologias` | `agnostico` (314), `express` (22), `flutter` (18), `prisma` (40), `dart` (17), `docker` (22), `figma` (5), `javascript` (3), `postgresql` (42), `riverpod` (1), `supertest` (4), `typescript` (115), `vitest` (9), `zod` (1), `n8n` (10), `supabase` (31), `firebase` (15), `firestore` (3), `git` (36), `jest` (9), `nodejs` (14), `react` (78), `python` (42), `nextjs` (15), `playwright` (22), `nestjs` (47), `tanstack-query` (1), `auth0` (3), `flyway` (7), `junit` (2), `kotlin` (12), `postman` (1), `spring-boot` (16), `testcontainers` (1), `tailwindcss` (9), `vite` (7), `github-actions` (16), `k6` (2), `turborepo` (1), `cypress` (1), `terraform` (1) |
| `metodologia` | `scrum` (430), `kanban` (10), `agnostico` (59) |
| `herramientas` | `claude-code` (489), `cursor` (53), `codex` (182), `otra` (118) |
| `requiere` | `jira` (66), `github` (171), `figma` (5), `google-sheets` (12), `slack` (0), `dart-mcp` (2), `chrome` (19), `discord` (14), `google-drive` (15), `engram` (70), `linear` (113), `playwright` (9), `talksmith` (2), `openrouter` (13), `multica` (49), `supabase` (1), `platformance` (1), `cloudflare` (1), `neon` (5), `render` (1), `agentation` (5), `codegraph` (28), `stitch` (8), `canva` (1), `gemini` (2), `vertex-ai` (2) |
| `madurez` | `experimental` (246), `probado` (28), `usado-en-proyecto` (303), `prototipo` (3) |
<!-- LISTAS:FIN -->
