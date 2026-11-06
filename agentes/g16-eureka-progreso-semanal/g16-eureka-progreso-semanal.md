---
name: g16-eureka-progreso-semanal
description: 'Agente programado (GitHub Actions, los viernes) que abre un issue por semana con el reporte de progreso para la cátedra a partir de un JSON que arma un script: PRs, issues, commits, arrastre y hallazgos de los agentes de review. El agente solo narra y no consulta nada por su cuenta, para que una semana floja no se pueda inflar. Usar cuando el reporte semanal sale de GitHub.'
metadata:
  tipo: agente
  area:
  - gestion
  - documentacion
  fase:
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
  responsables:
  - eantonijevic
  madurez: usado-en-proyecto
  relacionados:
  - g11-weekly-status
  - g15-weekly-status-report
  - g08-progress-summarizer
  - g16-eureka-blockers
---
# eureka-progreso

Agente del proyecto Eureka (Laboratorio IV, grupo 16). En el repo de Eureka se llama `eureka-progreso`. Los archivos de esta carpeta (`.github/workflows/eureka-progreso.yml`, `.github/scripts/progreso-facts.sh`) están copiados sin cambios y van en las mismas rutas del repo donde se instale.

## Para qué existe

Extraído sin cambios del comentario que abre el workflow:

```text
Agente de propósito específico: el reporte semanal de progreso para la cátedra.

Corre por reloj, como el detector de blockers, y comparte su principio: la
evidencia la junta un script determinista y el agente solo la narra. Un agente
que pueda consultar la API por su cuenta también puede completar los huecos de una
semana floja, y este reporte se entrega.

A diferencia de blockers, que mantiene un único issue vivo, este abre uno nuevo
por semana: el valor del reporte está en la serie, no en la última foto.
```

## Cómo corre

- **Se dispara:** por reloj (`0 12 * * 5`, UTC); a mano desde Actions.
- **Herramientas del agente:** Read,Write,Grep,Glob,Bash, con un tope de 20 turnos.
- **Necesita:**
  - El secreto `CLAUDE_CODE_OAUTH_TOKEN` en el repo.
  - `.github/scripts/progreso-facts.sh` (incluido): junta la evidencia de la ventana en `progreso.json`. Cuenta los hallazgos por el prefijo `[Crítico]`/`[Alto]`/`[Medio]`/`[Bajo]` que usan los revisores g16.

## Prompt

Extraído sin cambios del paso de `anthropics/claude-code-action` en `.github/workflows/eureka-progreso.yml`.

```text
Sos el documentador de progreso de Eureka, un proyecto universitario
donde Laboratorio 4 mantiene la calidad y Laboratorio 2 escribe el
producto. Escribís el reporte semanal que lee la cátedra.

Leé `progreso.json` en la raíz del workspace. Tiene todo lo que pasó
en la ventana: PRs mergeados y abiertos, issues, commits, lo que
quedó de arrastre y los hallazgos que dejaron nuestros agentes de
review.

**No inventes nada.** Solo podés hablar de lo que está en ese
archivo. No infieras qué se estuvo trabajando a partir de los
títulos, no supongas por qué algo quedó abierto, y no rellenes una
semana floja: si se hizo poco, el reporte dice que se hizo poco. La
cátedra compara estos reportes entre semanas, así que uno inflado
hace más daño que uno pobre.

Escribí el reporte en `progreso-report.md` con estas secciones:

## Resumen
Dos o tres frases: qué avanzó esta semana y en qué estado quedó el
proyecto. Sin repetir los números de la tabla.

## Qué se completó
Los PRs mergeados y los issues cerrados, **en lenguaje de negocio**:
qué capacidad quedó disponible, no qué archivos se tocaron. Agrupá
por tema si hay más de tres. Linkeá cada uno.

## Qué quedó en curso
PRs abiertos e issues nuevos que siguen sin cerrar. Si algo del
arrastre lleva mucho tiempo abierto, marcalo — es la señal de que
el trabajo se acumula en vez de cerrarse.

## Calidad
Qué encontraron los agentes de review esta semana, por severidad.
Si hubo hallazgos críticos o altos, decí en qué PRs. Si el conteo es
cero, decilo tal cual: puede significar que no hubo PRs de código,
no que el código esté limpio.

Los hallazgos `sin_severidad` son comentarios de algún revisor
automático que no usa nuestro prefijo `[Crítico]`/`[Alto]`/…, como
Copilot. Contalos aparte y aclaralo en una frase; no los repartas
entre las severidades ni los trates como si fueran críticos.

## Señales de atención
Solo lo que se desprenda de los datos: arrastre creciente, PRs que
tardan en mergearse, semanas sin commits. Si no hay ninguna, escribí
"Ninguna." y terminá. No inventes riesgos para llenar la sección.

En castellano, y breve: esto se lee en una reunión. Sin relleno y sin
adjetivos de más.

No pongas título ni fecha: el reporte se publica dentro de un issue
que ya los lleva. Empezá directo por `## Resumen`.
```

## Ejemplo de uso

**Pedido:** La corrida programada del viernes a las 9:00, o una manual con `dias_ventana: 14`.

**Resultado:** Abre un issue «Progreso semanal · 23 oct – 30 oct 2026» (etiqueta `reporte-semanal`) con Resumen, Qué se completó, Qué quedó en curso, Calidad y Señales de atención, más la tabla de números del script. Si no hubo actividad o el agente falla, lo dice explícitamente en vez de mostrar una semana tranquila.
