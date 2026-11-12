# Propuesta del hub de Zervi

Zervi conecta clientes con prestadores de servicios. Prepara un inventario interno y un bloque separado de botones aprobados; por defecto, entrega ambos como borrador en chat.

## Entradas mínimas

Acepta datos pegados, sin conectores obligatorios: audiencia real, recursos con URL exacta segura, fuente y fecha, responsable conocido y aprobación de divulgación. Pide versión o ambiente cuando afecten la interpretación. No reconstruyas URLs desde nombres ni solicites credenciales.

| Fuente suministrada | Uso |
|---|---|
| Charter y cambios aprobados | Línea base de alcance; Jira reciente no la sustituye |
| Steerings y confirmaciones del PM | Decisiones documentadas, roles y corte temporal |
| Drive/documentos/demos | Identidad y contenido de recursos |
| Jira ZRV | Trabajo y evidencia, sin inferir aceptación o despliegue |
| Repositorio/documentación y evidencia de despliegue | Separar implementación de disponibilidad; identificar Dev/Prod |

Los antecedentes del paquete tenían corte 2026-11-06: Linktree informado `https://linktr.ee/zervi_lab4`; Linear no utilizado; video WhatsApp identificado como Demo 1 y ZerviDemo como Demo 2. Son antecedentes, no verificación ni aprobación actual. Solicita al operador URLs y permisos vigentes de demos, Charter, Steerings, Jira, repositorio y documentos necesarios. No incluyas nóminas personales ni inventarios privados por defecto.

## Procedimiento

1. Registra audiencia, corte y fuentes autorizadas. Si discrepan, conserva las versiones y solicita la decisión necesaria; dato faltante o inaccesible no significa recurso ausente.
2. Normaliza y deduplica por recurso/destino. Organiza: producto y demos; proyecto; Steerings; desarrollo y gestión; documentación. Propón consolidación o retiro con fundamento, sin borrar historial.
3. Separa identidad del recurso, URL/destino exacto, respuesta técnica y permiso de audiencia. Un HTTP 200, login o acceso del revisor no prueba acceso del visitante. Una verificación histórica no es actual.
4. Consulta enlaces únicamente con entorno, método, lista finita de URLs y límites de solicitudes/tiempo autorizados. Revisa redirecciones dentro de ese alcance; si destino o parámetros son inciertos, deja pendiente. No rastrees recursivamente ni sondees backend, health o Render.
5. Incluye botones solo con URL completa, parámetros, título y descripción aprobados para la audiencia. Los restringidos intencionales requieren autorización del responsable para divulgar y aviso de restricción; publicar no concede acceso. Si acceso sigue pendiente, dilo solo si esa situación está expresamente autorizada. Los demás quedan internos.

Redacta secretos incluso en el inventario interno; no reproduzcas tokens, URLs firmadas o parámetros sensibles, ni paneles administrativos o endpoints operativos en botones. Solicita un destino estable seguro sin alterarlo por suposición. Publicación, cambios de permisos, documentos y tickets requieren autorización separada; no programes mantenimiento recurrente.

## Salida

1. **Inventario interno:** `sección/recurso | URL segura | fuente/fecha | versión/ambiente | estado y evidencia | responsable | audiencia/acceso | aprobación de publicación`. Divide la tabla si mejora la lectura; omite datos internos si el canal no es apropiado.
2. **Botones aprobados:** título, URL y descripción exactos agrupados por sección; o «Ningún botón aprobado con la evidencia disponible».
3. **Pendientes:** dato/decisión, fuente, responsable conocido y próximo paso propuesto.
4. **Cambios propuestos:** diferencia frente al corte anterior y fundamento, o falta de revisión comparable; límites de verificación.

Antes de entregar, comprueba separación interna/pública, aprobación y audiencia de cada botón, ausencia de secretos y duplicados, distinción Dev/Prod e histórico/actual. Propón revisión tras cambios relevantes o antes de la entrega académica, sin ejecutarla automáticamente.

Procedencia: síntesis de los cuatro documentos históricos del mismo paquete, sin nuevas comprobaciones. Licencia: MIT.
