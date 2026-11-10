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
| `area` | `frontend` (57), `backend` (78), `mobile` (20), `datos` (14), `ia` (10), `qa` (122), `devops` (33), `seguridad` (18), `gestion` (162), `diseno` (22), `documentacion` (48) |
| `fase` | `planificacion` (94), `analisis` (57), `diseno` (25), `desarrollo` (73), `testing` (67), `revision` (155), `despliegue` (16), `mantenimiento` (38), `integracion` (5) |
| `tecnologias` | `agnostico` (175), `express` (22), `flutter` (18), `prisma` (24), `dart` (17), `docker` (16), `figma` (2), `javascript` (3), `postgresql` (25), `riverpod` (1), `supertest` (4), `typescript` (85), `vitest` (7), `zod` (1), `n8n` (1), `supabase` (17), `firebase` (14), `firestore` (3), `git` (21), `jest` (7), `nodejs` (10), `react` (48), `python` (18), `nextjs` (11), `playwright` (14), `nestjs` (25), `tanstack-query` (1), `auth0` (3), `flyway` (3), `junit` (2), `kotlin` (8), `postman` (1), `spring-boot` (9), `testcontainers` (1), `tailwindcss` (6), `vite` (3), `github-actions` (2), `k6` (2), `turborepo` (1) |
| `metodologia` | `scrum` (255), `kanban` (10), `agnostico` (15) |
| `herramientas` | `claude-code` (300), `cursor` (53), `codex` (87), `otra` (37) |
| `requiere` | `jira` (47), `github` (117), `figma` (1), `google-sheets` (11), `slack` (0), `dart-mcp` (2), `chrome` (12), `discord` (14), `google-drive` (7), `engram` (33), `linear` (55), `playwright` (7), `talksmith` (2), `openrouter` (9), `multica` (38), `supabase` (1) |
| `madurez` | `experimental` (116), `probado` (15), `usado-en-proyecto` (227), `prototipo` (3) |
<!-- LISTAS:FIN -->
