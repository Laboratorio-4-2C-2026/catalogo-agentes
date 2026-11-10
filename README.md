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
| `area` | `frontend` (50), `backend` (72), `mobile` (19), `datos` (12), `ia` (10), `qa` (104), `devops` (26), `seguridad` (17), `gestion` (130), `diseno` (21), `documentacion` (40) |
| `fase` | `planificacion` (74), `analisis` (49), `diseno` (24), `desarrollo` (68), `testing` (56), `revision` (126), `despliegue` (12), `mantenimiento` (32), `integracion` (3) |
| `tecnologias` | `agnostico` (152), `express` (22), `flutter` (18), `prisma` (18), `dart` (17), `docker` (11), `figma` (2), `javascript` (1), `postgresql` (20), `riverpod` (1), `supertest` (4), `typescript` (72), `vitest` (6), `zod` (1), `n8n` (1), `supabase` (17), `firebase` (14), `firestore` (3), `git` (14), `jest` (6), `nodejs` (10), `react` (37), `python` (2), `nextjs` (11), `playwright` (7), `nestjs` (16), `tanstack-query` (1), `auth0` (3), `flyway` (3), `junit` (2), `kotlin` (8), `postman` (1), `spring-boot` (9), `testcontainers` (1), `tailwindcss` (4), `vite` (2), `github-actions` (1), `k6` (2), `turborepo` (1) |
| `metodologia` | `scrum` (193), `kanban` (10), `agnostico` (14) |
| `herramientas` | `claude-code` (237), `cursor` (53), `codex` (87), `otra` (37) |
| `requiere` | `jira` (45), `github` (88), `figma` (1), `google-sheets` (5), `slack` (0), `dart-mcp` (2), `chrome` (9), `discord` (14), `google-drive` (1), `engram` (33), `linear` (51), `playwright` (7), `talksmith` (2), `openrouter` (9), `multica` (16), `supabase` (1) |
| `madurez` | `experimental` (83), `probado` (6), `usado-en-proyecto` (206), `prototipo` (3) |
<!-- LISTAS:FIN -->
