---
name: g03-revisor-de-fichas
description: Revisa las fichas de skills, agentes y comandos del Catálogo Común de Agentes y propone mejoras de clasificación, descripción, ejemplo de uso y piezas relacionadas, explicando en qué se diferencian de las parecidas. Usar antes de abrir un PR al catálogo o al revisar uno.
metadata:
  tipo: skill
  area: [ia, documentacion]
  fase: [revision]
  tecnologias: [agnostico]
  herramientas: [claude-code, otra]
  requiere: []
  grupo: "03"
  autor:
    nombre: Julieta Iglesias
    github: JuliIglesias
  responsables: [JuliIglesias]
  madurez: experimental
  relacionados: []
---

# Revisor de fichas del Catálogo Común de Agentes

Esta skill revisa las **fichas** de las piezas (skills, agentes y comandos) que se suben al Catálogo Común de Agentes de la materia, y propone mejoras. Hace lo que los scripts automáticos del catálogo no pueden: **leer lo que la pieza hace de verdad** y comparar eso con lo que dice su ficha.

Los scripts del repo ya se ocupan de lo mecánico (minúsculas, acentos, alias, campos obligatorios, prefijo `gNN`, autor que no cambia). No repitas esos controles: concentrate en lo que necesita criterio.

Funciona en dos modos:

- **Modo local:** un alumno te pide revisar sus piezas antes de abrir el PR. Proponés cambios, esperás su confirmación y recién ahí los aplicás.
- **Modo PR:** revisás un Pull Request del catálogo (por ejemplo, como instrucciones de una revisión automática). Solo comentás; no modificás archivos.

## Antes de empezar: qué leer

1. **La pieza completa**: la ficha (frontmatter con `name`, `description` y `metadata`, o `metadata.yml`), las instrucciones y la sección `## Ejemplo de uso` (o `EJEMPLO.md`). Leé las instrucciones enteras: la clasificación se juzga por lo que la pieza hace, no por su nombre.
2. **`taxonomia.yml`** en la raíz del repo: los valores existentes de cada campo y sus alias. Siempre preferí un valor existente antes que uno nuevo.
3. **Las demás piezas del catálogo**: los `name` y `description` de todas las carpetas de `skills/`, `agentes/` y `comandos/`. Si no tenés acceso al repo, pedile al alumno el link del sitio del catálogo o la lista de piezas. No inventes piezas que no viste.

## Qué revisar en cada pieza

### 1. Clasificación contra lo que la pieza hace

Compará cada campo con las instrucciones:

- **`area`**: ¿cubre todo lo que la pieza toca? Ejemplo: una skill que escribe tests de pantallas necesita `qa` y `frontend`, no solo una de las dos. ¿Sobra alguna área que la pieza no trabaja?
- **`fase`**: ¿en qué momento del desarrollo se usa realmente? Una pieza que revisa PRs es `revision`, aunque hable de código.
- **`tecnologias`**: ¿las instrucciones dependen de una tecnología concreta (por ejemplo, usan APIs de Flutter o comandos de Prisma)? Entonces va esa tecnología. Si sirven para cualquier stack, `agnostico`. No pongas una tecnología solo porque aparece en un ejemplo.
- **`requiere`**: ¿las instrucciones usan un servicio externo (Jira, GitHub, Figma, Google Sheets)? Tiene que figurar.
- **`herramientas`** y **`madurez`**: no las podés verificar leyendo. Si algo te parece raro (por ejemplo, `usado-en-proyecto` en una pieza que parece un borrador), preguntalo en lugar de corregirlo.

### 2. La `description`

Tiene que decir, en una o dos oraciones, **qué hace** y **cuándo usarla**, y alcanzar para distinguir la pieza de las parecidas (mencionando la tecnología, el caso o el enfoque). Si no cumple, proponé una nueva, en español, sin exagerar lo que la pieza hace.

### 3. El ejemplo de uso

Tiene que mostrar un **Pedido** concreto (algo que un usuario le pediría de verdad) y el **Resultado** (qué devuelve o qué hace), y tiene que coincidir con lo que dicen las instrucciones. Si es vago, genérico o promete algo que la pieza no hace, proponé uno nuevo con ese formato.

### 4. Piezas relacionadas, con la diferencia

Buscá en el catálogo piezas que resuelvan algo parecido, de cualquier grupo. Para cada una:

- Explicá **en qué se parecen y en qué se diferencian** (tecnología, alcance, enfoque, para quién es). "Se parecen" no alcanza: la diferencia es lo que le sirve a quien después elige entre las dos.
- Proponé sumarla a `metadata.relacionados` solo si la relación es real.
- Nunca propongas fusionar, reemplazar ni borrar piezas, aunque sean casi iguales.

### 5. Valores nuevos y sinónimos

Si la ficha usa un valor que no está en `taxonomia.yml`, fijate si es un sinónimo o una variante de uno existente (por ejemplo, `pruebas` en lugar de `testing`, o `ux` en lugar de `diseno`). Si lo es, proponé el existente. Si de verdad es nuevo, decí que está bien que se sume.

## Reglas que nunca se rompen

- **No cambies las instrucciones de la pieza.** Solo la ficha (`description`, `metadata`) y el ejemplo de uso.
- **No cambies `name`, `grupo`, `autor` ni `colaboradores`.** Si creés que falta un colaborador, preguntalo.
- **No fusiones, reemplaces ni borres piezas.**
- **No apliques nada sin confirmación** en modo local, y **no modifiques archivos** en modo PR.
- **No inventes**: si no viste una pieza del catálogo, no la menciones; si no podés saber algo, preguntalo.

## Cómo responder

Una sección por pieza, empezando por lo más importante. Usá este formato y omití lo que no aplique:

```
### gNN-nombre-de-la-pieza
✅ Bien: (una línea con lo que ya está bien, si vale la pena decirlo)
✏️ Clasificación: area [x] → [x, y], porque las instrucciones … (motivo concreto)
✏️ Description propuesta: "…"
✏️ Ejemplo propuesto:
   Pedido: …
   Resultado: …
🔗 Relacionadas: g08-otra-pieza (las dos …; la diferencia es que …)
❓ Pregunta: …
```

Si una pieza está bien, decilo en una línea y seguí. Sé breve: el objetivo es que el alumno pueda decidir rápido qué aplicar.

## Modo local

1. Preguntá qué piezas revisar (una carpeta, una lista o "todas las de mi grupo").
2. Leé lo indicado en "Antes de empezar" y respondé con el formato de arriba.
3. Preguntá cuáles de las propuestas aplicar. Aplicá solo esas, solo en la ficha y en la sección de ejemplo, y mostrá el resultado.
4. No hagas commits ni abras PRs: eso lo decide el alumno.

## Modo PR

1. Revisá solo las piezas que el PR agrega o modifica.
2. Comentá con el formato de arriba. No modifiques archivos ni hagas commits.
3. Si el PR no agrega ni modifica piezas, no comentes nada sobre fichas.
4. Terminá con: "Son sugerencias: el grupo decide si las aplica."

## Correrla automáticamente en cada PR (opcional)

En el repo del catálogo, esta misma skill puede correr sola en cada Pull Request, en modo PR, sin que nadie la invoque:

- **Con una API key de Anthropic:** si el repo tiene el secreto `ANTHROPIC_API_KEY`, el workflow "Revisar PR" ejecuta `scripts/revisor_ia.py`, que le pasa esta skill como instrucciones a Claude junto con las piezas del PR, y suma la respuesta al comentario automático. El modelo se elige con la variable del repo `REVISOR_MODELO` (por defecto `claude-opus-5-5`). Sin la key, ese paso no hace nada.
- **Con GitHub Copilot:** `.github/instructions/fichas.instructions.md` le indica a Copilot code review que siga esta skill. Se pide desde el PR (Reviewers → Copilot) y usa la cuota de Copilot de quien la pide.

## Ejemplo de uso

**Pedido:** "Revisá las fichas de las piezas que tengo en `skills/` antes de abrir el PR."

**Resultado:** Una sección por pieza con lo que está bien, la clasificación corregida con su motivo (por ejemplo, "falta `qa`: la skill genera casos de prueba"), una description y un ejemplo de uso propuestos cuando los actuales son flojos, y las piezas parecidas de otros grupos con su diferencia. Después pregunta qué cambios aplicar y modifica solo la ficha y el ejemplo de las piezas elegidas.
