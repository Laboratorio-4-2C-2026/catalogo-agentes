# Cómo subir piezas al catálogo

1. Abrí tu herramienta (Claude Code, Cursor o Codex) en la carpeta donde tenés tus piezas.
2. Pegá el prompt de `prompts/1-preparar-piezas.md` y completá los DATOS DEL EQUIPO.
3. Revisá la tabla que te devuelve la IA y corregí lo que haga falta.
   - **Recomendado:** pedile a tu herramienta que revise las fichas con la skill `skills/g03-revisor-de-fichas/SKILL.md` (modo local). Propone mejoras de clasificación, descripción, ejemplo y piezas relacionadas, y solo aplica las que aceptes.
4. En tu copia del repo, creá una rama: `git checkout -b g03-carga-inicial` (con tu número de grupo).
5. Copiá las carpetas `gNN-…` a `skills/`, `agentes/` o `comandos/`.
6. `git add`, `git commit` y `git push -u origin <tu-rama>`.
7. Abrí el Pull Request en GitHub hacia `main`.
8. Esperá el comentario automático: si hay errores, corregilos y volvé a hacer push.
9. Cuando esté todo en orden, aceptá el PR (botón **Merge**).

Reglas:

- Trabajá **en una rama del repo, no en un fork**: el bot necesita poder corregir tu rama.
- Tocá **solo las piezas de tu grupo** (las que empiezan con tu prefijo).
- No edites a mano `taxonomia.yml`, `sitio/` ni las tablas de categorías: se actualizan solos.

Para actualizar una pieza que ya está, usá `prompts/2-actualizar-pieza.md`.

## Valores disponibles

Preferí siempre estos valores. Si ninguno encaja, podés escribir uno nuevo: se suma solo al aceptar el PR.

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
