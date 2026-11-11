---
name: g07-panel-validacion-feature
description: "Valida y ajusta una feature de front con un panel de cuatro subagentes con roles separados: un experto en UX que escribe los casos, un experto en UI que la implementa, y un usuario entusiasta y otro indiferente que la prueban en Claude in Chrome sin ver el código. Cierra con una tabla de ajustes que el usuario aprueba antes de aplicarlos. Usar al explorar o pulir una pantalla o flujo antes de llevarlo a ticket. Pide al inicio el prototipo, el repo y sus convenciones."
metadata:
  tipo: skill
  area:
  - diseno
  - frontend
  - qa
  fase:
  - diseno
  - testing
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - chrome
  grupo: "07"
  autor:
    nombre: Julieta Garberoglio
    github: JulietaG13
  responsables:
  - JulietaG13
  madurez: usado-en-proyecto
  relacionados: []
---

# Panel de validación de una feature

Cuatro subagentes, cada uno con un solo rol y solo el contexto que ese rol necesita. La gracia está en la separación: quien diseña los casos no implementa, y quien prueba no lee ni los casos ni el código.

Documento vivo: cuando una ronda descubre algo general, se agrega.

---

## Antes de empezar: datos del proyecto

Usá lo que ya esté en la conversación o en el `CLAUDE.md` / `AGENTS.md` del repo. Lo que falte, pedilo **en un solo mensaje** y no lo adivines.

| Dato | Para qué |
|---|---|
| Ruta del repo del front y cómo se levanta en local | Implementar y probar |
| URL o capturas del prototipo de diseño, si hay | Fuente de verdad visual |
| Guía de convenciones de front o design system, si existe | Lo que el experto en UI tiene que respetar |
| Idioma de la interfaz | Textos y casos |
| Ticket de Jira, si existe | Contexto del brief |
| Carpeta ignorada por git para la entrega | Dejar el resultado |

## 0. Reglas que valen para todo el panel

- **La rama es de exploración.** Se trabaja en una rama o worktree propio (`explora/<feature>`), nunca en la rama de un developer. No hay commits a la rama principal, ni push, ni PR.
- **El prototipo es la fuente de verdad visual**, si hay. Lo que el prototipo define no se rediseña; el panel solo decide donde el prototipo no dice nada.
- **Todo en el idioma de la interfaz**, aunque el prototipo tenga textos en otro.
- **Sin librerías nuevas.** Si algo no sale con lo que el proyecto ya usa, se anota como límite y no se instala nada.
- **Datos neutros.** `Test User`, `user@example.com`, nada de nombres ni mails reales.
- **Máximo dos rondas.** Si después de la segunda ronda sigue habiendo hallazgos graves, se para y se reporta: la feature necesita una decisión de producto, no más iteraciones.

## 1. Brief (lo arma el orquestador)

Antes de lanzar a nadie, juntar en un bloque corto:

- Qué es la feature y para quién (una o dos oraciones).
- Pantallas del prototipo que la cubren.
- Qué está fuera de alcance.
- Ticket, si existe.

Mostrarle el brief al usuario y esperar el OK. Sin brief aprobado no se lanza el panel.

## 2. Experto en UX: escribe los casos

**Recibe:** el brief y el prototipo. **No recibe:** código.

Escribe una lista numerada de casos de uso. Cada caso tiene quién, qué quiere lograr, pasos, y un resultado observable que se pueda marcar ✅ o ❌ mirando la pantalla. Tiene que cubrir:

- El camino feliz.
- Estados vacíos, de carga y de error (sin conexión, error del servidor, respuesta lenta).
- Cancelar o volver atrás a mitad del flujo.
- Teclado: Tab, Enter y Escape (Escape cierra solo el overlay que esté arriba).
- Textos: que se entiendan sin contexto y que digan qué hacer cuando algo falla.

Si un caso contradice el prototipo, gana el prototipo y el caso se reescribe.

La lista se le muestra al usuario, que puede aceptar, sacar o reescribir casos. Recién con la lista aprobada se pasa al §3.

## 3. Experto en UI: implementa

**Recibe:** el brief, el prototipo, los casos aprobados y la guía de front del repo. **No recibe:** las opiniones de los testers (todavía no existen).

- Implementa en la rama de exploración, respetando las convenciones del proyecto (espaciado, colores, componentes base).
- Los skeletons de carga respetan la geometría real del contenido.
- Al terminar, levanta el front y devuelve la URL local y qué casos cree que cubrió. Lo que no pudo cubrir lo dice, no lo esconde.

## 4. Los dos testers, en paralelo y por separado

Se lanzan al mismo tiempo, cada uno en su propio contexto. **Reciben:** la URL, una consigna de usuario y nada más: ni casos, ni código, ni lo que dijo el otro tester.

**Tester entusiasta.** Le gusta la idea y quiere usarla. Prueba todo lo que la feature promete y reporta:
- Dónde se trabó o tuvo que adivinar.
- Qué esperaba encontrar y no estaba.
- Qué lo haría volver a usarla.

**Tester indiferente.** No le importa la feature, entró a la app a hacer otra cosa. Reporta:
- Si la feature le estorbó para lo que iba a hacer.
- Si la pudo ignorar o cerrar sin leer.
- Si algún texto o aviso lo confundió.
- Cuántos clics de más le costó.

Los dos navegan como usuarios con Claude in Chrome: no leen el código ni el DOM para decidir qué hacer. Cada hallazgo va con la pantalla y los pasos para llegar.

## 5. Síntesis (orquestador)

Cruzar los dos reportes con los casos de UX y armar una sola tabla:

| | Hallazgo | Quién lo vio | Caso UX | Ajuste propuesto |
|---|---|---|---|---|
| ❌ | … | entusiasta / indiferente / ambos | #N o "sin caso" | … |

- Lo que vieron **los dos** va primero.
- Un hallazgo **sin caso UX** significa que a la lista le faltaba un caso: se propone agregarlo.
- Un caso UX que **ningún tester tocó** se marca "no ejercitado" y no se da por bueno.
- Los ajustes que contradicen el prototipo no se proponen: van como pregunta para producto.

El usuario aprueba ajuste por ajuste. El experto en UI aplica solo los aprobados, y los dos testers vuelven a probar (ronda 2, con contexto nuevo).

## 6. Entrega

Un markdown en `<carpeta>/panel-<feature>.md` con:

1. Brief aprobado.
2. Casos de UX finales con su ✅/❌.
3. Tabla de hallazgos con lo que se aplicó y lo que quedó pendiente.
4. Preguntas para producto, si hay.

Ese archivo sirve de base para escribir el ticket. La rama de exploración no se mergea: es material de referencia.

## Ejemplo de uso

**Pedido:** "Pasá la pantalla de mazos de flashcards por el panel: quiero ver si el flujo de crear un mazo y agregarle tarjetas se entiende."
**Resultado:** pide el prototipo y la guía de front si faltan, muestra el brief y la lista de casos de UX para aprobar, implementa la pantalla en una rama de exploración y la hace probar por el usuario entusiasta y el indiferente. Entrega la tabla de hallazgos con los ajustes aprobados y los que quedan como pregunta para producto.
