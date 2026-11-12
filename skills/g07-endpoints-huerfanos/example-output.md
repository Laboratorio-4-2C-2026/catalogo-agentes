# Ejemplo de output — endpoints huérfanos en Study Arena

Corrida real del 11/11/2026 sobre `main` (commit `874dc77`), con `--base-front /api` porque `VITE_API_URL` termina en `/api` y el front llama a `/v1/...`.

```
$ python3 -I scan_endpoints.py --back backend/src/main/java --front frontend/src --base-front /api
Endpoints backend: 62 · usados por el front: 48 · usados de forma indirecta: 10 · sin uso: 4
Llamadas frontend: 48 · sin endpoint: 0
```

## Resumen

- **62 endpoints** en 16 controllers: 48 se llaman directamente desde el front, 10 de forma indirecta y 4 no los usa el front.
- **48 llamadas** del front: **ninguna rota**. Todas apuntan a un endpoint que existe.
- **Ningún endpoint muerto.**

## 🐛 Llamadas rotas

Ninguna.

## Endpoints sin uso en el front

| Método y ruta | Fuente | Clasificación | Ticket / evidencia | Acción |
|---|---|---|---|---|
| `POST /api/v1/groups/{groupId}/flashcard-sets/generate` | `FlashcardSetController.java:59` | 🔌 Pendiente de integrar | STUDY-78 finalizada; el front llega con STUDY-79/80 (PRs #101 y #102 abiertos, agregan `aiGenerationService.ts`). | Nada: se usa al mergear esos PRs. |
| `GET /api/v1/health` | `HealthController.java:14` | 🧪 De soporte | No lo llama el front; sirve para chequear desde afuera que el backend responde (monitoreo, pings de latencia). | Documentarlo. |
| `POST /api/v1/internal/metrics/snapshots` | `MetricsController.java:41` | 🧪 De soporte | Disparo manual del job de KPIs, protegido con un header secreto (`requireJobSecret`). | Documentarlo en la guía de operación. |
| `POST /api/v1/internal/metrics/reports` | `MetricsController.java:50` | 🧪 De soporte | Reenvío manual del reporte de KPIs, con el mismo secreto. | Documentarlo en la guía de operación. |

## Usados de forma indirecta (verificados a mano)

El front pasa la ruta como parámetro o la guarda en una constante: `fetchMaterialList('/v1/materials', …)`, `report('/v1/metrics/landing-views')`, `const ENDPOINT = '/v1/users/me/study-goals'`.

| Método y ruta | Dónde se usa | Resultado |
|---|---|---|
| `GET /api/v1/materials`, `/files`, `/flashcard-sets`, `/quizzes` | `materialService.ts`, `quizService.ts` (helper `fetchMaterialList`) | ✅ Usados |
| `POST /api/v1/metrics/landing-views`, `/invited-registrations` | `metricsService.ts` (función `report`) | ✅ Usados |
| `GET` y `PUT /api/v1/users/me/study-goals` | `studyGoalsService.ts` (constante `ENDPOINT`) | ✅ Usados |
| `GET /api/v1/groups/{groupId}/quizzes/{quizId}` | `quizPlayService.ts` (helper `quizPath`) | ✅ Usado |
| `GET /api/v1/groups/{groupId}/invitations` | Solo coincide con el texto del `POST` de invitaciones | 🔌 **Pendiente de integrar**: el `GET` llega con STUDY-49 (PR #105 abierto). |

## Ajustes al script que salieron de esta corrida

La primera pasada daba 62 endpoints sin uso y solo 4 llamadas detectadas, porque el front de Study Arena:
1. usa tipos genéricos anidados (`apiClient.post<ApiEnvelope<{ id: string }>>(…)`), que la expresión regular no reconocía;
2. arma rutas con helpers (`quizPath(...)`) y constantes;
3. pasa rutas como parámetro a wrappers (`fetchMaterialList`, `report`).

Se corrigió el script para los tres casos y se agregó la categoría "usados de forma indirecta" para lo que no se puede atribuir a un método con certeza.

## Limitaciones

- El método de los endpoints "indirectos" se confirmó a mano.
- No se levantó el stack: no se confirmó con `curl` que las rutas respondan.
