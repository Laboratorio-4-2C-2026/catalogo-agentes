---
name: g09-verificar-despliegue
description: Verifica si una publicación concreta de Zervi quedó correcta comprobando versión, deployments activos, frontend canónico, salud, API, CORS y migraciones. Usar después de un despliegue o para diagnosticar una versión publicada; no publica, corrige infraestructura ni hace rollback.
metadata:
  tipo: skill
  area:
  - devops
  - qa
  fase:
  - despliegue
  - revision
  tecnologias:
  - react
  - vite
  - spring-boot
  - flyway
  - postgresql
  metodologia:
  - agnostico
  herramientas:
  - codex
  requiere:
  - render
  - cloudflare
  - neon
  - chrome
  grupo: "09"
  autor:
    nombre: Xoaquin Sanchez Varsallona
    github: XoaquinSanchezVarsallona
  responsables:
  - XoaquinSanchezVarsallona
  madurez: experimental
  relacionados: []
---
# Verificación de un despliegue

Determiná con evidencia si el ambiente sirve la versión esperada y sus componentes funcionan juntos. Un build exitoso, un deploy marcado live o un HTTP 200 de la home no son suficientes por separado.

## Entrada y preparación

Recibí ambiente y SHA esperado o manifiesto del release. Aceptá IDs de deployments como entrada auxiliar y resolvelos a una revisión verificable. Si solo se pide revisar el ambiente actual, podés comprobar salud y descubrir versiones, pero no certifiques que corresponde a una publicación solicitada sin identificar el objetivo.

Leé completo el [runbook](references/runbook-despliegue.md) y consultá el código de la revisión objetivo para elegir rutas y migraciones. Revalidá URLs, cuentas, IDs y configuración; no uses el estado histórico del runbook ni [el deploy v1.1.0](references/despliegue-historico.md) como resultado actual. Usá herramientas conectadas o APIs de lectura disponibles.

Fijá el SHA esperado al inicio. Si main avanza durante la consulta, no reemplaces ese SHA silenciosamente. Separá el cumplimiento de la política HEAD-de-main al momento de publicar de la identidad de una publicación histórica; un HEAD más reciente no demuestra por sí mismo que el deploy anterior falló. No cambies branches locales ni exijas limpiar el checkout para observar un deployment ya publicado.

## Comprobaciones

1. **Identidad del ambiente y release.** Registrá SHA esperado, origen de ese dato, cuentas/proyectos y URLs estables e inmutables cuando existan. Correlacioná IDs y timestamps del release; los checks de CI de otra revisión no acreditan este release.
2. **Backend activo.** Comprobá servicio, repositorio/rama y deployment que está sirviendo tráfico. Debe estar live/saludable y corresponder al SHA esperado. Un deploy exitoso en el historial que ya fue reemplazado no prueba la versión activa.
3. **Frontend activo.** En Pages comprobá proyecto, `production_branch`, environment, estado y deployment canónico. Una URL de preview o un deployment successful no demuestra que la URL estable apunte a él. Correlacioná metadatos de SHA con hashes/manifest del artefacto o marcador de versión si están disponibles: un hash declarado durante Direct Upload no prueba por sí solo el contenido subido.
4. **Contenido servido.** Consultá la URL estable y la inmutable; verificá HTML y assets esperados. Detectá discrepancias por caché, bundle anterior o service worker cuando haya evidencia. Si no hay trazabilidad de artefactos, dejá la identidad del frontend como no concluyente en lugar de inventar un marcador.
5. **Salud y contrato público.** Consultá `/actuator/health` y un endpoint público real del SHA, por ejemplo categorías si existe. Validá status y contenido esperado: un HTML de error/fallback con HTTP 200 no es una API funcionando. Registrá timestamps, latencia y reintentos acotados para distinguir arranque en frío de falla persistente.
6. **Integración frontend/backend.** Confirmá que el bundle publicado consuma el backend del mismo ambiente y que el preflight CORS para el origen real y un endpoint aplicable devuelva los headers esperados. Probá desde navegador un flujo público de lectura, observando peticiones y errores relevantes.
7. **Persistencia y migraciones.** Compará el historial Flyway del ambiente con las migraciones de la revisión esperada: versiones, éxito y validación/checksums cuando el mecanismo existente lo permita. No fijes V1-V8 ni V1-V11 como estado actual. Consultá metadatos de esquema sin extraer registros personales. Si falta acceso, marcá esta parte no verificada; no ejecutes repair, migraciones ni resets.
8. **Dependencias según alcance.** Para autenticación/R2/pagos, comprobá configuración y flujos de lectura disponibles. Un login con cuenta de prueba requiere sesión disponible; una carga a R2 o una operación de negocio exige alcance de prueba con escrituras y fixtures. No presentes configuraciones o mocks como integraciones reales probadas. No hagas pagos ni envíes notificaciones como comprobación implícita.
9. **Coherencia final.** Volvé a consultar los IDs activos al finalizar para detectar una publicación concurrente. Si cambiaron, indicá el intervalo y qué resultados pertenecen a cada versión; no mezcles pruebas como si se hubieran realizado sobre un solo release. El plan Terraform puede aportar evidencia de infraestructura, pero no reemplaza estos checks ni es necesario para afirmar solo la identidad del artefacto.

## Veredicto e informe

Usá **verificado**, **con fallas** o **no concluyente/parcial** para el alcance solicitado. Solo declaralo verificado si las comprobaciones obligatorias de ese alcance tienen evidencia positiva. Para una verificación completa exigí identidad backend/frontend, frontend canónico, salud/API, integración/CORS y migraciones. Si el usuario pide solo un smoke test, identificá ese alcance limitado y evitá presentarlo como verificación completa.

| Comprobación | Esperado | Observado | Resultado | Evidencia / timestamp |
| --- | --- | --- | --- | --- |

Incluí SHA esperado y observado por componente, IDs activos al inicio/final, URLs, casos probados, reintentos, fallas y comprobaciones bloqueadas o no aplicables con su razón. Si un check confirma un desajuste y otros están bloqueados, informá la falla confirmada y el alcance parcial; la falta de acceso no borra el defecto observado.

Cada aprobado debe tener evidencia observable. Conservá solo datos no sensibles y redactá tokens, cookies, headers de autenticación y datos personales en capturas/logs. Proponé próximos pasos vinculados a la evidencia, sin ejecutarlos automáticamente.

## Límites y aceptación

No dispara deploy, reanuda servicios, invalida cachés, modifica variables, cambia Terraform, ejecuta rollback ni limpia datos. El runbook incluye comandos de publicación: leerlos no autoriza ejecutarlos para verificar. La tarea termina con el informe; si detecta una falla, conserva evidencia y explica qué componente no cumple.

## Ejemplo de uso

**Pedido:** Comprobá si el ambiente indicado sirve el SHA esperado en frontend y backend, incluyendo salud, API, CORS y migraciones, sin publicar cambios.

**Resultado:** Un informe por comprobación con versiones, deployments activos, evidencia y un veredicto verificado, con fallas o parcial según lo observado.
