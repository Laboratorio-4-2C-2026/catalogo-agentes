---
name: g14-pantallas-figma-para-tickets
description: Baja pantallas de Figma por MCP a capturas PNG versionadas y a links por frame (con el nombre del archivo en la URL, para que abran el frame) y los deja como «Referencia visual» en cada ticket, cuidando el cupo de llamadas del plan Starter. Usala al preparar tickets de UI que tienen que llegar al dev con su pantalla.
metadata:
  tipo: skill
  area:
  - diseno
  - gestion
  fase:
  - analisis
  - diseno
  tecnologias:
  - figma
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - figma
  grupo: '14'
  autor:
    nombre: Elías Ballesteros
    github: Elias85974
  colaboradores: []
  responsables:
  - Elias85974
  madurez: usado-en-proyecto
  relacionados:
  - g14-redactor-de-tickets-ejecutables
  - g04-imagenes-para-ticket
  - g12-revisar-diseno
  - g03-figma-inspect-design
  - g13-figma-fidelity-review
---

# Pantallas de Figma para tickets

Que cada ticket de UI llegue con su pantalla: una captura que se adjunta y un link que abre **el frame exacto**. En VaiVen las capturas viven en `docs/diseño/capturas/` y los links en la línea «Referencia visual» de cada ticket.

## 0. Antes de la primera llamada

1. **Leé la bitácora de Figma del repo** (en VaiVen, `docs/bitacora/2026-08-02-figma-mcp-limite-plan-starter.md` y las demás de Figma). No investigues los límites en la web ni los infieras de la documentación del MCP: ya se infirió mal una vez.
2. **Corré `whoami`** (no cuenta) y leé `seat` y `tier`. Con asiento View o Collab en Starter, el cupo es de **6 llamadas por mes** y, agotado, se bloquean **todas** las herramientas, escrituras incluidas. Starter limita además a 3 páginas por archivo.
3. **Presupuestá las llamadas** de la tarea y decí el costo antes de gastarlas. Las caras son `get_screenshot`, `get_design_context`, `get_metadata` y `search_design_system`.

## 1. Ubicá los frames sin gastar

- Partí de los links que ya están en el repo (tickets anteriores, kit de UI) para sacar `fileKey` y `node-id`. Un frame nuevo se pide a quien lo dibujó o se lee del navegador.
- Si hay que leer el árbol del archivo, hacelo en **un solo** script de `use_figma` que recorra la página y devuelva nombre e id de cada frame de nivel superior.

## 2. Capturá

- **Dentro del mismo script de `use_figma`**, `await node.screenshot()` devuelve la imagen inline sin llamada aparte: un script por pantalla o por grupo de pantallas, nunca una llamada por frame.
- Si la pantalla nació como maqueta HTML con los tokens del kit, capturala del HTML renderizado y subila a Figma con `generate_figma_design` (no gasta el cupo de Starter). Exige servir el HTML en localhost: si el modo del agente no deja levantar el servidor, pedile a la persona que lo corra.
- Capturá **el frame, no el contenedor**: si una pantalla tiene dos estados, son dos frames y dos referencias.

## 3. Nombrá y guardá

`docs/diseño/capturas/<ticket>-<código de pantalla>-<estado>.png`, en minúsculas y con guiones. Ejemplos reales: `scrum-92-02c-login-sesion-vencida.png`, `scrum-82-06g-vacio.png`, `scrum-143-89-08d-editar-perfil.png` (una captura para dos tickets lleva los dos). Si la captura reemplaza a una vieja, se sobreescribe el archivo: git guarda la anterior.

## 4. El link por frame

```
https://www.figma.com/design/<fileKey>/<nombre-del-archivo-url-encoded>?node-id=<id-con-guion>
```

- **El tramo con el nombre del archivo es obligatorio.** Sin él, Figma abre la página principal y no el frame.
- El `node-id` va con guion (`2615-789`), como lo copia el navegador.

## 5. La línea del ticket

```
**Referencia visual:** Figma, página `<página>`, «<nombre del frame>», <link> . <qué estado muestra>. La pantalla manda en lo visual; los textos son los de esta sección.
```

- Un link por estado, cada uno con su nombre de frame entre comillas.
- Si la maqueta muestra algo que no va (un botón que en ese estado no existe), decilo en la misma línea.
- Nombrá el token o la regla del kit de UI cuando el estado lo necesite («usa el estado atención, porque no es un error»), sin copiar valores.
- Adjuntá la captura al issue al publicarlo y verificá que se vea en Jira.

## Reglas

- La cuenta de Figma es la institucional del equipo; un archivo creado con otra cuenta no es accesible desde ésta y hay que duplicarlo a mano.
- Cambiar de cuenta exige reiniciar el MCP para que `whoami` tome la nueva identidad.
- Los scripts de `use_figma` son atómicos: si uno falla, corregí y reintentá sin limpiar.
- No escribas código de producto a partir del diseño: el ticket describe, el dev implementa.

## Ejemplo de uso

**Pedido:** Sumale a los tickets de la semana 11 la referencia visual de las dos versiones del inicio que están en la página 04 · App.

**Resultado:** Confirma el asiento con `whoami`, captura los dos frames en un solo script, guarda `s11-03-inicio-card-motor-categorias.png` en `docs/diseño/capturas/` y escribe en cada ticket la línea «Referencia visual» con un link por frame que incluye el nombre del archivo.
