---
name: g07-sync-prototipo
description: "Mantiene al día el repo de un prototipo navegable con lo que el producto ya tiene en su rama principal: inventaría los commits y tickets de front cerrados desde la última sincronización, compara pantalla por pantalla con Claude in Chrome, arma una tabla de diferencias para aprobar e implementa solo lo aprobado en una rama, sin pushear ni deployar. Usar al cerrar un sprint o después de un merge grande. Pide al inicio los repos, los deploys y la base de datos del prototipo."
metadata:
  tipo: skill
  area:
  - frontend
  - diseno
  - gestion
  fase:
  - mantenimiento
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - jira
  - chrome
  grupo: "07"
  autor:
    nombre: Julieta Garberoglio
    github: JulietaG13
  responsables:
  - JulietaG13
  madurez: usado-en-proyecto
  relacionados: []
---

# Mantener al día el repo del prototipo

Un prototipo navegable que se arma a partir del producto queda atrás cada vez que el producto cierra un ticket de front. Esta skill lo pone al día: **producto → prototipo**.

Documento vivo.

---

## Antes de empezar: datos del proyecto

Usá lo que ya esté en la conversación o en el `CLAUDE.md` / `AGENTS.md` de los repos. Lo que falte, pedilo **en un solo mensaje** y no lo adivines.

| Dato | Para qué |
|---|---|
| Ruta del repo del prototipo | Implementar los cambios |
| URL del deploy del prototipo | Comparar y chequear después del deploy |
| Ruta del repo del producto, su rama principal y la carpeta del front | Ver qué cambió |
| URL del producto deployado, si hay | Comparar en vivo |
| URL del prototipo de diseño, si es distinto del navegable | Saber qué es desvío del producto |
| Dónde guarda datos el prototipo (por ejemplo Supabase) y qué no tiene (por ejemplo storage de archivos) | Saber qué se puede copiar y qué no |
| Sitio de Jira y key del proyecto | Listar los tickets cerrados |
| Desde cuándo sincronizar, si no hay un resumen anterior | Delimitar el rango |
| Carpeta ignorada por git para la entrega | Dejar el resumen |

## 0. Reglas

- **No se pushea ni se deploya.** El deploy y los cambios en la base del prototipo los hace el usuario. Se trabaja en una rama `sync/AAAA-MM-DD` y se entrega el resumen.
- **El prototipo copia al producto, no lo mejora.** Si el producto tiene algo a medio hacer o se aparta del prototipo de diseño, no se "arregla" en el prototipo: va a "Para avisar al equipo".
- **Respetar lo que el prototipo no tiene.** Si no tiene storage, subir un archivo guarda solo los metadatos. No se agrega infraestructura.
- **Sin librerías nuevas** en el prototipo.
- **Datos de ejemplo neutros.** `Test User`, nada copiado de usuarios reales.

## 1. Qué cambió desde la última vez

Partir de la última sincronización: la fecha y el commit de la rama principal del producto que figuran en el último resumen. Si no hay ninguno, usar el dato que dio el usuario.

- `git log --oneline <commit anterior>..<rama principal> -- <carpeta del front>` en el repo del producto.
- En Jira, los tickets pasados a Done en ese período, con su summary y su label.
- Para cada ticket de front: qué pantalla, ruta o componente toca.
- Los tickets solo de back entran únicamente si cambian algo visible: un mensaje de error nuevo, un campo nuevo en un listado, un permiso que esconde un botón.

## 2. Comparar

Para cada pantalla o flujo afectado, mirar el producto y el prototipo con Claude in Chrome. Si no hay producto deployado, levantar el front de la rama principal en local:

- Qué hay: secciones, campos, botones, textos.
- Estados: vacío, cargando, error, sin permisos (cada rol que importe).
- Interacción: qué abre un modal, qué navega, qué pide confirmación.
- Datos: qué lee o escribe, y si el prototipo tiene dónde guardarlo.

Capturas de cada pantalla en las dos versiones, en la carpeta de entrega.

## 3. Tabla de diferencias

| | Pantalla / flujo | Ticket | Producto | Prototipo | Cambio propuesto | Datos |
|---|---|---|---|---|---|---|
| ❌ | … | KEY-NN | … | … | … | nada / tabla nueva / columna nueva |

- Solo las filas que difieren. Lo que ya está igual se resume en una línea arriba.
- Si un cambio necesita tocar el esquema de la base del prototipo, la columna dice qué tabla y qué columnas, y se escribe la migración **sin aplicarla**.
- Lo que en el producto parece un error o se aparta del prototipo de diseño va en una sección aparte, "Para avisar al equipo", y no se copia.

El usuario aprueba fila por fila.

## 4. Implementar lo aprobado

- En la rama `sync/AAAA-MM-DD` del repo del prototipo, un commit por pantalla o flujo, con el ticket en el mensaje.
- Reusar los componentes que el prototipo ya tiene. Del producto se copia el comportamiento, no necesariamente el código.
- Correr el build y el lint del prototipo.
- Recorrer en local las pantallas cambiadas y sacar capturas del después.

## 5. Entrega

`<carpeta>/sync-prototipo-AAAA-MM-DD.md` con:

1. Rango sincronizado: commit anterior y actual de la rama principal del producto.
2. La tabla aprobada, con lo aplicado.
3. Migraciones pendientes de aplicar en la base del prototipo, si hay.
4. "Para avisar al equipo".
5. Lo que quedó afuera y por qué.

Cuando el usuario avise que deployó, chequear en el deploy del prototipo que las pantallas cambiadas se vean igual que en local.

## Ejemplo de uso

**Pedido:** "Terminó el sprint, poné el prototipo al día con lo que hay en main."
**Resultado:** pide los repos, los deploys y la base del prototipo si faltan. Lista los commits de front y los tickets cerrados desde la última sincronización, compara esas pantallas y muestra la tabla de diferencias para aprobar. Implementa lo aprobado en una rama sin pushear y deja el resumen con las migraciones pendientes.
