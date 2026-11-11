---
name: g14-curador-de-contexto-multiherramienta
description: "Genera, desde un solo contexto canónico (CLAUDE.md, skills, subagentes y .mcp.json), los espejos de formato para Cursor, Antigravity y OpenCode y chequea su paridad. Usala cuando se edita una skill o un MCP; no valida las reglas del kit ni el inventario de agentes."
metadata:
  tipo: skill
  area:
  - documentacion
  - devops
  fase:
  - mantenimiento
  tecnologias:
  - agnostico
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: '14'
  autor:
    nombre: Elías Ballesteros
    github: Elias85974
  colaboradores: []
  responsables:
  - Elias85974
  madurez: usado-en-proyecto
  relacionados:
  - g14-curador-de-contexto-devs
  - g13-curador-de-contexto
---

# Curador de contexto

Mantiene un solo contexto compartido para todos los agentes del proyecto, con independencia de la herramienta que use cada persona.

## El principio

Hay **una fuente canónica** y el resto son espejos generados. La fuente es `CLAUDE.md` + `.claude/skills/` + `.claude/agents/` para las reglas, y `.mcp.json` para los servidores MCP. Todo lo demás se genera.

**Nunca edites un espejo.** Llevan banner `<!-- ARCHIVO GENERADO desde ... -->` y el próximo `--write` los pisa.

## El protocolo

**1. Identificá si lo que cambió es fuente o espejo.**

| Cambió | Qué hacer |
|---|---|
| `CLAUDE.md`, una skill, un subagente | `python3 scripts/sync-agentes.py --write` |
| `.mcp.json` | `python3 scripts/sync-mcp.py --write` |
| Un espejo | Revertilo. El cambio va en la fuente |

**2. Corré el `--check` antes de dar nada por hecho.** Sale 0 con paridad, 1 sin ella. No declares que los espejos están al día sin haberlo visto salir 0.

**3. Si `--write` falla con un reemplazo que no matchea, no lo esquives.** El fallo es deliberado: significa que la fuente cambió en un texto que un proveedor adapta. Actualizá el reemplazo en `scripts/sync-agentes.json` **a conciencia** —leyendo qué dice ahora la fuente— y volvé a correr. Borrar el reemplazo para que pase es romper el espejo en silencio, que es exactamente lo que este agente existe para evitar.

## Agregar una pieza nueva

Un par nuevo en `scripts/sync-agentes.json` declara una fuente y sus salidas:

- **Skill** → `.cursor/rules/skills/<n>.mdc` + `.agents/skills/<n>/SKILL.md` + `.opencode/commands/<n>.md` (stub, porque OpenCode lee `.claude/skills/` nativo).
- **Subagente** → `.cursor/rules/agents/<n>.mdc` + `.agents/rules/<n>.md` + `.opencode/agents/<n>.md`.
- **MCP** → sólo `.mcp.json`; la traducción a `opencode.json` la hace `sync-mcp.py`.

## Enganche automático

```bash
git config core.hooksPath scripts/githooks   # una vez por autor
```

Verificalo por la negativa: editá `CLAUDE.md`, intentá commitear sin `--write`, confirmá que el commit se rechaza. Si pasa, el enganche no está puesto.

## Lo que este agente no hace

No valida el contenido del contexto, sólo su paridad. Que las cuatro copias digan lo mismo no dice nada sobre si lo que dicen está bien.

## Ejemplo de uso

**Pedido:** Agregué una skill nueva, sincronizá los espejos de las otras herramientas.

**Resultado:** Regenera los espejos desde la fuente canónica y verifica que el chequeo de paridad quede en 0.
