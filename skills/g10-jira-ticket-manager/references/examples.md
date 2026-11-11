# Ejemplos de propuesta, duplicado y autorización

Ejemplos hipotéticos. Las claves y datos que provea una simulación no son tickets reales ni deben producir enlaces externos.

## Solicitud de propuesta, sin autorización de escritura

**Entrada:** "Prepará un ticket para mostrar intenciones activas en Mis Viajes; la creación y la API de consulta ya existen. No ejecutes cambios". La búsqueda de ejemplo no encuentra solapamientos. El equipo usa prefijos por capa; aún no proporcionó estimaciones, usuarios ni fechas.

**Salida:**

- **Operación / proyecto / tipo:** creación propuesta; proyecto y tipo por confirmar con metadatos.
- **Título:** [FE] Mostrar intenciones activas en Mis Viajes.
- **Descripción:** incorporar la visualización de las intenciones activas del usuario en la pantalla existente, reutilizando la API disponible.
- **Criterios de aceptación:**
  - Solo aparecen intenciones del usuario autenticado.
  - Se muestran únicamente las activas.
  - Se diferencian visualmente de los viajes.
  - Se reutiliza la API existente.
  - No se modifica el flujo de creación de intenciones.
- **Estimación:** por estimar con el equipo.
- **Asignado:** por confirmar.
- **Prioridad:** por confirmar según los valores y objetivos del proyecto.
- **Start date:** sin definir; verificar disponibilidad del campo.
- **Due date:** sin definir.

"Propuesta preparada; Jira no fue modificado. Para registrar este borrador se necesita resolver los campos obligatorios y aprobar la propuesta concreta". No solicitar autorización para un payload que todavía contiene campos obligatorios desconocidos; mostrar primero todo lo que ya sea revisable.

## Ticket existente

**Entrada:** misma necesidad. Un export de simulación aporta DEMO-17, "Listar intenciones activas del usuario", En progreso, con los mismos criterios y trabajo ya asignado.

**Salida:** "DEMO-17 cubre el alcance solicitado según el export aportado. Recomiendo reutilizarlo; no propongo crear un duplicado ni modificarlo sin necesidad. No se modificó Jira". Señalar la antigüedad del export si se conoce y que no es una consulta en vivo. No inventar su URL.

Si DEMO-17 estuviera Done, comprobar si la entrega funciona; no suponer que un fallo exige un duplicado ni reabrirlo sin autorización. Puede justificarse un bug separado según evidencia y convenciones.

## Autorización limitada

**Entrada:** tras mostrar dos borradores completos, el usuario dice "Aprobado solo el primero, sin fechas ni cambio de responsable".

**Salida esperada:** ejecutar únicamente el primer borrador si el payload sin fechas/asignación es válido y coincide con lo aprobado. No ejecutar el segundo ni agregar asignaciones, fechas, vínculos, comentarios o transiciones. Releer y reportar los valores guardados con clave y URL devueltas por Jira.

Si una creación da timeout, buscar si fue aplicada. Si sigue siendo incierto, detenerse e informar; no repetirla. Si el primer ticket se confirmó pero falla una relación posterior, informar el ticket creado y la relación pendiente, sin volver a crear el ticket ni borrar lo exitoso.
