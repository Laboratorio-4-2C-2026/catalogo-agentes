---
name: g01-external-api-cache-auditor
description: Audita cómo un backend consume una API externa (caché, reintentos, rate limit, timeouts, mapeo y conteo de llamadas) y propone el patrón proveedor + cliente HTTP + mapper + caché. Usar al integrar o revisar una API de terceros como TMDB, Spotify o una API de clima.
metadata:
  tipo: skill
  area:
  - backend
  fase:
  - revision
  - mantenimiento
  tecnologias:
  - nestjs
  - typescript
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: '01'
  autor:
    nombre: Francisco Zizzi
    github: FranciscoZizzi
  responsables:
  - FranciscoZizzi
  madurez: experimental
  relacionados:
  - g01-review-pr
---
# External API Cache Auditor

Revisás una integración con una API externa y decís qué falta para que sea barata, resistente y fácil de testear. Solo reportás: modificás código únicamente si te lo piden.

## Pasos

1. Encontrá todos los puntos que llaman a la API: grep de la URL base, de `fetch(`, `axios`, `HttpService` y de la variable de entorno con la API key.
2. Revisá cada punto contra esta lista:
   - **Un solo cliente:** las llamadas pasan por un cliente HTTP único, no por `fetch` sueltos en los servicios.
   - **Timeout:** cada request tiene un timeout explícito.
   - **Reintentos:** reintenta solo los 429 y 5xx, con backoff y respetando `Retry-After`. No reintenta los 4xx.
   - **Rate limit:** conoce el límite del proveedor y no lo supera cuando hay varias requests en paralelo (`Promise.all` sobre cientos de IDs).
   - **Caché:** guarda lo que no cambia seguido (en memoria o en la base), con un TTL definido y la fecha de la última actualización. Distingue entre "no existe" y "falló la llamada".
   - **Mapeo:** la respuesta cruda se convierte a un tipo propio en un solo lugar (mapper). El dominio no conoce los nombres de campos del proveedor.
   - **Observabilidad:** cuenta las llamadas por endpoint y por resultado, para saber cuánto se consume.
   - **Secretos:** la API key no se loguea ni llega al cliente.
   - **Tests:** el proveedor se puede reemplazar por un fake (interfaz + token de inyección).
3. Marcá cada ítem como **OK**, **Falta** o **Parcial**, citando `archivo:línea`.
4. Priorizá: primero lo que cuesta plata o rompe en producción (rate limit, falta de caché, key expuesta) y después lo que mejora el diseño.

## Patrón de referencia

```
Servicio de dominio → CatalogProvider (interfaz)
                         └ TmdbCatalogProvider → TmdbHttpClient (timeout, reintentos, stats)
                                               → TmdbResponseMapper (crudo → tipo propio)
                    → CacheService (lee de la base, si no está o venció llama al proveedor)
```

En Cinematch es `catalog/providers/` (`TMDB_PROVIDER`, `TmdbHttpClient`, `TmdbResponseMapper`, `ProviderCallStatsService`) más `catalog/cache/MovieCacheService` y un job de refresco (`catalog/refresh/`).

## Salida

La checklist con su estado, los tres arreglos más urgentes con un fragmento de código cada uno y, si falta la estructura, el esqueleto del patrón adaptado a la API del proyecto.

## Ejemplo de uso

**Pedido:** Auditá cómo el backend consume la API de TMDB.

**Resultado:** Devuelve la checklist (cliente único, timeout, reintentos, rate limit, caché, mapeo, observabilidad, secretos, tests) con OK, Falta o Parcial y su archivo:línea, más los tres arreglos más urgentes con código.
