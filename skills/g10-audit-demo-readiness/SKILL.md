---
name: g10-audit-demo-readiness
description: Comprobar desde la interfaz si una aplicación poblada permite demostrar los escenarios acordados, incluyendo datos y medios. Usar antes de una demo para
  obtener veredicto, evidencia y problemas priorizados.
metadata:
  tipo: skill
  area:
  - qa
  fase:
  - testing
  - revision
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
  - g10-uat-planner
  - g09-preparar-demo-sprint
---

# Comprobar preparación de una demo

Evaluar si la aplicación y sus datos permiten demostrar los escenarios esperados. Ejecutar la auditoría y entregar evidencia; no limitarse a enumerar comprobaciones. Responder en el idioma del usuario.

## Entrada y alcance

Aceptar URL o proyecto local, entorno, escenarios esperados, dispositivo o viewport y cuentas disponibles. Por ejemplo:

```text
$audit-demo-readiness Revisá la app local para presentar una búsqueda, una reserva y el historial; comprobá también las fotos.
```

La skill funciona sin un dataset generado por otra skill. Si existe un guion o informe de generación, aprovecharlo como expectativa, no como prueba de que la carga se realizó o funciona.

Permitir inspección, navegación y preparación de recursos locales aislados. Antes de operaciones que cambien cuentas o datos compartidos, describir el cambio concreto y obtener autorización si no existe ya para esa acción. Un login no autoriza por sí solo a reservar, publicar, borrar o cambiar perfiles. No pedir aprobación otra vez cuando el usuario ya autorizó el recorrido y sus efectos.

No implementar correcciones, regenerar datos, publicar resultados, crear commits ni cambiar configuración para hacer pasar la demo, salvo un pedido adicional. Si un recorrido necesita una modificación no autorizada, verificar lo anterior y dejar pendiente ese paso.

## Preparar escenarios y entorno

Leer las instrucciones del proyecto y descubrir cómo ejecutarlo, sus servicios, autenticación y almacenamiento. Reutilizar servicios existentes cuando sea adecuado; si se requieren servicios propios, registrar procesos, puertos y recursos y no interferir con el entorno del usuario.

Precisar el entorno auditado, la fecha y la versión si está disponible, sin convertir la tarea en una revisión de PR o exigir un ticket. Tomar de las instrucciones del usuario los criterios de éxito. Si no hay escenarios definidos, seleccionar los recorridos centrales visibles del producto y declarar esa selección y las precondiciones.

Localizar navegador o automatización disponibles. Para una app local, levantar primero los servicios necesarios y esperar que estén listos. Si se requiere login manual, preparar previamente la URL y el navegador y pedir solo ese paso; continuar verificaciones independientes mientras tanto. No retener sesiones o tokens en la evidencia.

Preparar una matriz compacta: escenario, datos o identidad necesarios, pasos, resultado esperado y evidencia a obtener. No cambiar los datos solo porque falta un escenario.

## Probar desde la interfaz

Usar el navegador para recorrer el producto con los datos realmente disponibles:

- Acceso y navegación a los escenarios, incluyendo el estado al volver a entrar cuando forme parte del recorrido.
- Listados, búsquedas, filtros y detalles pertinentes; comprobar que la identidad y relaciones mostradas corresponden al recurso seleccionado.
- Operaciones centrales autorizadas, sus resultados visibles y persistencia cuando corresponda.
- Calidad de datos: nombres y contenido plausibles, variedad, fechas vigentes, estados compatibles y relaciones coherentes. Distinguir un resultado vacío válido de la ausencia de datos necesarios para la presentación.
- Medios: carga efectiva de imágenes y reproducción de los videos relevantes. Revisar lo que muestra el navegador; un HTTP 200 o un archivo presente no prueban que el medio sea usable.
- Viewports necesarios para la presentación; incluir móvil y escritorio si no se especifica uno y la app ofrece ambos. No exigir dispositivos físicos que no estén disponibles: declarar el alcance real.

En autenticación, distinguir entrar con una cuenta precargada de probar registro, envío, recepción y confirmación de email. Revisar las restricciones de acceso pertinentes al recorrido; una cuenta marcada como verificada por un administrador no prueba que su titular recibió un mensaje ni su pertenencia institucional. No enviar correos ni crear cuentas externas para comprobarlo sin un pedido que cubra esas acciones.

Revisar estados de carga, errores, confirmaciones y falta de resultados cuando afecten los escenarios. No inventar un error remoto ni provocar efectos compartidos para ampliar la cobertura.

Complementar la interfaz con red, API, logs o consultas de datos cuando ayuden a explicar un fallo o comprobar cantidades. No afirmar el total de la base a partir de una página de resultados. Usar datos controlados o fallos simulados solo como evidencia identificada de ese caso, no como prueba del proveedor o entorno real.

## Evidencia y diagnóstico

Guardar capturas reales del navegador después de la carga, con nombres descriptivos de escenario, estado y viewport. Conservar comandos, pasos, respuesta o error relevante y resultados necesarios para reproducir los problemas. Ocultar datos sensibles antes de capturar y no guardar tokens, contraseñas o perfiles reales completos en los artefactos. Indicar si los datos son de demo, reales o simulados.

Para cada problema, describir esperado, observado, consecuencia para la presentación y evidencia. Priorizar por impacto concreto:

- Bloqueante: impide un escenario requerido o un acceso indispensable.
- Importante: permite continuar pero compromete el recorrido o realismo de forma visible.
- Menor: defecto acotado que no impide demostrar el escenario.

Distinguir fallo observado, riesgo detectado por lectura, simulación y bloqueo del entorno. No atribuir un fallo a la aplicación si solo falló el navegador o un servicio de prueba. Si no hay navegador disponible, completar las verificaciones restantes y dejar explícitamente pendiente la validación visual y funcional; no declarar la demo lista basándose solo en lectura o checks de API.

## Entrega y cierre

Entregar en el chat un informe con enlaces a la evidencia:

1. Veredicto: **lista**, **lista con observaciones** o **no lista** para los escenarios acordados. Si falta una comprobación indispensable, indicar **auditoría inconclusa** y qué falta.
2. Matriz de escenarios con esperado, observado, resultado y evidencia o pendiente. Distinguir aprobado, fallido y no ejecutado.
3. Problemas priorizados con reproducción y consecuencia. Proponer correcciones concretas sin implementarlas.
4. Guion de presentación con los recorridos comprobados, identidades o recursos de demo, precondiciones y advertencias que afecten su ejecución. No recomendar como comprobado un camino no probado.
5. Entorno, fecha, alcance, datos usados, verificaciones ejecutadas y límites. Incluir efectos reales autorizados, recursos retenidos y limpieza.

Un defecto menor no vuelve automáticamente imposible una demo. Una falla en un escenario requerido no se convierte en aprobada por omitirlo del guion. Si el usuario cambia el alcance, conservar claro qué quedó fuera.

Detener solo los procesos creados para la auditoría y eliminar las sesiones y credenciales transitorias propias. Conservar el informe y evidencia útil en la carpeta indicada, o en una carpeta de artefactos elegida para la ejecución, explicando su ubicación. No borrar datos del usuario ni revertir efectos compartidos sin autorización.

## Ejemplo de uso

**Pedido:** Auditá búsqueda, detalle e historial en la aplicación preparada y comprobá que las fotos se vean.

**Resultado:** Matriz ejecutada, veredicto, hallazgos y guion comprobado, con capturas y pasos no ejecutados.
