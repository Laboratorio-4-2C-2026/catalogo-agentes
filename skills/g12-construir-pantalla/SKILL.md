---
name: g12-construir-pantalla
description: Construye en el prototipo la pantalla de una historia que todavia no tiene ninguna, y la enchufa al canvas con su direccion estable. Usar cuando una historia del backlog no aparece en el canvas, cuando hay un frame de Figma que hay que pasar al prototipo, o cuando el PO pide una pantalla nueva.
owner: '@n-mangini'
role: po
created: '2026-09-10'
metadata:
  tipo: skill
  area:
  - diseno
  - frontend
  fase:
  - diseno
  tecnologias:
  - nextjs
  - react
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  - figma
  grupo: '12'
  autor:
    nombre: Nicolas Mangini
    github: n-mangini
  responsables:
  - n-mangini
  madurez: usado-en-proyecto
  relacionados:
  - g12-to-canvas
  - g12-iterar-canvas
  - g12-revisar-diseno
  - g12-orientar-sprint
---

# Construir la pantalla de una historia

## Dónde entra

La metodología tiene un orden. Esta skill cubre el hueco entre la historia escrita y la
pantalla iterable:

1. **Las historias** — se escriben y se publican como issues, con sus criterios.
2. **El prototipo** — se construye la app mockeada entera contra esas historias.
3. **`to-canvas`** — una vez por proyecto: convierte el prototipo en canvas.
4. **`construir-pantalla`** — esta skill. Cuando llega una historia **posterior** al armado
   inicial y no tiene pantalla, o cuando aparece un diseño que el prototipo todavía no tiene.
5. **`iterar-canvas`** — con la pantalla ya en el canvas, cruzar criterios y cerrar huecos.

El paso 2 construye todo de una. Esta skill es para las que llegan después, de a una.

**Precondición:** la historia existe como issue y tiene criterios. Si no los tiene, no se
inventan acá — es trabajo de backlog, y lo decide el PO.

## Con quién se está hablando

El PO. Aplican las mismas reglas de registro que `iterar-canvas`: se reporta **lo que se ve
en pantalla y qué criterio cierra**, nunca qué archivo se tocó. Lo objetivamente roto se
arregla y se avisa; lo opinable se pregunta **de a uno**, con una recomendación.

---

## Procedimiento

### 1. Relevar las convenciones antes de dibujar

**Es el paso que más se saltea y el que más correcciones cuesta.** Una pantalla nueva se
siente terreno libre, y no lo es: el prototipo ya tiene un sistema, y dibujar un botón
propio significa que el PO va a tener que pedir que se parezca al resto.

```bash
cat AGENTS.md                                   # que dice el repo de si mismo
grep -rn "export const" lib/*styles*.ts         # estilos compartidos: mandan
grep -rn ":root" -A40 app/globals.css | head -50 # tokens
ls components/                                   # que ya existe antes de crear
```

Tres preguntas concretas antes de escribir la primera línea:

- ¿Hay un archivo de estilos compartidos que ya define el botón primario y los campos? Si
  existe, **sale de ahí**, aunque el diseño pida otra cosa. Si el diseño y el token no
  coinciden, eso es una decisión del PO, no una excepción que se toma sola.
- ¿El componente que necesito ya existe en `components/`? Si vive en otra pantalla y ahora
  lo usan dos, se extrae.
- ¿La pantalla va dentro del shell de la app o tiene cabecera propia?

Si el `AGENTS.md` del repo contradice lo que el código hace, **gana el código** — y avisar,
porque el archivo quedó viejo y va a hacer tropezar a la próxima sesión.

### 2. Leer los criterios, no la ficha

```bash
gh issue view <n> --repo <owner>/<repo> --json title,body -q '.title + "\n" + .body'
```

Si `gh issue view` falla por Projects clásicos deprecados, usar la API REST:

```bash
gh api repos/<owner>/<repo>/issues/<n> --jq .body
```

La pantalla se construye contra los criterios. El diseño dice **cómo se ve**; los criterios
dicen **qué tiene que poder hacerse**, y suelen incluir estados que ningún frame dibuja.

### 3. Si hay Figma, es insumo — no juez

Un frame es un punto de partida, no la especificación. Dos cosas que pasan siempre:

- **El texto real no rompe donde rompe en Figma.** Las métricas de la fuente difieren; un
  ancho copiado literal deja una palabra colgada. Se ajusta a ojo sobre el navegador, y se
  deja un comentario diciendo por qué ese número no coincide con el diseño.
- **Los assets exportados a veces vienen rotos** (un PNG de 57 bytes es un archivo vacío).
  Verificar tamaño antes de integrarlos; si un asset no aporta nada más que un color de
  fondo, se descarta en vez de arrastrarlo.

**Terminada la pantalla, el Figma deja de ser referencia.** El canvas pasa a ser la fuente de
verdad del diseño, y la iteración es contra la pantalla. Comparar contra el frame después es
otro caso y tiene su propia skill (`revisar-diseno`).

### 4. Elegir la ruta y registrarla primero

Registrar la pantalla en `lib/prototype-map.ts` **antes** de construirla: así nace con su
dirección `/canvas/SPLT-XXX` y no queda huérfana.

- **Nunca `route: '/'`.** La raíz es del canvas; una pantalla ahí se renderiza dentro de sí
  misma. Si el diseño dice que esa pantalla es la home del front real, igual va en un alias
  (`/inicio`) y se aclara con un comentario en el mapa.
- La `epic` sale del backlog, no se inventa.
- Si la historia tiene un estado vacío o alternativo, es otra entrada de la misma historia.

### 5. Construir, con proporción

El prototipo es descartable: el equipo lo reimplementa. El esfuerzo tiene que seguir a
**cuántas decisiones de producto carga** lo que se está haciendo.

| Qué se está haciendo | Cuánto vale invertir |
|---|---|
| un flujo, un estado, una jerarquía de contenido | iterar con el PO hasta que cierre |
| un componente que van a reusar tres pantallas | vale extraerlo bien |
| un fondo decorativo, una ilustración | se mira y se aprueba **a ojo** |

Medir un fondo con diffs de píxeles es trabajo que nadie va a leer y que se tira igual. Si
aparece la tentación de instrumentar algo para validar un adorno, ahí hay que parar.

Mostrar el producto de verdad cuando se pueda: una tarjeta que corre sobre los datos mock
vale más que una ilustración genérica, y no se desactualiza.

Revisar a **390px de ancho** antes que en desktop.

### 6. Dejar descargable el arte propio

El argumento de que el dev "inspecciona y saca los tokens" cubre colores, radios y
tipografía. **No cubre el arte dibujado para el producto**: un fondo, una ilustración. Eso
hay que dárselo.

- Va en `public/<pantalla>/` y se declara en el campo `assets` de la pantalla en el mapa,
  para que la ficha del canvas lo ofrezca para bajar.
- **Un archivo por viewport**, no las capas sueltas. Quince SVG que solo sirven armados no
  son algo que alguien pueda llevarse.
- La pantalla tiene que renderizar **el mismo archivo** que se ofrece descargar. Si el
  componente rearma el arte por su cuenta, lo que el dev baja no es lo que ve.
- **No** se suben iconos (salen del paquete que ya tienen) ni capturas de pantalla.
- El arte se entrega crudo: sin bordes redondeados ni sombras aplicadas al archivo. Eso lo
  resuelve el dev con CSS.

### 7. Verificar

```bash
npx tsc --noEmit
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/<ruta>
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/canvas/SPLT-XXX
```

Y en un navegador real: la pantalla a 390px, y la ficha del canvas mostrándola dentro del
artboard.

### 8. Cerrar

- **La PR** del prototipo nombra la historia como texto. **Nunca `Closes`, `Fixes` ni
  `Resolves`**: el mock no es el incremento, y mergearlo cerraría alcance que nadie
  construyó.
- **La sección `## Diseño` de la issue** apunta a `/canvas/SPLT-XXX`. El link recién sirve
  cuando el deploy levantó — verificarlo antes de darlo por hecho.
- **Auditar la historia contra lo construido.** Casi siempre el diseño se movió mientras se
  construía y los criterios quedaron atrás. Ese cruce es `iterar-canvas <n> --auditar`, y de
  ahí sale si hay que reescribir la issue.
- Si durante la construcción apareció una decisión de producto —dónde vive la pantalla, qué
  pasa con sesión iniciada—, va al decision log. No a la issue.

---

## Lo que esta skill no hace

- **No escribe criterios de aceptación.** Si la historia no los tiene, se avisa y lo resuelve
  el PO antes de construir.
- **No rediseña pantallas que ya existen.** Eso es `iterar-canvas`.
- **No cierra la historia.** La cierra el PO cuando el equipo la implementa en el front real.
- **No toca la metodología del canvas.** Las cuatro invariantes de `to-canvas` siguen
  valiendo; esta skill agrega pantallas dentro de ellas, no las revisa.

## Ejemplo de uso

**Pedido:** La historia 24 de dividir gastos no tiene pantalla en el canvas, construila.

**Resultado:** Construye la pantalla en el prototipo con los estilos y componentes que ya existen, la registra en el canvas con su dirección estable y le reporta al PO qué criterios cubre lo que se ve.
