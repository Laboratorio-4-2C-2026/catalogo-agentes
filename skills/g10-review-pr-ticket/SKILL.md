---
name: g10-review-pr-ticket
description: Revisar una PR contra su ticket y comprobar su comportamiento con pruebas locales y navegador, conservando evidencia por versión. Usar para obtener un
  veredicto y comentario listo para copiar, sin publicarlo.
metadata:
  tipo: skill
  area:
  - qa
  fase:
  - revision
  - testing
  tecnologias:
  - agnostico
  metodologia:
  - agnostico
  herramientas:
  - codex
  requiere:
  - github
  grupo: "10"
  autor:
    nombre: Pedro Ramirez Neira
    github: pedroramirezneira
  responsables:
  - pedroramirezneira
  madurez: experimental
  relacionados:
  - g10-branch-pr-review
  - g07-code-review-tl
---

# Revisar PR contra ticket

Recibir una PR y un ticket; ejecutar la revision completa, no quedarse en una propuesta de plan. Responder en el idioma del usuario.

## Entrada

Invocaciones equivalentes:

```text
$review-pr-ticket 80 KAN-175
$review-pr-ticket PR=80 ticket=KAN-175
$review-pr-ticket https://github.com/organizacion/repositorio/pull/80 KAN-175
```

Son obligatorios el numero o URL de PR y el codigo o URL de ticket. Inferir el repositorio del remoto del directorio actual, salvo que la URL o el usuario indiquen otro. Inferir el proveedor del ticket de los conectores disponibles y del contexto del proyecto; no asumir Jira por el formato del codigo. Admitir restricciones adicionales: cuenta de prueba, dependencias ya revisadas, servicios reales, dispositivo disponible o alcance limitado.

Preguntar solo por informacion indispensable que no aparezca en el repositorio, ticket o servicios conectados. Si hay ambiguedad real sobre repositorio o ticket, resolverla antes de operar sobre el candidato equivocado. Continuar con el trabajo independiente mientras se espera una respuesta.

## Alcance y autorizacion

- Revisar codigo, contrastar la PR con el ticket y probar su comportamiento. Incluir regresiones introducidas por la PR aunque queden fuera del ticket.
- Crear archivos auxiliares, instalar dependencias y preparar servicios y datos locales aislados cuando sean necesarios. Respetar las restricciones del entorno y las autorizaciones existentes.
- Usar datos de prueba aislados por defecto. Antes de acciones que modifiquen una cuenta o datos reales, describir concretamente que se cambiara y pedir permiso, salvo autorizacion previa explicita para esa accion. Un login manual por si solo no autoriza cambiar datos. No usar credenciales administrativas para eludir el login manual acordado.
- No implementar correcciones en el codigo revisado, modificar la PR, publicar comentarios o reviews, hacer commits, push ni merge, salvo un pedido explicito adicional. El veredicto es una recomendacion en el chat.

## Preparar una revision reproducible

1. Leer las instrucciones del repositorio. Consultar las herramientas conectadas para obtener el ticket completo, criterios de aceptacion, aclaraciones relevantes y dependencias. Obtener los metadatos de la PR, descripcion, rama base, ultimo SHA, diff y checks del mismo SHA. Preferir conectores disponibles; usar CLI autenticada como alternativa.
2. Registrar repositorio, numero de PR, ticket, SHA completo de head y base, fecha, estado inicial y comandos de validacion. Comparar el diff de la PR desde el ancestro comun con su base; no comparar arbitrariamente contra main. Distinguir lo agregado por dependencias incluidas en el diff.
3. Preservar rama inicial, archivos modificados y servicios existentes del usuario. Preparar una copia aislada, preferentemente un worktree detached del SHA revisado, en una ruta permitida. No cambiar el checkout principal ni modificar globalmente Git para resolver problemas de permisos. Pedir la elevacion requerida cuando corresponda.
4. Inventariar lo necesario para ejecutar el alcance: runtimes, dependencias, variables, base, backend, navegador y proveedores externos. Usar puertos, base y nombres de recursos exclusivos; no aplicar migraciones, resets ni seeds a una base compartida o de produccion. No imprimir secretos. Llevar registro de procesos y recursos propios para limpiarlos al terminar.

## Revisar codigo y cumplimiento

Construir una matriz de criterios a partir del ticket antes de disenar las pruebas. Para cada criterio, identificar implementacion, camino de datos y evidencia necesaria. Separar requisito explicito, expectativa inferida y mejora opcional.

Seguir el comportamiento de extremo a extremo: entrada de usuario, estado de UI, request, autenticacion/autorizacion pertinente, contrato del backend, persistencia, respuesta y renderizado al volver a entrar. Comprobar la identidad de las entidades cuando se muestran datos de varias personas o recursos. Revisar exito, carga, errores, cancelacion y reintento segun el flujo modificado.

Buscar regresiones concretas en codigo, dependencias, lockfiles y configuracion afectados. Verificar las hipotesis contra la base cuando sea necesario para atribuirlas a la PR. No afirmar que un fallo es preexistente o nuevo sin evidencia. No volver a validar en profundidad una dependencia declarada ya revisada, salvo que haya cambiado o exista un problema concreto de integracion.

No convertir preferencias personales, mejoras fuera del ticket ni casos excepcionales de bajo impacto en bloqueantes. Priorizar impacto y probabilidad, no solo la posibilidad teorica de fallo.

## Ejecutar verificaciones

Elegir las comprobaciones proporcionales al cambio y al repositorio. Leer [references/testing.md](references/testing.md) al preparar servicios o pruebas de navegador.

- Instalar desde los manifiestos y lockfiles revisados. Si una instalacion limpia falla, conservar su resultado y diagnosticarlo. Una alternativa como `npm install` o `--legacy-peer-deps` permite continuar, pero no convierte la instalacion original en exitosa. No regenerar ni corregir el lockfile para ocultar el defecto.
- Ejecutar compilacion, lint y chequeo de formato aplicables, sin autocorrecciones. Inspeccionar scripts: un comando llamado lint puede incluir `--fix`; invocar directamente la herramienta sin ese flag. Ejecutar las pruebas existentes pertinentes y completar los checks requeridos por el proyecto.
- Separar los checks remotos de GitHub de los resultados locales. Registrar versiones y diferencias de entorno relevantes. Si el formato falla masivamente por finales de linea del checkout, informar el resultado original y hacer una comprobacion diagnostica sin reescribir archivos; no atribuirlo automaticamente a la PR.
- Probar el comportamiento, no solo que compile. Usar navegador para cambios de interfaz y pruebas de API/integracion para backend. Agregar arneses temporales solo cuando ayuden a reproducir los criterios o un defecto. No modificar el codigo productivo para hacerlo pasar.
- Si la PR modifica UI, guardar screenshots reales del navegador para validacion visual manual: cubrir las pantallas afectadas y los estados relevantes del flujo probado; incluir vistas movil y escritorio cuando el cambio afecte el comportamiento responsive. Esperar a que termine la carga antes de capturar. Conservar las imagenes en la carpeta de evidencia, sin secretos ni datos personales, con nombres descriptivos e indicar escenario, viewport y si se usaron datos reales o simulados. Si no se pueden obtener, informar el motivo y dejar esa validacion pendiente.
- Combinar datos controlados y fallos simulados reproducibles con una prueba real del recorrido principal cuando el entorno y la autorizacion lo permitan. Los mocks no prueban que el backend, las reglas o el proveedor real funcionen.
- Cuando se necesite login manual, preparar primero servicios y navegador; solicitarlo con instrucciones concretas y continuar tareas independientes. No cerrar la sesion por una espera corta ni pedir otro login por errores evitables del arnes. No guardar tokens o sesiones salvo necesidad concreta; eliminarlos al terminar.
- Si falta un dispositivo, cuenta, permiso o servicio, completar el resto e identificar exactamente que queda pendiente. No inventar evidencia ni declarar que un flujo funciona porque no se pudo probar. Si impide una conclusion responsable, decir que la revision queda inconclusa en ese punto.

## Cerrar y entregar

Antes de cerrar, comprobar si cambio el head remoto. Si cambio, revisar el delta y repetir solo las pruebas afectadas; identificar claramente el SHA cubierto y cualquier delta sin cubrir. No atribuir al ultimo head pruebas de un SHA anterior.

Conservar evidencias utiles sin secretos: comandos, salidas relevantes, resultados, pasos de reproduccion y capturas recortadas cuando aporten. Comprobar que los archivos productivos revisados siguen intactos. Detener solo los procesos y servicios propios; eliminar copias temporales de credenciales, sesiones y recursos transitorios. Informar que artefactos o datos de prueba se conservan y por que. No borrar recursos del usuario ni modificar su estado para dejar artificialmente el checkout limpio.

Entregar en el chat:

1. **Veredicto:** aprobar, aprobar con observaciones no bloqueantes o pedir cambios. Si falta una verificacion indispensable, explicitar la limitacion y no presentar una aprobacion plena como comprobada.
2. **Hallazgos por impacto:** severidad, bloqueante o no, archivo y linea, reproduccion, esperado, observado y consecuencia. Distinguir fallo en flujo real, fallo simulado, fallo de herramientas/entorno y riesgo detectado solo por lectura. Fundamentar por que un hallazgo exige cambios; no bloquear solo por un caso excepcional sin impacto suficiente.
3. **Matriz del ticket:** criterio, resultado y evidencia o pendiente. No marcar como comprobado un criterio sustentado solo por lectura.
4. **Validaciones:** comandos y resultados relevantes, separando CI remoto y ejecucion local; incluir cualquier alternativa usada para continuar. Resumir las pruebas y enlazar evidencia local cuando exista. No afirmar pruebas exitosas sin salida que lo respalde. Para cambios de UI, incluir enlaces directos a los screenshots conservados y una breve indicacion de que validar manualmente en cada captura.
5. **Limites y limpieza:** validaciones pendientes, cambios reales autorizados realizados, estado del checkout principal y recursos retenidos.
6. **Comentario listo para copiar en la PR:** breve, autosuficiente, con lo que impide aprobar y las observaciones utiles. No publicarlo automaticamente. Evitar duplicar todo el informe cuando una referencia clara basta.



## Ejemplo de uso

**Pedido:** Revisá PR=94 ticket=KAN-197, contrastá criterios y probá el flujo con evidencia.

**Resultado:** Veredicto, hallazgos, matriz del ticket, checks y capturas con límites explícitos.
