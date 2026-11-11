---
name: g10-design-consistency-auditor
description: Comparar colores, espaciados y tipografía entre los `index.css` de distintos componentes para detectar inconsistencias visuales, dado que el proyecto no tiene un archivo central de tokens de diseño. Usar antes de una revisión visual o al agregar un componente nuevo.
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

El frontend de Conexia no tiene un archivo central de variables CSS: cada componente define sus propios colores y medidas en su `index.css` (`frontend/src/components/*/index.css`). Esta skill detecta cuándo esa falta de tokens genera inconsistencia visual real, no solo "podría haber un token".

## Qué revisar

1. Recorrer los `index.css` de `frontend/src/components/**` y `frontend/src/pages/**`, extrayendo valores de color (`#hex`, `rgb(...)`), `border-radius`, `padding`/`margin` y `font-size`.
2. Agrupar colores por similitud (ej. varios azules casi iguales pero no idénticos: `#2e55c8` vs `#2d54c7`) y señalar los que deberían ser el mismo valor pero no lo son.
3. Señalar `border-radius` o `font-size` que se repiten con pequeñas variaciones sin motivo aparente entre componentes del mismo tipo (ej. todos los botones deberían compartir el mismo radio).
4. Verificar que los componentes de feedback (`progressbar`, `toggleswitch`, `selectablecard`) usen una paleta coherente para estados "activo"/"inactivo"/"error" entre sí.
5. No proponer un sistema de tokens completo salvo que el usuario lo pida: el objetivo es encontrar inconsistencias puntuales, accionables en el componente afectado.

## Salida esperada

Tabla: `componentes afectados` | `propiedad` | `valores encontrados` | `inconsistencia` | `valor sugerido para unificar`. No editar los CSS: solo reportar, salvo pedido explícito.

## Ejemplo de uso

**Pedido:** Fijate si los colores de los botones y las cards son consistentes entre sí en el frontend.
**Resultado:** Tabla con los componentes cuyo azul, radio o padding difiere ligeramente del resto, y el valor sugerido para unificarlos.
