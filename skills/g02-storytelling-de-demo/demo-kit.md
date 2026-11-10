# Kit de demo: paquete de salida, fallas, checklists, preguntas y ensayo

Lo que la skill entrega y las herramientas para que la demo salga bien el día del
steering.

## 1. El paquete de demo

La skill entrega todo esto junto, en un solo documento, para que el equipo lo
pueda imprimir o abrir en el celular durante la presentación.

```
# Demo <evento> — <fecha>

## Ficha
Público · tiempo total · tiempo de demo · quién presenta · quién maneja la compu
· estructura elegida (y por qué) · versión de datos (personas.md)

## Mensaje central
<una frase: lo que el público tiene que recordar>

## Tarjetas funcionalidad → valor
<una por funcionalidad que entra, ver frameworks.md §4>

## Arco
<la estructura elegida, beat por beat, con el contraste "lo que es / lo que podría ser">

## Guion
| # | Tiempo | Quién | Acción (un clic por fila) | Qué se dice | Qué tiene que verse | Si falla |
|---|---|---|---|---|---|---|

## Versiones cortas
30 s · 2 min · 5 min — el mismo mensaje, para cuando el tiempo se achica

## Transiciones
<la frase que une cada bloque, incluidas la entrada a la demo y la salida>

## Preguntas probables
<pregunta → respuesta corta → dato o pantalla que la respalda>

## Plan B
<qué capturas o qué grabación, en qué paso se usan>

## Checklist
<T−3 días, T−30 min, T−2 min (abajo)>
```

## 2. Mapa de fallas de Zest

Cada paso del guion que toca alguna de estas cosas lleva la recuperación en la
columna "Si falla". Quien presenta tiene que poder seguir sin pensar.

| Dónde puede fallar | Por qué | Prevención | Si pasa igual |
|---|---|---|---|
| Backend en Render | El plan gratuito se duerme y tarda en despertar | Pegarle a `/health` 2–3 minutos antes y dejar el feed cargado | "Mientras carga, les cuento..." y seguir con la frase de la persona; si pasan 30 s, plan B |
| Login con Auth0 | Redirección, cookie vencida, red del aula | Sesión iniciada antes, en una pestaña aparte | Saltar el login: "ya estamos adentro como Sofi" |
| Subida de imagen a S3 | Red lenta, archivo pesado | Imagen chica (<1 MB) ya elegida en el escritorio | Crear la receta sin imagen y decirlo; mostrar una ya cargada |
| Búsqueda y filtros | Datos de prueba distintos a los del guion | Datos de [`personas.md`](./personas.md) cargados y verificados el mismo día | Usar el filtro por categoría, que es el más estable |
| Datos | Alguien del equipo editó o borró algo en producción | Revisar el set completo en el ensayo T−30 min | Plan B con capturas |
| Proyector o resolución | Pantalla chica, zoom raro | Probar la resolución en el aula; zoom del navegador al 110–125% | Seguir; describir en voz alta lo que no se lee |
| Red del aula | Wi-Fi saturado | Hotspot del celular listo | Grabación |

## 3. Checklists

**T−3 días: ensayo general**
- [ ] Ensayo completo con el guion, cronometrado, con quien va a presentar.
- [ ] Todo lo que se muestra está en `done` y en producción (no solo en una rama).
- [ ] Datos de la demo cargados en producción, según `personas.md`.
- [ ] Grabación del recorrido completo (plan B) y capturas de cada pantalla clave.
- [ ] Preguntas probables repasadas en voz alta.
- [ ] Si algo falló en el ensayo, está arreglado o tiene su línea de recuperación.

**T−30 minutos**
- [ ] Datos revisados: recetas, colecciones, planificador como en el guion.
- [ ] Sesión de Sofi iniciada en una pestaña; pestañas extra cerradas.
- [ ] Notificaciones apagadas; modo no molestar.
- [ ] Grabación y capturas abiertas en otra ventana, listas.
- [ ] Hotspot disponible.

**T−2 minutos**
- [ ] `/health` respondió; feed cargado.
- [ ] Zoom del navegador ajustado al proyector.
- [ ] Guion impreso o en el celular de quien no maneja la compu.

## 4. Banco de preguntas por público

La skill elige las que aplican y les agrega la respuesta con su respaldo (una
pantalla, un número con fuente, un documento).

**Steering (Lab IV)**
- ¿Por qué el SPI da así? ¿Cómo midieron el EV? → skill de gestión
  (`../project-management.md` (skill `g02-valor-ganado-evm`)).
- ¿Qué recortaron y por qué, si van adelantados? → control de cambios del 13/10.
- ¿Qué pasa si no llegan con el planificador al 12/11?
- ¿Cómo saben que la gente usaría esto? → KPIs (`active_users_30d`,
  `platform_managed_rate`).
- ¿Cuál es el riesgo más alto hoy y qué hacen con él?

**Lab II (técnico)**
- ¿Cómo se autentica el usuario? ¿Dónde se guardan las contraseñas? → Auth0, JWT
  validado con JWKS; no hay contraseñas en la base.
- ¿Dónde van las imágenes? → S3 con URLs prefirmadas; el backend no toca los
  bytes.
- ¿Cuánta cobertura de tests tienen? → RNF-03 (≥ 75% en backend); traer el
  número real del último reporte.
- ¿Cómo deployan? → Vercel + Render + Neon, CI en GitHub Actions.

**Demo day / usuarios**
- ¿Es gratis? ¿Hay app?
- ¿Puedo importar mis recetas de Instagram? → fuera de alcance: decirlo sin
  prometer.
- ¿Puedo seguir a otras personas? → fuera de alcance.

**Regla:** si la respuesta es "no está en el alcance", se dice así, con el
porqué, sin prometer "lo estamos pensando".

## 5. Modo ensayo

Cuando la persona pida ensayar, la skill hace de público:

1. **Hace de profesor** (o del público que se elija): escucha el guion o lee lo que
   le pegan, y hace 3–5 preguntas difíciles, una por vez, sin dar las respuestas.
2. **Cronometra**: estima la duración leyendo el guion a ~130 palabras por
   minuto y avisa si se pasa del tiempo.
3. **Devuelve feedback** con esta grilla:

| Criterio | Pregunta |
|---|---|
| Gancho | ¿Los primeros 30 segundos tienen una persona y un problema, no un login? |
| Mensaje | ¿Se puede repetir el mensaje central después de escucharlo una vez? |
| Recorrido | ¿El orden sigue a la persona, o al backlog? |
| Resultado | ¿Cada funcionalidad cierra con qué gana la persona o qué KPI mueve? |
| Jerga | ¿Aparecen "endpoint", "modal", "CRUD" delante de un público no técnico? |
| Verdad | ¿Todo lo que se muestra existe y está en producción? ¿Todo número tiene fuente? |
| Tiempo | ¿Entra en el tiempo, con lugar para preguntas? |
| Plan B | ¿Cada paso riesgoso tiene su recuperación? |

4. **Propone el cambio más importante primero**, no una lista de veinte.
