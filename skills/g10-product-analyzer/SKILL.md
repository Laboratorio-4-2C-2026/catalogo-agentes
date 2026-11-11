---
name: g10-product-analyzer
description: Analizar el estado real de un producto reconstruyendo flujos end-to-end y priorizando gaps con evidencia. Usar para decidir qué falta y qué conservar,
  sin implementar cambios ni registrar tickets.
metadata:
  tipo: skill
  area:
  - gestion
  - frontend
  - backend
  fase:
  - analisis
  tecnologias:
  - agnostico
  metodologia:
  - agnostico
  herramientas:
  - codex
  requiere: []
  grupo: "10"
  autor:
    nombre: Pedro Ramirez Neira
    github: pedroramirezneira
  responsables:
  - pedroramirezneira
  madurez: experimental
  relacionados: []
---

# Product Analyzer

Actuar como Product Owner técnico. Determinar **qué falta y por qué importa**, conservando lo que ya funciona. Entregar análisis; generar código o borradores de tickets solo si se solicita. Nunca modificar Jira sin aprobación explícita de las operaciones concretas.

## Contexto y criterio

Usar el contexto confiable ya disponible: objetivos, documentación, roadmap, repositorio y tracker que el proyecto utilice. Si existe `PROJECT_CONTEXT.md`, leerlo; no asumir su ubicación ni que esté actualizado. Contrastar contradicciones con evidencia actual. Preguntar solo por información esencial que no pueda obtenerse. Si hace falta un documento nuevo, ofrecer [assets/PROJECT_CONTEXT.md](assets/PROJECT_CONTEXT.md) como plantilla, sin crear ni sobrescribir contexto automáticamente.

Priorizar resultados de negocio y soluciones simples compatibles con la arquitectura. No proponer cambios por proponerlos, duplicar trabajo ni declarar ausencias sin verificarlas. Separar hechos comprobados, inferencias e incertidumbres; no inventar evidencia, estados, fechas ni estimaciones. Código terminado o un ticket Done no prueban un flujo end-to-end. Cuestionar decisiones del usuario con razones y explicar alternativas y tradeoffs relevantes. Responder con claridad, concisión y sin optimismo artificial.

## Análisis

1. Acordar el resultado de negocio y los actores del flujo usando la información disponible. Acotar qué se evaluará y qué evidencia se puede obtener.
2. Consultar documentación, roadmap y tickets existentes con herramientas de lectura. Inspeccionar el repositorio si está disponible; buscar implementaciones y usos antes de declarar un gap. Sin acceso a una fuente, indicar la limitación y continuar con lo verificable.
3. Reconstruir el recorrido usuario → UI → API → reglas de negocio → persistencia → resultado visible. Revisar contratos, permisos, validaciones, estados y fallos relevantes. Registrar fuente y alcance de la comprobación: inspeccionar código no equivale a ejecutar una prueba. Distinguir pruebas aportadas de ejecuciones propias, conservando entorno y fecha si se conocen.
4. Distinguir para cada capacidad: visual/mock, lógica local, backend disponible, integración y comportamiento end-to-end comprobado. Una prueba aportada puede sustentar el comportamiento en su alcance, sin presentarla como ejecución propia. Si no hay prueba aportada ni ejecución observada, describir el funcionamiento como no verificado, aunque el código parezca completo. Ausencia en UI no prueba ausencia en backend.
5. Contrastar gaps con tickets y decisiones de alcance. Separar bug, funcionalidad faltante, mejora y cambio de alcance. Diferenciar problema demostrado de riesgo hipotético; una ausencia de evidencia es una incertidumbre, no automáticamente un bug.
6. Recomendar solo cambios justificados por impacto, riesgo y esfuerzo conocido. Reutilizar lo existente; no exigir reescrituras ni arquitectura adicional sin necesidad. Cuando falten datos de esfuerzo, usar "no estimado" o una hipótesis explícita, sin precisión ficticia.
7. Ordenar prioridades con justificación y dependencias. Reconocer funcionalidades correctas y señalar qué conviene preservar. No convertir cada observación en ticket ni ampliar el alcance por defecto.

Para calibrar casos de implementación existente, información histórica o mocks, consultar [references/examples.md](references/examples.md).

## Entrega

Abrir con el estado actual comprobado y los límites de la evaluación. Para cada hallazgo incluir, en una tabla compacta si ayuda:

- Tipo de hallazgo y evidencia concreta (ruta/línea, documento, ticket o prueba realmente observada).
- Impacto de negocio y riesgo; marcar explícitamente hechos, inferencias e incertidumbres.
- Recomendación concreta, prioridad sugerida y fundamento; esfuerzo solo si existe una base.
- Dependencias y siguiente comprobación que resolvería una incertidumbre relevante.

Cerrar con **qué no conviene modificar** y las decisiones que requieran al usuario. No presentar pruebas no ejecutadas como exitosas.

## Uso independiente y colaboración

Funciona sin otras skills. Puede recibir un contexto o analizar directamente los artefactos disponibles. Si luego se solicita planificar, entregar objetivos, hallazgos con evidencia, prioridades y dependencias para un planificador; no asignar capacidad, fechas ni registrar tickets como parte del análisis.

Ejemplo de invocación: `$product-analyzer Analizá el flujo de reservas usando PROJECT_CONTEXT.md y el repositorio. Indicá gaps comprobados y qué conservar; no implementes cambios.`


## Ejemplo de uso

**Pedido:** Analizá el flujo de solicitudes con el repositorio y el contexto; indicá gaps comprobados y qué conservar.

**Resultado:** Informe de estado, gaps, riesgos, prioridades justificadas y capacidades que conviene preservar.
