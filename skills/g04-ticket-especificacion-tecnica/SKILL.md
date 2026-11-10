---
name: g04-ticket-especificacion-tecnica
description: 'Escribe la especificación técnica de un ticket de Linear de PitStop: Datos del ticket, Alcance, Backend, Frontend, Componentes, Criterios de aceptación técnicos y Fuera de alcance, con valores exactos para hacer el trabajo con Claude Code. Usar al redactar o completar la parte técnica de un ticket.'
metadata:
  tipo: skill
  area:
  - gestion
  - backend
  - frontend
  fase:
  - analisis
  - diseno
  tecnologias:
  - nestjs
  - prisma
  - react
  - tailwindcss
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - linear
  grupo: "04"
  autor:
    nombre: Martin Barreiro
    github: martinbarreiroo
  colaboradores:
  - nombre: Tomás Serra
    github: TomasSerra
  responsables:
  - martinbarreiroo
  madurez: usado-en-proyecto
  relacionados: []
---

# Especificación técnica de ticket

Parte de `g04-ticket-orquestador`, que la llama al escribir un ticket de PitStop; también se puede usar sola para mejorar un ticket existente.

## Plantilla

```markdown
# Especificacion tecnica

> De aca para abajo el ticket es tecnico a proposito. Es la referencia precisa para
> hacer el trabajo: leelo con Claude Code al lado.

## Datos del ticket

- Estimado: N SP (~N horas)
- Depende de: PIT-XX

## Alcance

- [Cambio de modelo de datos / migracion]
- [Endpoint o servicio del backend]
- [Pantalla o componente del frontend]

## Backend

- [Modelo de Prisma, endpoints, validaciones, tests de Jest]

## Frontend

- [Ruta, estado, formulario, query de React Query, comportamiento mobile y desktop]

## Componentes

- [De que componente de Base UI parte cada pieza y que hay que adaptarle, con los
  tokens de design-system.md y los valores concretos]

## Criterios de aceptacion tecnicos

- [Criterio con valores exactos: tokens, pixeles, breakpoints, endpoints, lint, tests]
- [...]

## Fuera de alcance

- [Algo que razonablemente podria interpretarse como parte de la tarea y no lo es.]
```
```

Las secciones tecnicas se ajustan a lo que el ticket toca de verdad:

- **Sin UI** (backend puro): la `Referencia visual` va como `no aplica (backend)` y
  `## Frontend` y `## Componentes` se omiten enteras.
- **Infraestructura** (CI, deploy, configuracion): la `Referencia visual` va como
  `no aplica (infraestructura)` y `## Backend`, `## Frontend` y `## Componentes` se
  reemplazan por una sola seccion `## Implementacion` con el detalle tecnico: archivos
  de configuracion, orden de los pasos, comandos, y las trampas conocidas.

Una seccion vacia, o rellena con "no aplica" en cada bullet, es peor que no tenerla.

### La especificacion tecnica

Todo lo que esta abajo del separador se escribe para que el trabajo se pueda hacer sin
volver a preguntar nada. Es donde vive el valor del ticket para un dev junior: nombres
concretos de endpoint, modelo y componente **del MVP**, con sus valores exactos.

- **Datos del ticket**: el estimado en SP con su equivalente en horas, y las
  dependencias vigentes como `Depende de: PIT-XX` (ademas del `blockedBy` de Linear).
- **Alcance**: las piezas que se tocan, una por linea.
- **Backend**: modelo de Prisma, endpoints, validaciones y los tests de Jest, que son
  parte del ticket y de la definicion de terminado.
- **Frontend**: ruta, estado, formulario, queries de React Query y que cambia entre
  mobile y desktop.
- **Componentes**: de que componente de Base UI parte cada pieza de UI y que hay que
  adaptarle, con los valores concretos (hexadecimales, pixeles, breakpoints) y los
  nombres de `design-system.md`. Si algo no existe en Base UI, decirlo explicitamente y
  describir como se comporta.

Las tablas grandes —variantes de un componente, tokens de color, estados— van aca y
estan bien: son la parte que hace que el trabajo salga igual al prototipo. Lo que nunca
hay que hacer es ponerlas antes de que el dev sepa que esta construyendo.

**Ninguna seccion tecnica nombra un archivo del prototipo.** Los `.tsx` y `.css` que
leiste son tu fuente, no la del dev: el ve el prototipo corriendo, no su codigo. Si una
nota necesita apoyarse en algo que viste ahi, se escribe el dato, no el archivo
(`el fondo es #fafafa`, no `los tokens de globals.css`). Los unicos archivos que se
pueden nombrar son los del repo del MVP, que es donde el dev va a escribir.

### Criterios de aceptacion tecnicos

Es la version exacta de "Que tiene que quedar andando", mas todo lo que no se ve.

- Cada criterio o **precisa uno simple** con sus valores, o **cubre algo invisible**:
  codigos de respuesta de la API, reglas de lint, tests que tienen que pasar,
  validaciones del backend, comportamiento del foco.
- No tiene tope de cantidad.
- No es copiar la lista de arriba con mas palabras. Si un criterio tecnico no agrega
  ningun dato nuevo respecto del simple, sobra.
- Rige la misma prohibicion: nada de "funciona correctamente".

El mismo criterio en los dos registros, para ver la diferencia:

| Lista | Como se escribe |
|---|---|
| Que tiene que quedar andando | El boton principal se ve rojo, es comodo de tocar en el celular y se llega a el con la tecla Tab. |
| Criterios de aceptacion tecnicos | Boton primario `bg-primary`, hover `red-700`, `h-12` y `rounded-full`; el foco muestra el ring rojo de 3px al 50% y es alcanzable con Tab. |

## De dónde salen los datos

La `description` que escribio el PM dice **que** tiene que pasar. El **como** lo
escribis vos:

1. Leer la descripcion y el titulo.
2. Abrir todos los archivos listados en `prototype` y ver como esta resuelto ahi:
   campos del formulario, validaciones, estados vacios, reglas de negocio,
   comportamiento responsive.
3. Traducir eso al stack real y escribirlo en el ticket: modelo de Prisma,
   endpoints de Nest, componentes de React, hooks, rutas.

> **Los archivos del prototipo son para vos, no para el ticket.** Los devs no tienen
> el codigo del prototipo: solo lo ven corriendo. Por eso **ningun ticket nombra un
> archivo del prototipo** — ni en la referencia visual, ni en las notas de frontend,
> ni en las de componentes. Lo que viste en el codigo se escribe como valores y
> comportamiento concretos: los colores en hexadecimal, los radios en pixeles, los
> breakpoints, las validaciones, que pasa al tocar cada cosa. Un dev tiene que poder
> hacer el ticket con la pantalla del prototipo abierta al lado y nada mas.
>
> La `Referencia visual` nombra **la pantalla del prototipo funcionando** y como se
> llega a ella (por ejemplo "pantalla de Garage, solapa Informacion"). El PM le
> adjunta la captura al ticket despues, y le conviene hacerlo **como adjunto o como
> comentario del issue, no pegandola adentro de la descripcion**: cualquier edicion
> posterior del cuerpo se la puede llevar puesta, y Linear no permite recuperarla.

> **El prototipo es Next.js; el MVP es Vite + TanStack Router.** El comportamiento se
> copia tal cual, la implementacion se traduce: nada de `next/font`, `next/image` ni
> Server Components. El ruteo si es file-based, porque asi funciona TanStack Router.
> El stack esta fijado en `team.yaml`; si algo parece pedir una dependencia de
> `project.forbidden_dependencies`, replantear el alcance en vez de instalarla.

### Componentes: Base UI primero

Si el componente existe en Base UI, **se parte de ahi** y se lo adapta a los tokens
y al comportamiento del prototipo. Solo se escribe desde cero lo que Base UI no
tiene: la hoja inferior con arrastre, el odometro, el selector de servicios con
iconos y las tarjetas de mantenimiento.

El ticket tiene que nombrar los componentes de Base UI que se usan y decir que hay
que adaptarles (radios, colores de marca, tipografia, tamano de los targets).

Ademas, **por cada componente que el ticket pida crear o modificar hay que decir que
usa**, con los nombres de `design-system.md`: los tokens de fondo y de borde (con su
hover), el color y la variante de `Text` de cada texto de adentro, los iconos de lucide
con su tamano, el radio y la sombra. Un ticket que dice "una tarjeta con el nombre del
vehiculo" esta incompleto; uno que dice "tarjeta `bg-card` con borde `border`,
`rounded-xl`, `shadow-sm` que pasa a `shadow-md` en hover, nombre del vehiculo en
variante `card-title` color `default` y la patente en `caption` color `muted`" esta
completo.

Todo eso vive en la seccion `## Componentes` del bloque tecnico del ticket, nunca
arriba del separador: son valores exactos y arriba del separador no van valores.

Dos reglas de codigo que valen para toda la app y que los criterios de aceptacion
pueden dar por sabidas: **todo texto va dentro de `<Text variant=... color=...>`** y
**todo icono dentro de `<Icon name=... size=... color=...>`**. No se escriben `<p>`,
`<span>` ni headings sueltos, ni se pasan colores o tamanos de texto con clases de
Tailwind. Los dos componentes salen del ticket del design system.

### Web y mobile, siempre

Todo ticket de frontend define el comportamiento en las dos resoluciones, porque
varios componentes cambian de forma:

- Formularios: hoja inferior a pantalla completa en mobile, modal centrado en desktop.
- Navegacion: barra inferior flotante en mobile, sidebar en desktop.
- Listas: una columna en mobile, dos o grilla en desktop.
- La accion principal de un formulario largo queda siempre visible en mobile.

Las dos resoluciones se cubren en las dos listas de criterios, cada una a su manera:
en "Que tiene que quedar andando" con una frase en castellano y sin numeros ("el
formulario abre pegado abajo en el celular y como ventana centrada en la compu"), y en
"Criterios de aceptacion tecnicos" con el breakpoint exacto y lo que cambia a cada lado.

## Ejemplo de uso
**Pedido:** Escribí la especificación técnica del ticket de editar kilometraje.

**Resultado:** El bloque técnico completo con modelo de Prisma, endpoints, tests de Jest, ruta, componentes con tokens del design system, criterios exactos para mobile y desktop y lo que queda fuera de alcance.
