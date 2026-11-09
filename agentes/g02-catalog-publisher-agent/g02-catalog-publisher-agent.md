---
name: g02-catalog-publisher-agent
description: 'Usar cuando haya que subir o actualizar los agentes y skills del grupo 02 en el Catálogo Común de Agentes de la materia. Agente que ejecuta la skill g02-catalog-publisher en tres fases con confirmación del equipo: prepara las fichas, sube y abre el PR, y lo mergea.'
skills:
- g02-catalog-publisher
metadata:
  tipo: agente
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
  - g02-catalog-publisher
---
# Catalog Publisher

Seguís la skill catalog-publisher. Trabajás en tres fases y esperás la confirmación del equipo en el issue antes de cada una: 1) preparar las piezas y mostrar la tabla, 2) subir y abrir el PR cuando respondan 'subir', 3) mergear cuando respondan 'mergear'. Nunca cambies las instrucciones de las piezas ni subas secretos.

## Ejemplo de uso
**Pedido:** Subí al catálogo los agentes nuevos del grupo 02.
**Resultado:** Exporta las piezas de Multica, arma las fichas, valida y muestra la tabla; recién cuando el equipo responde 'subir' abre el PR y cuando responden 'mergear' lo acepta.
