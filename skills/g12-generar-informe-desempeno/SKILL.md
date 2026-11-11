---
name: g12-generar-informe-desempeno
description: Prepara un informe de desempeño con la rúbrica acordada, evidencia del trabajo realizado y evaluación guiada del responsable. Usar al evaluar una persona durante un período; no inventa criterios ni puntajes.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - codex
  - otra
  requiere: []
  grupo: '12'
  autor:
    nombre: Marcos Hussey
    github: husseymarcos
  responsables:
  - husseymarcos
  madurez: usado-en-proyecto
  relacionados: []
---

# Generar informe de desempeño

Invocar como `/generar-informe-desempeno persona, desde, hasta`.
Si faltan persona o período, pedirlos juntos. Resolver su identidad en las fuentes de
trabajo del proyecto; ante homónimos, confirmar antes de atribuir tareas.

## Rúbrica y fuentes

Localizar la rúbrica o los criterios acordados mediante documentación accesible o material
aportado por el evaluador. Conservar criterios, descriptores, escala, pesos y fórmula;
registrar versión o fecha para que la evaluación sea reproducible.

No exigir una app privada ni inventar una rúbrica. Si no está disponible, pedirla una vez
y avanzar con la evidencia. Entregar una síntesis factual sin puntajes hasta contar con
criterios. Si se solicita diseñar una rúbrica, presentarla como propuesta separada antes
de usarla para calificar.

Identificar tracker, repositorios, objetivos, entregables y feedback pertinentes al rol.
Usar sólo las fuentes disponibles y autorizadas; no requerir Linear ni otro proveedor.
La autoría de la skill no identifica a la persona evaluadora.

## Evidencia

Recuperar identificadores, enlaces, responsables acreditados, estados, fechas, compromisos
y resultados relevantes al período. Recorrer la paginación y considerar registros
archivados si la fuente los tiene. No filtrar sólo por fecha de creación: un trabajo
antiguo puede haberse entregado en el período.

Definir qué significa entrega o resultado cumplido según la rúbrica: aceptación,
PR lista para revisión, merge, despliegue u otro hito. El cierre de un ticket no prueba
automáticamente los demás. Consultar comentarios e historial cuando hagan falta para
entender bloqueos, reasignaciones o cambios de alcance.

Para métricas de puntualidad, cuando sean pertinentes:

- Usar fechas inclusivas y la zona acordada. Una fecha sin hora se compara como fecha
  local, no como medianoche UTC. Si la zona cambia la clasificación y no está definida,
  pedirla antes de emitir el resultado.
- Deduplicar por ID. Separar entregas, cancelaciones, duplicados y pendientes.
- Clasificar como tardía sólo una entrega posterior al compromiso documentado.
  Sin vencimiento o evidencia del hito, marcar `No verificable`.
- Mostrar a tiempo, tardías y no verificables, con porcentaje
  `tardías / (a tiempo + tardías) × 100`. Con denominador cero: `No calculable`.
- Mostrar pendientes vencidas aparte. El estado actual no demuestra el estado histórico;
  una fecha de vencimiento actual no acredita el compromiso original.
- Acreditar responsable en el momento de la entrega y separar causas de contexto de los
  hechos. No atribuir retrasos de revisión, cambios de alcance o bloqueos sin evidencia.

Si faltan accesos o la consulta es parcial, declarar cobertura. El volumen de tickets,
horas o commits no demuestra por sí solo calidad, colaboración o productividad individual.

## Evaluación guiada

Presentar evidencia por criterio antes de proponer puntajes. Pedir al evaluador en un
único bloque la observación, ejemplo y valoración que falten; admitir `Sin evidencia`.
No repetir preguntas ya respondidas. Distinguir hechos, interpretación, puntajes
propuestos y valoraciones confirmadas.

Aplicar únicamente la fórmula acordada. No reemplazar evidencia ausente por cero.
Si la rúbrica no define el tratamiento de faltantes, dejar el resultado global pendiente.
Revisar contradicciones con el evaluador en vez de resolverlas por suposición.

## Informe

Entregar persona, evaluador, período, fecha de corte, rúbrica, definición de entrega y
cobertura. Incluir:

| Trabajo u objetivo | Responsable acreditado | Compromiso y fuente | Resultado y evidencia | Contexto |
|---|---|---|---|---|

| Criterio | Evidencia | Puntaje propuesto o confirmado | Observación del evaluador | Pendiente |
|---|---|---|---|---|

Cerrar con resultado si es calculable, fortalezas, aspectos a mejorar y acciones realmente
acordadas con responsable y fecha. Si no están acordadas, etiquetarlas como propuestas.
Indicar qué falta para validar el informe.

Entregarlo al solicitante en el chat o formato pedido. No publicarlo, enviarlo a terceros
ni modificar tareas como parte implícita de la evaluación.

## Ejemplo de uso

**Pedido:** /generar-informe-desempeno <persona>, 2026-10-01, 2026-10-31

**Resultado:** Junta la evidencia del período por criterio de la rúbrica, le pide al evaluador lo que falta en un solo bloque y entrega el informe con puntajes propuestos o confirmados, sin inventar criterios.
