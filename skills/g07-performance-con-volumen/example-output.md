# Ejemplo de output — performance con volumen sobre Study Arena

Corrida real del 11/11/2026, hecha con Cursor siguiendo esta skill.

- **Commit:** `874dc77` (`main`).
- **Máquina:** Apple M1 Max, 10 cores, 64 GB.
- **Entorno:** stack aislado con `docker compose -p studyarena-perf`. La plataforma de KPIs y Gemini quedaron desactivados; Azure Storage tuvo que ir con un valor de prueba local porque vacío no arranca.
- **Volumen:** 1.000, después 10.000 y después 100.000 sesiones, con unos 2.000 usuarios en 20 grupos. Un grupo "caliente" concentra cerca del 40% de las sesiones.

## p95 (ms) por volumen

| Endpoint | 1k | 10k | 100k | Crecimiento | Bytes @100k |
|---|---:|---:|---:|---|---:|
| Ranking semanal **caliente** (puntos ya calculados) | 26 | 30 | 136 | 🟢 sublineal | 8 KB |
| Ranking semanal **frío** (primer GET de la semana, puntos pendientes) | 258–410 | 2.900–3.600 | **222.000** (≈3,7 min) | 🔴 lineal → superlineal | — |
| `GET /sessions/me` | 169 | 707 | **7.582** | 🟠 lineal | **25,6 MB** |
| `GET /sessions/me?status=FINISHED` | 82 | 568 | 5.022 | 🟠 lineal | 14,5 MB |
| `GET /sessions/me?groupId=<grupo caliente>` | 84 | 655 | 5.779 | 🟠 lineal | 22,0 MB |
| `GET /sessions/me?status=ACTIVE` | 12 | 48 | 254 | 🟡 sublineal | 454 KB |
| `GET /sessions/{id}` | 10 | 7 | 6 | 🟢 constante | 457 B |
| `GET /users/me/metrics` (historial) | 9 | 9 | 25 | 🟢 constante | 3 KB |
| `GET /users/me` | 29 | 42 | 198 | 🟡 sublineal | 164 B |

Con un umbral de 300 ms de p95 a 10.000 sesiones, se pasan el **listado de sesiones** (todas sus variantes, salvo `ACTIVE`) y el **ranking frío**.

## Queries por request

| Endpoint | 1k | 10k |
|---|---:|---:|
| Ranking caliente | 4 | 4 |
| `sessions/me` | 557 | **4.758** |
| `sessions/me?status=FINISHED` | 347 | 3.447 |
| `sessions/me?groupId=…` | 483 | 4.084 |
| `sessions/me?status=ACTIVE` | 15 | 67 |
| Detalle, métricas y perfil | 5–6 | 5–6 |

## Causas

- **Listado de sesiones (🟠):** `findVisibleForUser` trae **todas** las sesiones del usuario y después las filtra por estado y las ordena en Java. Por cada sesión, `SessionQueryService.toView` hace otra consulta de participantes (`findAllActiveBySession`): un **N+1**. Además no pagina, así que el JSON crece con el volumen (25,6 MB a 100k).
- **Ranking frío (🔴):** antes de armar el ranking, `PointsService.awardPendingSessionPoints` recorre las sesiones terminadas del grupo e inserta una fila de puntos por participación, cada una en su propia transacción (`REQUIRES_NEW`). Todo eso pasa dentro del GET, y lo paga el primero que abre el ranking en la semana. Con los puntos ya calculados, el mismo ranking tarda entre 30 y 136 ms.
- **Historial (🟢):** agrega por día en SQL y aguanta. `/users/me` crece un poco porque también dispara el cálculo pendiente de puntos de cada grupo activo.

## Arreglos propuestos (no se tocó el repo)

1. **Paginación** (`Slice`/`Pageable`) en `GET /sessions/me`, con `ORDER BY starts_at` y el filtro por estado en SQL.
2. **Una sola consulta de participantes** para toda la página (`WHERE session_id IN (...)`) o una proyección, en lugar de una por sesión.
3. **Puntos fuera del GET:** calcularlos en un job o en lote al terminar la sesión, no al abrir el ranking. Agregar los índices `(group_id, planned_ends_at)` y `(group_id, earned_at)` para el `NOT EXISTS`.
4. Si la UI no necesita el total, evitar el `COUNT(*)` de `Page`.

## Limitaciones

- Una sola máquina, sin concurrencia.
- El 40% de las sesiones concentrado en un grupo es un caso extremo a propósito; un grupo real acumula muchas menos sesiones por semana, así que la espera real del ranking frío es menor que la de esta corrida, pero crece de la misma forma.
- El log de Postgres estuvo apagado durante las corridas de latencia.
