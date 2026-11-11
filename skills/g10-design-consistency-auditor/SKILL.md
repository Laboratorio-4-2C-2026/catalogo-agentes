---
name: g10-design-consistency-auditor
description: Revisar que los componentes y páginas del frontend usen los tokens de color y tipografía definidos en `frontend/src/index.css` en vez de valores sueltos, y detectar valores repetidos que deberían ser token. Usar antes de una revisión visual o al agregar un componente nuevo.
metadata:
  tipo: skill
  area:
  - diseno
  - frontend
  fase:
  - revision
  - diseno
  tecnologias:
  - react
  - typescript
  metodologia:
  - agnostico
  herramientas:
  - claude-code
  requiere: []
  grupo: "10"
  autor:
    nombre: Victoria Martin Botter
    github: vmartinbotter
  responsables:
  - vmartinbotter
  madurez: experimental
  relacionados:
  - g10-a11y-component-reviewer
  - g11-revisar-diseno
  - g11-alternativas-pantalla
---
# Design Consistency Auditor

El frontend de Conexia define sus tokens de diseño en `frontend/src/index.css`: paleta de color (`--color-primary-100` a `900`, `--color-grey-*`, `--color-error-*`, `--color-success-*`, colores semánticos por feature como `--color-badge-*`, `--color-day-*`, `--color-subject-*`) y escala tipográfica (`--fs-*`, `--fw-*`, `--lh-*`, `--ls-*`, más las clases utilitarias `.text-h1` a `.text-body-3`). Esta skill revisa que los `index.css` de `frontend/src/components/*/` y `frontend/src/pages/*/` usen esos tokens en vez de reinventarlos.

## Qué revisar

1. Leer primero `frontend/src/index.css` completo para tener la lista real de tokens vigentes (no asumir que la lista de este archivo está actualizada: los tokens nuevos se agregan seguido).
2. Recorrer los `index.css` de componentes y páginas, buscando colores en `#hex` o `rgb(...)` escritos directo en vez de `var(--color-...)`.
3. Para cada color hardcodeado encontrado:
   - Si coincide o es casi idéntico a un token ya existente (ej. `#5d93c8` en vez de `var(--color-primary-500)`), marcarlo como "debería usar el token X".
   - Si no coincide con ningún token pero se repite igual en dos o más componentes, marcarlo como "candidato a token nuevo" en vez de pedir que se unifique a uno existente que no corresponde.
4. Revisar tipografía: `font-size`, `font-weight` o `line-height` puestos a mano en vez de usar las variables `--fs-*`/`--fw-*`/`--lh-*` o las clases `.text-*` ya definidas en `index.css`.
5. Revisar que los componentes de feedback por estado (`progressbar`, `toggleswitch`, `selectablecard`, badges de `questionnaire`) usen los tokens semánticos correspondientes (`--color-success-*`, `--color-error-*`, `--color-badge-*`) en vez de un color suelto para el mismo significado.
6. No proponer tokens nuevos de más: solo cuando un valor se repite sin corresponder a ninguno existente.

## Salida esperada

Tabla: `archivo` | `valor encontrado` | `problema` | `token a usar o token nuevo sugerido`. No editar los CSS: solo reportar, salvo pedido explícito.

## Ejemplo de uso

**Pedido:** Fijate si los componentes nuevos de notificaciones y chat están usando los tokens de color que ya tenemos, o metieron valores sueltos.
**Resultado:** Tabla con los colores o tamaños de fuente hardcodeados en esos componentes, y el token de `index.css` que deberían usar en su lugar.
