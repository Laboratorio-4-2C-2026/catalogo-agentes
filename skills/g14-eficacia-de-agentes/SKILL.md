---
name: g14-eficacia-de-agentes
description: Descubre los agentes, skills y workflows de cualquier conjunto de repositorios git (sin depender de un formato propio) y reporta, con datos de git y de GitHub Actions, cuáles corrieron, cuándo, con qué evidencia, si la evidencia quedó vencida, si la pieza deriva de lo que cita y qué señales de hallazgo dejó. Usala al cerrar un proyecto o un hito para saber qué de lo construido realmente opera; no evalúa si el resultado de cada corrida fue correcto.
metadata:
  tipo: skill
  area:
  - ia
  - gestion
  fase:
  - revision
  tecnologias:
  - agnostico
  - git
  - python
  metodologia:
  - agnostico
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: '14'
  autor:
    nombre: Macarena Alimena
    github: MackyAlimena
  colaboradores: []
  responsables:
  - MackyAlimena
  madurez: probado
  relacionados:
  - g14-auditor-de-agentes
---

# Eficacia de agentes

`g14-auditor-de-agentes` responde si una pieza **está completa** (ficha, skill, disparo, fila de inventario). Esta responde otra pregunta: **¿corrió, sigue viva y dejó algo?** Funciona sobre cualquier repo: no necesita fichas ni inventario.

## Protocolo

1. `python3 scripts/eficacia.py --raiz <carpeta con los repos> [--excluir <repo ajeno>] [--online] --salida eficacia.md --json eficacia.json`
   - `--excluir` deja afuera catálogos o repos que no son del proyecto.
   - `--online` consulta `gh run list` (sólo lectura) para los workflows.
2. Leé el resumen por estado y, en especial, `sin-corridas`, `evidencia-vencida` y `fallando`.
3. Para cada pieza que importe, decidí con una persona: ¿se corre y se registra, se actualiza, o se da de baja? Las señales de hallazgo orientan; no prueban que lo hallado sea correcto.

## Qué descubre y qué mide

- **Piezas:** `SKILL.md` en cualquier carpeta (`.claude`, `.agents`, `.cursor`, `.codex`, `.opencode`, catálogos), agentes con frontmatter y workflows de GitHub Actions. Los espejos de una misma skill se agrupan y se avisa si divergieron.
- **Evidencia:** archivos versionados en carpetas de salidas/evidencia/reportes que nombran a la pieza o a sus scripts, con cantidad de commits y fecha. Las evidencias globales que nombran a más de cuatro piezas no se le atribuyen a ninguna.
- **Disparo inferido:** `hook`, `cron`, `evento` o `humano`, según qué automatización invoca a la pieza.
- **Estados:** `sin-corridas` · `evidencia-vencida` (la pieza cambió después de su última evidencia) · `corrio-sin-hallazgos` · `corrio-con-hallazgos` · para workflows, `corriendo`, `fallando`, `nunca-corrio`.
- **Deriva:** rutas citadas entre backticks que ya no existen.

## Límites

- La evidencia se atribuye por nombre; una pieza con evidencia en un archivo sin su nombre figura `sin-corridas`.
- «Hallazgos» es un conteo textual (🔴, ✗, ALTA, bloqueante…). Un informe limpio cuenta como `corrio-sin-hallazgos`, que puede ser un buen control o una pieza sin efecto: lo decide una persona.
- No mide el valor del resultado (acierto del revisor, tiempo ahorrado).

## Evidencia de uso

`salidas/eficacia-de-agentes.md` (08/11/2026), sobre los repos del proyecto sin el catálogo de la cátedra: 75 piezas (52 skills, 12 agentes, 11 workflows). Mostró, por ejemplo, workflows en ejecución real con su tasa de éxito, `vaivendev:revisar-pr` fallando (6 éxitos de 9), y piezas cuyas especificaciones citan rutas que ya no existen.

## Ejemplo de uso

**Pedido:** ¿Cuáles de los agentes y skills del proyecto realmente operan?

**Resultado:** Descubre las piezas de los repos, cruza evidencia y ejecuciones de workflows, y devuelve una tabla por estado con las que no corrieron, las de evidencia vencida y los workflows que fallan.
