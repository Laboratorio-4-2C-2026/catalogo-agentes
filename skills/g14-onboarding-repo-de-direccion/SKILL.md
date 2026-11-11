---
name: g14-onboarding-repo-de-direccion
description: 'Orienta a quien abre por primera vez (o después de semanas) el repositorio de dirección de un proyecto: qué está decidido, qué significa cada código interno y dónde se escribe cada cosa. Pensada para repos de dirección con ADRs, estado vivo y bitácora.'
metadata:
  tipo: skill
  area:
  - documentacion
  - gestion
  fase:
  - analisis
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: '14'
  autor:
    nombre: Elías Ballesteros
    github: Elias85974
  colaboradores: []
  responsables:
  - Elias85974
  madurez: experimental
  relacionados:
  - g14-tutor-del-proyecto
  - g14-ponerse-en-tema
  - g02-zest-onboarding
---

# Onboarding al repositorio de dirección

## Qué es esto

Un recorrido guiado para alguien del equipo de dirección que llega al repo y necesita **poder trabajar**, no leer 17 000 líneas.

El principio que gobierna el recorrido: **entregar el mínimo que la tarea necesita.** El corpus está escrito para consultarse por decisión, no para leerse entero. Un onboarding que abruma es peor que ninguno, porque la persona sale creyendo que ya miró.

## Cuándo no usarla

Si la persona ya sabe qué documento quiere, andá directo a ese documento. Esta skill sirve para orientar, no para intermediar.

## El recorrido

**1. Cargá el estado, y nada más.** Leé `docs/PLANNING-STATE.md` completo y `docs/INDEX.md`. Todavía no abras ningún otro documento — el INDEX existe justamente para no tener que hacerlo.

**2. Preguntá qué viene a hacer.** Una sola pregunta, con opciones concretas. Por ejemplo: entender el proyecto · cerrar una decisión pendiente · escribir o revisar un documento · preparar una entrega para la cátedra · trabajar el cronograma.

**3. Entregá dos o tres documentos. Nunca más de tres.** Con una línea de por qué cada uno, sacada del INDEX. Si te parece que hacen falta seis, la tarea está mal delimitada: volvé al paso 2 y estrechala.

**4. Marcá las trampas que aplican a *esa* tarea.** No las generales — las que van a morder:

- Si toca algo cerca del código del producto, la **Regla #1** de `CLAUDE.md`, que tiene un 2 para el equipo entero como penalidad.
- Las **preguntas abiertas** de `PLANNING-STATE.md` que caen sobre esa tarea. Trabajar encima de una pregunta abierta sin saberlo produce trabajo que se tira.
- Lo que en ese terreno está `[asumido]` y no `[verificado]`.

**5. Cerrá diciendo qué actualizar.** Según el **Ruteo de conocimiento** de `CLAUDE.md`: dónde va lo que produzca, y que `PLANNING-STATE.md` se actualiza al terminar.

## Cómo se leen los códigos del corpus

Los documentos se referencian entre sí con códigos. Sin esta tabla son opacos:

| Código | Qué es | Dónde vive |
|---|---|---|
| `D-N` | Decisión firme. Ya se discutió; no se reabre sin motivo nuevo | `PLANNING-STATE.md` |
| `H-N` | Hallazgo de la revisión del charter, con severidad y estado | `charter/hallazgos-revision.md` |
| `P-N` | Pregunta abierta. **Nadie sabe la respuesta todavía** | `PLANNING-STATE.md` |
| `R1`, `R2`… | Riesgo, con respuesta y señal de alerta. **Sin guion**, a diferencia del resto | `charter/riesgos.md` |
| `L-N` | Palanca: algo que devuelve horas al plan si se acciona | `charter/cronograma.md` |
| `INC-N` | Incremento protegido de alcance | `planning/README.md` |
| `CA-N` | Criterio de aceptación | documento de la entrega |
| `ADR-NNNN` | Decisión de arquitectura | `architecture/adr/` |

Regla de lectura: un `D-N` cierra la discusión, un `P-N` la abre. Confundirlos hace que alguien reabra lo cerrado o dé por resuelto lo que no lo está.

## Errores comunes

| Error | Por qué duele |
|---|---|
| Volcar el INDEX entero como "recorrido" | Es el corpus otra vez, con otro nombre. El valor está en el recorte |
| Dar por vigente el PDF del charter | La fuente canónica es el charter en markdown. El PDF es un snapshot histórico |
| Tratar el catálogo de agentes como inventario | El catálogo es un menú de ideas. Si no está en `agentes/inventario.md` con evidencia, no existe |
| Afirmar estado sin abrir el documento | «Debería estar hecho» no es un estado. Se mira o no se dice |

## Portabilidad

Este archivo es un `SKILL.md` estándar: no depende de ninguna herramienta. Funciona cargado como skill, como regla de proyecto en otro editor, o pegado directo en un chat con cualquier agente que pueda leer los archivos del repo.

## Ejemplo de uso

**Pedido:** Es la primera vez que abro este repo, ¿por dónde empiezo y qué significa D-16?

**Resultado:** Explica la estructura del repo, el orden de lectura recomendado y resuelve el código interno contra el documento que lo define.
