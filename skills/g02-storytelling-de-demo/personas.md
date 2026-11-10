# Personas y datos de la demo

> **Propuesta, no validada.** Las personas salen de los interesados del Project
> Charter (cocineros y planificadores, creadores de contenido) y del problema que
> describe (recetas en 3+ fuentes, siempre los mismos platos). El PO tiene que
> validarlas o corregirlas. Cuando estén validadas, sacá este aviso.

Una buena demo tiene **una** protagonista y la sigue de principio a fin. La
segunda persona aparece solo si la historia la necesita (por ejemplo, para que
Sofi guarde una receta de alguien más).

## Sofía, "Sofi" — la planificadora (protagonista)

| | |
|---|---|
| Quién es | 29 años, trabaja en una oficina, vive con su pareja en CABA |
| Cocina | De lunes a jueves a la noche; el domingo decide qué se come en la semana |
| Dónde tiene las recetas hoy | Capturas de Instagram, un chat de WhatsApp con su mamá, un cuaderno, links sueltos |
| Lo que le pasa | El domingo pierde media hora decidiendo y termina haciendo siempre los mismos 4 platos |
| Lo que quiere | Tener todo en un lugar y que planificar la semana le lleve 5 minutos |
| Frase | "Sé que guardé una receta de pasta buenísima... no sé dónde." |
| Requisitos que la tocan | RF-02, RF-03, RF-04, RF-05, RNF-01 |
| KPI que representa | El 70% que gestiona sus recetas solo en Zest y el 50% que usa el planificador |

## Lucía — la creadora de contenido (secundaria)

| | |
|---|---|
| Quién es | 35 años, cocinera aficionada con una cuenta chica de recetas |
| Lo que le pasa | Publica en redes y las recetas se pierden en el feed |
| Lo que quiere | Que sus recetas estén ordenadas, con ingredientes y pasos claros, y que otros las guarden |
| Frase | "Escribí la receta en un posteo y nadie la encuentra después." |
| Requisitos que la tocan | RF-01 (perfil público), RF-02 |

No usar en la demo a "empresas de alimentos": publicidad y visibilidad paga
están fuera de alcance.

## Datos de la demo

Los datos son un personaje más: tienen que ser realistas, estar cargados **antes**
y ser siempre los mismos, para que el guion no cambie entre ensayos. Las imágenes
están en `../../design/zest/assets/recipes/` (`zest-support/design/zest/assets/recipes`) y
coinciden con el prototipo.

### Cuentas

| Cuenta | Para qué | Regla |
|---|---|---|
| Sofi (demo) | La que presenta la demo | Cuenta creada para la demo, nunca la de alguien del equipo. Sesión iniciada antes de empezar |
| Lucía (demo) | Autora de recetas de la comunidad | Solo para que haya recetas de otra persona en el feed |

Las credenciales no van en este repo ni en el guion: las tiene quien presenta.

### Recetas

Si ya hay un seed de demo cargado en producción (el equipo tiene uno de más de 30
recetas, ZEST-82), **usá esas recetas** y adaptá esta tabla a lo que exista. La
tabla de abajo es el set mínimo que la historia necesita.

| Receta | Autora | Categoría | Dificultad | Tiempo | Imagen |
|---|---|---|---|---|---|
| Ensalada de cítricos y palta | Lucía | Saludable | FACIL | 15 min | `citrus-salad.png` |
| Panqueques de ricota y limón | Lucía | Desayuno | FACIL | 30 min | `pancakes.png` |
| Pasta al limón y ajo | Sofi | Cena | FACIL | 25 min | `pasta.png` |
| Bowl arcoíris | Lucía | Saludable | MEDIA | 40 min | `buddha-bowl.png` |
| Tacos de pescado | Lucía | Cena | MEDIA | 35 min | `tacos.png` |
| Bowl de mango y cítricos | Sofi | Desayuno | FACIL | 10 min | `smoothie.png` |
| Pollo al horno con hierbas | Sofi | Cena | MEDIA | 80 min | `roast-chicken.png` |
| Tarta de limón vegana | Lucía | Postre | DIFICIL | 90 min | `dessert.png` |

Ingredientes con cantidad y unidad del enum (`G`, `TAZA`, `UNIDAD`...) según
`../../docs/db.md` (`zest-support/docs/db.md`). Los pasos se pueden tomar de
`design/uploads/zest-wireframe-design/lib/data.ts`, traducidos.

**Una receta queda sin cargar a propósito**: la que Sofi crea en vivo para
demostrar el RNF-01 (primera receta en menos de 5 minutos). Tené la imagen ya
elegida en el escritorio.

### Colecciones de Sofi

| Colección | Recetas | Para qué en la historia |
|---|---|---|
| Favoritos | Pasta al limón, Pollo al horno | Ya existe: muestra que Sofi usa Zest |
| Desayunos | Panqueques, Bowl de mango | Ya existe |
| Para compartir | (vacía) | Se llena en vivo: guardar desde el feed sin salir de la página |

### Planificador (cuando esté en producción)

La semana de la demo ya planificada de lunes a jueves, con viernes libre para
agregar en vivo. Mezclá recetas propias y de Lucía, para mostrar que se puede
planificar con recetas de la comunidad.

## Cómo se mantiene

- Si el PO cambia las personas, actualizá este archivo y avisá en el guion.
- Si cambia el esquema (`docs/db.md`), revisá que los datos sigan siendo válidos.
- Si se agrega una funcionalidad, agregá los datos que necesita para la demo.
