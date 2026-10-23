---
applyTo: "skills/**,agentes/**,comandos/**"
---

# Revisión de fichas del Catálogo Común de Agentes

Este repo es un catálogo de skills, agentes y comandos de IA hechos por los grupos de la materia. Cada pieza vive en una carpeta `gNN-nombre/` con una ficha (frontmatter con `name`, `description` y `metadata`, o un `metadata.yml`), sus instrucciones y una sección `## Ejemplo de uso`.

Al revisar un PR, seguí la skill `skills/g03-revisor-de-fichas/SKILL.md` en **modo PR**. En resumen:

- Revisá solo las piezas que el PR agrega o modifica. Comentá en español.
- Los scripts del repo ya controlan lo mecánico (minúsculas, alias, campos obligatorios, prefijo, autor). No repitas esos controles.
- **Clasificación:** leé las instrucciones completas y compará con `area`, `fase`, `tecnologias` y `requiere`. Si falta o sobra un valor, decilo con el motivo concreto. Preferí siempre los valores de `taxonomia.yml`; si la ficha usa un sinónimo de uno existente (por ejemplo `pruebas` por `testing`), proponé el existente.
- **Description:** tiene que decir qué hace la pieza y cuándo usarla, y distinguirla de las parecidas. Si no, proponé una.
- **Ejemplo de uso:** tiene que tener un Pedido concreto y un Resultado que coincida con las instrucciones. Si es vago, proponé uno.
- **Relacionadas:** si en el catálogo hay piezas parecidas de cualquier grupo, nombralas y explicá en qué se diferencian. Proponé sumarlas a `metadata.relacionados`.
- **Nunca** sugieras cambiar las instrucciones de la pieza, cambiar `name`, `grupo`, `autor` o `colaboradores`, ni fusionar, reemplazar o borrar piezas.
- No comentes sobre estilo de código ni sobre los scripts o workflows del repo, salvo que el PR los modifique.
- Terminá con: "Son sugerencias: el grupo decide si las aplica."
