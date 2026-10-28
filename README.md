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
| `area` | `frontend` (2), `backend` (13), `mobile` (19), `datos` (2), `ia` (1), `qa` (14), `devops` (1), `seguridad` (2), `gestion` (5), `diseno` (4), `documentacion` (1) |
| `fase` | `planificacion` (4), `analisis` (3), `diseno` (6), `desarrollo` (16), `testing` (8), `revision` (14), `despliegue` (1), `mantenimiento` (4) |
| `tecnologias` | `agnostico` (7), `express` (10), `flutter` (18), `prisma` (4), `dart` (17), `docker` (1), `figma` (1), `javascript` (1), `postgresql` (3), `riverpod` (1), `supertest` (3), `typescript` (11), `vitest` (3), `zod` (1) |
| `metodologia` | `scrum` (5), `kanban` (0), `agnostico` (0) |
| `herramientas` | `claude-code` (40), `cursor` (0), `codex` (38), `otra` (1) |
| `requiere` | `jira` (4), `github` (5), `figma` (1), `google-sheets` (3), `slack` (0), `dart-mcp` (2) |
| `madurez` | `experimental` (0), `probado` (0), `usado-en-proyecto` (40) |
<!-- LISTAS:FIN -->
