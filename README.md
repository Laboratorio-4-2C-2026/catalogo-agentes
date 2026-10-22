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
| `area` | `frontend` (0), `backend` (0), `mobile` (0), `datos` (0), `ia` (0), `qa` (0), `devops` (0), `seguridad` (0), `gestion` (1), `diseno` (0), `documentacion` (0) |
| `fase` | `planificacion` (1), `analisis` (1), `diseno` (0), `desarrollo` (0), `testing` (0), `revision` (0), `despliegue` (0), `mantenimiento` (0) |
| `tecnologias` | `agnostico` (0), `express` (1), `flutter` (1), `prisma` (1) |
| `metodologia` | `scrum` (1), `kanban` (0), `agnostico` (0) |
| `herramientas` | `claude-code` (1), `cursor` (0), `codex` (0), `otra` (0) |
| `requiere` | `jira` (1), `github` (0), `figma` (0), `google-sheets` (0), `slack` (0) |
| `madurez` | `experimental` (0), `probado` (0), `usado-en-proyecto` (1) |
<!-- LISTAS:FIN -->
