---
name: g02-comite-de-decisiones
description: 'Usar cuando haya que tomar una decisión del proyecto Zest (técnica, de alcance, de presupuesto, de equipo o de cómo presentar algo) y se quiera una mirada sin sesgo: convoca a tres subagentes en paralelo, un abogado del diablo, un aliado y un neutral, y devuelve sus posiciones con preguntas para que decida la persona.'
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  - analisis
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: "02"
  autor:
    nombre: Maria Clara Lopez
    github: ClaraLopez1
  responsables:
  - ClaraLopez1
  madurez: usado-en-proyecto
  relacionados:
  - g08-devils-advocate
  - g11-analizar-cambio-alcance
  - g02-control-de-cambios
---

# Decision committee — three views before you decide

For any decision (technical, scope, budget, team, how to present something),
Claude convenes a committee of three roles so the user gets an unbiased view
and has to think before choosing. The point is not that Claude decides: it is
that the user decides knowing the best case for, the best case against, and a
cold reading of the trade-off.

Answer in Spanish.

## The three members

| Member | Job | Must not |
|---|---|---|
| **Abogado del diablo** (critic) | Argue against the option the user is leaning towards. Find the risks, hidden costs, false assumptions, what can go wrong and what it would cost Zest. Propose the strongest alternative. | Be negative for the sake of it, or attack a strawman. Every objection points to something concrete. |
| **Aliado** (advocate) | Make the strongest honest case for the option. Why it is a good idea, what it unlocks, how to mitigate the critic's objections. | Flatter. If the option is weak, say what would have to be true for it to work. |
| **Neutral** (arbiter) | Weigh both sides without a stake. Lay out the trade-off, the criteria that really decide it, what information is missing and how cheaply it could be obtained, and how reversible the decision is. | Pick the middle by default, or repeat the other two. It adds what both missed. |

## How to run it

1. **Frame the decision** in one or two sentences: what is being decided, the
   options on the table, which one the user leans towards (if any), and the
   deadline. If the question is vague, ask one clarifying question first.
2. **Gather context** relevant to the decision — the Zest rules in
   `../AGENTS.md` (`zest-support/AGENTS.md`), the schema in `../docs/db.md` (`zest-support/docs/db.md`),
   the budget and schedule in `project-management.md` (skill `g02-valor-ganado-evm`),
   the relevant tickets in Multica. Every member argues from the same facts.
3. **Hear each member independently.** When the tool can run subagents (Claude
   Code's `Agent` tool), run the three as separate subagents in parallel, each
   with the framing, the shared context and only its own role, so none of them
   is anchored by the others. Without subagents, write each position in full
   before reading the next, and do not let a later member just rebut the
   earlier one.
4. **One round of replies** (optional, only when the positions clash on a
   fact): the critic and the advocate each answer the other's strongest point
   in two or three lines.
5. **Hand it back to the user** in this format:

```
## La decisión
<one or two sentences>

## 😈 Abogado del diablo
<3–5 points, the strongest first>

## 🤝 Aliado
<3–5 points, the strongest first>

## ⚖️ Neutral
- Lo que realmente decide esto: <the 1–3 criteria>
- Lo que no sabemos: <missing info, and how to get it>
- Reversibilidad: <easy / costly / one-way, and why>
- Lectura: <which way the evidence leans and under what condition it flips>

## Preguntas para vos
<2–3 questions that make the user take a position>
```

6. **Let the user decide.** Don't close with "I recommend X" as the last word —
   the neutral member's reading is as far as the committee goes. If the user
   asks for Claude's own opinion explicitly, give it, labelled as such.

## When one option is clearly indefensible

Sometimes the facts rule an option out (it breaks a rule, repeats a known
mistake). Then the three members will lean the same way, and that is fine — it
is not bias, as long as each one still does its job:

- The **devil's advocate** does not defend the dead option for the sake of it.
  It attacks the surviving option *as proposed*: its weak version, the costs and
  side effects nobody mentioned, the facts it rests on that are not verified.
- The **advocate** argues for the best version of the surviving option, not
  just against the dead one.
- The **neutral** says plainly that one option is out and why, and puts the
  weight on the condition that would bring it back.

Say it in the output, right under "La decisión": *"Una de las opciones no se
sostiene con los datos; el comité discute cómo hacer bien la otra."* That way
the user doesn't read the agreement as three copies of the same opinion.

## Scale it to the decision

- Small, reversible decision (a name, the order of two slides): a short version
  of each member, a few lines each.
- Costly or one-way decision (changing the stack, dropping a module, moving the
  baseline): the full format, and the neutral member says what a wrong call
  would cost to undo.

## Zest-specific guardrails

- Settled architecture decisions (NestJS, Prisma, Auth0, the Render/Vercel/Neon
  deploy) can be put before the committee, but the result is a proposal to the
  team, never a change made on the spot — see `../AGENTS.md` (`zest-support/AGENTS.md`).
- A decision that changes scope, time or cost goes through change control
  afterwards (see `project-management.md` (skill `g02-valor-ganado-evm`)).
- Nobody in the committee invents data: missing numbers are listed under "Lo
  que no sabemos", not estimated silently.

## Instalación de los subagentes

Los tres miembros del comité son subagentes de Claude Code y están en
[`agents/`](./agents). Copialos a `.claude/agents/` del repo donde vayas a usar
la skill. En sus archivos dicen `support/skills/decision-committee.md`: si la
skill vive en otra ruta, pasales la ruta real en el pedido (la skill ya lo
indica).

## Ejemplo de uso

**Pedido:** "/g02-comite-de-decisiones ¿En el Steering 3 recalculamos el EV midiendo gestión e infraestructura como nivel de esfuerzo, aunque el SPI baje, o seguimos con el método del Steering 2?"

**Resultado:** Encuadra la decisión, lanza los tres subagentes en paralelo con los mismos datos y devuelve las tres posiciones (el abogado del diablo marcó que el CPI también cae, el aliado defendió recalcular y el neutral dijo qué dato da vuelta la decisión), cerrando con preguntas para la persona, sin decidir por ella.
