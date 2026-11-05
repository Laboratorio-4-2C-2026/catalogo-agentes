---
name: g16-eureka-blockers
description: Agente programado (GitHub Actions, lunes a viernes a las 9) que mantiene un único issue con los PRs sin review humana y los tickets sin código o que rebotan de estado. La detección la hace un script determinista y el agente solo ordena lo encontrado y propone quién destraba cada item. Usar para la daily cuando el tablero vive en GitHub Issues.
metadata:
  tipo: agente
  area:
  - gestion
  fase:
  - desarrollo
  - revision
  tecnologias:
  - agnostico
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: "16"
  autor:
    nombre: Esteban Antonijevic
    github: eantonijevic
  colaboradores:
  - nombre: Valentino Gianuzzo
    github: ValentinoGianuzzo
  responsables:
  - eantonijevic
  madurez: usado-en-proyecto
  relacionados:
  - g16-eureka-progreso-semanal
  - g07-pr-jira-sync
  - g15-risk-register-keeper
  - g11-radar-de-sprint
---
# eureka-blockers

Agente del proyecto Eureka (Laboratorio IV, grupo 16). En el repo de Eureka se llama `eureka-blockers`. Los archivos de esta carpeta (`.github/workflows/eureka-blockers.yml`, `.github/scripts/blockers-facts.sh`) están copiados sin cambios y van en las mismas rutas del repo donde se instale.

## Para qué existe

Extraído sin cambios del comentario que abre el workflow:

```text
Agente de propósito específico: detección temprana de blockers.

A diferencia de los dos revisores, este no mira código: mira el estado del
tablero y de la cola de PRs a lo largo del tiempo. Corre por reloj, no por
pull request.

La detección la hace un script determinista y el agente solo tríagea lo que
ese script encontró. Es a propósito: un blocker inventado sería indistinguible
de uno real, y el detector perdería toda su utilidad el primer día.
```

## Cómo corre

- **Se dispara:** por reloj (`0 12 * * 1-5`, UTC); a mano desde Actions.
- **Herramientas del agente:** Read,Write,Grep,Glob,Bash, con un tope de 20 turnos.
- **Necesita:**
  - El secreto `CLAUDE_CODE_OAUTH_TOKEN` en el repo.
  - `.github/scripts/blockers-facts.sh` (incluido): mide PRs y tickets contra los umbrales y escribe `facts.json`.

## Prompt

Extraído sin cambios del paso de `anthropics/claude-code-action` en `.github/workflows/eureka-blockers.yml`.

```text
Sos el detector de blockers de Eureka, un proyecto universitario
donde Laboratorio 4 mantiene la calidad y Laboratorio 2 escribe el
producto.

Leé `facts.json` en la raíz del workspace. Contiene el estado de los
PRs y los tickets abiertos, ya medido contra los umbrales.

**No inventes nada.** Solo podés hablar de items que estén en ese
archivo. Si algo no está ahí, no existe para vos.

Escribí un reporte en `blockers-report.md` con esta forma:

1. Una línea de resumen: cuántos items están frenados y desde
   cuándo el peor.
2. Una sección por cada item marcado, ordenada por cuánto tiempo
   lleva frenado. Para cada uno: el link, una frase de por qué está
   frenado, y **la acción concreta que lo destraba y quién debería
   hacerla** (el autor, el asignado, o quien tenga la review
   pedida). Si no hay a quién señalar, decilo.
3. Si algún item está marcado pero tenés razones para pensar que no
   es un blocker real —un PR abierto a propósito como referencia,
   un ticket que espera algo externo— decilo en vez de tratarlo
   como urgente.

Sé breve: esto lo lee alguien en la daily. Nada de relleno, sin
repetir los números que ya están en la tabla, y en castellano.

No pongas título ni fecha: el reporte se publica dentro de una
sección que ya tiene encabezado, y el pie ya lleva la fecha.
Empezá directo por la línea de resumen.
```

## Ejemplo de uso

**Pedido:** La corrida de las 9:00 de un día hábil, o una manual desde Actions con `horas_sin_review: 24`.

**Resultado:** Actualiza el issue «Blockers detectados» (etiqueta `blockers-report`) con una línea de resumen, una sección por PR o ticket frenado con la acción que lo destraba y quién debería hacerla, y la tabla de números del script. Si no hay nada marcado, no corre el agente y publica «Sin blockers detectados».
