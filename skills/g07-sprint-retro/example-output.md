# Ejemplo de output — Sprint Retro (StudyArena)

> Generado con datos ficticios, solo para mostrar el formato esperado.

## 1. Resumen del sprint cerrado

🟡 **Entrega parcial.** `STUDY Sprint 1` cerró con 12 de 21 issues completadas (18 de 34 story points). Un poco más de la mitad del scope planificado se entregó.

## 2. Completado vs. no completado

**Completado (12)**
- `STUDY-9` — Pantalla de login de usuario (Julia)
- `STUDY-11` — Setup Frontend (Marco)
- `STUDY-14` — Pantalla de perfil de usuario (Julia)
- *(+9 más, ver board)*

**No completado — nunca se empezó (5)**
- `STUDY-16` — Pantalla de creación de grupo (sin asignar)
- `STUDY-20` — Endpoint de notificaciones (Denise)
- *(+3 más)*

**No completado — quedó a mitad (4)**
- `STUDY-8` — Setup Backend (Marco)
- `STUDY-10` — Modelo de sesiones de estudio (sin asignar)
- *(+2 más)*

## 3. Señales de qué no salió bien

- `STUDY-8` (Setup Backend) bloquea a `STUDY-10`, `STUDY-16`, `STUDY-17` y `STUDY-26` — ninguna de las cuatro arrancó. Es la dependencia individual con más impacto en lo no completado.
- `STUDY-10` fue arrastrada de `STUDY Sprint 0` a `STUDY Sprint 1` (2 sprints) — sigue sin asignar.
- `STUDY-20` tiene el flag de Impediment activo desde el 3/8, sin comentarios que expliquen el motivo.
- Barrido de comentarios: `STUDY-16` tiene un comentario de Denise ("esperando que Marco termine el setup de backend") que coincide con la dependencia de `STUDY-8` — mismo bloqueo, dos señales distintas.

## 4. Qué salió bien

- `STUDY-9`, `STUDY-11` y `STUDY-14` se completaron sin ninguna señal de bloqueo ni comentario de demora — el flujo de autenticación y setup de frontend salió según lo planificado.

## 5. Agenda de retro / Acciones para el próximo sprint

- Priorizar `STUDY-8` (Setup Backend) al arranque del próximo sprint — bloqueó 4 issues completas este sprint y ninguna pudo arrancar sin eso resuelto.
- Asignar dueño a `STUDY-10` antes del próximo planning — lleva 2 sprints arrastrada sin asignar.
- Pedirle a Denise que actualice `STUDY-20` (Impediment sin comentarios) antes de la reunión de retro, para saber si sigue bloqueada o se puede cerrar el flag.
- Replanificar `STUDY-16`, `STUDY-17`, `STUDY-26` para el próximo sprint solo si `STUDY-8` se resuelve primero — si no, van a volver a quedar sin arrancar.

## 6. Datos no disponibles / limitaciones

- No hay herramienta de changelog conectada: el carry-over se detectó por el campo de sprint actual de cada issue, no por historial completo — si alguna issue salió del sprint por completo en algún momento, no se refleja acá.
- No se pasaron novedades de Discord para este sprint más allá del comentario citado en `STUDY-16`.
- Los story points están completos para todas las issues de este sprint — el total de 34 es confiable.
