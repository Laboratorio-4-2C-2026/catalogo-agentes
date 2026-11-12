---
name: g16-eureka-revisor-ux
description: 'Agente de GitHub Actions que revisa los PRs que tocan pantallas de Eureka y comenta en línea, con severidad, lo que el usuario ve: acciones sin feedback durante un minteo, errores que no dicen qué hacer, jerga técnica sin explicar y accesibilidad verificable en el código. Propone el texto exacto en voseo. Usar en apps donde cada paso puede tardar o fallar.'
metadata:
  tipo: agente
  area:
  - frontend
  - diseno
  fase:
  - revision
  tecnologias:
  - react
  - nextjs
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: "16"
  autor:
    nombre: Valentino Gianuzzo
    github: ValentinoGianuzzo
  responsables:
  - ValentinoGianuzzo
  madurez: experimental
  relacionados:
  - g16-ux-review
  - g01-screen-state-ux-reviewer
  - g07-auditoria-accesibilidad
---
# eureka-ux

Agente del proyecto Eureka (Laboratorio IV, grupo 16). En el repo de Eureka se llama `eureka-ux`. Los archivos de esta carpeta (`.github/workflows/eureka-ux.yml`) están copiados sin cambios y van en las mismas rutas del repo donde se instale.

**Estado:** ya está en `master` de Eureka, pero todavía no se abrió ningún PR que lo despierte, así que no corrió en el proyecto.

## Para qué existe

Extraído sin cambios del comentario que abre el workflow:

```text
Agente de propósito específico: lo que el usuario lee y ve.

Los revisores que ya tenemos miran que la autoría no se pueda robar, que el
documento no se filtre y que el saldo de créditos no quede mal. Ninguno mira
la pantalla. Y en Eureka la pantalla importa más de lo que parece: registrar
cifra, sube a Arweave y escribe en la cadena, cada paso puede tardar o fallar,
y un usuario que ve "bytes32", un botón congelado o un error que no dice qué
hacer abandona el registro a la mitad, a veces con el crédito ya reservado.

Revisa tres cosas: jerga técnica en los textos, estados de carga, error y
vacío, y accesibilidad básica verificable desde el código. Respalda los
criterios de aceptación de EP-61 y evita que se vuelva atrás después.
```

## Cómo corre

- **Se dispara:** cada PR (opened, ready_for_review, reopened) que toque pantallas: `app/` sin `app/api/`, y `visual_pages/`.
- **Herramientas del agente:** Read,Grep,Glob,Bash(git diff:*),Bash(git log:*),Bash(git show:*),mcp__github_inline_comment__create_inline_comment, con un tope de 40 turnos.
- **Necesita:**
  - El secreto `CLAUDE_CODE_OAUTH_TOKEN` en el repo.
  - La skill `.github/skills/ux-review/SKILL.md` (en este catálogo: `g16-ux-review`).
  - `.github/copilot-instructions.md`: el contexto del producto. No se incluye porque es propio del proyecto.

## Prompt

Extraído sin cambios del paso de `anthropics/claude-code-action` en `.github/workflows/eureka-ux.yml`.

```text
Revisá este pull request como revisor de experiencia de usuario del
proyecto Eureka.

Tu alcance es lo que el usuario lee y ve: los textos de la
interfaz, los estados de carga, éxito, error y vacío de cada acción,
y la accesibilidad básica que se puede verificar en el código.

Fuera de tu alcance: seguridad, cifrado y claves
(eureka-confidentiality), créditos (eureka-credits), contratos
(eureka-authorship) y el gusto visual. Si el diff no toca nada que
vea el usuario, decilo en un comentario y terminá.

Leé y aplicá:
- .github/copilot-instructions.md — contexto del producto
- .github/skills/ux-review/SKILL.md — tu checklist, con el orden de
  prioridad y qué severidad corresponde a cada cosa

Para juzgar si un texto o un estado es consistente, mirá las
pantallas que ya existen en `visual_pages/` y `app/` aunque no estén
en el diff.

Reglas de salida:
- Un comentario por hallazgo, anclado a la línea exacta.
- Prefijá cada uno con [Crítico], [Alto], [Medio] o [Bajo].
- Contá qué ve el usuario y por qué le molesta, y proponé el texto
  exacto o el cambio concreto.
- Si es una sospecha y no un hallazgo confirmado, decilo.
- No comentes estilo de código ni naming.
```

## Ejemplo de uso

**Pedido:** Se abre un PR que muestra «Transaction reverted: bytes32 mismatch» cuando falla el registro.

**Resultado:** El check **Eureka UX** comenta en esa línea, por ejemplo con `[Alto]`, qué ve el usuario y por qué no sabe qué hacer, y propone el texto exacto, en voseo, que explica qué pasó y si puede reintentar.
