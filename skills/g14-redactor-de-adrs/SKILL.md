---
name: g14-redactor-de-adrs
description: Redacta un ADR corto y numerado (contexto, decisión, consecuencias y alternativas descartadas con su motivo) a partir de una decisión de arquitectura o de alcance ya tomada, con etiquetas de procedencia y la propagación al charter y al resto del repo. Usala cuando una sesión de dirección cerró una decisión durable que cambia límites del sistema, contrato de datos o entornos y todavía no está escrita.
metadata:
  tipo: skill
  area:
  - documentacion
  - gestion
  fase:
  - diseno
  - analisis
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: "14"
  autor:
    nombre: Anapaola Borda
    github: AnaB2
  colaboradores: []
  responsables:
  - AnaB2
  madurez: usado-en-proyecto
  relacionados: []
---

# Redactor de ADRs

Un ADR es una decisión durable, escrita corta. **El humano decide; el agente redacta.** Ejemplos reales en VaiVen: `docs/architecture/adr/0014-…`, `0016-la-puerta-del-motor-gemini-por-vertex.md`, `0018-la-nube-es-produccion.md`; índice en `docs/architecture/adr/README.md`; especificación en `docs/agentes/especificaciones/7.1-redactor-de-adrs.md`.

## Antes de escribir: ¿es un ADR?

- **Sí:** cambia los límites del sistema, el contrato de datos, los entornos o una tecnología, y va a seguir valiendo semanas.
- **No:** un cambio de alcance va **primero al charter**; un aprendizaje operativo va a la bitácora; el estado del proyecto va a `PLANNING-STATE.md`. Escribir ADRs de más ensucia el índice.

## Procedimiento

1. **Número.** Leé el índice: el siguiente libre, que no colisione con uno existente ni con uno **reservado**. Los números no se reciclan; un reservado que se resolvió por otra vía queda registrado con su destino.
2. **Material.** Leé la conversación o el documento donde se tomó la decisión y los ADRs vigentes. Listá cuáles **contradice o reemplaza**: se nombran explícitamente («Reemplaza el § 4 y el § 6 del ADR-0013; el resto sigue vigente»), nunca se escribe encima.
3. **Redactá** con la plantilla de abajo.
4. **Etiquetá cada hecho del contexto** con su procedencia: `[verificado — fuente, fecha]`, `[asumido]`, `[por-verificar — quién, cuándo]`.
5. **Propagá** (ver abajo) y agregá la línea al índice de ADRs y al índice general de documentos.

## Plantilla

```markdown
# ADR-NNNN · <la decisión en una frase, no el tema>

**Estado:** Propuesto — a ratificar por <quién> | Decidido por <quién> el dd/mm
**Fecha:** dd/mm/aaaa
**Dueño:** <rol>
**Reemplaza:** <ADR y sección, o «—»>
**Tickets:** <los que crea, cambia o da de baja>

## Contexto
- Hechos, uno por viñeta, cada uno con su etiqueta de procedencia.

## Decisión
1. Numerada, en presente, verificable.

## Consecuencias
- Lo que cuesta, incluido el costo aceptado y su mitigación.

## Alternativas descartadas
| Alternativa | Por qué no |

## Propagación
| Dónde | Qué cambia |
```

Optativas cuando aplican: «Verificaciones abiertas» (qué falta medir y quién), «Cómo se comunica» (a la cátedra o al cliente), «La medición» (tabla con la corrida que sostiene la decisión, como en el 0016).

## Reglas

- **Lo `[asumido]` no se hornea en un ADR.** Un supuesto que entra sin etiqueta se vuelve verdad del proyecto en dos semanas. Si la decisión se apoya en un supuesto, se dice con la etiqueta y se escribe qué haría falta para verificarlo; si el supuesto es la decisión misma, el ADR nace **propuesto**, con fecha de vencimiento o el evento que lo ratifica.
- **Alternativas descartadas: al menos una, con su motivo.** Un ADR sin alternativas es un anuncio. **No inventes alternativas**: si no se evaluó ninguna, se dice que no se evaluó.
- **Un ADR que sale del agente nace propuesto**, nunca aceptado, salvo que el dueño ya haya decidido y lo diga (el 0018 nació «Decidido por el PM»).
- **Corto.** Contexto en viñetas, decisión numerada. La deliberación larga va a otro documento y se enlaza.
- **La decisión se propaga.** Si toca alcance, KPIs, entregables o fechas, **primero se actualiza `docs/charter/project-charter.md`** y después el resto. La tabla de propagación lista cada documento afectado (charter, `PLANNING-STATE.md`, README de tickets, kit de los devs, índices) y se cumple en el mismo cambio o queda como checklist pendiente.
- Lo que cruza al kit de los devs es **la regla en presente**, sin el número de ADR ni la deliberación.

## Qué NO hacer

- No marques un ADR como aceptado por tu cuenta.
- No reescribas un ADR vigente para cambiar la decisión: se escribe uno nuevo que lo reemplaza.
- No cierres el ADR sin la línea en los índices y sin la tabla de propagación.

## Ejemplo de uso

**Pedido:** El PM decidió que el entorno desplegado se promueve a producción y no armamos `vaiven-prd`; escribí el ADR.

**Resultado:** Borrador `ADR-0018 · La nube es producción`, con el contexto etiquetado (lo que pide el charter, el costo de 6 h de dev, el límite del SMTP verificado en la doc), la decisión numerada, el costo aceptado y su mitigación, tres alternativas descartadas con motivo, el reemplazo explícito de las secciones del ADR-0013 y la propagación a tickets, índices y estado del proyecto.
