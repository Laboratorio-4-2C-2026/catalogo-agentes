---
name: g10-a11y-component-reviewer
description: Revisar componentes React contra un checklist básico de accesibilidad (labels, roles, contraste, navegación por teclado). Usar al crear o modificar un componente en `frontend/src/components` o una página en `frontend/src/pages`.
metadata:
  tipo: skill
  area:
  - frontend
  - diseno
  fase:
  - revision
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
  - g10-empty-loading-error-states-checker
  - g10-design-consistency-auditor
  - g11-revisar-diseno
---
# A11y Component Reviewer

Revisar un componente o página del frontend de Conexia (React + Vite + TypeScript, cada componente en su propia carpeta con `index.tsx` + `index.css`) contra un checklist de accesibilidad concreto, no genérico.

## Checklist

1. **Inputs y formularios** (`textfield`, `timefield`, `dayselector`, `numberstepper`, páginas `login`, `register`, `questionnaire`): todo input tiene `label` asociado (por `htmlFor`/`id` o `aria-label`), y los mensajes de error se anuncian (`aria-describedby` o `role="alert"`), no solo color rojo.
2. **Botones e interactivos** (`button`, `toggleswitch`, `navbar`): elementos clicables son `<button>` o tienen `role="button"` + `tabIndex` + manejo de `onKeyDown` si son `<div>`. Ningún control depende solo de `onClick` sin equivalente de teclado.
3. **Imágenes y iconos** (`assets/icons`, `logo`, `ConexiaLoader`): toda `<img>` o ícono decorativo tiene `alt=""` (si es decorativo) o `alt` descriptivo (si transmite información).
4. **Estados dinámicos** (`progressbar`, `ConexiaLoader`, `emptytripsstate`): loaders y estados vacíos usan `role="status"` o `aria-live` para que lectores de pantalla los anuncien, no solo texto visual.
5. **Contraste**: si el componente define colores propios en su `index.css`, estimar si el contraste texto/fondo cumple un mínimo razonable (evitar gris claro sobre blanco para texto principal).
6. **Diálogos** (`deletescheduledialog`, `editscheduledialog`): el modal atrapa el foco, se puede cerrar con `Escape`, y al cerrarse el foco vuelve al elemento que lo abrió.

## Salida esperada

Lista por componente: `componente` | `problema` | `impacto` | `fix sugerido` (código concreto, ej. agregar `aria-label="Cerrar"` al botón de cerrar). No editar el código salvo pedido explícito.

## Ejemplo de uso

**Pedido:** Revisá el componente `editscheduledialog` y la página `questionnaire` por accesibilidad antes de mergear.
**Resultado:** Lista de problemas concretos (ej. input sin label, modal sin manejo de Escape) con el fix sugerido para cada uno.
