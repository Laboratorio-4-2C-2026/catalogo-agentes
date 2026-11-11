---
name: g12-triar-reporte-de-bug
description: Convierte un reporte de bug (herramienta de reportes, chat, captura o relato) en un veredicto — bug, comportamiento esperado, duplicado, no reproduce o problema de ambiente — con pasos de reproducción, el requisito que rompe, severidad y un borrador de issue listo para cargar. Usar cuando llega un reporte y hay que decidir qué hacer con él; no corrige el bug.
owner: '@lucasmonteverdi1'
role: qa
created: '2026-11-09'
metadata:
  tipo: skill
  area:
  - qa
  fase:
  - testing
  - mantenimiento
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  - codex
  requiere: []
  grupo: '12'
  autor:
    nombre: Lucas Monteverdi
    github: lucasmonteverdi1
  responsables:
  - lucasmonteverdi1
  madurez: experimental
  relacionados:
  - g12-reportar-incidente
---

# Triar un reporte de bug

## Para qué

Si la clasificación de un reporte es mala, todo lo que sigue — test, rama, PR — se hace sobre
algo que no era un bug, o se duplica uno que ya estaba cargado. Esta skill es solo ese primer
paso, hecho bien.

## Entrada

El reporte tal cual llegó: texto, captura, URL, navegador o dispositivo, usuario de prueba.
Si falta la URL o el ambiente, preguntarlo antes de seguir.

## Descubrir las fuentes

Identificar en el proyecto el tracker de issues (Linear, Jira, GitHub Issues, etc.), dónde
están los requisitos o criterios de aceptación (historias, specs, PRD) y qué ambientes
existen. Si no está claro, preguntar en vez de asumir.

## Pasos

1. **Ambiente.** Dónde pasó (producción, staging, preview de una PR, local) y qué versión
   estaba desplegada. Un reporte sobre una versión vieja puede estar ya corregido.
2. **Duplicados.** Buscar en el tracker y en los reportes recientes algo con el mismo
   síntoma. Si hay, se termina acá: **Duplicado de X**.
3. **Requisito.** Buscar la historia o spec que cubre ese flujo y su criterio de aceptación.
   Si el comportamiento reportado es el que el criterio pide, es **Esperado**, con la cita.
4. **Reproducir.** Intentar reproducir en el mismo ambiente con pasos numerados mínimos. Si hay
   navegador disponible, hacerlo de verdad y guardar captura. Si no reproduce, probar con el
   navegador o dispositivo del reporte antes de descartar: cookies, permisos y APIs difieren
   entre navegadores. Si sigue sin reproducir: **No reproduce**, con lo intentado.
5. **Ambiente vs código.** Si el fallo es de configuración, dominio, datos de prueba o
   plataforma y no de código, es **Ambiente**, diciendo qué falta.
6. **Severidad.** Alta si bloquea un flujo principal o pierde datos; Media si hay un camino
   alternativo; Baja si es visual o de texto.

## Salida

```
Veredicto: Bug | Esperado | Duplicado de <ref> | No reproduce | Ambiente
Severidad: Alta | Media | Baja       (solo si es Bug)
Ambiente y versión: …
Requisito: <ref> — "<criterio que rompe>"
Pasos:
1. …
Esperado: …
Obtenido: …
Evidencia: <captura, request, log>
```

Si es **Bug**, agregar un borrador de issue con título que describa el síntoma ("El total no
suma los gastos en otra moneda") y el nombre del test de regresión que lo cubriría. No cargar
la issue sin que el usuario lo confirme.

## Qué no hace

No corrige código ni abre ramas. No sube la severidad para que se priorice: si el reporte
viene con urgencia, se dice aparte.

## Ejemplo de uso

**Pedido:** Llegó este reporte: "el total del evento no suma los gastos en dólares", en producción desde Safari.

**Resultado:** Devuelve un veredicto (bug, esperado, duplicado, no reproduce o ambiente) con pasos de reproducción, el criterio que rompe y la severidad; si es bug, suma un borrador de issue sin cargarlo.
