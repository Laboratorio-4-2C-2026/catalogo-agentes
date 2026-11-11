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
| `area` | `frontend` (70), `backend` (90), `mobile` (20), `datos` (19), `ia` (10), `qa` (141), `devops` (39), `seguridad` (18), `gestion` (197), `diseno` (29), `documentacion` (57) |
| `fase` | `planificacion` (108), `analisis` (65), `diseno` (31), `desarrollo` (77), `testing` (77), `revision` (194), `despliegue` (19), `mantenimiento` (44), `integracion` (5) |
| `tecnologias` | `agnostico` (224), `express` (22), `flutter` (18), `prisma` (26), `dart` (17), `docker` (20), `figma` (3), `javascript` (3), `postgresql` (28), `riverpod` (1), `supertest` (4), `typescript` (91), `vitest` (7), `zod` (1), `n8n` (2), `supabase` (17), `firebase` (14), `firestore` (3), `git` (24), `jest` (7), `nodejs` (12), `react` (52), `python` (25), `nextjs` (15), `playwright` (17), `nestjs` (26), `tanstack-query` (1), `auth0` (3), `flyway` (3), `junit` (2), `kotlin` (8), `postman` (1), `spring-boot` (11), `testcontainers` (1), `tailwindcss` (7), `vite` (4), `github-actions` (5), `k6` (2), `turborepo` (1), `cypress` (1) |
| `metodologia` | `scrum` (312), `kanban` (10), `agnostico` (28) |
| `herramientas` | `claude-code` (350), `cursor` (53), `codex` (115), `otra` (49) |
| `requiere` | `jira` (53), `github` (140), `figma` (3), `google-sheets` (11), `slack` (0), `dart-mcp` (2), `chrome` (17), `discord` (14), `google-drive` (13), `engram` (33), `linear` (74), `playwright` (7), `talksmith` (2), `openrouter` (10), `multica` (38), `supabase` (1), `platformance` (1) |
| `madurez` | `experimental` (142), `probado` (17), `usado-en-proyecto` (269), `prototipo` (3) |
<!-- LISTAS:FIN -->
