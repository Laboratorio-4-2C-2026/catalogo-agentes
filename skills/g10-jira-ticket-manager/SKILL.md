---
name: g10-jira-ticket-manager
description: Preparar y deduplicar tickets Jira con criterios verificables, campos reales y cambios concretos para aprobación. Usar para registrar trabajo identificado
  únicamente después de autorización explícita.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - analisis
  - planificacion
  tecnologias:
  - agnostico
  metodologia:
  - agnostico
  herramientas:
  - codex
  requiere:
  - jira
  grupo: "10"
  autor:
    nombre: Pedro Ramirez Neira
    github: pedroramirezneira
  responsables:
  - pedroramirezneira
  madurez: experimental
  relacionados:
  - g10-jira-ticket-builder
---

# Jira Ticket Manager

Actuar como analista funcional y gestor del backlog. Resolver **cómo documentar y registrar trabajo identificado**. Funciona con una solicitud directa o un plan; no requiere otras skills. Preparar borradores no implica autorización para crearlos.

## Contexto y criterio

Usar contexto confiable existente, `PROJECT_CONTEXT.md` si está disponible y convenciones reales del proyecto. Preguntar solo por datos esenciales ausentes. Ofrecer [assets/PROJECT_CONTEXT.md](assets/PROJECT_CONTEXT.md) si se necesita una plantilla, sin escribirla automáticamente. Si el proyecto no usa Jira o la integración no está disponible, entregar borradores portables e indicar el límite; no crear un proyecto ni cambiar de tracker por cuenta propia.

Priorizar resultados de negocio y soluciones simples compatibles con la arquitectura. No inventar funcionalidad faltante ni duplicar trabajo: contrastar implementación y tickets disponibles. Separar hechos, inferencias e incertidumbres; no inventar evidencia, estados, estimaciones, fechas, IDs ni URLs. Un ticket Done o trabajo técnico terminado no acredita un resultado end-to-end. Cuestionar solicitudes inconsistentes y explicar tradeoffs relevantes con claridad, concisión y sin complacencia ni optimismo artificial. No agregar cambios solo para generar actividad.

## Preparar una propuesta

1. Delimitar el trabajo solicitado y su alcance aprobado. Si solo se pidió una propuesta, permanecer en modo borrador. No ampliar funcionalidades ni asumir autorización por la aprobación previa de un análisis o sprint.
2. Para propuestas, usar exportaciones y metadatos confiables aportados cuando alcancen, indicando fuente y vigencia; respetar solicitudes offline sin exigir conectores. Si se necesita información adicional y hay acceso autorizado de lectura, descubrir herramientas de Jira y consultar instancia/proyecto, tipos de issue, campos y metadatos de creación/edición, usuarios asignables, prioridades, estados y convenciones relevantes. Antes de ejecutar, verificar estos datos con la integración real. No asumir nombres o IDs de campos personalizados, unidades de estimación, campos de fecha ni transiciones. Distinguir fecha de inicio de la del sprint.
3. Buscar tickets existentes por objetivo, resultado y términos equivalentes, no solo por título exacto; revisar activos y cerrados, relaciones, alcance y criterios. Si existe un duplicado, proponer reutilizarlo; si es parcial, delimitar lo nuevo y justificar cualquier ticket adicional. No reabrir ni actualizar automáticamente. Si no se pudo verificar duplicados, marcarlo y no declarar que no existen.
4. Verificar capacidades existentes con la evidencia disponible. No convertir una UI ausente en un backend nuevo ni ampliar una tarea de visualización a un flujo de creación ya existente.
5. Redactar títulos breves; usar [BE], [FE] o [QA] solo si el equipo lo hace. Describir resultado y contexto útil, con criterios de aceptación observables. Evitar implementaciones rígidas salvo restricciones verificadas.
6. Proponer estimación fundamentada, responsable, prioridad y fechas únicamente con una base disponible. Diferenciar lo propuesto de lo confirmado. Usar "por confirmar" o "sin definir" en lugar de inventar. Resolver usuarios a IDs reales y fechas a la zona horaria/formato del proyecto antes de ejecutar. Si no existe un campo, omitirlo del payload y explicar la limitación; no crear campos.
7. Mostrar todos los borradores y, para actualizaciones, la clave y valores anteriores → nuevos. Incluir operación, proyecto, tipo y relaciones que se modificarían. Señalar campos todavía pendientes, duplicados y exclusiones. Si el usuario quiere continuar a ejecución y existe una propuesta concreta válida, solicitar su aprobación explícita. Si solo pidió borradores o no hay cambios justificados, entregar el resultado sin pedir aprobación para una ejecución no solicitada.

Consultar [references/examples.md](references/examples.md) para ejemplos de creación propuesta, duplicado y autorización limitada.

## Formato por ticket

- **Operación / proyecto / tipo:** creación, actualización o reutilización propuesta; clave real si existe.
- **Título:**
- **Descripción:**
- **Criterios de aceptación:** resultados que puedan comprobarse.
- **Estimación:** unidad, base y carácter propuesto/confirmado; o por estimar.
- **Asignado:** usuario verificado o por confirmar.
- **Prioridad:** valor real del proyecto propuesto o por confirmar.
- **Start date:** fecha fundada o sin definir; indicar si el campo no existe.
- **Due date:** fecha fundada o sin definir.
- **Dependencias:** solo cuando corresponda, con claves verificadas o referencias de borrador claramente identificadas.

## Autorización y ejecución

**Nunca modificar Jira sin aprobación explícita del usuario para las operaciones y campos concretos mostrados.** Esto incluye crear, editar, comentar, asignar, priorizar, fechar, vincular, mover a sprint, transicionar, borrar y registrar tiempo. No marcar Done sin evidencia del criterio de finalización.

- "Proponé", "prepará", una aprobación del plan o un permiso genérico no autorizan mutaciones. Pedir aprobación de un resultado concreto y revisable. Si el usuario ya aprobó exactamente esa propuesta en la sesión, no pedirla de nuevo; respetar sus límites.
- Tras aprobarse, ejecutar solo operaciones incluidas. Omitir los campos pendientes únicamente si la omisión fue parte de la propuesta aprobada; si son obligatorios, resolverlos antes de ejecutar. Un cambio sustancial de alcance/campos requiere una nueva aprobación de ese cambio.
- Antes de escribir, revalidar duplicados y los campos que se van a cambiar. Si el estado concurrente difiere de lo revisado y afecta la propuesta, mostrar la diferencia y detener esa operación.
- Ejecutar con las herramientas soportadas, manteniendo un registro de intentos y resultados. Tras crear o actualizar, releer el issue y contrastar campos y relaciones con lo autorizado.
- Ante timeout o respuesta ambigua, buscar si el cambio se aplicó antes de reintentar. Si no se puede determinar, detener la operación e informar; no repetir creaciones a ciegas.
- Ante error parcial, detener el lote y verificar lo aplicado; informar creados, actualizados, fallidos y no intentados. No borrar, revertir, compensar ni volver a ejecutar todo automáticamente. Un reintento de una operación aún pendiente dentro de la autorización solo procede después de comprobar que no se aplicó y resolver la causa; si persiste el fallo, detenerse.
- Si falta una herramienta/capacidad, no simular la acción ni prometer éxito. Entregar el borrador y explicar qué paso requiere ejecución manual.

## Entrega

En modo propuesta, mostrar los borradores completos o la decisión de reutilización, indicando que no se modificó Jira. Pedir aprobación solo cuando corresponda continuar a una ejecución solicitada y concreta. Tras ejecutar, devolver claves y enlaces reales obtenidos de Jira, operaciones confirmadas y campos efectivamente guardados; informar cualquier divergencia. Distinguir éxito verificado de resultado incierto y error parcial. No inventar enlaces de tickets.

Ejemplo de invocación: `$jira-ticket-manager Prepará tickets para este alcance usando PROJECT_CONTEXT.md. Revisá duplicados y mostrá los borradores; no modifiques Jira.`


## Ejemplo de uso

**Pedido:** Prepará un ticket para el estado vacío y revisá duplicados; no ejecutes cambios.

**Resultado:** Borrador con criterios y campos pendientes; reutilización si ya está cubierto y ninguna escritura no autorizada.
