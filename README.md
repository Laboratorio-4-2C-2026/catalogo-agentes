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
| `area` | `frontend` (47), `backend` (70), `mobile` (19), `datos` (9), `ia` (10), `qa` (92), `devops` (21), `seguridad` (17), `gestion` (107), `diseno` (19), `documentacion` (37) |
| `fase` | `planificacion` (60), `analisis` (40), `diseno` (20), `desarrollo` (62), `testing` (51), `revision` (117), `despliegue` (12), `mantenimiento` (26), `integracion` (3) |
| `tecnologias` | `agnostico` (133), `express` (21), `flutter` (18), `prisma` (18), `dart` (17), `docker` (8), `figma` (2), `javascript` (1), `postgresql` (16), `riverpod` (1), `supertest` (4), `typescript` (70), `vitest` (6), `zod` (1), `n8n` (1), `supabase` (17), `firebase` (14), `firestore` (3), `git` (10), `jest` (6), `nodejs` (8), `react` (34), `python` (2), `nextjs` (11), `playwright` (7), `nestjs` (16), `tanstack-query` (1), `auth0` (3), `flyway` (3), `junit` (1), `kotlin` (8), `postman` (1), `spring-boot` (8), `testcontainers` (1), `tailwindcss` (4), `vite` (2), `github-actions` (1), `k6` (2), `turborepo` (1) |
| `metodologia` | `scrum` (173), `kanban` (0), `agnostico` (14) |
| `herramientas` | `claude-code` (227), `cursor` (53), `codex` (77), `otra` (17) |
| `requiere` | `jira` (25), `github` (79), `figma` (1), `google-sheets` (4), `slack` (0), `dart-mcp` (2), `chrome` (5), `discord` (14), `google-drive` (1), `engram` (33), `linear` (51), `playwright` (7), `talksmith` (2), `openrouter` (9), `multica` (6), `supabase` (1) |
| `madurez` | `experimental` (69), `probado` (6), `usado-en-proyecto` (190), `prototipo` (3) |
<!-- LISTAS:FIN -->
