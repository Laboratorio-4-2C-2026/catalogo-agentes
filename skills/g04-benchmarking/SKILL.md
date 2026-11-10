---
name: g04-benchmarking
description: 'Compara un producto o una funcionalidad con alternativas reales: matriz de capacidades con fuentes verificables y oportunidades concretas. Usar cuando se pide investigar la competencia, comparar apps del mercado o elegir entre herramientas.'
metadata:
  tipo: skill
  area:
  - gestion
  - diseno
  fase:
  - analisis
  - planificacion
  tecnologias:
  - agnostico
  metodologia:
  - agnostico
  herramientas:
  - claude-code
  requiere: []
  grupo: "04"
  autor:
    nombre: Manuel Lostaló
    github: ManuLosta
  responsables:
  - ManuLosta
  madurez: experimental
  relacionados: []
---

# Benchmarking

Responde "¿cómo lo resuelven los demás y qué nos conviene hacer?" con evidencia.

## Flujo

1. **Definir la pregunta:** qué decisión va a tomar el equipo con este resultado. Sin decisión no hay benchmarking útil.
2. **Elegir de 3 a 6 alternativas** directas e indirectas, incluida la alternativa informal (una planilla, una libreta).
3. **Definir criterios** antes de buscar, a partir de la funcionalidad: qué ofrece, flujo, precio, plataformas, reseñas.
4. **Investigar** en páginas oficiales, tiendas de apps y documentación. Guardar el link y la fecha de cada dato.
5. **Armar la matriz:** alternativa contra criterio, con "no se pudo verificar" donde falte el dato.
6. **Sacar conclusiones:** qué se volvió estándar, qué hacen mal y qué oportunidades concretas hay.
7. **Filtrar por el alcance:** contrastar con `out_of_scope`. Lo que queda fuera se menciona, pero no se propone.

## Reglas

- Cada afirmación lleva su fuente. Separar datos de opinión.
- No copiar textos ni diseños de otros: se describe y se resume.
- Decir qué no se pudo verificar y cuándo se consultó, porque precios y funciones cambian.

## Ejemplo de uso
**Pedido:** Hacé un benchmarking de apps de mantenimiento de vehículos para el recordatorio de kilometraje.

**Resultado:** Una matriz de cinco apps con funciones, precio y fuentes, qué hace bien cada una y tres oportunidades para PitStop dentro del alcance del MVP.
