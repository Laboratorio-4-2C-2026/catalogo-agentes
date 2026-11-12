---
name: g05-watchparty-ci-flaky-tests
description: "Busca pruebas intermitentes de WatchParty en el historial de CI. Usa resultados comparables por prueba para distinguir alternancia real de cambios de código o entorno."
metadata:
  tipo: agente
  area: ["qa","devops"]
  fase: ["mantenimiento","revision"]
  tecnologias: ["github-actions"]
  metodologia: [scrum]
  herramientas: [codex]
  requiere: []
  grupo: '05'
  autor:
    nombre: Manuel Salas Seeber
    github: Manuelsalasseeber
  responsables: [Manuelsalasseeber]
  madurez: experimental
  relacionados: ["g05-watchparty-ci-diagnosis","g05-watchparty-regression-selection"]
---

# Seguimiento de tests intermitentes

## Procedimiento

1. Fijá ventana y suite. Reuní resultados por prueba, commit, job, runner o matriz e intento. Conservá los reintentos como evidencia y distinguí corridas omitidas, canceladas o bloqueadas antes de la suite.
2. Agrupá por identificador estable y configuración comparable. Señalá una intermitencia observada cuando haya éxito y fallo para la misma prueba en el mismo commit bajo condiciones comparables. Si cambiaron los insumos o faltan datos, tratala como candidata.
3. Registrá fallos sobre intentos observados, primera y última aparición, enlaces y firma del error. Si varias pruebas fallan en el mismo paso de preparación, tratá el fallo común como hipótesis y vinculá la ejecución al diagnóstico de CI.
4. Entregá una tabla priorizada por impacto y recurrencia. Para cada caso, proponé la evidencia adicional que permitiría confirmar la causa. Conservá el estado actual de la suite y sus checks.

## Ejemplo de uso

**Pedido:** Revisá si la prueba de reacciones que pasó en el reintento aparece como intermitente en las últimas corridas.

**Resultado:** Entrega los intentos comparables, su frecuencia observada y los enlaces que sostienen la clasificación.
