---
name: g14-traductor-de-tickets-para-jira
description: "Adapta tickets ya redactados al texto publicable en Jira: resuelve cada referencia interna (decisiones numeradas, ADR, charter, horas) en una regla que el dev pueda leer y verifica el resultado con los chequeos T1 a T6. Usala antes de publicar un ticket Markdown que cita documentos que el dev no puede abrir; no redefine alcance ni estimación."
metadata:
  tipo: skill
  area:
  - gestion
  - documentacion
  fase:
  - planificacion
  - analisis
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - jira
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

# Traductor de tickets para Jira

El ticket en Markdown es nuestro; la descripción en Jira es del dev. El dev **no tiene el repo de dirección**: tiene la descripción de Jira y el kit de contexto (en VaiVen, `ai-config/docs/`). Todo lo que el ticket cite y el dev no pueda abrir es un puntero muerto.

Fuentes en VaiVen: `docs/planning/tickets/criterio-de-traduccion.md` (los chequeos), la sección «Estándar de redacción de tickets» de `CLAUDE.md` y el ADR-0014 (cómo se produce el kit).

## Qué se publica

Las secciones 1 a 5 son las del formato de g14-redactor-de-tickets-ejecutables; su «Ficha y relaciones» no se publica. Sólo esto llega a Jira: la línea **«En una línea»**, las secciones **1, 2, 3**, la **evidencia de la 4** y la **5**. En una tarea madre: «Qué construye», la tabla de subtareas y las dependencias. La **Ficha y Relaciones** y los avisos `>` se quedan de nuestro lado: es el único lugar donde van horas, tripletes y citas a ADR o `D-XX`.

**Todo chequeo corre sobre el texto publicado.** El `.md` se corrige para que lo publicado salga bien.

## Procedimiento: cada cita se resuelve al escribir, no al publicar

Recorré las secciones publicables y, por cada `D-XX`, `R-X`, `ADR-XXXX § n`, código WBS o «el charter», decidí una de tres:

1. **Es horas, calibración, triplete, estado de ratificación, alternativa descartada, algo `[asumido]` o un vencimiento** → se borra. Queda en la ficha o en su documento. Las horas van al campo de estimación de Jira, nunca al cuerpo.
2. **Es una regla que usa sólo este ticket** → se escribe en el ticket, **en presente**, en una o dos frases, sin el código.
3. **Es una regla que usa más de un ticket** (la forma de una tabla, el contrato de una llamada, las políticas) → vive en el kit. Primero buscá si el kit ya la trae; si no, escribila ahí en el mismo cambio, con su línea en el `INDEX.md` del kit. El ticket **nombra el documento y la sección por su título** («`datos/esquema.md`, sección `contactos`»).

**Nunca se saca una cita sin poner la regla en su lugar.** Si al borrar el código la frase queda sin sentido, la regla todavía no está escrita del lado del dev.

Llevá una tabla de trabajo (no se publica):

| Cita sacada | Qué la reemplaza |
|---|---|
| `ADR-0002 § 4` | (b) `datos/permisos.md`, fila `matches` |
| `D-XX` (decisión del PM) | (a) «La semilla usa sólo publicaciones que ya no están activas.» |
| triplete 1,0/1,5/2,25 | (c) se queda en la ficha |

## Chequeos (criterio de aceptación de la traducción)

- **T1 — Ninguna cita interna.** Grep sobre lo publicado, cero coincidencias: `\b[DHPVLRI]-\d+`, `ADR-?\d{4}`, `ADR`, `§`, códigos WBS `\d\.[A-D]\.\d`, `charter`, `checkpoint`, `grilla`, `calibra`, `triplete`, `ratific`, `asumido`, `por-verificar`, y **ninguna hora** (ni columna `h`, ni `(1,5 h)`). Se permiten IDs de ticket (`H4-A.1.1`, `SCRUM-76`), nombres de documentos del kit y la numeración `CA-n` del checklist.
- **T2 — No se sacó nada sin poner la regla.** Cada fila de la tabla es (a), (b) o (c); una (c) que no sea horas/calibración/supuesto/vencimiento hace fallar el ticket.
- **T3 — Una sola explicación.** Lo que aparece en más de un ticket de la semana no se explica en el ticket: se nombra el documento del kit.
- **T4 — Del lado del kit.** Cada documento nombrado existe, tiene su línea en el `INDEX.md` del kit y **contiene la regla** (grep de la frase). Lo agregado pasa T1, no trae nada asumido y lo pide un ticket ya publicado (entrega progresiva: el kit no se adelanta).
- **T5 — Lectura en frío.** Un revisor sin contexto, con acceso sólo al kit y a los textos publicados, dice por ticket qué construye, qué regla gobierna cada decisión y dónde tendría que deducir o preguntar. Pasa con cero huecos atribuibles a una cita sacada (ver `g14-revisor-fresco-de-tickets`).
- **T6 — Publicado.** Publicar, releer desde Jira, correr T1 sobre lo publicado y confirmar que ninguna madre quedó vacía y que la estimación sigue cargada.

**El criterio no lo escribe quien traduce**, o se escribe antes de traducir.

## Qué NO hacer

- No copies la estructura del repo de dirección al kit ni lo organices por códigos internos.
- No marques cada pieza del kit con el ticket que la crea y la entregues entera: eso no es entrega progresiva.
- No metas horas en el cuerpo «para que el dev sepa»: van al campo de Jira.
- No declares la traducción hecha sin la corrida de T1 sobre el texto publicado.

## Ejemplo de uso

**Pedido:** Traducí `H5-B.3.0` para publicarlo: la sección 1 dice «como ADR-0002 § 2» y «según D-XX» (la semilla sin publicaciones activas), y la 3 tiene «(1,5 h)».

**Resultado:** Reemplaza «ADR-0002 § 2» por «`datos/esquema.md`, secciones `contactos` y `matches`» (verificando que el kit las trae), escribe esa regla en presente en el ticket, borra la hora del cuerpo, devuelve la tabla cita → reemplazo y la corrida de T1 con cero coincidencias.
