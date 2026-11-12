---
name: g07-documentar-producto
description: "Arma y mantiene la documentación de producto de Study Arena en docs/producto/ (qué es, funcionalidades por épica con su estado real, flujos de usuario, reglas visibles para el usuario y un glosario del dominio) cruzando el código React y Spring Boot con los tickets Done de Jira, y marca dónde el código, la UI y los tickets usan nombres distintos para lo mismo. Usar para tener un manual de producto actualizado antes de una entrega o para que alguien nuevo entienda la app; no son release notes de una entrega."
metadata:
  tipo: skill
  area:
  - documentacion
  - gestion
  fase:
  - analisis
  - mantenimiento
  tecnologias:
  - react
  - spring-boot
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - jira
  - github
  grupo: "07"
  autor:
    nombre: Ana Abramowich
    github: AbramowichAna
  responsables:
  - AbramowichAna
  madurez: usado-en-proyecto
  relacionados:
  - g07-release-notes
  - g07-role-handoff
  - g07-balance-gamificacion
---

# Documentar el producto

Las release notes cuentan **qué cambió** en una entrega. Esta skill mantiene **qué es el producto hoy**: un manual vivo que cualquiera (la cátedra, un compañero nuevo, el PO) puede leer para entender Study Arena sin abrir el código.

Además mantiene el **glosario del dominio**: cuando el código dice `Session`, la UI dice "Sala de estudio" y el ticket dice "juntada", alguien se va a confundir. La skill lo detecta y lo propone unificar.

## Cuándo usar esta skill

"Documentá el producto", "armá el manual de Study Arena", "actualizá la doc de producto", "¿qué hace hoy la app?", "glosario", "¿cómo le decimos a X?", antes de una entrega final o cuando entra alguien nuevo al equipo.

## Estructura que mantiene

```
docs/producto/
├── README.md            # Qué es Study Arena, para quién y el índice
├── funcionalidades.md   # Por épica: qué hace, estado, dónde vive en el código
├── flujos.md            # Recorridos de usuario paso a paso (con rutas de la app)
├── reglas.md            # Reglas que el usuario percibe (puntos, ranking, límites, permisos)
└── glosario.md          # Términos del dominio y sus equivalencias código ↔ UI ↔ tickets
```

Si el repo ya tiene otra carpeta de documentación, preguntá antes de crear una nueva.

## Paso 1: relevar (solo lectura)

1. **Frontend (React)**: el router (rutas y páginas), los textos visibles (títulos, botones, mensajes de estado vacío y de error) y los componentes de cada página. Las rutas son el mapa de lo que el usuario puede hacer.
2. **Backend (Spring Boot)**: controllers (qué operaciones existen), entidades y enums (los conceptos del dominio y sus estados) y services con reglas que se notan desde afuera.
3. **Jira**: épicas y tickets **Done** (tool MCP que termine en `searchJiraIssuesUsingJql`, por ejemplo `project = STUDY AND statusCategory = Done ORDER BY parent`), para nombrar las funcionalidades como las nombra el equipo y saber a qué épica pertenece cada una. Traé también lo **In Progress** para marcar lo que está en camino.
4. Si ya existe `docs/producto/`, leela completa: vas a actualizar, no a reescribir.

## Paso 2: estado real de cada funcionalidad

Para cada funcionalidad, el estado sale de cruzar las fuentes, no de una sola:

- ✅ **Disponible**: tiene ruta o pantalla en el front **y** endpoint en el back, y el ticket está Done.
- 🟡 **Parcial**: existe en una capa y no en la otra, o el ticket está Done pero falta una parte del flujo (por ejemplo, el endpoint existe y la pantalla no lo usa).
- 🔜 **En camino**: ticket In Progress o In Review.
- ⚠️ **Inconsistente**: el ticket dice Done pero no se encuentra en el código. Listalo aparte para que el equipo lo revise.

Cada funcionalidad lleva: descripción en lenguaje de usuario (2–4 oraciones), estado, épica, tickets y **dónde vive** (ruta del front y endpoints), para quien la quiera seguir en el código.

## Paso 3: flujos

Escribí los recorridos principales (registrarse, crear o unirse a un grupo, programar y entrar a una sesión de estudio, jugar un quiz, ver el progreso y el ranking…) como pasos numerados desde el punto de vista del usuario, con la ruta de la app en cada paso y qué pasa si algo sale mal (los mensajes de error reales del front).

## Paso 4: reglas

Solo las reglas que **el usuario percibe** (cuántos puntos da cada cosa, cómo se ordena y cuándo se reinicia el ranking, límites y quién puede hacer qué). Cada una con su fuente `archivo:línea` en un comentario HTML (`<!-- QuizService.java:88 -->`) para que se pueda verificar sin ensuciar la lectura. Si `g07-balance-gamificacion` ya generó una tabla de reglas, reutilizala.

## Paso 5: glosario

Para cada concepto del dominio (grupo, sesión, ciclo, focus, break, presencia, quiz, intento, flashcards, material, meta de estudio, puntos, ranking… los que existan en el código), una fila:

| Término (UI) | Definición | En el código | En los tickets | Estado |
|---|---|---|---|---|

- Buscá cada término en los tres lados (textos del front, clases, enums y tablas del back, títulos y descripciones de tickets).
- **Estado** ✅ si los nombres son consistentes o tienen una equivalencia obvia (`Group` ↔ "grupo"); ⚠️ si un mismo concepto tiene nombres distintos que no son una traducción directa (`Session` ↔ "Sala" ↔ "juntada"), o si una misma palabra se usa para dos cosas distintas.
- Para cada ⚠️, proponé **un** término recomendado y dónde habría que cambiarlo. No hagas el cambio.

## Paso 6: escribir

1. Mostrá primero un **resumen de cambios** respecto de la doc existente (o "doc nueva") y los ⚠️ encontrados.
2. Con el OK del usuario, escribí o actualizá los archivos. Preservá lo que alguien escribió a mano y no contradiga el código.
3. Al pie de cada archivo: `Actualizado: <fecha> · Commit: <hash corto>`.
4. No hagas commit: dejá los cambios para que el usuario los revise.

## Estilo

- Lenguaje de usuario, no de desarrollador, en todo menos en "dónde vive" y en las fuentes.
- Español rioplatense, claro y sin marketing ("permite", no "revoluciona").
- Sin capturas inventadas: si el usuario quiere capturas, decile qué pantallas conviene capturar.

## Qué no hacer

- No documentes como disponible algo que solo está en un ticket.
- No renombres nada en el código, la UI ni Jira: solo lo proponés.
- No escribas en Jira.

## Ejemplo de uso

**Pedido:** Armame la documentación de producto de Study Arena para la entrega final y decime si estamos usando nombres distintos para lo mismo.

**Resultado:** Releva las rutas del front, los controllers y las entidades del back y los tickets Done de Jira, y genera `docs/producto/` con funcionalidades por épica y su estado real, flujos, reglas con su fuente y glosario. Marca los conceptos que tienen nombres distintos en el código, la UI y los tickets, propone un término único para cada uno y escribe los archivos recién con el OK del usuario.
