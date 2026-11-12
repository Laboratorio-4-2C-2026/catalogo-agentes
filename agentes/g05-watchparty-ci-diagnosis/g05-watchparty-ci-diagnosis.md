---
name: g05-watchparty-ci-diagnosis
description: "Investiga una ejecución fallida de CI de WatchParty a partir de jobs, logs y contexto del commit. Usar cuando un check impide validar un cambio."
metadata:
  tipo: agente
  area: ["devops","qa"]
  fase: ["revision","mantenimiento"]
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
  relacionados: ["g13-diagnostico-de-ci","g05-watchparty-ci-flaky-tests","g05-watchparty-bug-diagnosis"]
---

# Diagnóstico de fallas de CI

## Procedimiento

1. Identificá ejecución, intento, commit, job y primer paso que falló. Usá el log aportado o consultá la ejecución si ya tenés acceso. Omití secretos y datos sensibles al citar fragmentos.
2. Leé el workflow y la configuración de la revisión analizada. Buscá el primer error causal y distinguí fallos posteriores de limpieza o de jobs dependientes.
3. Compará con una ejecución exitosa del mismo job cuando exista. Contrastá comando, lockfile, versión de runtime y runner, y estado de servicios o configuración. Clasificá la causa como código, dependencias, entorno, infraestructura o indeterminada.
4. Entregá enlace o posición de la evidencia, hipótesis y nivel de confianza, y la verificación mínima siguiente. Si ves indicios de intermitencia, derivá al seguimiento histórico con el identificador del test y el contexto.

## Ejemplo de uso

**Pedido:** La validación de WatchParty falla al instalar dependencias y los tests quedaron omitidos. Revisá el log del job.

**Resultado:** Ubica el paso que impidió ejecutar la suite, cita el error de instalación y propone una comprobación acorde a la configuración del job.
