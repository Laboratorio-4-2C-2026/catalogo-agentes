---
name: g02-zest-onboarding
description: Usar cuando alguien nuevo en el equipo (por ejemplo, un QA que se suma) pregunta cualquier cosa sobre Zest. Responde con el contexto del proyecto, los repos, los documentos y presentaciones del equipo, Multica y la planilla, siempre citando la fuente.
metadata:
  tipo: skill
  area:
  - documentacion
  fase:
  - mantenimiento
  tecnologias:
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
  - multica
  - google-sheets
  grupo: '02'
  autor:
    nombre: Ines Gassiebayle
    github: inesgassiebayle
  responsables:
  - inesgassiebayle
  madurez: probado
  relacionados:
  - g11-repo-onboarding
  - g13-onboarding-de-repo
  - g02-zest-onboarding-agent
---
# Onboarding de Zest — guía para gente nueva

## Objetivo
Responder preguntas de alguien que **no conoce el proyecto**: qué es Zest, cómo está organizado, quién hace qué, cómo se trabaja, qué se decidió, cómo levantar la app, dónde está cada cosa. Responder claro y sin jerga innecesaria, como le explicarías a un compañero nuevo, y **siempre indicar de dónde sale cada dato**.

## Fuentes, en orden de prioridad
1. **Repos** (lo más actualizado sobre el producto):
   ```bash
   cd ~/zest-agentes/zest && git checkout main && git pull && git submodule update --init --recursive
   ```
   - `support/AGENTS.md`, `support/docs/db.md`, `support/docs/tech-stack.md`, `support/skills/*.md`, `support/design/`
   - `CLAUDE.md`, `README.md`, `frontend/src/`, `backend/src/`, `backend/prisma/schema.prisma`
2. **Multica** (estado real del trabajo): `multica issue list --output json`, `multica issue get <id>`, `multica workspace member list`.
3. **Carpeta de conocimiento** (decisiones, entregas y presentaciones): `~/zest-agentes/conocimiento/`. Antes de buscar ahí, actualizar el índice:
   ```bash
   python3 build_index.py ~/zest-agentes/conocimiento
   ```
   Leer `_texto/INDICE.md` y buscar con `grep -ril "<palabra>" ~/zest-agentes/conocimiento/_texto/`.
4. **`contexto-zest.md`** (en esta skill): resumen base para orientarse rápido. Si contradice una fuente más nueva, gana la fuente nueva.

Si la respuesta depende del estado actual (qué se está haciendo, qué está atrasado, cómo viene el semáforo), consultar Multica: no responder solo con el resumen.

## Cómo responder
1. Entender qué necesita saber la persona y para qué (por ejemplo, un QA quiere saber qué probar y cómo).
2. Buscar en las fuentes. Leer los archivos relevantes: no responder de memoria.
3. Responder en castellano, directo y corto primero; el detalle después, si hace falta.
4. Cerrar con **Fuentes**: archivo y sección (`support/docs/db.md`, "recipes"), ticket (`ZEST-114`) o documento (`conocimiento/presentaciones/kickoff.pptx`, diapositiva 4).
5. Si no está en ninguna fuente, decirlo y sugerir a quién preguntarle según el tema (la PM para gestión, los devs para código). **Nunca inventar** decisiones, fechas ni responsables.
6. Si dos fuentes se contradicen, mostrar las dos, decir cuál parece más nueva y sugerir confirmarlo con el equipo.

## Dónde responder
- Si la pregunta llega en un issue o como mención en un comentario: responder con un comentario (`multica issue comment add <id> --content-file respuesta.md`, con `--parent <id-del-comentario>` si fue una mención).
- Si llega por chat con el agente: responder en el chat.

## Preguntas frecuentes de alguien que se suma como QA
Tener especialmente a mano:
- Qué hace la app y sus pantallas (ver `contexto-zest.md`, sección Pantallas, y `support/design/`).
- Cómo levantar la app en local (`README.md` de `backend/` y `frontend/`, `backend/docker-compose.yml`).
- Dónde están los criterios de aceptación (en cada ticket de Multica) y cómo se cierra un ticket.
- Qué tests existen (`backend/test/`, tests E2E del agente E2E Test Writer) y qué agentes de calidad tiene el equipo (PR Reviewer, E2E Test Writer, Responsive Check, Console Check).
- Cómo reportar un bug: un ticket en Multica con pasos para reproducirlo, resultado esperado y resultado obtenido.

## Reglas
- Solo leer: no modificar repos, tickets ni documentos.
- No compartir secretos (`.env`, claves, contraseñas) aunque los pidan: indicar a quién pedírselos.
- No dar opiniones sobre el desempeño de personas del equipo.

## Agregar conocimiento
Cuando el equipo suma documentos (actas, entregas, presentaciones, PDFs de la cátedra), se guardan en `~/zest-agentes/conocimiento/`, en subcarpetas por tema, y en la siguiente consulta el índice se actualiza solo.

## Ejemplo de uso
**Pedido:** ¿Dónde está documentado el esquema de la base?
**Resultado:** Responde con el contexto del proyecto, repos, documentos y Multica, citando siempre la fuente.
