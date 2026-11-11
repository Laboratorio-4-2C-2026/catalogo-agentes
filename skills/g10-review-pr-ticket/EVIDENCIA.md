# Caso de uso — PR94 / KAN-197 de Conexia

La revisión del 9/11/2026 contrastó la implementación de notificaciones con el ticket, ejecutó comprobaciones locales y probó la integración con backend y FCM reales.

**Resultado:** aprobar con observaciones no bloqueantes. El informe entrega matriz del ticket, validaciones y una mejora de recuperación del registro del token.

- [Informe conservado de la revisión](evidencias/PR94-KAN197-REVISION.txt).
- [Listado de notificaciones probado](evidencias/01-listado-notificaciones.jpg).
- [Recepción de un aviso enviado mediante FCM](evidencias/02-recepcion-fcm.jpg).

Las capturas son originales de las pruebas en navegador. El listado usa datos de prueba locales; el segundo caso usa envío real de FCM. El informe distingue esa integración de los fallos inducidos y contratos controlados. La captura aislada del fallo de token se retiró de la selección; su hallazgo sigue explicado en el informe. No se volvió a ejecutar la PR para esta entrega.
