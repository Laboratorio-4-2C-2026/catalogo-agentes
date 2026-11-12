# Ejemplo de output — preguntas de la cátedra (Study Arena, cierre del Sprint 3)

Corrida real del 11/11/2026, el día antes de la entrega final (12/11), pensando en el tercer steering.

**Material usado:** consigna del Challenge KPI, propuesta del Escenario 2, consigna del Challenge Sorpresa 2, deck del Steering 2 (15/10), sprint abierto en Jira (28 tickets), 31 PRs de GitHub desde el 15/10 y el código del repo (commit `874dc77`).

**Faltó:** lo que marcó la cátedra en el Steering 2, el deck del Steering 3, el valor ganado del Sprint 3 y la confirmación de que los KPIs llegan a la plataforma.

## Semáforo

1 🟢 · 7 🟡 · 5 🔴

## Las 3 acciones antes de presentar

1. Decidir hoy qué entra de los 5 PRs abiertos (#100 a #105) y dejar escrito lo que se difiere.
2. Calcular el valor ganado del Sprint 3: el Steering 2 cerró con un SPI del sprint de 0,88.
3. Confirmar los datos de la demo (5.000 registros y 500 usuarios realistas) y juntar el reporte del QA rotado.

---

### 1. Mañana es la entrega y tienen 5 tickets en revisión con los PRs abiertos. ¿Qué entra?
- **Por qué la harían:** STUDY-49, 79, 80, 110 y 111 vencen el 12/11, y sus PRs (#100 a #105) están abiertos desde el 6 y 7/11.
- **Evidencia:** Jira del sprint (22 de 28 tickets finalizados) y los PRs abiertos en GitHub.
- **Respuesta sugerida:** "Cerramos 22 de los 28 tickets del sprint. De los 5 en revisión entran X e Y, y diferimos Z porque… Quedó registrado como cambio de alcance."
- **Estado:** 🔴
- **Para mejorarla:** el TL y el PO deciden hoy qué se mergea y lo dejan escrito.

### 2. ¿No habían sacado las tarjetas con IA por el Challenge?
- **Por qué la harían:** el slide "Impacto del Challenge N1" del Steering 2 dice "Tarjetas con IA: reemplazadas por el Challenge", pero STUDY-78 está finalizada y STUDY-79 y 80 están en revisión.
- **Evidencia:** no hay ninguna decisión registrada de volver a incluirlas.
- **Respuesta sugerida:** explicar qué cambió (por ejemplo, que se liberó capacidad) y mostrar dónde quedó registrada la decisión. Si no está registrada, reconocerlo.
- **Estado:** 🔴
- **Para mejorarla:** registrar hoy la decisión en el registro de cambios.

### 3. ¿Cómo cerró el Sprint 3 en valor ganado?
- **Por qué la harían:** en el Steering 2 el sprint cerró con SPI 0,88 ("ritmo menor al planificado") y CPI 1,02.
- **Evidencia:** ninguna para el Sprint 3.
- **Respuesta sugerida:** mostrar PV, EV, AC, SPI y CPI del Sprint 3 y la proyección final. Si el SPI sigue por debajo de 1, reconocerlo y explicar la causa.
- **Estado:** 🔴
- **Para mejorarla:** la PM lo calcula antes del steering.

### 4. ¿Cómo saben que los 10 KPIs llegan todos los días? ¿Cuál es su nota del challenge?
- **Por qué la harían:** la nota del challenge sale de los KPIs válidos recibidos por día.
- **Evidencia:** el backend los manda a las 18:00 y los reenvía a las 20:00 (`MetricsScheduler.java`), pero no hay evidencia de que lleguen.
- **Respuesta sugerida:** "Reportamos 10 KPIs por día de forma automática desde el backend; en el portal se ve que llegaron N de M días."
- **Estado:** 🟡
- **Para mejorarla:** sacar del portal de KPIs el resumen diario del equipo y mostrar los días con 10 KPIs válidos.

### 5. ¿La demo tiene los 5.000 registros y los 500 usuarios realistas que pedía el Challenge Sorpresa 2?
- **Por qué la harían:** es el desafío del TL para el tercer steering.
- **Evidencia:** ninguna.
- **Respuesta sugerida:** mostrar cuántos registros y usuarios hay y cómo se generaron (datos realistas, sin "Usuario_001").
- **Estado:** 🔴
- **Para mejorarla:** el TL lo confirma. Si falta, `g07-seed-mundo-gamificado` lo puede generar.

### 6. La gamificación estaba al 50%. ¿Está completa? ¿Se puede hacer trampa?
- **Por qué la harían:** en el Steering 2 la gamificación estaba al 50% y el hito H4 (quizzes) estaba pendiente.
- **Evidencia:**
  - Los quizzes están terminados (STUDY-87 a 98), así que H4 se cumplió.
  - La simulación de `g07-balance-gamificacion` encontró dos problemas: crear y jugar quizzes propios de 1 pregunta da unos 75 puntos por minuto, contra 1,5 a 1,8 de una sesión; y quedarse solo el 20% de una sesión paga más por minuto que quedarse hasta el final.
- **Respuesta sugerida:** "La gamificación está completa. Simulando las reglas detectamos dos formas de sumar puntos sin estudiar, y proponemos un mínimo de preguntas para que un quiz dé puntos y que el autor no cobre por su propio quiz."
- **Estado:** 🟡 (la falla existe, pero el equipo la detectó y tiene una propuesta)

### 7. ¿Por qué agregaron el plan de estudio una semana antes del cierre?
- **Por qué la harían:** STUDY-110 y 111 se crearon el 05/11, vencen el 12/11 y siguen en revisión.
- **Evidencia:** no tienen épica; STUDY-91 tampoco.
- **Respuesta sugerida:** explicar qué valor aporta y por qué se priorizó. Si no llega, que quede como diferido.
- **Estado:** 🟡
- **Para mejorarla:** asignarles épica y registrar la decisión de alcance.

### 8. ¿Qué encontró el QA rotado? ¿Qué bugs conocidos tienen?
- **Por qué la harían:** la rotación de QA es parte del Challenge Sorpresa 2.
- **Evidencia:** no hay reporte del QA rotado. La documentación generada con `g07-documentar-producto` encontró:
  - editar y cancelar una sesión piden permisos distintos (`SessionService.java`);
  - la UI mezcla "tú" y "vos";
  - el dueño de un grupo no ve el botón para abandonarlo, aunque el backend lo permite.
- **Respuesta sugerida:** mostrar los hallazgos, cuáles se arreglaron y cuáles quedan registrados.
- **Estado:** 🔴
- **Para mejorarla:** juntar el reporte del QA rotado y decidir qué se arregla y qué se reconoce.

### 9. ¿Qué testing tienen?
- **Por qué la harían:** es la pregunta típica para el rol de QA.
- **Evidencia:**
  - El backend tiene 76 archivos de tests de API y el CI corre en cada PR.
  - El frontend no tiene tests: el CI solo corre lint, typecheck y build.
  - 2 de los 25 PRs mergeados desde el 15/10 no tuvieron review.
- **Respuesta sugerida:** mostrar la cobertura del back, reconocer que el front no tiene tests y explicar cómo se compensó (QA manual, agentes de QA).
- **Estado:** 🟡

### 10. Todos los tickets del sprint son de los dos desarrolladores. ¿Qué hicieron los otros cuatro roles?
- **Por qué la harían:** en Jira, los roles de gestión no tienen tickets.
- **Evidencia:** el trabajo de gestión no está en Jira.
- **Respuesta sugerida:** mostrar el trabajo de cada rol fuera de Jira (steering, valor ganado, QA, reviews, el challenge de KPIs y los 40 agentes del catálogo), por rol y sin nombrar personas.
- **Estado:** 🟡

### 11. En el Steering 2 tenían tres riesgos abiertos. ¿Qué pasó?
- **Por qué la harían:** seguían abiertos la falta de experiencia técnica de los devs, la carga académica y el gasto bajo presupuesto.
- **Evidencia:** no hay actualización del registro de riesgos.
- **Respuesta sugerida:** el estado de cada riesgo, qué se hizo y si se cerró.
- **Estado:** 🟡
- **Para mejorarla:** actualizar el registro antes del steering.

### 12. ¿Dónde está todo el proyecto?
- **Por qué la harían:** el Linktree es el desafío de la PM en el Challenge Sorpresa 2.
- **Evidencia:** no sé si está hecho.
- **Respuesta sugerida:** mostrar el Linktree con producto, repos, Jira, steerings, Project Charter y documentación.
- **Estado:** 🟡
- **Para mejorarla:** que la PM lo tenga listo y lo muestre.

### 13. Métricas estaba al 0% en el Steering 2. ¿Lo terminaron?
- **Por qué la harían:** era la épica más atrasada.
- **Evidencia:** STUDY-100, 101, 104, 107 y 108 están finalizados (serie diaria, métricas y metas en el perfil, historial).
- **Respuesta sugerida:** mostrarlo en la demo: es el mejor avance para contar.
- **Estado:** 🟢

---

## Limitaciones

- Faltan las devoluciones de la cátedra del Steering 2: lo que marcaron y no se arregló suele ser la primera pregunta.
- La actividad de GitHub se leyó por la API REST (PRs y reviews); no se revisaron los comentarios de cada review.
- Lo que no tiene evidencia en el material se marcó como tal; no se completó con supuestos.
