---
name: g04-cronograma
description: 'Arma o actualiza el cronograma de PitStop a partir de features.yaml y team.yaml: semanas de jueves a jueves, carga en SP contra la capacidad y dependencias. Usar cuando se pide el cronograma del proyecto, ver qué toca cada semana o detectar semanas sobrecargadas.'
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
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

# Cronograma

Muestra qué se hace cada semana y si entra en la capacidad real. Fuentes en `pitstop-management/project-plan/`.

## Flujo

1. Leer `team.yaml` (sprints, inicio de semana, capacidad, reservas) y `features.yaml` (épicas, `starts`, `ends`, `estimate`, `depends_on`, `status`).
2. Agrupar por semana según `starts`. El `ends` es el jueves de cierre de esa semana.
3. Calcular por semana: SP planificados, capacidad y diferencia. Las reservas cuentan como carga, pero se muestran aparte porque no son trabajo consumido.
4. Controlar:
   - Semanas por encima de la capacidad, o con capacidad libre.
   - Una funcionalidad que empieza antes de que termine aquello de lo que depende.
   - Funcionalidades sin fecha, o con fecha fuera de su sprint.
   - Trabajo atrasado: `starts` ya pasó y sigue en `todo` o `backlog`.
5. Mostrar el cronograma por sprint y semana, con los problemas al final.

## Reglas

- PV y capacidad no son lo mismo: una semana con menos carga es válida si el plan lo dice.
- Solo lectura. Para mover fechas usar `g04-reorganizar-cronograma`.
- `features.yaml` se reescribe entero desde la app: no agregar comentarios.

## Ejemplo de uso
**Pedido:** ¿Cómo queda el cronograma hasta el cierre del Sprint 3?

**Resultado:** Una tabla por semana con funcionalidades, SP planificados contra los 18 disponibles y dependencias, más las semanas sobrecargadas o vacías y las funcionalidades sin fecha.
