---
name: g12-verificar-historias-completadas
description: Cruza cada historia abierta del roadmap contra el código real de SplitIt (PR mergeada, endpoint y UI en main) para detectar las que ya están completas pero siguen abiertas, y las cierra con evidencia una vez confirmadas. Usar periódicamente, o cuando el estado del roadmap parece desactualizado respecto del repo de aplicación.
owner: '@lucasmonteverdi1'
role: pm
created: '2026-10-05'
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  - codex
  requiere:
  - github
  - linear
  grupo: '12'
  autor:
    nombre: Lucas Monteverdi
    github: lucasmonteverdi1
  responsables:
  - lucasmonteverdi1
  madurez: experimental
  relacionados:
  - g12-orientar-sprint
---

# Verificar historias completadas

El roadmap (`SplitItLab/roadmap`) y el código real (`SplitItLab/SplitIt`) se desalinean solos:
una historia se implementa, su PR se mergea, pero nadie vuelve a cerrar la issue de roadmap que
la describía. Con el tiempo, el roadmap deja de reflejar el estado real del producto, y el PO
termina priorizando sobre un mapa viejo.

Esta skill hace el cruce inverso al de `orientar-sprint`: en vez de partir de qué falta, parte
de **qué historia abierta podría ya estar hecha**, y lo verifica contra el código, no contra
suposiciones.

## Con quién se está hablando

El PM. Le interesa saber qué issues puede cerrar con evidencia, no una lista de código tocado.
Se reporta como una tabla corta de propuestas, nunca como cierres ya hechos sin confirmar.

## Invocación

`/verificar-historias-completadas` revisa todas las historias abiertas del roadmap.

El texto que siga agrega alcance, por ejemplo:

`/verificar-historias-completadas solo las de la épica de eventos`

## Procedimiento

### 1. Actualizar los repos antes de cruzar nada

```bash
git -C SplitIt pull origin main
git -C roadmap pull origin main   # si el roadmap tiene checkout local
```

Un cruce contra un checkout desactualizado da falsos negativos (historias que ya están hechas
pero el código local todavía no las tiene). Si algún repo no está disponible localmente, usar
`gh` contra GitHub directamente y decirlo.

### 2. Traer las historias abiertas

```bash
gh issue list -R SplitItLab/roadmap --state open --json number,title,body,milestone
```

Excluir las `EPICA-*` (son agrupadoras, no se verifican individualmente) y los issues que no
son historias de producto (deuda técnica, QA, infra).

### 3. Por cada historia, buscar evidencia — nunca por tema

Hay una sola regla de entrada, la misma que usa `orientar-sprint` para el cruce SPLT↔SPT: la
relación tiene que estar **declarada**, no inferida. Vale como evidencia:

- el cuerpo de la PR o del ticket de Linear menciona el `SPLT-XXX` explícitamente, o
- el cuerpo de la issue de roadmap linkea el PR o el ticket de Linear que la implementa.

El formato real de las PRs de `SplitIt` es `Solves: [SPT-XXX](link a Linear)` — ese vínculo
identifica el ticket de **Linear**, no la historia de roadmap. Declara el primer salto
(PR → Linear); **no declara el segundo** (Linear → `SPLT-XXX`). Si ninguna de las dos fuentes
de arriba declara ese segundo salto, no hay vínculo verificable todavía — pasar directo al
criterio de abajo, nunca completar el salto adivinando por tema o por similitud de número
(`SPT-20` no es `SPLT-20`).

Sin vínculo declarado, la única entrada válida es la verificación directa contra el código:

1. **Código real en `main`.** Leer los criterios de la historia (`gh issue view <n>`) y buscar
   el endpoint/componente que describen directamente en el repo de aplicación — no una PR de
   tema similar, el código efectivamente mergeado en `main`, no en una branch sin mergear ni
   en el canvas de prototipo. Grep del endpoint esperado (`grep -n "Mapping" EventController.kt`,
   o el archivo de frontend correspondiente).
2. **Criterios de aceptación cumplidos, no solo el feature presente.** Chequear cada criterio
   contra el código: autorización (401/403/404), validaciones, mensajes de confirmación. Una
   historia con el happy path implementado pero sin un criterio de validación no está
   completa — se reporta como parcial, no como lista para cerrar.

Si hay un vínculo declarado (PR cita el `SPLT-XXX`, o la issue de roadmap linkea el PR), ese
vínculo ahorra el paso 1 pero no el 2: los criterios se verifican igual contra el código, el
vínculo no los da por cumplidos solo. Sin vínculo y sin código verificable en `main`, la
historia queda fuera de toda propuesta — nunca se cierra ni se marca por sospecha.

### 4. Reportar — propuesta, nunca cierre automático

Tabla con: historia, evidencia (vínculo declarado o archivo/endpoint que lo confirma), y en
cuál de estos tres cubos cae — decidido acá, no al momento de cerrar:

- **Para cerrar**: evidencia fuerte, todos los criterios verificables cumplidos, y la
  funcionalidad es usable end-to-end tal como la describe la historia.
- **Hechas pero bloqueadas**: el código de esta historia está confirmado en `main` y cumple
  sus propios criterios, pero no es usable end-to-end porque depende de otra historia que
  sigue abierta (por ejemplo: compartir enlace ya implementado, bloqueado porque acceder
  mediante ese enlace todavía no existe). No se propone cerrar — se nombra qué la bloquea.
- **Dudosas**: hay código relacionado pero no se puede confirmar un criterio específico (ej.
  autorización no testeable sin correr la app) — se nombran, no se proponen para cerrar.

Esperar confirmación del PM antes de tocar cualquier issue. Si el PM confirma el cubo de
"para cerrar" (todas o un subconjunto), recién ahí cerrar.

### 5. Ejecutar lo que el paso 4 ya decidió

```bash
gh issue comment <n> -R SplitItLab/roadmap --body "..."
gh issue close <n> -R SplitItLab/roadmap   # solo para "para cerrar"
```

Para **"para cerrar"**: el comentario cita el vínculo declarado o el endpoint/componente real
que la implementa (`PUT /events/{id}` + `updateEvent()` en frontend, PR #NN), no una
descripción vaga de "ya está hecho", y recién después se cierra.

Para **"hechas pero bloqueadas"**: no se cierra. Se comenta el estado real (qué está
implementado y confirmado) y qué otra historia la bloquea — mismo criterio que en el ejemplo de
compartir enlace. Ese comentario es la ejecución de lo que el paso 4 ya clasificó, no un
descubrimiento nuevo en este paso.

## Lo que esta skill no hace

- No cierra nada sin confirmación explícita del PM.
- No infiere una relación SPLT↔SPT, SPLT↔PR, ni asume que `Solves: [SPT-XXX]` cierra el salto
  hasta la historia de roadmap — ese segundo salto exige su propio vínculo declarado, o se
  cae al criterio de código verificado en `main`.
- No mezcla "hecho y usable" con "hecho pero bloqueado por otra historia" — son cubos
  distintos desde el reporte, no algo que se descubre recién al comentar la issue.
- No evalúa historias que ya están cerradas, ni las épicas (`EPICA-*`).
- No reemplaza `orientar-sprint`: esa parte de qué falta y prioriza; esta parte de qué ya está
  hecho y lo confirma.

## Ejemplo de uso

**Pedido:** /verificar-historias-completadas solo las de la épica de eventos

**Resultado:** Devuelve una tabla de historias abiertas clasificadas en "para cerrar", "hechas pero bloqueadas" y "dudosas", con la evidencia en main; solo comenta y cierra issues después de que el PM lo confirma.
