---
name: g04-qa-ui-ux
description: 'Revisa una pantalla corriendo contra el prototipo y el design system de PitStop: tokens, Text e Icon, mobile y desktop, estados vacíos y de error, foco y claridad para usuarios no técnicos. Usar al hacer QA visual o de experiencia de un PR o una pantalla.'
metadata:
  tipo: skill
  area:
  - qa
  - diseno
  fase:
  - testing
  - revision
  tecnologias:
  - react
  - tailwindcss
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: "04"
  autor:
    nombre: Alexander Köttner
    github: Alexander-Kottner
  responsables:
  - Alexander-Kottner
  madurez: experimental
  relacionados: []
---

# QA de UI/UX

Comprueba en la app corriendo que la pantalla se vea y se use como se definió. El código solo se mira para confirmar la causa.

## Fuentes

Ticket de Linear, prototipo corriendo y `project-plan/design-system.md`. Si el ticket y el prototipo se contradicen, manda el ticket.

## Flujo

1. Levantar la app en la rama del PR: pedirle a la persona que corra `/g04-start-stack` o seguir el README.
2. Recorrer cada flujo en dos resoluciones: mobile (375 px) y desktop (1280 px o más). Sacar capturas.
3. Revisar:
   - **Visual:** colores, tipografías, radios y sombras contra los tokens. Sin colores sueltos.
   - **Responsive:** formularios en hoja inferior en mobile y modal en desktop, navegación, listas, acción principal visible.
   - **Estados:** vacío, cargando, error, éxito, deshabilitado y contenido largo.
   - **Interacción:** hover, confirmaciones, volver atrás, recarga de página.
   - **Accesibilidad:** navegación con Tab, foco visible, targets cómodos, labels y contraste.
   - **Claridad:** alguien sin conocimientos técnicos entiende qué hacer y qué pasó, y los errores dicen cómo seguir.
4. Comprobar en el código las reglas que se ven mal: todo texto en `<Text>` y todo icono en `<Icon>`.

## Severidad

- **Must fix:** impide completar el flujo o incumple un criterio del ticket.
- **Should fix:** se aparta del design system o confunde al usuario.
- **Nit:** detalle menor; va aparte.

## Reglas

- Cada hallazgo lleva captura, resolución y pasos para reproducir.
- Reportar, no arreglar. Publicar en el PR solo con autorización.
- Decir qué no se pudo probar.

## Ejemplo de uso
**Pedido:** Hacé QA de UI/UX de la pantalla de historial del PR 57.

**Resultado:** Un reporte por hallazgo con captura, resolución, severidad, resultado esperado y obtenido, más los estados que no se pudieron probar.
