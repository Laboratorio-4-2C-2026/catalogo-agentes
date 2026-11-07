---
name: g04-desarrollo-ui-ux
description: Construye pantallas y componentes de PitStop a partir del design system y Base UI, resueltos para mobile y desktop y con todos sus estados. Usar al implementar o rediseñar interfaz; las convenciones de código generales están en la skill de frontend.
metadata:
  tipo: skill
  area:
  - frontend
  - diseno
  fase:
  - diseno
  - desarrollo
  tecnologias:
  - react
  - tailwindcss
  - typescript
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: "04"
  autor:
    nombre: Tomás Serra
    github: TomasSerra
  responsables:
  - TomasSerra
  madurez: experimental
  relacionados: []
---

# Desarrollo de UI/UX

Lleva una pantalla del ticket a código sin inventar estilos. Para estructura, ruteo y estado del proyecto, seguir `g04-frontend-vite-react-typescript`.

## Antes de escribir

1. Leer el ticket, ver la pantalla del prototipo corriendo y leer `design-system.md`.
2. Buscar en `apps/web/src/components` si ya existe el componente o uno parecido. Si existe, se usa o se extiende.

## Flujo

1. **Definir el comportamiento** en mobile y desktop: qué cambia de forma, qué queda siempre visible.
2. **Elegir la base:** primitivo de `@base-ui/react` si existe, adaptado a la identidad de PitStop. Desde cero solo lo que Base UI no trae.
3. **Usar el sistema:** tokens de color, `<Text variant color>` para todo texto, `<Icon name size color>` para todo icono. Nada de colores ni tamaños sueltos con Tailwind.
4. **Resolver todos los estados:** vacío, cargando, error, éxito, deshabilitado y texto largo.
5. **Cuidar la experiencia:** flujos cortos para usuarios no técnicos, textos en español claro, errores que dicen cómo seguir, confirmación antes de una acción destructiva.
6. **Cuidar la accesibilidad:** labels, foco visible, navegación con teclado, targets cómodos para el dedo.
7. **Probar en el navegador** en las dos resoluciones y correr lint y typecheck. Para una revisión independiente, usar `g04-qa-ui-ux`.

## Reglas

- No agregar librerías de componentes. Revisar `forbidden_dependencies` en `team.yaml`.
- No inventar decisiones de producto: si la pantalla no define algo, preguntar.
- No dar por terminada una pantalla que solo compila.

## Ejemplo de uso
**Pedido:** Hacé la pantalla de lista de deseos siguiendo el prototipo.

**Resultado:** Implementa la pantalla con componentes y tokens existentes, en sus dos resoluciones y con estados vacío, de carga y de error, y la prueba en el navegador.
