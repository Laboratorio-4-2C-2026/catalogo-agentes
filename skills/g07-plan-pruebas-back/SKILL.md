---
name: g07-plan-pruebas-back
description: "Arma el plan de pruebas de backend de un ticket para pasárselo al QA como contexto con el que implementar los tests: matriz de casos por criterio con request, datos de partida, esperado (status, código de error, formato de respuesta y persistencia) y controles de borde, más lo que dio una corrida manual sobre base limpia. Usar cuando el QA vaya a automatizar las pruebas de un endpoint y necesite saber qué cubrir y qué esperar."
metadata:
  tipo: skill
  area:
  - qa
  - backend
  fase:
  - testing
  - analisis
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - jira
  grupo: "07"
  autor:
    nombre: Julieta Garberoglio
    github: JulietaG13
  responsables:
  - JulietaG13
  madurez: usado-en-proyecto
  relacionados: []
---

# Plan de pruebas de backend para el QA

El documento que sale de acá **lo usa el QA como contexto** para implementar las pruebas automáticas del endpoint, con la herramienta que use. Tiene que alcanzar para que escriba los tests sin volver a leer el ticket ni adivinar datos: qué casos, con qué request, desde qué estado, y qué se espera exactamente.

La corrida manual sirve para dos cosas: confirmar que el esperado es alcanzable y avisarle al QA qué casos hoy fallan, así no los toma por tests mal escritos.

Documento vivo.

---

## Antes de empezar: datos del proyecto

Usá lo que ya esté en la conversación o en el `CLAUDE.md` / `AGENTS.md` del repo. Lo que falte, pedilo **en un solo mensaje** y no lo adivines.

| Dato | Para qué |
|---|---|
| Sitio de Jira y key del ticket | Traer los criterios |
| Rama y commit a probar | Dejarlo anotado |
| Comando para levantar el entorno y para resetear la base | Corrida sobre base limpia |
| URL base de la API | Armar los requests |
| Cómo se autentica (login que devuelve token, header que se usa) | Casos de autenticación |
| Comando para consultar la base | Verificar persistencia |
| Roles del sistema que importan para el endpoint | Casos de permisos |
| Formato de respuesta común del proyecto, si tiene uno | Criterio transversal |
| Herramienta con la que el QA va a implementar los tests, si se sabe | Ajustar las notas para el QA |
| Carpeta ignorada por git para la entrega | Dejar el markdown |

## 0. Reglas

- **El esperado sale del ticket**, no de lo que hace el código. Si el código hace otra cosa, el caso queda con el esperado del ticket y se marca ❌.
- **No se toca la rama.** Si algo no se puede probar sin cambiar código, va como "no verificable sin cambiar el código", con el motivo.
- **Datos que el QA pueda recrear.** Todo dato de partida se crea por API desde base vacía, y el documento dice cómo. Si un estado solo se alcanza escribiendo en la base (por ejemplo una fecha en el pasado), se aclara, porque el QA va a tener que resolverlo de otra forma en su herramienta.
- **Datos neutros.** `owner@example.com`, `member@example.com`, `other@example.com`, `Test User`.
- **Nunca un 500.** Un input malformado que dé 500 es un caso que falla, aunque el ticket no lo nombre.

## 1. De criterios a casos

Traer el ticket de Jira (`description` y `comment`) y numerar los criterios. Para cada uno, generar los casos así:

| Si el criterio habla de… | Casos mínimos |
|---|---|
| Un campo obligatorio | ausente, `null`, `""`, solo espacios |
| Un largo o rango | justo afuera (falla) **y** justo en el borde (control que pasa), y en el borde con espacios a los lados (para probar que hace trim antes de validar) |
| Un formato (fecha, UUID, enum) | dos o tres formatos inválidos distintos; en fechas, sin offset, solo fecha, con offset distinto de Z |
| Una fecha relativa (futuro/pasado) | en el pasado, en el instante de la petición, en el futuro |
| Autenticación | sin header de auth, token mal formado, token válido |
| Permisos por rol | cada rol que importa, usuario sin acceso, acceso revocado o eliminado lógicamente |
| Un recurso por id | inexistente, eliminado lógicamente, id con formato inválido |
| Algo que no se debe crear o modificar | filas antes y después: "0 filas nuevas" |
| Un campo que el server calcula o fija | mandarlo en el body con otro valor y ver que se ignora |

Si el proyecto tiene un formato de respuesta común, se suma como criterio transversal: **todas** las respuestas lo cumplen, tanto en el éxito como en el error.

Mostrarle la matriz al usuario antes de correrla. Si un criterio es ambiguo, preguntar qué se espera en vez de asumirlo.

## 2. Corrida manual

- Base limpia, con el comando de reset del proyecto.
- Un script por tanda (`g07-check-script`) o `curl` y consultas a la base a mano.
- Anotar el **commit** exacto y la **fecha de la corrida**.
- En el obtenido, copiar el status y el código de error tal cual vienen; en timestamps, el valor completo.

## 3. El documento

```
# <KEY>-NN — Plan de pruebas de backend

`MÉTODO /ruta` · rama `<rama>`, commit `<sha>`.

**Corrida manual:** AAAA-MM-DD, sobre base limpia.
**Resultado:** X de Y criterios cumplen hoy. Fallan el A y el B (ver "Lo que hoy falla").
```

### Datos de partida

Tabla de usuarios con su rol y los recursos que hay que crear, con el request que crea cada uno, en orden. El QA lo usa como setup.

| Usuario | Rol | Cómo se crea |
|---|---|---|
| `owner@example.com` | dueño | registro, después alta del recurso |
| `member@example.com` | miembro | registro + invitación del dueño + aceptación |

### Request base

El request del camino feliz completo (método, ruta, headers, body). Los casos de abajo se describen como cambios sobre este request.

### Casos, por tema

Secciones por tema (por ejemplo: creación y permisos, estado, validación de campos, recursos y contrato transversal). Cada sección es una tabla:

| # | Caso | Esperado | Obtenido hoy | |
|---|---|---|---|---|
| 8 | `title` de 101 caracteres | `400`, `title` / `MAX_LENGTH` | `400`, `title` / `MAX_LENGTH` | ✅ |
| 8 | **Control:** `title` de 100 caracteres | `201` | `201` | ✅ |

- `#` es el número de criterio del ticket. Un criterio puede tener varias filas.
- **Caso** es el cambio sobre el request base, escrito para que se pueda pasar tal cual a un test.
- **Esperado** incluye todo lo que el test tiene que afirmar: status, campo y código de error, campos de la respuesta, y "0 filas nuevas" o el valor persistido cuando el criterio habla de persistencia.
- La última columna lleva ✅, ❌ o ⚠️ (⚠️ cuando status y cuerpo están bien pero falla un detalle, con una nota debajo).

### Para el QA

Una lista corta con lo que no sale de las tablas:

- Casos que requieren forzar un estado (tiempo, borrado lógico) y cómo se llegó en la corrida manual.
- Casos que no conviene automatizar o que dependen de concurrencia.
- Códigos de error que usa el endpoint, con su HTTP.

### Casos fuera de los criterios del ticket

Lo probado para acotar el comportamiento. Se aclara que ninguno es un incumplimiento, y el QA decide si los suma.

### Lo que hoy falla

Un subtítulo por criterio que falla, con la tabla de inputs y la evidencia (fila de la base, cuerpo de respuesta). Sin propuesta de fix: eso va en el comentario de PR. El QA implementa el test con el **esperado**, y queda en rojo hasta que se corrija.

## 4. Entrega

`<carpeta>/<KEY>-NN-pruebas-back.md`, para pasárselo al QA tal cual. Si después hay que comentar la PR, el comentario toma solo las filas ❌.

## Ejemplo de uso

**Pedido:** "Armame el plan de pruebas de backend de PROJ-41, el endpoint de creación de sesión, para pasárselo al QA."
**Resultado:** pide los datos del entorno que falten, muestra la matriz de casos por criterio para aprobar y la corre sobre base limpia con un usuario por rol. Deja el documento con los datos de partida, el request base, cada caso con su esperado, las notas para automatizar y el detalle de lo que hoy falla.
