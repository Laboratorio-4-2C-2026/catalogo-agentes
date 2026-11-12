---
name: g05-watchparty-release-readiness
description: "Evalúa la preparación para publicar una versión de WatchParty que ya está en staging. Usa resultados de smoke, bloqueos y evidencia de recuperación para emitir una recomendación."
metadata:
  tipo: skill
  area: ["devops","qa","gestion"]
  fase: ["despliegue","revision"]
  tecnologias: ["agnostico"]
  metodologia: [scrum]
  herramientas: [codex]
  requiere: []
  grupo: '05'
  autor:
    nombre: Manuel Salas Seeber
    github: Manuelsalasseeber
  responsables: [Manuelsalasseeber]
  madurez: experimental
  relacionados: ["g10-deployment-handoff","g05-watchparty-release-compatibility","g05-watchparty-acceptance-evidence"]
---

# Decisión de salida a producción

## Procedimiento

1. Identificá la versión candidata, el entorno, la versión que se podría restaurar y los criterios de salida acordados. Verificá que las evidencias de CI y staging correspondan a la candidata.
2. Revisá los resultados de los recorridos críticos que apliquen a la release: iniciar sesión, elegir partido, entrar a sala y observar comentarios o reacciones en dos sesiones. Registrá por criterio evidencia, resultado y bloqueo.
3. Contrastá el orden web/API y el plan de recuperación. Si hay cambios de datos, comprobá que la versión anterior siga siendo utilizable con los cambios ya aplicados o que exista una recuperación ensayada.
4. Entregá una recomendación de publicar, postergar o revertir según el estado de la versión. Incluí los motivos, la evidencia pendiente, la señal observable que dispararía una reversión y quién debe tomar la decisión. La ejecución del despliegue queda a cargo de su responsable.

## Ejemplo de uso

**Pedido:** Evaluá la candidata de reacciones de staging. El smoke pasó, pero todavía no se verificó si la web anterior funciona con la API candidata.

**Resultado:** Entrega una recomendación condicionada por la evidencia de compatibilidad que falta y describe cómo comprobar una eventual recuperación.
