---
name: g07-check-script
description: "Convierte una tanda de escenarios de un ticket en una verificación que se vuelve a correr igual: script de bash con curl y consultas a la base para el backend, y guion para Claude in Chrome para el frontend, con estados forzados (errores, demoras, respuestas fuera de contrato) y salida ordenada por escenario. Usar cuando una review o un plan de pruebas necesite repros repetibles. Pide al inicio la URL de la API, la del front y cómo acceder a la base."
metadata:
  tipo: skill
  area:
  - qa
  - backend
  - frontend
  fase:
  - testing
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
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

# Verificaciones repetibles por ticket

Cada tanda de escenarios de una review se convierte en algo que se vuelve a correr igual: en la re-review del fix, en otra máquina o en la corrida final sobre base limpia. No son tests del proyecto: viven en una carpeta ignorada por git y no tocan la rama.

Documento vivo.

---

## Antes de empezar: datos del proyecto

Usá lo que ya esté en la conversación o en el `CLAUDE.md` / `AGENTS.md` del repo. Lo que falte, pedilo **en un solo mensaje** y no lo adivines.

| Dato | Para qué |
|---|---|
| Ticket y escenarios a cubrir | Saber qué verificar |
| URL base de la API y endpoint de health | Requests y espera del arranque |
| Cómo se autentica (login, header) | Sacar tokens por usuario |
| Comando para consultar la base | Verificar persistencia |
| Comando para levantar el entorno y para resetear la base | Correr sobre base limpia |
| URL local del front | Guion de UI |
| Carpeta ignorada por git donde guardar scripts y capturas | No ensuciar la rama |

Si en esa carpeta ya hay scripts de tandas anteriores, leerlos y reusar sus funciones comunes en vez de reescribirlas.

## 0. Reglas

- **Una verificación por tanda**, no una por escenario ni una por ticket entero.
- Nombre: `<carpeta>/checks/<key>-<tema>.sh` (back) o `<key>-<tema>.md` (guion de front).
- **No se toca la rama.** Ni código, ni configs, ni el `.env`.
- **Datos neutros** con nombres que digan el rol: `owner@`, `creator@`, `outsider@example.com`.

## 1. Encabezado

Siempre arranca con un comentario que dice el ticket, qué cubre y cómo se corre:

```bash
#!/usr/bin/env bash
# PROJ-43: escenarios 1 a 9 de DELETE /sessions/{id}, sobre base limpia.
#   bash <carpeta>/checks/proj43-cancel.sh
```

## 2. Backend: bash, curl y la base

- Un bloque de variables al principio (URL de la API, comando de la base) y funciones chicas: `register`, `token <email>`, `wait_for_health`. Si ya existen de una tanda anterior, se importan con `source`.
- Las relaciones entre usuarios (membresías, invitaciones) se arman por el flujo real de la API, no insertando filas.
- La base es para **leer**. Solo se escribe para forzar un estado que depende del tiempo (por ejemplo una fecha de inicio en el pasado), en una función con nombre claro (`mk_session_past`) y un comentario que lo diga. **Un estado al que solo se llega escribiendo en la base no es hallazgo.**
- Textos con acentos o caracteres especiales: armar el body en un archivo UTF-8 y mandarlo con `--data-binary @archivo.json`. Inline, algunas terminales los mandan en otra codificación y el back responde 400.
- Parsear el JSON con lo que haya instalado (`jq` o `node -e`). Si no hay ninguno, preguntar antes de instalar algo.

## 3. Frontend: guion para Claude in Chrome

El front se verifica con Claude in Chrome. Lo que se escribe es un **guion** que se vuelve a ejecutar paso por paso:

```markdown
## Escenario 4 — vuelve al Grupo A como MEMBER
1. Login como `user@example.com`.
2. Desde el sidebar, abrir Grupo D y después volver a Grupo A (sin recargar).
3. Leer los botones del encabezado.
Esperado: Invitar, Salir del grupo.
```

- **Estados que el back no produce a pedido** (500, red caída, respuesta lenta, cuerpo fuera de contrato): forzarlos desde la página, con la herramienta de JavaScript del navegador, envolviendo `fetch` o `XMLHttpRequest` para la ruta y el método del escenario. Si el front usa un cliente HTTP propio, se intercepta igual, porque por debajo usa uno de los dos. El override se instala después de cargar la página y se dice en el paso.
- **Navegación sin recarga** cuando el escenario habla de cambiar de ruta: clic en el link del sidebar, no escribir la URL.
- **Contar pedidos filtrando por método**: los preflight `OPTIONS` también aparecen en la red.
- **Capturas** de cada estado que se mira, guardadas como `<key>-<qué-muestra>.png` en la carpeta de capturas.
- Si un escenario depende de algo que Claude in Chrome no puede hacer en esa sesión, el guion lo dice y el escenario queda "no verificado".

## 4. Salida

El script y el guion se ordenan por escenario, en el orden del ticket:

```
### E4 vuelve a Grupo A (MEMBER): acciones
["Invitar", "Salir del grupo"]
```

- El título dice el número de escenario y qué se mira, para que la salida se pueda pasar directo a la tabla esperado/obtenido.
- Se registra el **dato**, no un veredicto: ✅ o ❌ lo decide quien revisa, contra el ticket.
- Incluir el **control** (la variante que tiene que funcionar) como un escenario más.
- En el front, anotar al final los errores de consola, si hubo.

## 5. Antes de darla por terminada

- Correrla dos veces seguidas sobre base limpia: tiene que dar lo mismo.
- Que no dependa de ids de una corrida anterior. Los ids se crean en el script o se reciben por argumento.
- En el back, que el script corte con error si un paso de setup falla (`set -euo pipefail`), en vez de seguir con datos a medias.

## Ejemplo de uso

**Pedido:** "Pasame a verificación los escenarios 1 a 9 de PROJ-51, el botón de eliminar grupo, con el DELETE fallando de las distintas formas que pide el ticket."
**Resultado:** escribe el script de setup que crea los usuarios y grupos por API y el guion para Claude in Chrome. Por cada escenario, el guion fuerza la respuesta del DELETE (500, red caída, demora) envolviendo `fetch` y registra las acciones visibles, el diálogo, los avisos y el sidebar, con capturas.
