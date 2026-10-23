# Catálogo Común de Agentes

Skills, agentes y comandos de IA hechos por todos los grupos de la materia.

- **Explorar el catálogo y ver el avance por alumno:** https://laboratorio-4-2c-2026.github.io/catalogo-agentes/ (se actualiza solo después de cada merge). También se puede abrir `sitio/index.html` con doble clic.
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
| `area` | `frontend` (0), `backend` (1), `mobile` (2), `datos` (0), `ia` (1), `qa` (2), `devops` (0), `seguridad` (0), `gestion` (5), `diseno` (1), `documentacion` (1) |
| `fase` | `planificacion` (4), `analisis` (3), `diseno` (2), `desarrollo` (1), `testing` (0), `revision` (5), `despliegue` (0), `mantenimiento` (1) |
| `tecnologias` | `agnostico` (7), `express` (1), `flutter` (3), `prisma` (1), `dart` (1) |
| `metodologia` | `scrum` (5), `kanban` (0), `agnostico` (0) |
| `herramientas` | `claude-code` (10), `cursor` (0), `codex` (8), `otra` (1) |
| `requiere` | `jira` (4), `github` (4), `figma` (0), `google-sheets` (3), `slack` (0) |
| `madurez` | `experimental` (6), `probado` (0), `usado-en-proyecto` (4) |
<!-- LISTAS:FIN -->
