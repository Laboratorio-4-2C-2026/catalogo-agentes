# Ejemplo de output — documentación de producto de Study Arena

Corrida real sobre el repo de Study Arena · commit `874dc77` · 11/11/2026

## Qué se relevó

- **Front (React)**: 11 rutas en `frontend/src/App.tsx` (10 pantallas + 404) y sus textos visibles.
- **Back (Spring Boot)**: 16 controllers, 62 endpoints, entidades y enums de `edu.studyarena.app`.
- **Jira (proyecto `STUDY`, solo lectura)**: 95 issues — 10 épicas y 85 tareas (78 finalizadas, 5 en revisión, 2 sin empezar). No hay estado "In Progress": el intermedio es "En revisión".
- No existía `docs/producto/`: doc nueva.

Archivos generados: `docs/producto/README.md`, `funcionalidades.md`, `flujos.md`, `reglas.md` y `glosario.md`.

## Funcionalidades por estado

| Estado | Cantidad |
|---|---|
| ✅ Disponible | 40 |
| 🟡 Parcial | 1 |
| 🔜 En camino | 2 |
| ⚠️ Inconsistente | 0 |

Ejemplos:

- ✅ **Puntos por sesión y ranking semanal**: pestaña Ranking de `/groups/:groupId` · `GET /api/v1/groups/{groupId}/leaderboard/weekly` · STUDY-56, STUDY-57.
- ✅ **Jugar un cuestionario**: botón "Jugar" · `POST …/quizzes/{quizId}/attempts` y `…/answers` · STUDY-88, STUDY-96.
- ✅ **Presencia en la sesión**: aviso cada 20 s desde `/sessions/:sessionId` · `POST /api/v1/sessions/{sessionId}/presence` · STUDY-46, STUDY-58.
- 🟡 **Generar tarjetas con IA**: `POST …/flashcard-sets/generate` existe (STUDY-78 finalizada), pero ninguna pantalla lo usa; STUDY-79/80 en revisión.
- 🔜 **Invitaciones pendientes del grupo**: STUDY-49 en revisión; el endpoint `GET …/groups/{groupId}/invitations` ya está, falta la pestaña.
- 🔜 **Plan de estudio en sesiones**: STUDY-110/111 en revisión, sin código en este commit.

## Extracto del glosario (⚠️)

| Término (UI) | En el código | En los tickets | Propuesta |
|---|---|---|---|
| Sesión | `Session` (estudio) | "Sesiones de Estudio" (STUDY-1) y "Sesiones de usuario" para el login (STUDY-6) | "sesión" solo para estudio; épica STUDY-6 → "Cuenta y acceso"; "Cerrar sesión" → "Salir de la cuenta" |
| Pomodoro | `lib/pomodoro.ts` (temporizador) y `BLOCK_SECONDS` = 25 min | "timer" | En perfil y metas, "bloques de 25 min" |
| Eliminar sesión | `cancelSession` | "cancelación de sesión" (STUDY-43) | "Cancelar sesión"; el botón para cerrar el diálogo pasa a "Volver" |
| Mazo / "Tarjetas" / "flashcards" | `FlashcardSet` | "mazo de tarjetas" | Pestaña "Mazos"; landing "mazos de tarjetas" |
| Ranking / tabla de posiciones | `WeeklyLeaderboard` y `QuizLeaderboard` | "leaderboard semanal" | "ranking semanal" (grupo) y "tabla de posiciones" (cuestionario) |
| Tablero | `HomePage`, `/home` | "Home" (STUDY-104) | "Tablero" en tickets y docs |

## Limitaciones

- Jira se leyó solo por título, estado, tipo y épica, no por descripción: un ticket finalizado con alcance mayor que su título podría estar más incompleto de lo que se ve.
- El estado sale de leer el código, no de correr la app: no se probó en el navegador ni se corrieron tests.
- Funcionalidades internas sin pantalla (KPIs, STUDY-83/84/85) se marcaron ✅ como "internas", fuera del criterio estricto de front + back.
- Se encontró solo un commit (clon shallow): no se pudo ver historia para distinguir lo recién mergeado.
- Sin capturas: se sugieren las pantallas a capturar en el README.
