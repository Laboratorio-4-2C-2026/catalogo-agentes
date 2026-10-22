# Cómo subir piezas al catálogo

1. Abrí tu herramienta (Claude Code, Cursor o Codex) en la carpeta donde tenés tus piezas.
2. Pegá el prompt de `prompts/1-preparar-piezas.md` y completá los DATOS DEL EQUIPO.
3. Revisá la tabla que te devuelve la IA y corregí lo que haga falta.
4. En tu copia del repo, creá una rama: `git checkout -b g03-carga-inicial` (con tu número de grupo).
5. Copiá las carpetas `gNN-…` a `skills/`, `agentes/` o `comandos/`.
6. `git add`, `git commit` y `git push -u origin <tu-rama>`.
7. Abrí el Pull Request en GitHub hacia `main`.
8. Esperá el comentario automático: si hay errores, corregilos y volvé a hacer push.
9. Cuando esté todo en orden, aceptá el PR (botón **Merge**).

Reglas:

- Trabajá **en una rama del repo, no en un fork**: el bot necesita poder corregir tu rama.
- Tocá **solo las piezas de tu grupo** (las que empiezan con tu prefijo).
- No edites a mano `taxonomia.yml`, `explorador/` ni las tablas de categorías: se actualizan solos.

Para actualizar una pieza que ya está, usá `prompts/2-actualizar-pieza.md`.

## Valores disponibles

Preferí siempre estos valores. Si ninguno encaja, podés escribir uno nuevo: se suma solo al aceptar el PR.

<!-- LISTAS:INICIO -->
| Campo | Valores (cantidad de piezas que lo usan) |
|---|---|
| `area` | `frontend` (0), `backend` (0), `mobile` (0), `datos` (0), `ia` (0), `qa` (0), `devops` (0), `seguridad` (0), `gestion` (0), `diseno` (0), `documentacion` (0) |
| `fase` | `planificacion` (0), `analisis` (0), `diseno` (0), `desarrollo` (0), `testing` (0), `revision` (0), `despliegue` (0), `mantenimiento` (0) |
| `tecnologias` | `agnostico` (0) |
| `metodologia` | `scrum` (0), `kanban` (0), `agnostico` (0) |
| `herramientas` | `claude-code` (0), `cursor` (0), `codex` (0), `otra` (0) |
| `requiere` | `jira` (0), `github` (0), `figma` (0), `google-sheets` (0), `slack` (0) |
| `madurez` | `experimental` (0), `probado` (0), `usado-en-proyecto` (0) |
<!-- LISTAS:FIN -->
