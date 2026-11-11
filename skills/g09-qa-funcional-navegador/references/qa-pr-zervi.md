# QA de una pull request de Zervi

## Cómo usar esta guía

Pedile al agente: «Hacé QA de la PR <URL o número> siguiendo `docs/QA_PULL_REQUEST.md`». Podés agregar la URL del entorno y las cuentas de prueba disponibles. Si no indicás una PR, el agente debe intentar identificar la correspondiente a la branch actual.

Las siguientes instrucciones están dirigidas al agente que realiza el QA. El objetivo es comprobar que la feature satisface sus tickets, detectar regresiones y evaluar el flujo real y su usabilidad en **Google Chrome**. Entregá un informe respaldado por evidencia.

## 1. Identificar la PR y recuperar sus tickets

1. Leé los `AGENTS.md` aplicables y revisá el estado del repositorio. Conservá los cambios locales del usuario.
2. Identificá la PR mediante la URL o número recibido, o consultá la PR asociada a la branch actual. Si hay varias candidatas, preguntá cuál revisar.
3. Recuperá título, descripción, branch base, branch de origen, SHA del último commit, archivos modificados, diff completo, comentarios, revisiones y checks de CI. Usá las herramientas conectadas disponibles; si no alcanzan, usá `gh` si está disponible y autenticado.
4. Buscá referencias a tickets en la descripción, enlaces de cierre, título, comentarios, nombre de branch y mensajes de commits. Seguí tanto issues de GitHub como enlaces o claves de un gestor externo, por ejemplo `ZRV-123`.
5. Abrí cada ticket relevante y leé descripción, criterios de aceptación, adjuntos accesibles, decisiones en comentarios y dependencias vinculadas que afecten el alcance. Revisá también especificaciones referenciadas en `docs/tickets/` cuando correspondan.
6. Si un ticket no es accesible, intentá recuperarlo con los conectores disponibles. Si sigue sin acceso, pedí su contenido o acceso. No deduzcas los requisitos únicamente del código implementado.

Registrá las URLs de la PR y de los tickets y el SHA revisado. Compará contra la base real de la PR mediante su ancestro común; no asumas que la base es `main`. Si el diff viene truncado, recuperá los archivos o parches faltantes antes de dar por completa la revisión.

## 2. Entender la feature y resolver dudas

Antes de ejecutar escenarios, explicá brevemente:

- Qué problema resuelve la feature y para qué usuario o rol.
- Desde dónde comienza el flujo y cuál es su resultado esperado.
- Qué reglas, permisos, estados y errores definen el comportamiento correcto.
- Qué partes dependen de otras PR, servicios externos o configuración.

Convertí los criterios de aceptación en casos observables. Conservá el texto o la referencia del requisito original y asigná identificadores estables, como `CA-01` y `QA-01`.

**Si no entendés la feature o hay ambigüedades que cambian el resultado esperado, hacé preguntas concretas antes de validar esos casos.** Por ejemplo: «¿La cancelación está permitida después de confirmar el pago?» o «¿Este botón lo ve el cliente, el prestador o ambos?». Indicá el ticket o criterio que origina la duda. No inventes reglas de negocio ni resuelvas contradicciones entre ticket, comentarios y PR sin consultar.

Mientras esperás respuestas, avanzá con la lectura de código, revisión de tests y escenarios independientes. Marcá como bloqueados los casos que dependen de esas respuestas.

## 3. Preparar la matriz de QA y buscar regresiones

Seguí el cambio desde la interfaz hasta API, permisos, persistencia e integraciones. Revisá también los consumidores de funciones, componentes y contratos compartidos aunque sus archivos no aparezcan en el diff.

Para cada criterio y riesgo concreto, completá:

| Caso | Ticket / criterio o riesgo | Rol y precondiciones | Pasos | Resultado esperado | Test existente o prueba manual |
| --- | --- | --- | --- | --- | --- |
| QA-01 | Enlace y CA-01 | Cuenta, datos y estado inicial | Acciones reproducibles | Comportamiento observable | Ruta del test o escenario en Chrome |

Incluí el camino exitoso, entradas inválidas, estados vacíos, permisos y recuperación de errores que correspondan al cambio. Priorizá regresiones según las dependencias observadas:

| Área afectada | Flujos relacionados que conviene comprobar |
| --- | --- |
| Autenticación, roles o rutas | Login/logout con Auth0, retorno a la ruta solicitada, sesión expirada y acceso como visitante, cliente y prestador |
| Catálogo y servicios | Búsqueda, filtros, resultados, detalle, publicación y edición, imágenes y visibilidad de los cambios |
| Contrataciones / reservas | Crear reserva, listarla, abrir detalle, transiciones de estado y consistencia entre cliente y prestador |
| Pagos | Inicio del pago, retorno del proveedor, estado pendiente/aprobado/rechazado, reintentos y coherencia con la reserva |
| Chat, preguntas y reseñas | Acceso por participantes, envío y lectura, persistencia y restricciones según el estado del servicio o reserva |
| Perfil, componentes o cliente HTTP compartidos | Consumidores reales, navegación, permisos, manejo de errores, caché y actualización de datos |
| Backend, contratos o migraciones | Compatibilidad con frontend, validaciones, autorización, restricciones de base de datos y datos existentes |

Elegí los escenarios que tengan relación demostrable con la PR y explicá esa relación. No conviertas esta tabla en una obligación de probar toda la aplicación en cada revisión.

## 4. Revisar y ejecutar pruebas automatizadas

1. Leé los tests nuevos y existentes de las áreas afectadas. Comprobá qué comportamiento verifican realmente, qué casos faltan y si los mocks ocultan una incompatibilidad con el backend o la interfaz real.
2. Revisá los checks y logs de CI del SHA evaluado. Diferenciá tests fallidos, omitidos y no ejecutados.
3. Ejecutá primero los tests relevantes y después los checks necesarios según el alcance y las reglas del repositorio. Confirmá scripts y tareas en la revisión actual; los siguientes comandos son referencias de este proyecto.

Desde `frontend/`:

```bash
npm test -- src/pages/BookingDetail.test.tsx
npm test
npm run lint
npm run build
```

El primer comando ejemplifica una prueba puntual: reemplazá la ruta por el archivo relacionado con la PR.

Desde `backend/`:

```bash
./gradlew test --tests 'zervi.backend.booking.BookingIntegrationTest'
./gradlew test
./gradlew spotlessCheck
./gradlew bootJar
```

Reemplazá la clase del primer comando por la que corresponda. El backend requiere Java 21; algunas pruebas de persistencia usan PostgreSQL mediante Testcontainers y necesitan Docker. Si la PR afecta la orquestación de reportes, revisá además `node --test scripts/report-kpis.test.mjs` desde la raíz.

Registrá cada comando, directorio, resultado y motivo de cualquier omisión. Un error de entorno o una prueba omitida no cuenta como prueba aprobada. Si encontrás una falla, determiná si fue introducida por la PR; cuando sea necesario, compará con la base en un entorno aislado y sin alterar el trabajo local.

En esta revisión, documentá las pruebas faltantes y las correcciones propuestas. Si el usuario también pidió implementar cambios, ejecutá nuevamente las comprobaciones afectadas después de corregirlos.

## 5. Preparar el entorno para Google Chrome

1. Identificá las herramientas disponibles para controlar **Google Chrome** e inspeccionar su consola y tráfico de red. Confirmá qué navegador se está usando: una ejecución en otro navegador no cumple por sí sola este paso.
2. Usá un preview de la PR o un entorno local que ejecute su revisión. Comprobá el SHA desplegado, o registrá expresamente si no pudiste verificarlo. No atribuyas resultados de otro despliegue a la PR.
3. Comprobá si frontend y backend ya están levantados. Consultá `frontend/README.md`, `frontend/.env.example`, la configuración de Vite y la configuración actual del backend antes de iniciar servicios. El frontend documenta `npm run dev` y el puerto 8443; verificá la URL efectiva. Revisá `VITE_API_URL` y la configuración de Auth0 sin volcar secretos al informe.
4. Prepará cuentas y datos de prueba para los roles involucrados. Asegurá que las acciones necesarias puedan ejecutarse en ese entorno. Para pagos, usá el sandbox del proveedor.
5. Si falta acceso a Chrome, una URL accesible, una sesión o datos indispensables, pedí lo que falta y continuá con las comprobaciones independientes. Indicá el bloqueo; no declares navegación real a partir de capturas ajenas, lectura de código o tests unitarios.

## 6. Recorrer el flujo y evaluar usabilidad en Chrome

Ejecutá la matriz de QA desde la entrada real que usaría una persona. No valides únicamente abriendo por URL la pantalla final.

Para cada caso:

1. Registrá rol, URL inicial, datos relevantes y estado previo.
2. Navegá y realizá las acciones del usuario. Verificá el resultado visible y su correspondencia con la respuesta de la API o el estado persistido cuando aplique.
3. Comprobá la persistencia al recargar y el comportamiento al volver atrás, reingresar o cambiar de usuario, según corresponda.
4. Inspeccioná errores de consola y solicitudes de red fallidas o inesperadas. Distinguí los rechazos esperados por el escenario de los errores del producto.
5. Guardá evidencia de los resultados y de cada problema: captura, URL, pasos, respuesta relevante o log, sin tokens ni datos sensibles.

Evaluá la usabilidad durante el recorrido:

- **Claridad:** se entiende qué hacer, qué campos son obligatorios y qué sucedió después de la acción.
- **Feedback:** existen estados de carga, éxito, error y vacío; no quedan botones bloqueados indefinidamente ni acciones duplicadas por varios clics.
- **Recuperación:** los errores explican cómo continuar y conservan los datos ingresados cuando corresponde.
- **Navegación:** enlaces, volver atrás, rutas directas y retorno del login mantienen un flujo coherente.
- **Accesibilidad básica:** se puede completar el flujo con teclado, el foco es visible y razonable, los campos tienen etiquetas y los errores son identificables.
- **Presentación:** probá escritorio y una vista móvil con dimensiones registradas; buscá desbordes, textos cortados, controles superpuestos y acciones difíciles de alcanzar. Aclarar que emular una vista móvil no equivale a probar un dispositivo físico.
- **Coherencia entre roles:** cada actor ve las acciones y estados que corresponden, y los cambios se reflejan al actualizar la información.

Separá incumplimientos verificables de sugerencias de usabilidad. No presentes una preferencia estética como un bug. Si una falla corta el recorrido, registrala y continuá con los casos que puedan probarse de forma independiente.

## 7. Entregar el informe de QA

Guardá el informe en `docs/qa/PR-<numero>.md`, salvo que el usuario indique otro destino. No publiques comentarios, issues ni reviews en servicios externos sin que el usuario lo solicite.

Usá esta estructura:

```markdown
# QA — PR #<numero>: <título>

## Resultado
Estado: APROBADO / CON HALLAZGOS / BLOQUEADO / INCOMPLETO.
Motivo y alcance de lo comprobado.

## Feature y fuentes
- PR, base y SHA revisado.
- Tickets y criterios de aceptación.
- Resumen del comportamiento esperado, dudas y respuestas.

## Entorno
- URL, revisión ejecutada y cómo se verificó.
- Google Chrome: versión, dimensiones, roles y datos de prueba.
- Dependencias relevantes y limitaciones del entorno.

## Casos ejecutados
| Caso | Ticket / criterio o riesgo | Resultado esperado | Resultado observado | Estado | Evidencia |
| --- | --- | --- | --- | --- | --- |
| QA-01 | CA-01 / enlace | ... | ... | PASÓ / FALLÓ / BLOQUEADO / NO EJECUTADO | Captura, log o test |

## Pruebas automatizadas
| Comando o check de CI | Directorio / SHA | Resultado | Evidencia o limitación |
| --- | --- | --- | --- |

## Hallazgos
### QA-BUG-01 — <título> — <severidad>
- Ticket o regresión relacionada:
- Entorno, rol y precondiciones:
- Pasos para reproducir:
- Resultado esperado y observado:
- Impacto:
- Evidencia y archivo/línea cuando se identificó la causa:
- Introducido por la PR / preexistente / origen sin confirmar:

## Usabilidad
Observaciones reproducibles, impacto y mejoras sugeridas.

## Pendientes
Preguntas sin resolver, criterios sin cobertura y pruebas bloqueadas o no ejecutadas.
```

Ordená los hallazgos por impacto: crítico (pérdida de datos, acceso indebido o flujo central inutilizable), alto (criterio o flujo principal roto), medio (camino alternativo afectado con solución temporal) y bajo (problema menor sin impedir completar la tarea).

Usá **APROBADO** solamente cuando los criterios estén claros, se hayan ejecutado los casos requeridos, los checks necesarios y el recorrido en Chrome, y no queden fallas ni bloqueos relevantes. Usá **CON HALLAZGOS** si hay defectos confirmados; **BLOQUEADO** si una dependencia impide concluir la validación; **INCOMPLETO** si queda trabajo requerido sin ejecutar. Si hay hallazgos y bloqueos a la vez, explicitá ambos.

No confundas «no encontré problemas» con «no pude probar». Distinguí siempre lo observado en Chrome, lo probado automáticamente, lo inferido de código y lo pendiente. Si cambia el SHA durante la revisión, identificá qué resultados siguen siendo válidos y repetí las comprobaciones afectadas antes de cerrar el informe.
