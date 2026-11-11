# KAN-164: de un problema de datos a un ticket verificable

[Ticket original](https://conexia-lab.atlassian.net/browse/KAN-164). Reporter: pedroramirezneira. Creado el 12/10/2026; estado consultado el 10/11/2026: Finalizado. Texto completo y fechas en [TICKETS-CONEXIA.json](TICKETS-CONEXIA.json).

## Problema registrado

Al aceptar un match debía quedar asociada a la participación la información necesaria para recoger y dejar al pasajero. El ticket describe que, en ese momento, la ubicación pertenecía a TravelIntent y no quedaba conservada permanentemente con TripPassenger.

## Criterios que hacen accionable el ticket

1. Conservar origen y destino del pasajero al aceptar el match.
2. Conservar las coordenadas de ambos puntos.
3. Asociar esa información a TripPassenger o una relación equivalente persistente.
4. Devolverla al consultar el viaje.
5. Evitar que cambios posteriores en otras entidades hagan perder la ubicación acordada.
6. Mantener compatibles las participaciones manuales.

El texto original contiene siete viñetas, separando origen y destino. También aclara su exposición en frontend. Esta enumeración resume el alcance sin reemplazar el texto conservado.

## Qué muestra de la skill

El ticket explica el problema y el resultado esperado, conserva compatibilidad y permite verificar la aceptación sin fijar una reescritura completa. KAN-167, incluido como segundo ejemplo, delimita una integración de frontend reutilizando la API existente y preservando un flujo que ya funcionaba.

La evidencia es el ticket real elegido por el autor. Que figure Finalizado no se usa como prueba suficiente del comportamiento end-to-end.
