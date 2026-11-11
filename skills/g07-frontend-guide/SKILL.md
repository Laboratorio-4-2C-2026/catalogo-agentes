---
name: g07-frontend-guide
description: "Guía de reglas para frontends React + TypeScript + Vite con Tailwind de tokens propios, shadcn sobre Radix y axios, salidas de reviews de PR: una sola normalización en formularios, timeout y los tres caminos de error del cliente HTTP, escala de espaciado y tokens de color, overlays de Radix que se comen el Escape, skeletons con la geometría real y atributos en el nodo que recibe el puntero. Usar al implementar un ticket de front y como checklist antes de abrir la PR; si el repo tiene su propia guía, gana la del repo."
metadata:
  tipo: skill
  area:
  - frontend
  fase:
  - desarrollo
  - revision
  tecnologias:
  - react
  - typescript
  - vite
  - tailwindcss
  metodologia:
  - agnostico
  herramientas:
  - claude-code
  requiere: []
  grupo: "07"
  autor:
    nombre: Julieta Garberoglio
    github: JulietaG13
  responsables:
  - JulietaG13
  madurez: usado-en-proyecto
  relacionados: []
---

# Guía de frontend — React + Vite + Tailwind + shadcn/Radix + axios

Reglas que salieron de reviews de PR de un proyecto real. Documento vivo: cuando una review encuentra algo nuevo y general, se agrega.

Pensada para: React + TypeScript + Vite / Tailwind con tokens propios / shadcn sobre Radix / axios.

## Cómo usarla

- **Si el repo tiene su propia guía de frontend, gana la del repo.** Esta se usa como base para lo que la del repo no dice.
- La sección **Convenciones del equipo** son decisiones de estilo de un equipo, no errores: se aplican solo si el repo las adopta. El resto son reglas del stack, que valen siempre.
- Los nombres de archivos, helpers, constantes y tokens que aparecen (`normalizeText`, `countedLength`, `GROUP_CARD_SIZE`, `p-l`…) son ejemplos: se reemplazan por los equivalentes del repo, y si el repo no los tiene, la regla dice qué hace falta.
- Antes de usar los comandos, pedile al usuario lo que no esté en el `CLAUDE.md` / `AGENTS.md` del repo: la carpeta del front, los comandos de lint, typecheck y build, y dónde están definidos los tokens.

---

## Antes de abrir la PR

- [ ] Lint, typecheck y build pasan limpios con los comandos del proyecto (por ejemplo `npm run lint`, `npm run typecheck` y `npm run build`, que suele ser lo que corre el CI).
- [ ] Lo nuevo se recorrió en el navegador, no solo se leyó: el `Escape` que no llega, el `title` tapado y el skeleton invisible no se ven en el código.
- [ ] Cada límite y cada regla de validación coincide con el DTO del backend.
- [ ] Ningún estilo nuevo usa clases crudas de espaciado o color fuera de `components/ui/`.

Si el repo no tiene infraestructura de tests de front y el CI corre lint + typecheck + build, la falta de tests automatizados no se reporta salvo que el ticket los pida.

---

## Convenciones del equipo

Opcionales: se aplican si el repo las adopta.

- Sin punto y coma, comillas simples, 2 espacios de indentación: es lo que hay en todo `src/`. El lint no lo fuerza, pero mezclarlo ensucia el diff.
- Solo exports nombrados, nada de `export default`.
- Un componente por archivo, en PascalCase; helpers y hooks en camelCase (`fieldCounter.ts`, `useGroups.ts`).
- Cada carpeta expone su barril `index.ts` y se importa desde ahí (`../../components`), no del archivo suelto.
- `import type` para lo que solo se usa como tipo.
- Los tipos compartidos viven en `src/types/`: `interface` para objetos, `type` para uniones.
- `components/ui/` lo genera el CLI de shadcn: no se edita a mano. Lo propio del proyecto va en `src/components/`.
- Las clases se componen con `cn()`, no concatenando strings.
- El estado y la validación de un formulario van en un hook `useXForm` y un `validation.ts` al lado de la página; el componente solo pinta.
- Los errores de servicio se tipan (`CreateGroupError` + `CreateGroupFailure`); el error de axios no sale del `services/`.
- Los textos de UI en el idioma de la interfaz, aunque el diseño traiga otro.
- Nada de `any`. Lo que queda intencionalmente sin usar lleva `_` adelante, que es lo que el lint ignora.

---

## Formularios

- Validación, payload y contador miden lo mismo. Tiene que haber una sola función de normalización compartida (por ejemplo `normalizeText`) y el contador tiene que pasar por ella (por ejemplo con un `countedLength`); si el contador mide el valor crudo, un campo válido se pinta `502/500` en rojo con `aria-invalid` y se envía igual.
- Las reglas del cliente son espejo exacto del DTO del backend: longitudes, patrón de password, formato de email.

---

## Llamadas a la API

- Toda llamada tiene `timeout`, configurado una vez en el cliente HTTP del proyecto (por ejemplo `10_000`). El default de axios es `timeout: 0`, sin límite: un servidor que acepta la conexión y no responde deja el spinner girando para siempre.
- El manejo de error cubre tres caminos: timeout (`ECONNABORTED`, sin `response`), error de red (sin `response`) y 5xx. Los tres terminan en el mensaje general y bajan `isSubmitting`.
- Los errores por campo se leen de `errors[]`, un mensaje por campo, colapsando los repetidos, inline y sin perder los valores cargados.
- Las variables de entorno nuevas llevan default. Sin `.env.local`, `VITE_API_URL` queda `undefined` y las peticiones pegan contra el propio dev server: el error real no aparece en ningún lado.

---

## Estilos y tokens

- Fuera de `components/ui/` no se usan clases crudas de espaciado: se usa la escala de tokens del proyecto. Por ejemplo, definida en `index.css` como `s` 8px, `m` 16px, `l` 24px, `xl` 32px → `p-l`, `gap-m`, `p-xl`.
- A los componentes de shadcn se les pasa el espaciado del proyecto: vienen con `p-4`/`gap-4` propios.
- Los overrides negativos se ajustan junto con el padding: `DialogFooter` trae `-mx-4 -mb-4` fijos y, con el contenido en `p-l`, la barra queda 8px corta de cada lado.
- Antes de elegir un color, mirar a qué apunta el token. Si `--muted` y `--background` apuntan los dos al mismo color, un bloque `bg-muted` sobre el `<main>` es contraste 1.00:1, y `animate-pulse` no lo revela porque el origen y el destino son el mismo color. Para superficies que tienen que distinguirse del fondo, usar un token que de verdad contraste con él.
- El contraste se verifica contra el tema que de verdad se aplica: si la clase `dark` no se usa en ningún punto de `src/`, no sirve verificarlo contra los valores de `.dark`.

---

## shadcn / Radix

- Ningún overlay descartable se monta encima de un sheet o un dialog: intercepta el `Escape` y lo consume. `SidebarMenuButton` monta el `Tooltip` siempre que recibe la prop y solo lo esconde con `hidden`, así que la decisión se toma en el consumidor.

  ```tsx
  const { isMobile } = useSidebar()
  const tooltipFor = (text: string) => (isMobile ? undefined : text)
  ```

- Todo overlay nuevo se prueba con `Escape` y con clic afuera: son dos caminos distintos.
- No escribir estado que nadie lee. O se lee (`defaultOpen={document.cookie.includes('sidebar_state=true')}`) o no se guarda: si no, aparenta una persistencia que no existe.

---

## Skeletons

- El skeleton ocupa exactamente lo mismo que el contenido real. Se consigue repitiendo los bloques dentro de los contenedores reales (`SidebarMenu` + `SidebarMenuItem`, el mismo grid), donde vive la geometría, en vez de reconstruirla a ojo con `flex gap-1 px-2`.
- El tamaño se comparte por constante, no se repite en los dos lados: por ejemplo un `GROUP_CARD_SIZE` que usan la card y su skeleton.
- El bloque tiene que verse: contraste contra la superficie donde efectivamente se monta (ver *Estilos y tokens*).
- El contenedor lleva `role="status"`, `aria-busy` y `aria-label`.

---

## Accesibilidad y puntero

- El atributo va en el nodo que recibe el evento. Un `title` en un `h2` cubierto por un `<Link>` `absolute inset-0` no se muestra nunca; se verifica con:

  ```js
  const r = el.getBoundingClientRect()
  document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2)
  ```

- `title` y `aria-label` no se reemplazan entre sí: el `aria-label` del enlace no le da tooltip al mouse. Si el criterio pide que el texto completo quede disponible, van los dos.
- El orden de tabulación y el `Escape` se prueban aparte del clic.

---

## Estructura y dependencias

- Una carpeta por página, con el componente en `index.tsx` y al lado lo propio de esa pantalla (`validation.ts`, subcomponentes). El barril `pages/index.ts` resuelve igual.
- Lo que no corre en runtime va en `devDependencies`. El CLI de `shadcn` se usa al generar componentes y al compilar: en `dependencies` se arrastra a cualquier instalación con `--omit=dev`.

## Ejemplo de uso

**Pedido:** "Pasá la guía de front sobre mi rama del modal de invitaciones antes de abrir la PR."
**Resultado:** recorre el checklist y las reglas contra el diff, y marca lo que no cumple con archivo, línea y el cambio que lo resuelve. Por ejemplo, un tooltip que se come el `Escape` del sheet, un skeleton sin contraste con el fondo o un contador que mide el valor sin normalizar.
