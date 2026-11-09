---
name: g02-done-evidence-check
description: Indica qué evidencia externa necesita un ticket de Zest para pasar a done y verifica si ya está, sobre todo en deploy e infraestructura, donde el código mergeado no alcanza. Usar antes de cerrar un ticket; no lo mueve.
metadata:
  tipo: skill
  area:
  - qa
  - devops
  fase:
  - revision
  - despliegue
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - multica
  - github
  grupo: '02'
  autor:
    nombre: Luz Laura
    github: luzlaura
  responsables:
  - luzlaura
  madurez: experimental
  relacionados:
  - g02-ticket-merge-sync
  - g02-multica-guide
---
# Done Evidence Check

En Zest algunos tickets no se pueden validar desde el repo: lo que pasa en Render o Vercel no se ve en el código. Una PR se aprueba por el código, pero el ticket pasa a done con evidencia.

## Pasos

1. Leé el ticket y sus comentarios: `multica issue get ZEST-N` y `multica issue comment list ZEST-N`.
2. Buscá su PR y confirmá que llegó a `dev`. Mergear en otra rama no cuenta.
3. Clasificá el ticket y pedí la evidencia que corresponda:

| Tipo | Evidencia necesaria |
|---|---|
| Código de producto | PR mergeada a `dev` y criterios de aceptación probados |
| Variables de entorno | Captura de la plataforma con los nombres, nunca los valores |
| Servicio desplegado | URL de `/health` respondiendo en prod |
| Deploy automático | Primer deploy automático correcto, con sus logs |
| Migraciones | Logs donde se vea la migración aplicada |
| Demo o ensayo | Registro de la prueba hecha en producción y de sus resultados |

4. Render despliega desde `main`, no desde `dev`: si la evidencia es de prod, confirmá que el cambio llegó a `main`.
5. Si la evidencia es una URL pública, podés comprobarla con `curl`. Solo lectura.

## Resultado

Una tabla con: evidencia necesaria, estado (Está, Falta o No verificable desde acá) y fuente. Después, un veredicto: **Listo para done** o **Falta evidencia**, con el pedido concreto para el responsable.

## Reglas

- No cambies el estado del ticket: eso lo decide una persona.
- Nunca pidas ni copies valores de secretos.
- No publiques comentarios sin OK explícito.

## Ejemplo de uso
**Pedido:** ¿Puedo pasar a done el ticket del deploy del backend?
**Resultado:** Revisa ticket y PR, comprueba `/health` en prod y responde qué evidencia está, cuál falta y a quién pedírsela.
