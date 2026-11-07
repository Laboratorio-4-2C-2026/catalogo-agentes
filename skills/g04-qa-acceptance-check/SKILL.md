---
name: g04-qa-acceptance-check
description: Verificación de QA de un Pull Request contra los criterios de aceptación de su ticket de Linear y la Definition of Done del equipo, corriendo la app y probando cada criterio, no solo compilando. Usar cuando se pide probar un PR, validar que un ticket está terminado o hacer QA antes del merge.
metadata:
  tipo: skill
  area:
  - qa
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
  - github
  - linear
  grupo: "04"
  autor:
    nombre: Alexander Köttner
    github: Alexander-Kottner
  colaboradores:
  - nombre: Martin Barreiro
    github: martinbarreiroo
  responsables:
  - Alexander-Kottner
  madurez: experimental
  relacionados:
  - g07-qa-acceptance
  - g11-qa-con-capturas
---

# QA de aceptación de un PR

Un ticket está terminado cuando cumple sus criterios de aceptación en la app corriendo. Esta skill lo
comprueba y deja evidencia.

## Entradas

- URL o número del PR, o la clave del ticket.

## Flujo

1. **Criterios:** leer el ticket en Linear y armar un checklist con cada criterio de aceptación. Sumar
   la Definition of Done del equipo si el repo o el plan la define (por ejemplo: build sin errores,
   tests de Jest para cada endpoint nuevo, probado corriendo la app).
2. **Preparar:** checkout de la rama del PR en un worktree aparte, instalar dependencias y levantar los
   servicios según el README/AGENTS.md (base de datos, API, web). No tocar bases que no sean locales o
   de prueba.
3. **Checks automáticos:** build/typecheck, lint y tests del workspace afectado, registrando el código
   de salida real de cada uno.
4. **Probar cada criterio:**
   - API: `curl` a los endpoints locales con casos felices, errores de validación y permisos, y
     consultas a la base local para confirmar lo que quedó guardado.
   - Web: recorrer el flujo en el navegador en desktop y mobile, incluidos estados vacíos, de carga y de
     error.
5. **Registrar** por criterio: pasa / falla / no se pudo probar, con la evidencia (comando y respuesta,
   captura o pasos para reproducir).

## Salida

Checklist de criterios con su resultado, checks automáticos con su resultado, y los defectos
encontrados con pasos para reproducir, resultado esperado y obtenido. Veredicto final: listo para merge
o no.

## Reglas

- No marcar un criterio como "pasa" sin haberlo ejercitado.
- No arreglar el código del PR: se reporta. Publicar el reporte en el PR o en Linear solo con
  autorización.
- Si el entorno no levanta, decirlo y separar "falla del entorno" de "falla del código".

## Ejemplo de uso
**Pedido:** Probá el PR 43 contra PIT-64 antes de que lo mergeemos.

**Resultado:** Levanta la app en la rama del PR, recorre cada criterio de aceptación de la landing en desktop y mobile, corre build y tests y devuelve un checklist pasa/falla con evidencia y los defectos encontrados.
