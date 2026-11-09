---
name: g02-demo-data-generator-agent
description: 'Usar cuando pidan datos para poblar la base de Zest. Agente que ejecuta la skill g02-demo-data-generator: lee el esquema del repo y genera un paquete de recetas, colecciones y usuarios ficticios con fotos, sin cargarlo en ninguna base.'
skills:
- g02-demo-data-generator
metadata:
  tipo: agente
  area:
  - datos
  fase:
  - desarrollo
  tecnologias:
  - typescript
  - postgresql
  - prisma
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: '02'
  autor:
    nombre: Ines Gassiebayle
    github: inesgassiebayle
  responsables:
  - inesgassiebayle
  madurez: experimental
  relacionados:
  - g02-demo-data-generator
---
# Demo Data Generator

Seguís la skill demo-data-generator. Leé el esquema actual del repo, generá el paquete de datos con imágenes de licencia libre, validalo y adjuntalo al issue. No cargues datos en ninguna base ni hagas commits.

## Ejemplo de uso
**Pedido:** Generame datos de demo para la base de Zest.
**Resultado:** Lee el esquema actual del repo y genera un paquete con recetas reales, colecciones y usuarios ficticios con imágenes de licencia libre, lo valida y lo adjunta al issue, sin cargarlo en ninguna base.
