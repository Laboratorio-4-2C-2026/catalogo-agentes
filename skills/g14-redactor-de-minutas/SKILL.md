---
name: g14-redactor-de-minutas
description: Convierte las notas sueltas de una reunión (con profesores, el cliente o el equipo) en una minuta operativa con asistentes, decisiones, citas textuales de lo que autorizó cada parte, pendientes con responsable y el destino al que se propaga cada decisión. Usala apenas termina la reunión, antes de que las notas se enfríen y las autorizaciones queden de memoria.
metadata:
  tipo: skill
  area:
  - gestion
  - documentacion
  fase:
  - planificacion
  - revision
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
  madurez: probado
  relacionados: []
---

# Redactor de minutas

Una minuta es un **registro operativo**: alimenta las decisiones durables (ADR, estado del proyecto, backlog), no las reemplaza. Su valor está en dos cosas que la memoria pierde rápido: **qué autorizó exactamente cada parte, con sus palabras**, y **qué quedó pendiente y de quién**.

Caso de origen: `docs/minutas/2026-08-20-reunion-profesores-labv.md` del repo de dirección de VaiVen (reunión con profesores sobre agentes, testing y Valor Ganado). Las citas textuales de la cátedra que hoy fijan límites del proyecto —por ejemplo, la autorización a que un agente corrija dejando un PR— se registraron con este mismo formato. Las autorizaciones citadas son específicas de ese caso y no habilitan a dirección a escribir código de producto.

## Entrada

- Notas crudas: bullets, transcripción, mensajes de chat, audio transcripto.
- Fecha, tipo de reunión y quiénes estuvieron. Si no lo dicen las notas, **preguntalo**; no lo deduzcas.
- Dónde vive cada tipo de conocimiento en el repo (tabla de ruteo del `CLAUDE.md` o equivalente).

## Procedimiento

1. **Separá el ruido de lo que obliga.** Clasificá cada nota como: decisión, autorización o restricción de una parte, sugerencia o idea, pendiente, o contexto. Lo que no entra en ninguna, se descarta.
2. **Agrupá por tema**, no por orden cronológico. Un tema por sección numerada (`## 1. Agentes`, `## 2. Testing y automatización`…).
3. **Citas textuales para todo lo que autoriza, prohíbe o exige.** Entre «comillas», atribuidas a quien lo dijo, con su etiqueta de procedencia:
   - `[verificado — escrito, DD/MM/AAAA]` si está en un mensaje o documento.
   - `[verificado — oral, DD/MM/AAAA]` si se dijo en la reunión y está en las notas.
   - `[por-verificar]` si alguien lo recuerda pero no está registrado. Eso **no** se usa como autorización hasta confirmarlo por escrito.
4. **Negrita sólo en lo que obliga** («**Vamos a tener que reportarlo.**», «**primero el proceso se hace manualmente**»). Si todo está en negrita, nada lo está.
5. **Pendientes con dueño y fecha.** Formato `- [ ] Qué — responsable — para cuándo`. Un pendiente sin responsable se marca `(sin responsable)` y se lo señala en el resumen: no se le asigna a nadie por inferencia.
6. **Propagación.** Cerrá con la sección `Pendiente de propagar`: cada decisión o idea con el **link al documento destino** y el estado (`no hecho todavía en esta sesión` o el commit que lo hizo). Destinos típicos:
   - decisión técnica o de alcance durable → ADR nuevo;
   - cambio de alcance → primero el charter;
   - estado, frente nuevo, pregunta abierta → archivo de estado del proyecto;
   - idea de agente → shortlist, contra su criterio de entrada (no al inventario);
   - tarea para el equipo de desarrollo → ticket.
   Si algo no tiene punto de entrada en el repo, decilo explícito («sin punto de entrada en el repo todavía»).

## Formato de salida

```markdown
# Minuta — <tipo de reunión>, DD/MM/AAAA

> Registro operativo. Fuente primaria para <ADRs, estado, backlog>: no reemplaza esos lugares, los alimenta.

**Asistentes:** <nombres y rol> · **Ausentes:** <si importa>

## 1. <Tema>
- <decisión o sugerencia, en presente>
- <Parte>: «<cita textual>» `[verificado — oral, DD/MM/AAAA]`

## N. Próxima reunión
- <qué se prepara antes>

---

**Pendientes**
- [ ] <qué> — <responsable> — <fecha>

**Pendiente de propagar**
- <decisión> → [`ruta/destino.md`](ruta/destino.md) — no hecho todavía
```

Nombre del archivo: `docs/minutas/AAAA-MM-DD-<tipo-de-reunion>.md`, y su línea en el índice de documentos si el repo lo tiene.

## Qué NO hacer

- No parafrasear una autorización: si la frase exacta no está, va `[por-verificar]`.
- No convertir una sugerencia de la reunión («evaluar Playwright») en una decisión del equipo.
- No propagar en silencio: si en la misma sesión escribís el ADR o actualizás el estado, la minuta lo dice con el link.
- No incluir datos personales de contacto de los asistentes.
- No juzgar a las personas: los problemas del equipo se registran como hechos y acciones, no como evaluación.

## Ejemplo de uso

**Pedido:** Pasá a minuta estas notas de la reunión de hoy con los profesores; dijeron que el agente puede abrir un PR con la corrección y que el merge lo hace una persona.

**Resultado:** Devuelve `docs/minutas/AAAA-MM-DD-reunion-profesores.md` con asistentes, temas numerados, la autorización como cita textual con `[verificado — oral, fecha]`, pendientes con responsable y una sección «Pendiente de propagar» que manda la autorización al ADR o al `CLAUDE.md` correspondiente.
