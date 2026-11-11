---
name: g10-technical-decision-advisor
description: Comparar alternativas técnicas según necesidades, restricciones y arquitectura, documentando evidencia, tradeoffs y condiciones de revisión. Usar para
  elegir o reconstruir una decisión, sin implementar una migración.
metadata:
  tipo: skill
  area:
  - documentacion
  fase:
  - analisis
  - diseno
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
  relacionados:
  - g04-arquitectura
  - g15-product-adr-drafter
---

# Technical Decision Advisor

Ayudar a tomar una decisión técnica concreta y producir un registro que explique alternativas, evidencia, incertidumbres y consecuencias. Completar la comparación y recomendación; responder en el idioma del usuario.

## Contexto y criterio

Funciona de forma independiente con la solicitud y fuentes disponibles; leer `PROJECT_CONTEXT.md` si existe sin exigirlo ni depender de otras skills. Priorizar el objetivo de negocio y soluciones simples compatibles con lo existente. Reutilizar contexto confiable y preguntar solo por información esencial ausente.

No proponer reemplazos por novedad, complejidad o preferencia personal. Incluir conservar la solución actual cuando sea una alternativa viable. Cuestionar restricciones o conclusiones incoherentes y explicar sus consecuencias sin optimismo artificial. Separar hechos comprobados, testimonios, inferencias y pendientes; no inventar costos, esfuerzo, benchmarks, incidentes ni evidencia.

Analizar y documentar no autoriza implementar adapters, cambiar configuración, crear cuentas, introducir una tarjeta, contratar planes, enviar datos privados a servicios externos ni modificar Jira. Pruebas locales aisladas pueden realizarse si son necesarias para la evaluación; pruebas externas con efectos, costos o datos compartidos requieren un pedido que las cubra. No hacer commits ni publicar resultados automáticamente.

## Evaluar la decisión

1. Delimitar la pregunta: capacidad requerida, consumidores, situación actual y resultado verificable buscado. Identificar decisor y estado de la decisión: propuesta, aceptada por el usuario o reconstrucción histórica. Una recomendación del agente no es una aceptación del equipo.
2. Separar requisitos excluyentes de preferencias. Considerar solo criterios relevantes: cobertura funcional, calidad, compatibilidad, operación, acceso, costos/cuotas y esfuerzo de adopción o salida. No asumir proveedor, región, unidad de costo, presupuesto ni disponibilidad de tarjeta. Documentar los supuestos que cambian la decisión.
3. Inspeccionar contratos y consumidores si hay repositorio, para determinar qué se necesita realmente. Seleccionar pocas alternativas plausibles; respetar el conjunto cerrado si el usuario lo indicó. Verificar primero requisitos excluyentes antes de profundizar en opciones inviables.
4. Consultar fuentes oficiales actuales para capacidades, precios, free tiers, cuotas, requisitos de registro, licencias y versiones que sustenten una elección actual. Registrar enlace, fecha y alcance por afirmación relevante. Distinguir tarjeta requerida, facturación habilitada, cuota gratuita, cobro por excedentes y límites técnicos; no son equivalentes.
5. Si la tarea es offline o reconstruye una decisión pasada, usar fuentes aportadas con su antigüedad y atribuir el relato al usuario. No inventar consultas, experimentos ni condiciones históricas a partir de una web actual. Sin evidencia suficiente de un criterio decisivo, dar una recomendación condicional o dejar esa decisión pendiente; completar el resto.
6. Comparar opciones en una tabla compacta con evidencia y consecuencia práctica. No inventar puntuaciones ni pesos para aparentar objetividad; si se usan, justificar su origen y mostrar cómo cambia la elección con los supuestos. Incluir costos de operación y transición solo con base, o marcarlos por estimar.
7. Examinar diferencias relevantes detrás de una interfaz común: formatos, unidades, estados nulos, errores, autenticación, semántica y calidad de resultados. Un Strategy o adapter facilita sustitución en su contrato; no demuestra equivalencia de proveedores ni que el alternativo esté implementado o probado. Evitar arquitectura adicional sin una necesidad concreta.
8. Para un problema reportado, distinguir observación y causa. Por ejemplo, coordenadas distintas para un texto igual no demuestran por sí solas un defecto no determinista: si importa para decidir, proponer o ejecutar dentro del alcance una comparación controlada de request, parámetros, idioma, contexto, tiempo y respuesta. No universalizar una anécdota.
9. Recomendar la opción más defendible, o conservar la actual, con razones, tradeoffs aceptados, riesgos y condiciones de revisión. Separar reversibilidad de diseño de migración comprobada; indicar qué faltaría validar para sustituirla. No prometer ausencia de impacto por tener una abstracción.

## Entrega y evidencia

Adaptar [assets/TECHNICAL_DECISION.md](assets/TECHNICAL_DECISION.md) al caso. Para ejemplos de restricciones operativas, comparación offline o conservación de una solución, leer [references/examples.md](references/examples.md).

Entregar en el destino pedido, o en el chat si no se pidió archivo:

- Pregunta, objetivo, contexto y requisitos excluyentes/preferencias.
- Alternativas y matriz de criterios con hechos, fuentes e incertidumbres.
- Recomendación fundamentada y estado de la decisión; ventajas y costos aceptados.
- Compatibilidad, riesgos, reversibilidad y condiciones para reconsiderar.
- Pruebas efectivamente realizadas, resultados, límites y siguientes comprobaciones necesarias.

Si faltan originales y se pide reconstruir un caso, etiquetar el documento como **reconstrucción elaborada ahora**, atribuir testimonios y enlazar evidencia actual por separado. No escribir una fecha de aceptación pasada ni simular actas, capturas, resultados de pruebas o documentos del sprint original. Una ejecución actual puede demostrar la capacidad de análisis del agente, sin acreditar el proceso histórico.

## Responsabilidad e invocación

La salida documenta una decisión; no define todo el roadmap, asigna capacidad ni crea tickets o implementaciones. Puede alimentar una planificación o handoff si luego se solicita, sin requerir esas herramientas.

Ejemplo: `$technical-decision-advisor Compará alternativas para este servicio usando PROJECT_CONTEXT.md y el contrato existente. Separá restricciones excluyentes, tradeoffs, evidencia y validaciones pendientes; no implementes cambios.`


## Ejemplo de uso

**Pedido:** Reconstruí la elección de proveedor geográfico con el relato y el contrato actual; distinguí evidencia y pendientes.

**Resultado:** Registro fechado hoy con alternativas, recomendación o decisión relatada, límites y reversibilidad comprobada o pendiente.
