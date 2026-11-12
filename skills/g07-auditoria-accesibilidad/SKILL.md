---
name: g07-auditoria-accesibilidad
description: "Audita la accesibilidad de una pantalla del frontend React de Study Arena en el navegador (axe-core más una revisión manual con teclado, foco, lector de pantalla, contraste, textos alternativos, timers y animaciones del juego) y devuelve los problemas por severidad WCAG con el arreglo concreto en el componente y archivo:línea. Usar antes de aceptar un ticket frontend o antes de una entrega; no modifica código."
metadata:
  tipo: skill
  area:
  - frontend
  - qa
  - diseno
  fase:
  - testing
  - revision
  tecnologias:
  - react
  - typescript
  - playwright
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - chrome
  grupo: "07"
  autor:
    nombre: Ana Abramowich
    github: AbramowichAna
  responsables:
  - AbramowichAna
  madurez: experimental
  relacionados:
  - g07-study-arena-prototype-parity-auditor
  - g07-qa-acceptance
  - g07-code-review-tl
---

# Auditoría de accesibilidad

Una app de estudio la usan personas que navegan con teclado, con lector de pantalla, con zoom o con baja visión. Las apps gamificadas tienen además problemas propios: **timers** que no se pueden pausar, **animaciones** de logro que marean, **colores** como única forma de saber si respondiste bien y **rankings** que el lector de pantalla lee como una sopa de números.

Esta skill audita **una pantalla o un flujo** por vez, combinando una herramienta automática (que detecta alrededor de un tercio de los problemas) con una revisión manual guiada (que encuentra el resto).

## Cuándo usar esta skill

"Revisá la accesibilidad de X", "¿esto se puede usar con teclado?", "a11y", "WCAG", antes de aceptar un ticket frontend o antes de una entrega.

## Paso 0: preparar

1. Front levantado (por ejemplo `npm run dev` en `frontend/`, normalmente `http://localhost:5173`) y, si la pantalla necesita datos, el backend y un usuario de prueba (si hace falta, generá el mundo con `g07-seed-mundo-gamificado`).
2. Definí con el usuario **qué pantalla y qué estados** auditar: vacío, cargando, con datos, error y, si hay juego, durante la partida y al terminar.

## Paso 1: pasada automática (axe-core)

Elegí la opción que esté disponible:

- **A. Navegador del agente** (Claude in Chrome o el navegador integrado): abrí la URL y ejecutá en la página axe-core desde el paquete del proyecto si está instalado, o desde `https://cdn.jsdelivr.net/npm/axe-core/axe.min.js` (inyectando un `<script>` y después `await axe.run()`). Si la página bloquea scripts externos, usá B.
- **B. Línea de comandos**: `npx @axe-core/cli <url> --tags wcag2a,wcag2aa,wcag21aa --exit` (necesita Chrome instalado).
- **C. Playwright**, si el repo ya lo usa: un test temporal fuera del repo con `@axe-core/playwright`.

Corré la pasada **en cada estado** acordado, no solo en la carga inicial. Para cada violación, guardá la regla, el impacto, el selector y el HTML.

## Paso 2: revisión manual (lo que axe no ve)

Hacé cada chequeo en el navegador y anotá el resultado con evidencia (qué tecla, qué pasó y una captura si sirve):

**Teclado**
- Con solo `Tab`, `Shift+Tab`, `Enter`, `Espacio` y flechas, ¿se puede completar la tarea principal de la pantalla?
- ¿El orden del foco sigue el orden visual?
- ¿El foco **se ve** siempre? (cuidado con `outline: none`).
- Al abrir un modal, ¿el foco entra, queda atrapado y vuelve al cerrarlo? ¿`Esc` lo cierra?
- ¿Hay `div` u `span` con `onClick` que no son alcanzables con teclado?

**Lector de pantalla y semántica**
- ¿Hay un `h1` único y una jerarquía de encabezados lógica?
- ¿Los botones de solo ícono tienen nombre accesible (`aria-label`)?
- ¿Los inputs tienen `label` asociado y los errores de formulario se anuncian (`aria-describedby`, `aria-invalid`)?
- ¿Los cambios dinámicos importantes (respuesta correcta o incorrecta, puntos ganados, cambio de posición en el ranking, tiempo de focus o break por terminar) se anuncian con una región `aria-live`?
- **Ranking y tablas**: ¿son una `<table>` con encabezados, o al menos una lista con texto que diga la posición, el nombre y los puntos?

**Visual**
- Contraste de texto (4,5:1, o 3:1 para texto grande) y de componentes de UI y foco (3:1). Revisá sobre todo los badges, los chips de puntos y el texto sobre degradados.
- ¿El **color es la única** señal de algo (verde = correcto, rojo = incorrecto, medalla dorada)? Tiene que haber también un ícono o un texto.
- Zoom al 200% y ancho de 320px: ¿se lee todo sin scroll horizontal?

**Propios de la gamificación**
- **Timers**: ¿se pueden pausar, extender o desactivar? (WCAG 2.2.1). Si es una competencia en tiempo real y no se puede, anotalo como una decisión de diseño a justificar.
- **Animaciones** (confeti, contadores, temporizador de la sesión): ¿respetan `prefers-reduced-motion`? ¿Algo parpadea más de 3 veces por segundo?
- **Sonidos**: ¿se pueden apagar? ¿Hay algo que solo se comunique con sonido?

## Paso 3: ubicar en el código y proponer el arreglo

Para cada problema, buscá el componente React responsable (`rg` por el texto visible, la clase o el `data-testid`) y proponé el arreglo concreto:

```tsx
// frontend/src/components/AnswerFeedback.tsx:23
- <div className="correct" />
+ <p role="status" className="correct"><CheckIcon aria-hidden="true" /> ¡Correcta! Sumaste 10 puntos</p>
```

## Output

1. Pantalla, estados auditados y herramientas usadas.
2. Resumen: N problemas (🔴 bloqueante · 🟠 serio · 🟡 moderado · ⚪ menor).
   - 🔴 Bloqueante: impide completar la tarea a alguien (por ejemplo, no se puede responder con teclado).
3. Problemas ordenados por severidad. Cada uno con: qué pasa, a quién afecta, el criterio WCAG, la evidencia, `archivo:línea` y el arreglo propuesto.
4. Lo que está bien (breve, para no romperlo).
5. Lo que no se pudo verificar (por ejemplo, no hubo lector de pantalla real disponible).

Si el usuario quiere cargarlo en Jira, ofrecé redactar los 🔴 y 🟠 como bugs, pero no los crees sin un "sí" explícito.

## Qué no hacer

- No modifiques el código: proponé el diff.
- No des la pantalla por "accesible" solo porque axe no encontró nada.
- No marques como bloqueante algo que es una preferencia de estilo.

## Ejemplo de uso

**Pedido:** Auditá la accesibilidad de la pantalla de partida de Study Arena, durante la partida y al terminar.

**Resultado:** Corre axe-core en los dos estados y revisa la pantalla a mano con teclado, foco, aria-live, contraste, timers y animaciones. Reporta, por ejemplo, 🔴 que las opciones de respuesta son divs no alcanzables con Tab, 🟠 que correcto e incorrecto solo se distinguen por el color y 🟡 que el confeti ignora prefers-reduced-motion, cada uno con su archivo:línea y el arreglo propuesto.
