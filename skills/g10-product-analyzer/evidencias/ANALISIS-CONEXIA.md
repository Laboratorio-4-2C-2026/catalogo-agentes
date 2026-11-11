# Conexia: intenciones y datos de participación

Análisis elaborado el 10/11/2026. Objetivo: determinar qué conviene conservar al completar la información de viajes, sin volver a implementar capacidades existentes.

## Recorrido comprobado por lectura

| Necesidad | Evidencia real | Conclusión |
|---|---|---|
| Crear una intención | El cliente createTravelIntent llama POST /travel-intents; el controller usa FirebaseAuthGuard y el servicio persiste la intención | Hay implementación de creación; no corresponde proponer otro endpoint de creación |
| Ver intenciones propias activas | Trips llama getMyTravelIntents en Próximos viajes, filtra ACTIVE y renderiza TravelIntentCard | El gap descrito históricamente en KAN-167 ya está cubierto en el código inspeccionado |
| Conservar dónde recoger y dejar al pasajero | TripPassenger tiene campos pickup/dropoff y la aceptación copia dirección/coordenadas desde TravelIntent | La persistencia pedida en KAN-164 ya tiene implementación; no recomendar rehacer el modelo |
| Mostrar esas ubicaciones | El detalle de viaje construye el texto de recogida/bajada a partir de esos campos | Hay consumidor de UI; la lectura no certifica el despliegue remoto |

## Valor del análisis

La recomendación es conservar la creación y consulta existentes, la copia de ubicaciones en la participación y los componentes actuales. Ante un reporte de ausencia en producción, comprobar primero versión desplegada, respuesta de API y datos de la cuenta antes de abrir otro desarrollo de backend.

La comprobación funcional siguiente sería crear una intención propia, verla entre las activas y aceptar una coincidencia autorizada para verificar sus ubicaciones en el viaje. Ese recorrido no se ejecutó en esta inspección. No se asignan fechas, esfuerzo ni tickets nuevos.

## Fuentes

[Snapshot de KAN-164, KAN-167 y KAN-154](TICKETS-REFERENCIA.json), consultado por MCP el 10/11/2026. [Extractos del checkout](FUENTES-CODIGO.md). El estado Finalizado de los tickets es un dato del tracker; la conclusión sobre implementación se sustenta además en el código.
