# Ejemplo de output — g07-weekly-process-checklist

Así se ve el documento de Google Drive después de la segunda corrida (ya tiene la sección fija de proceso, más dos entradas semanales). Esto es lo que la skill escribe en el doc y también muestra en el chat antes de subir.

---

# StudyArena — Seguimiento de proceso

## Proceso de seguimiento

Ordenamos el trabajo en sprints semanales sobre un board de Jira (`STUDY`), con un canal de Discord para novedades del día a día. Sabemos que hubo avance real cuando una issue pasa a estado Done con su criterio de aceptación cumplido, no solo por movimiento de tarjetas. Cada semana reportamos de forma fija: qué se hizo desde la clase anterior, qué decisiones se tomaron, y qué riesgos están abiertos. La evidencia mínima en cada reunión es el link al board de Jira más este documento. El formato es siempre el mismo (las cuatro secciones de abajo) para que sea comparable semana a semana. Lo que no puede faltar: al menos una decisión o una nota explícita de que no hubo decisiones, y el estado de los riesgos abiertos de la semana anterior (si se resolvieron o siguen abiertos).

---

## Semana del 04/08

### Organización
Ordenamos el trabajo en sprints semanales sobre el board de Jira (`STUDY`). Objetivo de esta semana: dejar funcionando el flujo de autenticación (STUDY-12 a STUDY-15). Se priorizó STUDY-12 (login) primero porque STUDY-14 (recuperar contraseña) depende de él (issue link "is blocked by"). Asignados: STUDY-12 y STUDY-13 a Franco, STUDY-14 y STUDY-15 a Valentina.

### Avance
Primera entrada del documento — no hay semana anterior con la que comparar, esto es la línea de base. Estado actual del sprint: STUDY-12 en curso, STUDY-13 To Do, STUDY-14 y STUDY-15 To Do (bloqueadas por STUDY-12). Evidencia: board de Jira, sin capturas adicionales esta semana.

### Decisiones
Se decidió usar JWT en vez de sesiones server-side para el login, porque el front va a ser una SPA y simplifica no tener que manejar cookies cross-origin. Participaron Franco y Valentina. Se descartó usar sesiones con Redis por complejidad de infra para el alcance del proyecto. Queda registrado acá y en el README del repo (sección Arquitectura).

### Riesgos y oportunidades
Riesgo más urgente: STUDY-12 sin avance real hace 3 días (sigue "en curso" pero sin commits asociados según lo que reportó el PM) — si no arranca esta semana, bloquea STUDY-14 y STUDY-15. Responsable de seguimiento: Franco. Acción concreta: check-in puntual el miércoles antes de la próxima clase.

---

## Semana del 11/08

### Organización
Mismo proceso. Objetivo de esta semana: cerrar el flujo de autenticación y arrancar el módulo de notificaciones (STUDY-16). Prioridad: terminar STUDY-14 y STUDY-15 antes de arrancar nada nuevo, porque quedaron a mitad la semana pasada.

### Avance
Cambió desde la clase anterior: STUDY-12 y STUDY-13 pasaron a Done. STUDY-14 pasó de To Do a In Progress (ya no está bloqueada). STUDY-15 sigue en To Do. Evidencia: board de Jira + demo del login funcionando (link que pasó el PM: `<link>`).

### Decisiones
No se tomaron decisiones de producto o arquitectura relevantes esta semana — el foco fue terminar lo planificado.

### Riesgos y oportunidades
El riesgo de STUDY-12 de la semana pasada se resolvió (completada el 07/08). Riesgo nuevo, más urgente ahora: STUDY-15 sigue sin arrancar y es la última pieza del flujo de auth — si no arranca esta semana compromete el objetivo. Responsable: Valentina. Acción: reasignar ayuda de otro developer si no arranca antes del jueves.
