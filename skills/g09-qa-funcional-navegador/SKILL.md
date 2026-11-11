---
name: g09-qa-funcional-navegador
description: Verifica funcionalidades y regresiones de una PR de Zervi o Conexia contra sus tickets, con pruebas pertinentes y navegación real en Google Chrome. Entrega una matriz de criterios y evidencia; no se limita a revisar el código ni al smoke test de un despliegue.
metadata:
  tipo: skill
  area:
  - qa
  - frontend
  - backend
  fase:
  - testing
  - revision
  tecnologias:
  - react
  - typescript
  - kotlin
  - spring-boot
  - nestjs
  - prisma
  - postgresql
  metodologia:
  - agnostico
  herramientas:
  - codex
  requiere:
  - github
  - jira
  - chrome
  grupo: "09"
  autor:
    nombre: Xoaquin Sanchez Varsallona
    github: XoaquinSanchezVarsallona
  responsables:
  - XoaquinSanchezVarsallona
  madurez: experimental
  relacionados:
  - g09-review-ticket-pr
  - g09-ticket-test-matrix
---
# QA funcional y navegador

Comprobá el comportamiento implementado contra los criterios de aceptación y entregá resultados reproducibles. Esta definición formaliza la guía de QA ya recopilada; no agrega otro agente por separar ejecución de navegador y análisis funcional.

## Entrada y procedimiento

Recibí proyecto, PR o revisión, tickets, entorno, cuentas/roles y alcance de pruebas con escrituras. Si no se indica PR, intentá identificar la asociada a la branch y resolvé cualquier ambigüedad. Conservá cambios locales y registrá base y SHA objetivo.

Leé la [guía de QA de Zervi](references/qa-pr-zervi.md), que define recuperación de requisitos, matriz, pruebas, navegación real, usabilidad, evidencia y veredictos. Aplicá sus pasos y formato. Para Zervi, usá el checkout elegido y sus instrucciones vigentes; para Conexia, adaptá las referencias de arquitectura y comandos al código real:

- Consultá sus scripts frontend/backend, esquema y migraciones Prisma y guía `conexia/e2e/README.md`. No ejecutes tareas Gradle ni traslades rutas o casos del marketplace a Conexia.
- Usá los roles, autenticación e integraciones realmente implementados; los ejemplos Auth0 de la guía no son requisitos de Conexia.
- Los casos de pagos, reservas o reseñas solo aplican cuando existan y estén relacionados con el cambio. Un caso no aplicable necesita motivo.
- Resolvé la URL y la revisión ejecutada antes de atribuir resultados a una PR. Si faltan acceso a tickets, Chrome, sesiones o servicios, marcá los casos afectados como bloqueados y continuá con lo independiente.

Confirmá los comandos desde el checkout actual; la guía contiene ejemplos históricos. Priorizá los casos relacionados con el cambio y sus consumidores. Si existe un mapa del analista de impacto, usalo como insumo verificable para seleccionar regresiones, sin sustituir los requisitos del ticket.

## Pruebas y límites

Validá resultados observables en Chrome: navegación desde el inicio del flujo, acciones, respuestas, recarga/persistencia, roles, consola/red y vistas desktop/móvil cuando corresponda. Usar mocks o interceptaciones valida el alcance simulado; no demuestra autenticación, persistencia o integraciones reales. Un viewport móvil no demuestra comportamiento en un dispositivo físico.

Usá cuentas y fixtures de prueba y respetá el alcance autorizado. Crear datos de prueba solo está permitido si la solicitud cubre esas acciones y el ambiente; no envíes notificaciones a terceros ni hagas cobros como efecto implícito de QA. No expongas tokens, cookies ni información personal en capturas o logs. La revisión no corrige código, mergea, despliega ni publica comentarios salvo que otra instrucción del usuario lo autorice.

## Resultado

Entregá informe con criterio → caso → esperado → observado → evidencia, comandos/checks y sus SHA, entorno, hallazgos reproducibles, severidad, relación con la PR y pendientes. Guardalo donde indique el usuario; por defecto usá `docs/qa/PR-<numero>.md` en Zervi o `qa/PR-<numero>/informe.md` en Conexia. Esta selección de destino adapta el ejemplo Zervi de la guía al proyecto elegido.

Usá APROBADO, CON HALLAZGOS, BLOQUEADO o INCOMPLETO según lo ejecutado. Aprobá solo con criterios claros, comprobaciones requeridas realizadas y ausencia de fallas/bloqueos relevantes. Distinguí pruebas automáticas, observación real, inferencias de código y aspectos pendientes; una prueba omitida no es un aprobado. Si cambia el SHA, separá las evidencias y repetí lo afectado.

## Ejemplo de uso

**Pedido:** Validá la PR de edición de perfil contra su ticket en el entorno de prueba indicado, recorriendo el flujo en Chrome con las cuentas disponibles.

**Resultado:** Un informe con matriz de criterios, pruebas automáticas y navegación observada, evidencia, hallazgos y casos bloqueados o pendientes.
