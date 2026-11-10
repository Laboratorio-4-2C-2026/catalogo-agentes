# Cómo usar la skill del deck

Guía para personas. Sirve para armar el deck de un steering (o cualquier
presentación de Zest) y para presentarlo.

## Qué hace

- Arma el deck como una **app web**, no como un .pptx: animaciones de React Bits
  con los colores de Zest, gráficos que se dibujan solos y números que cuentan
  hacia arriba.
- Primero te propone **los títulos de todas las slides** para que apruebes la
  historia, y después **tres estilos visuales** para que elijas.
- Revisa sola que nada se salga de la pantalla y que no quede ningún dato de
  ejemplo, y te muestra capturas.
- Te deja una **vista de presentador** (notas, reloj, slide siguiente) y un
  **PDF de respaldo**.

## Cómo llamarla

En Claude Code, dentro de `zest-support`:

```
/zest-steering-deck armame el deck del Steering 3
```

Si antes armaste la demo con `/zest-storytelling`, la skill lee ese guion
(`decks/<evento>/demo.md`) y usa sus notas.

## Ejemplos de pedidos

> Armame el deck del Steering 3 partiendo del Steering 2: mismas secciones,
> números nuevos.

> Pasame el Steering 2 de Google Slides a este formato.

> Mostrame tres estilos para la portada y la slide de valor ganado.

> Agregá una slide de cambio de alcance: volvieron el stepper y la acción
> rápida.

> La curva S tiene datos de ejemplo: cargá los de la planilla.

## Presentar

Desde la carpeta del deck (`decks/<evento>/`):

```bash
npm install
```

```bash
npm run dev
```

| Tecla | Qué hace |
|---|---|
| → / espacio / clic | Siguiente |
| ← | Anterior |
| Inicio / Fin | Primera / última |
| `F` | Pantalla completa |
| `P` | Abre la **vista de presentador** en otra ventana (notas, reloj, siguiente). Las dos ventanas se mueven juntas |
| `N` | Muestra las notas sobre la slide (para ensayar) |
| `R` (en la vista de presentador) | Reinicia el reloj |

En el aula: la ventana del deck va al proyector en pantalla completa, y la vista
de presentador queda en la notebook.

Antes del steering:

```bash
npm run check
```

```bash
npm run pdf
```

`check` tiene que terminar sin problemas, y el `deck.pdf` va al pendrive o al
celular por si falla la compu.

## Qué tenés que preparar vos

- Los números de la planilla (o pedile a `/zest-project-management` que los
  calcule).
- Las fotos del equipo, si van en la slide de roles.
- Nada de React Bits Pro: el equipo no tiene licencia, se usan los gratuitos.
