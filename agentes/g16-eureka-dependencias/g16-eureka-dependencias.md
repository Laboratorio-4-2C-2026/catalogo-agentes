---
name: g16-eureka-dependencias
description: 'Agente programado (GitHub Actions, los lunes) que toma lo que encuentra un script determinista con npm audit y prioriza qué vulnerabilidades de las dependencias importan para Eureka: si el paquete llega a producción, si el código usa la parte vulnerable y si el arreglo es un cambio mayor. Mantiene un único issue vivo.'
metadata:
  tipo: agente
  area:
  - seguridad
  - devops
  fase:
  - mantenimiento
  tecnologias:
  - nodejs
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: "16"
  autor:
    nombre: Valentino Gianuzzo
    github: ValentinoGianuzzo
  responsables:
  - ValentinoGianuzzo
  madurez: experimental
  relacionados:
  - g16-eureka-blockers
  - g13-vigia-de-dependencias
  - g11-plan-actualizacion
  - g04-dependency-version-control
---
# eureka-dependencias

Agente del proyecto Eureka (Laboratorio IV, grupo 16). En el repo de Eureka se llama `eureka-dependencias`. Los archivos de esta carpeta (`.github/workflows/eureka-dependencias.yml`, `.github/scripts/dependencias-facts.sh`) están copiados sin cambios y van en las mismas rutas del repo donde se instale.

**Estado:** ya está en `master` de Eureka, pero todavía no llegó el primer lunes desde que se mergeó, así que no corrió en el proyecto.

## Para qué existe

Extraído sin cambios del comentario que abre el workflow:

```text
Agente de propósito específico: las dependencias con vulnerabilidades
conocidas.

Eureka depende de librerías que manejan claves, firmas y pagos (Openfort,
viem, tweetnacl, @noble/post-quantum, MercadoPago) y de OpenZeppelin en los
contratos. Ningún revisor las mira: los agentes de PR leen el diff, y una
vulnerabilidad nueva aparece en una librería que nadie tocó.

`npm audit` solo tira una lista, y casi siempre larga. Lo que hace falta es
saber cuáles importan para Eureka: si el paquete llega a producción, si el
código usa la parte vulnerable, si el arreglo es un cambio mayor. Eso es lo
que hace el agente.

Como Blockers, la detección es de un script determinista y el agente solo
prioriza lo que el script encontró. Mantiene un único issue vivo (etiqueta
`dependencias`): lo abre o actualiza cuando hay algo y lo cierra cuando una
corrida sale limpia.
```

## Cómo corre

- **Se dispara:** por reloj (`0 12 * * 1`, UTC, los lunes); a mano desde Actions.
- **Herramientas del agente:** Read,Write,Glob,Grep, con un tope de 40 turnos.
- **Necesita:**
  - El secreto `CLAUDE_CODE_OAUTH_TOKEN` en el repo.
  - `.github/scripts/dependencias-facts.sh` (incluido): corre la auditoría y junta los hechos en archivos JSON para el agente.

## Prompt

Extraído sin cambios del paso de `anthropics/claude-code-action` en `.github/workflows/eureka-dependencias.yml`.

```text
Sos el revisor de dependencias de Eureka.

Leé `facts.json` en la raíz del workspace: las vulnerabilidades que
encontró `npm audit` (con `en_produccion` para saber si el paquete
llega a la app desplegada) y los avisos de GitHub para las versiones
de OpenZeppelin de los contratos. Para el contexto del producto,
`.github/copilot-instructions.md`.

**No inventes nada.** Solo podés hablar de vulnerabilidades que estén
en `facts.json`. No agregues CVEs, versiones ni arreglos que no
aparezcan ahí.

Para cada una, buscá en el código (`app/`, `lib/`, `visual_pages/`,
`contracts/src/`) si Eureka importa el paquete afectado y si usa la
parte vulnerable que describe el aviso. Si llega por otra
dependencia (`llega_por`), decí por cuál.

Escribí `dependencias-report.md` con esta forma:

1. Una línea de resumen: cuántas hay que atender ya y cuántas pueden
   esperar.
2. **Atender ya**: las críticas o altas que llegan a producción o a
   los contratos y cuyo código vulnerable Eureka usa. Para cada una:
   el paquete, qué permite el ataque en términos de Eureka (con el
   archivo donde se usa), el arreglo (versión, y si es un cambio
   mayor que puede romper algo) y quién lo hace (el TL).
3. **Pueden esperar**: el resto, una línea cada una con el motivo
   (solo desarrollo, Eureka no usa esa parte, severidad baja).
4. Si no podés saber si Eureka usa la parte vulnerable, ponela en
   "Atender ya" y decí que es una sospecha.

Si la lista es larga, investigá primero las críticas y altas que
llegan a producción. Las que llegan por la misma dependencia
directa se arreglan juntas: agrupalas bajo esa dependencia en vez
de listarlas una por una.

En castellano, breve. Sin título ni fecha: el issue ya los tiene.
```

## Ejemplo de uso

**Pedido:** Un lunes, `npm audit` reporta 14 vulnerabilidades, una de ellas alta en una librería de firmas que usa el backend.

**Resultado:** Abre o actualiza el issue con la etiqueta `dependencias`: una línea de resumen, «Atender ya» con las que llegan a producción y por qué, «Pueden esperar» con el motivo de cada una, y las que no puede saber si Eureka usa. Si una corrida sale limpia, cierra el issue.
