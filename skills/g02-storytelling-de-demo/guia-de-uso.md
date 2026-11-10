# Cómo usar la skill de storytelling

Guía para personas. Sirve para preparar la demo de un steering, de Lab II, de un
demo day o del final.

## Qué hace

- Convierte las funcionalidades que querés mostrar en **una historia** con una
  protagonista (Sofi) y un problema real.
- Arma el **guion de demo clic por clic**: qué se hace, qué se dice, quién lo
  dice, qué tiene que verse y qué hacer si algo falla.
- Te da **versiones de 30 s, 2 min y 5 min**, por si el tiempo se achica.
- Prepara las **preguntas probables** del público, con respuesta y respaldo.
- Arma el **plan B** y las **checklists** (ensayo, 30 minutos antes, 2 minutos
  antes).
- **Ensaya con vos**: hace de profesor, te cronometra y te devuelve feedback.

No inventa funcionalidades: si algo no está terminado y en producción, lo cuenta
como "lo que viene".

## Cómo llamarla

En Claude Code, dentro de `zest-support`:

```
/zest-storytelling armame la demo del Steering 3 con colecciones y el planificador
```

En otra herramienta, pegá [`../storytelling.md`](./SKILL.md) y los
archivos de esta carpeta.

## Qué le conviene saber

Si no se lo decís, te lo pregunta (máximo cuatro preguntas):

- Para quién es (steering, Lab II, demo day, final).
- Cuánto dura todo y cuánto la demo.
- Quién presenta y quién maneja la compu.
- Qué cambió desde la última presentación.

## Ejemplos de pedidos

> Armame el paquete de demo del Steering 3: 10 minutos de demo, presentan Ines y
> Santi, mostramos colecciones y el planificador.

> Dame la versión de 2 minutos de la demo, con "hacé lo último primero".

> Escribime la tarjeta funcionalidad → valor de "guardar en colección sin salir
> de la página".

> ¿Qué me van a preguntar en Lab II sobre la subida de imágenes? Dame respuestas
> cortas.

> Te pego mi guion. Hacé de profesor, preguntame 5 cosas difíciles y decime qué
> cambiarías primero.

> Armame las checklists del día del steering.

## Qué tenés que preparar vos

- **Los datos de la demo** cargados en producción, según
  [`personas.md`](./personas.md). La skill te dice cuáles; cargarlos es trabajo
  del equipo.
- **La cuenta de demo**, que no sea la de nadie del equipo.
- **Validar las personas con el PO.** Hoy son una propuesta.

## Mantenerla al día

- Después de cada steering, actualizá "Qué está construido" en
  `../../docs/product.md` (`zest-support/docs/product.md`).
- Si el PO cambia las personas o los datos, actualizá
  [`personas.md`](./personas.md).
- Si en una demo falló algo nuevo, sumalo al mapa de fallas de
  [`demo-kit.md`](./demo-kit.md).
- Si el tribunal hizo una pregunta que no estaba, sumala al banco de preguntas.
