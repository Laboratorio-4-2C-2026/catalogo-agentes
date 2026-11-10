---
name: g04-reorganizar-cronograma
description: Propone cómo reorganizar el cronograma de PitStop ante atrasos, bajas o cambios de alcance, sin superar la capacidad y conservando la fecha de entrega y el orden de prioridad. Usar cuando algo se atrasó, cambió el alcance o hay que replanificar las semanas que quedan.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  - mantenimiento
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: "04"
  autor:
    nombre: Tomás Serra
    github: TomasSerra
  responsables:
  - TomasSerra
  madurez: experimental
  relacionados: []
---

# Reorganizar cronograma

Replanifica lo que falta sin tocar lo ya cerrado. Fuentes en `pitstop-management/project-plan/`.

## Flujo

1. **Entender el cambio:** qué se atrasó, qué entró o salió, y qué fechas son fijas (entregas y finales). Si no está claro, preguntar.
2. **Ver el estado real:** `features.yaml`, `team.yaml` y Linear para confirmar qué está terminado. Usar `g04-cronograma` como punto de partida.
3. **Medir el hueco:** SP pendientes contra la capacidad de las semanas que quedan, reservas incluidas.
4. **Armar opciones, en este orden de preferencia:**
   1. Usar reservas, reemplazándolas por el trabajo concreto sin duplicar puntos.
   2. Mover trabajo a semanas con capacidad libre, respetando `depends_on`.
   3. Recortar primero lo `could`, después lo `should`. Nunca un `must` sin que lo decida el PM.
5. **Mostrar** dos opciones como máximo: qué se mueve, carga semanal resultante, qué se recorta y el riesgo que queda. Recomendar una y esperar la decisión.
6. **Aplicar** la opción elegida en `features.yaml` y `team.yaml`: fechas, notas del sprint y motivo.
7. **Avisar** qué tickets de Linear quedan desalineados (`g04-sync-linear`) y si hace falta rebaseline en `g04-earned-value-presentacion`.

## Reglas

- No cambiar semanas cerradas.
- No superar la capacidad para que el plan cierre en el papel.
- No cambiar el orden de prioridad del PM sin decirlo.
- No modificar Linear salvo pedido explícito.

## Ejemplo de uso
**Pedido:** Se atrasaron dos tickets de Perfil, reorganizá lo que queda del sprint.

**Resultado:** Dos opciones con sus movimientos y efectos en carga por semana y alcance, una recomendación y, una vez elegida, features.yaml actualizado con las fechas nuevas.
