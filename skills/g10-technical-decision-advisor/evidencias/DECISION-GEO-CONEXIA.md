# Google Maps y Geoapify: decisión de Conexia

Reconstrucción elaborada el 10/11/2026. Decisión histórica relatada por el autor: utilizar Geoapify.

## Necesidad y restricción

Conexia necesitaba resolver direcciones y distancias para sus recorridos. Pedro indicó que se evaluó Google Maps y se eligió Geoapify por su free tier y porque permitía avanzar sin introducir una tarjeta.

| Criterio | Información disponible | Consecuencia en la decisión |
|---|---|---|
| Acceso sin tarjeta | Restricción relatada por el autor | Favoreció Geoapify en aquella evaluación |
| Direcciones y rutas | El adaptador actual implementa geocode y getRouteDistanceKm | La solución cubre el contrato utilizado por el dominio |
| Calidad de ubicaciones | El autor observó coordenadas diferentes para un mismo texto entre ejecuciones | Se aceptó esa limitación relatada; no hay experimento conservado para atribuir su causa |
| Sustitución futura | GeoModule inyecta GeoapifyGeoService como implementación de GeoService | La selección está concentrada en el módulo; hay que implementar y validar el adaptador alternativo |

## Arquitectura comprobada

GeoService define geocode(address) y getRouteDistanceKm(points). GeoModule selecciona GeoapifyGeoService mediante useClass. El adaptador limita la búsqueda a Argentina, pide un resultado y aplica un umbral de confianza antes de aceptar sus coordenadas.

El autor llamó GeoServiceProvider al punto intercambiable; en el checkout inspeccionado la abstracción se llama GeoService. El patrón facilita sustituir el proveedor sin rediseñar los consumidores, pero no demuestra que exista un adaptador Google Maps ni que ambos proveedores respondan igual.

## Tradeoff y revisión

La elección priorizó la restricción operativa del proyecto y aceptó la calidad observada como compromiso. Conviene reconsiderarla si la resolución de ubicaciones afecta recorridos relevantes o cambia la restricción comercial. Antes de sustituir el proveedor se deben comparar solicitudes equivalentes, coordenadas, unidades, errores y valores nulos.

## Fuentes

Relato de Pedro en esta preparación y [extractos del código](FUENTES-CODIGO.md), consultados el 10/11/2026. No se conserva el acta original ni un benchmark comparativo. No se consultaron planes actuales ni se hicieron nuevas llamadas a los proveedores.
