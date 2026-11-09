---
name: g02-catalog-publisher
description: Usar para subir o actualizar los agentes y skills del grupo 02 (Zest) en el Catálogo Común de Agentes de la materia (Laboratorio-4-2C-2026/catalogo-agentes). Los exporta de Multica, les arma la ficha, valida y abre el PR.
metadata:
  tipo: skill
  area:
  - documentacion
  fase:
  - despliegue
  tecnologias:
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  - multica
  grupo: '02'
  autor:
    nombre: Ines Gassiebayle
    github: inesgassiebayle
  responsables:
  - inesgassiebayle
  madurez: experimental
  relacionados:
  - g03-revisor-de-fichas
---
# Publicador en el Catálogo Común de Agentes — grupo 02 (Zest)

## Contexto
- Repo: `Laboratorio-4-2C-2026/catalogo-agentes`. Reglas: `CONTRIBUTING.md`, `prompts/1-preparar-piezas.md` (subir) y `prompts/2-actualizar-pieza.md` (actualizar). **Leerlos al empezar cada corrida**: si cambiaron, mandan sobre esta skill.
- Somos el **grupo 02**: prefijo `g02-`, `grupo: "02"`, ramas `g02-...`.
- Integrantes (`integrantes.yml`, `grupo-02`, ya inscriptos en la pestaña "Inscripción catálogo" del Tablero): Ines Gassiebayle (`inesgassiebayle`, Tech Lead), Liz Lubelcyk (`lizlubelczyk`, QA), Luz Laura (`luzlaura`, PM), Maria Clara Lopez (`ClaraLopez1`, PO).
- **Cómo cuenta la cátedra:** cada integrante tiene que llegar a **10 piezas como autora**. Cuentan los agentes, las skills y los comandos por igual; los colaboradores no suman. El autor sale de la ficha (no de quién hace el push) y no se puede cambiar nunca. No hace falta subir todo de una vez.
- Cada agente de Multica se sube como **agente** (`agentes/g02-nombre/g02-nombre.md`) y cada skill que usa, como **skill** (`skills/g02-nombre/SKILL.md` con sus scripts al lado).
- **Regla principal del catálogo:** no se cambian las instrucciones ni el comportamiento de ninguna pieza. Solo cambian el nombre, la ubicación y la ficha, y se agrega `## Ejemplo de uso`.

El trabajo tiene **tres fases**. Cada una necesita la confirmación de una persona del equipo en el issue antes de pasar a la siguiente.

## Fase 1 — Preparar (sin subir nada)

### 1. Copia del catálogo y rama
```bash
cd ~/zest-agentes
[ -d catalogo-agentes ] || gh repo clone Laboratorio-4-2C-2026/catalogo-agentes
cd catalogo-agentes && git checkout main && git pull
git checkout -b g02-carga-agentes      # si ya existe: g02-carga-2, g02-carga-3...
python3 -m pip install --user pyyaml -q
```
Si el clone o el pull fallan por permisos, frenar y avisar: hay que aceptar las invitaciones de GitHub a la organización y al repo.

Revisar qué carpetas `g02-` ya existen en `skills/` y `agentes/`: esas piezas **no se duplican**. Para cambiarlas se usa la fase de actualización (ver al final).

### 2. Exportar de Multica
```bash
cd ~/zest-agentes/catalogo-agentes
python3 <ruta-de-esta-skill>/to_catalog.py export /tmp/g02-snapshot.json
python3 <ruta-de-esta-skill>/to_catalog.py plantilla /tmp/g02-snapshot.json /tmp/g02-fichas.json .
```
Con la copia del catálogo (`.`), la plantilla marca `incluir: false` las piezas que **ya están en `main` o en una rama `g02-*` de un PR abierto** (por ejemplo, las de una compañera cuyo PR todavía no se mergeó), para no duplicarlas. Las informa por pantalla; revisarlas y, si hay que incluirlas igual, cambiar el valor a mano. Para actualizar piezas ya subidas, agregar `--todas`.
El export trae los agentes que esta cuenta puede ver, con sus instrucciones y las skills vinculadas (contenido y archivos). Nunca incluye configuración MCP, variables de entorno ni tokens.

**Agentes de las compañeras:** si un agente del grupo no aparece en el snapshot (porque es privado de otra integrante), pedir en el issue que lo compartan con el workspace o que peguen su definición (nombre, instrucciones y skills). Si la pegan, agregarlo a `agents` del snapshot con el mismo formato y su `owner_id`.

Si el pedido indica qué piezas subir, marcar las demás con `"incluir": false` en `fichas.json`.

**Antes de seguir, revisar cuatro cosas y anotarlas como dudas en la tabla del issue:**
1. **Nombres:** el catálogo no permite el mismo nombre en `agentes/` y en `skills/` (el validador lo rechaza). Si un agente y su skill se llaman igual, la plantilla le agrega `-agent` al agente (por ejemplo `g02-console-check-agent`). No renombrar a mano de otra forma.
2. **Descripción vacía:** si una skill de Multica no tiene descripción, escribirla en `fichas.json` (la ficha no es parte de las instrucciones, por lo que se puede).
3. **Scripts que faltan:** si las instrucciones de una skill dicen "el script X de esta skill" y X no está entre sus archivos, avisar en el issue **antes de subir**: la pieza quedaría incompleta en el catálogo. (Los archivos que la skill genera al correr, como `issues.json` o `propuesta.json`, no cuentan.)
4. **Datos internos:** el catálogo es público. Si una pieza trae IDs de planillas, URLs internas o claves, avisarlo en la tabla. El filtro automático solo detecta claves y tokens conocidos, no el resto.

### 3. Completar las fichas
Para cada pieza de `/tmp/g02-fichas.json`, **leer sus instrucciones completas** en el snapshot y completar:

| Campo | Cómo completarlo |
|---|---|
| `name` | Ya viene como `g02-nombre`. Corregirlo solo si no dice qué hace la pieza (minúsculas, números y guiones, máximo 64). |
| `description` | Una o dos oraciones en español: qué hace y cuándo usarla, mencionando el caso concreto (Zest, Multica, el tablero de la cátedra) para que se distinga de piezas parecidas. |
| `area`, `fase`, `tecnologias`, `metodologia`, `requiere` | Usar primero los valores de `taxonomia.yml`. `tecnologias`: las que usa la pieza (`react`, `nestjs`, `prisma`, `postgresql`, `typescript`...) o `[agnostico]`. `requiere`: servicios externos (`github`, `google-sheets`, `multica`...) o `[]`. Si un valor es nuevo, anotarlo como "valor nuevo". |
| `herramientas` | `[claude-code]` (los agentes de Multica corren con Claude Code), salvo que el pedido diga otra cosa. |
| `madurez` | La que indique el pedido. Si no lo dice: `experimental` y anotarlo como "madurez sin confirmar". |
| `colaboradores` | Solo si el pedido los indica, con `nombre` y `github` de la lista del grupo. El autor lo pone el script según quién creó la pieza en Multica: **no adivinarlo**. |
| `relacionados` | Buscar en `skills/` y `agentes/` piezas parecidas de otros grupos (por ejemplo `g03-status-risks` para un status report) y nombrarlas. |
| `ejemplo` | `pedido`: algo concreto que alguien le pediría. `resultado`: qué hace, en una o dos oraciones, **basado solo en sus instrucciones**. |

### 4. Generar las piezas
```bash
python3 <ruta-de-esta-skill>/to_catalog.py build /tmp/g02-snapshot.json /tmp/g02-fichas.json .
```
El script escribe las carpetas, renombra las skills en el campo `skills:` de cada agente, copia los scripts de apoyo, no toca piezas que ya existen y se niega a escribir una pieza si encuentra algo que parece una clave o un token. Imprime la tabla de resultados.

Si alguna pieza quedó con "falta completar", volver al paso 3. Si quedó con "falta autor", pedir en el issue quién la hizo y agregarlo como `autor` a mano en su ficha.

### 5. Validar
```bash
python3 scripts/validar.py --base origin/main
```
Tiene que decir **"Todo en orden"**. Si no, corregir las fichas (nunca las instrucciones) y repetir.

Recomendado: revisar las fichas con la skill del catálogo `skills/g03-revisor-de-fichas/SKILL.md` en **modo local** y aplicar solo las sugerencias de clasificación, descripción, ejemplo y relacionados.

### 6. Mostrar el resultado y esperar
Comentar en el issue (sin hacer commit):
1. La tabla: nombre | tipo | autor | colaboradores | area | fase | tecnologias | requiere | madurez | dudas.
2. Cuántas piezas quedaron por autor.
3. Las piezas con dudas: "madurez sin confirmar", "falta autor", "referencia a revisar" (instrucciones que nombran una skill por su nombre viejo: **no se cambian**), "valor nuevo".
4. El avance de cada integrante hacia las 10 piezas como autora: las que ya están en el catálogo (contar las carpetas `g02-` cuyo `metadata.autor.github` es suyo) más las de este PR, y cuántas le faltan.
5. Al final: **"Para subir, respondé 'subir' (o indicá los cambios)."**

## Fase 2 — Subir (solo con "subir" en el issue)
```bash
cd ~/zest-agentes/catalogo-agentes
git add skills agentes
git commit -m "Agregar piezas del grupo 02"
git push -u origin <rama>
gh pr create --base main --title "Piezas del grupo 02" --body-file /tmp/g02-pr.md
```
`/tmp/g02-pr.md`: cantidad de piezas por tipo y por autor, y la lista de dudas abiertas.

Trabajar **siempre en una rama del repo**, nunca en un fork: el bot necesita poder corregirla. Solo tocar piezas `g02-`.

Después del push, esperar el **comentario automático del bot** (reintentar cada 2 minutos, hasta 15):
```bash
gh pr view --comments
```
El bot puede mover piezas, normalizar valores o sumar integrantes, y deja sus cambios en la rama. Si informa errores, hacer `git pull`, corregir las fichas, volver a validar y hacer push. Comentar en el issue el link al PR y qué dijo el bot, y terminar con **"Para aceptar el PR, respondé 'mergear'."**

## Fase 3 — Aceptar el PR (solo con "mergear" en el issue)
Verificar que el último comentario del bot no tenga errores y que los checks estén en verde (`gh pr checks`). Después:
```bash
gh pr merge --merge
```
Avisar en el issue que se mergeó y que el sitio del catálogo se actualiza solo: https://laboratorio-4-2c-2026.github.io/catalogo-agentes/

## Actualizar piezas que ya están
Si el pedido es actualizar (porque cambiaron las instrucciones de un agente o una skill), seguir `prompts/2-actualizar-pieza.md`:
```bash
python3 <ruta-de-esta-skill>/to_catalog.py build /tmp/g02-snapshot.json /tmp/g02-fichas.json . --actualizar
```
Conserva el autor y los colaboradores de la ficha existente. Si el cambio de instrucciones lo hizo alguien que no es autor ni colaborador, agregarlo en `colaboradores` de `fichas.json`. Nunca cambiar `name`, `grupo` ni `autor`, ni quitar a nadie. Usar una rama nueva (`g02-actualizacion-<fecha>`) y seguir con las fases 1 (desde el paso 5), 2 y 3.

## Reglas
- No modificar las instrucciones de ninguna pieza.
- No editar a mano `taxonomia.yml`, `sitio/`, `integrantes.yml` ni las tablas de categorías.
- No subir datos sensibles: si una skill tiene claves, contraseñas o tokens, frenar y avisar.
- No mergear sin el "mergear" de una persona del equipo.

## Ejemplo de uso
**Pedido:** Publicá las piezas nuevas en el catálogo.
**Resultado:** Explica las tres fases (preparar, subir, mergear), cada una con confirmación del equipo, y las reglas para no modificar instrucciones ni subir secretos.
