# Estructuras narrativas para la demo

Las técnicas que usa la skill, de dónde salen y cuándo conviene cada una. La
skill elige una principal según el público y el tiempo, y lo dice.

## 1. "Hacé lo último primero" (Peter Cohan, *Great Demo!*)

La demo tradicional arranca en el login y llega al resultado valioso a los 15
minutos, cuando la mitad ya se distrajo. Cohan propone darla vuelta: **mostrar
primero el resultado final**, la pantalla que resuelve el problema, y recién
después contar cómo se llega.

Para Zest:

1. **Situación** (una slide o una frase): quién es la persona, qué problema tiene
   y qué cambia si se resuelve.
2. **La pantalla final, ya armada**: la semana planificada, o la colección llena.
   "Así se ve el jueves de Sofi con Zest."
3. **"¿Cómo llegó acá?"**: el recorrido, solo los pasos imprescindibles.
4. **Preguntas**, mostrando más solo si alguien lo pide.

Usala cuando el tiempo es corto o el público no es técnico. Exige tener los datos
ya cargados (ver [`personas.md`](./personas.md)).

## 2. Sparkline (Nancy Duarte, *Resonate*)

Las grandes presentaciones no son una lista de funcionalidades: van y vienen
entre **lo que es** (hoy, con el problema) y **lo que podría ser** (con Zest). Ese
contraste crea tensión, y cada vuelta la resuelve un poco más hasta el cierre,
que termina en un llamado a la acción.

```
Lo que podría ser    ·  ╱╲    ╱╲    ╱╲      ← cierre: "el nuevo mundo" + pedido
Lo que es            · ╱  ╲  ╱  ╲  ╱  ╲
                     inicio                fin
```

Para Zest, cada funcionalidad es una vuelta:

| Lo que es | Lo que podría ser |
|---|---|
| La receta de la abuela está en una foto de WhatsApp | Está en Zest, con ingredientes y pasos |
| "Esa receta que vi la semana pasada... ¿dónde estaba?" | Guardada en la colección "Para compartir" |
| El domingo a la noche: "¿qué cocinamos esta semana?" | La semana ya planificada |

Usala en steerings y presentaciones de cierre, donde importa el porqué.

## 3. SCAR: Situación, Complicación, Acción, Resolución

La versión mínima de una historia, para presentar **una** funcionalidad en 20–40
segundos:

- **Situación**: Sofi tiene 40 recetas guardadas.
- **Complicación**: cuando quiere hacer algo dulce, no encuentra nada.
- **Acción**: arma la colección "Postres" y guarda ahí sin salir del feed.
- **Resolución**: dos clics y tiene todos los postres juntos.

Usala dentro de las otras estructuras, una por funcionalidad.

## 4. Tarjeta funcionalidad → valor

Antes de escribir el guion, cada funcionalidad que se va a mostrar se pasa a una
tarjeta. Si no se puede llenar, la funcionalidad no entra en la demo.

| Campo | Pregunta |
|---|---|
| Para quién | ¿Qué persona la usa? |
| Dolor | ¿Qué le pasa hoy sin esto? (con sus palabras) |
| Qué hace Zest | En una frase, sin jerga técnica |
| Prueba | ¿Qué se ve en pantalla que lo demuestra? |
| Requisito | ¿Qué RF/RNF del Charter cumple? |
| KPI | ¿Qué KPI mueve? (70% gestiona en Zest, 50% usa el planificador) |
| Estado | ¿Está en `done` y en producción? Si no, no se muestra |

## 5. El hilo entre steerings

Un steering no es una demo aislada: es un capítulo. Abrí retomando el anterior
("en el Steering 2 Sofi podía guardar recetas; hoy puede planificar la semana") y
cerrá con lo que viene. El tribunal tiene que sentir progreso, no una lista nueva
de pantallas.

## 6. Versiones por duración

Todo paquete trae el mismo mensaje en distintas longitudes:

| Versión | Contenido |
|---|---|
| **30 s** (elevator) | Persona + problema + Zest en una frase + un resultado |
| **2 min** | Hacé lo último primero, con una sola funcionalidad |
| **5 min** | Sparkline con 2–3 funcionalidades |
| **10 min** | Sparkline completa, con el hilo entre steerings y un cierre con pedido |

Si el tiempo se acorta en el momento (pasa seguido), quien presenta salta a la
versión más corta sin improvisar.

## 7. Reglas que vienen de todas las fuentes

- **Una sola historia, sin fallas**, antes que muchas funcionalidades a medias.
- **Ordená por el recorrido de la persona**, no por el backlog ni por módulo.
- **Datos realistas**: "Test User" o "receta 1" restan credibilidad. Los datos de
  la demo son un personaje más del guion.
- **Solo lo terminado** según la definición de "listo" del equipo.
- **Cada funcionalidad cierra con un resultado**: qué gana la persona, o qué KPI
  mueve.
- **Una demo es una conversación**: dejá lugar para preguntas y feedback, no la
  llenes de pantallas.

## Fuentes

- Peter Cohan, *Great Demo!* ("Do the Last Thing First"):
  [Pragmatic Institute](https://pragmaticinstitute.com/resources/webinars/product/create-and-deliver-surprisingly-compelling-software-demonstrations),
  [SK Murphy](https://www.skmurphy.com/?p=6924).
- Nancy Duarte, Sparkline:
  [Duarte — contrast](https://www.duarte.com/blog/ultimate-guide-to-contrast/),
  [charla TEDxEast](https://singjupost.com/nancy-duarte-discusses-common-structure-of-greatest-communicators-at-tedxeast-transcript/).
- Demos de sprint centradas en el usuario:
  [Atomic Object](https://spin.atomicobject.com/sprint-demos/),
  [Plane](https://plane.so/blog/how-to-run-an-effective-sprint-demo-a-complete-guide),
  [GitScrum](https://docs.gitscrum.com/en/how-to/sprint-demo-best-practices).
- Skills de la comunidad que inspiraron el paquete de salida (SCAR, guion con
  objeciones, empaquetado de la demo): *Demo Script Writer*, *Storytelling*
  (gtm-agents), *Demo Story Packager*.
