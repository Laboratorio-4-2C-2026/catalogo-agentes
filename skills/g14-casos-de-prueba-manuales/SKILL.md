---
name: g14-casos-de-prueba-manuales
description: Escribe casos de prueba manuales (UAT) para una pantalla o un flujo de punta a punta, uno por fila con cómo se provoca y resultado esperado, más los juegos de datos y la evidencia que el dev tiene que adjuntar. Usala cuando QA de dirección entrega el guion que un dev ejecuta en un ticket de QA, sin framework de tests.
metadata:
  tipo: skill
  area:
  - qa
  fase:
  - testing
  - analisis
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere: []
  grupo: "14"
  autor:
    nombre: Martina de Jesus
    github: mardejesus
  colaboradores: []
  responsables:
  - mardejesus
  madurez: usado-en-proyecto
  relacionados: []
---

# Casos de prueba manuales

Los casos los escribe QA de dirección; el dev los **ejecuta** y adjunta evidencia. Son el guion de la revisión, así que tienen que poder correrse sin preguntar nada.

## Antes de escribir

1. Leé el ticket (o los tickets) de la funcionalidad y sus criterios de aceptación, y el código en `main`: un caso que pide un estado que no existe no se puede correr.
2. Listá **los estados** de la pantalla (carga, error, sesión vencida, vacío, en proceso, con datos) y **el recorrido** que la atraviesa de punta a punta.
3. Listá lo que **está fuera de alcance** y que no se anota como bug (en VaiVen: la tarjeta todavía no se compara contra el Figma; la mensajería interna está excluida del MVP).

## Formato del set

Una tabla, un caso por fila, cerrada: **son estos y no se agregan otros.**

| Caso | Cómo se provoca | Resultado esperado | Resultado real | Evidencia |
|---|---|---|---|---|
| Carga | Throttling «Slow 3G» en DevTools | Skeleton | | captura 375 px |
| Error de red | Orquestador apagado | Mensaje y botón de reintento | | |
| Sesión vencida | Cerrar sesión en otra pestaña y volver | Redirige a `/login` | | |
| Vacío | Publicación sin nadie del otro lado | Estado vacío con el texto acordado | | |
| Recorrido | Publicar con una sesión algo compatible con lo publicado por otra | Aparece «analizando»; al recargar, con nivel | | |

Reglas de redacción:

- **«Cómo se provoca» es una acción concreta**, no «simular un error». Nombrá la herramienta o el dato.
- **Un resultado esperado observable por caso**: un texto, un componente, una URL. Nada de «funciona bien».
- **Dos sesiones** cuando el caso toca permisos o el otro lado de un flujo.
- Viewport fijo (VaiVen: 375 px, mobile-first).

## Juegos de datos

Agrupá los casos por el estado de la base que necesitan, con el comando exacto. Ejemplo:

1. **Juego 1, sin juicios**: `supabase db reset` común, orquestador arriba, `pnpm dev` → carga, error, sesión vencida, vacío, analizando.
2. **Juego 2, con juicios**: la receta documentada en el encabezado de la semilla → con datos, recorrido.

## Recorrido exploratorio (variante de punta a punta)

Cuando el pedido es «recorré el producto entero»: dos personas en dos navegadores (donante y receptor), ciclo completo (registro → perfil → publicar → candidatos → elegir → confirmar → contacto revelado). Además del camino feliz: reintentar, refrescar a mitad de flujo, volver atrás. Cada hallazgo con **pantalla, pasos, esperado vs. observado y severidad** (bloqueante / molesto / cosmético).

## Lo que el ticket le pide al dev

- Resultado real anotado al lado del esperado, una captura por caso.
- Cada caso fallido → un bug con pasos para reproducir. **No se arregla en el mismo PR** del QA.
- Un caso ambiguo o mal escrito se marca y se comunica; no se reinterpreta en silencio.
- Si no alcanza el tiempo, se prioriza corregir bloqueantes sobre ejecutar el 100 %, y lo pendiente queda documentado con severidad.
- No instalar un framework de tests en un ticket de QA manual.

## Ejemplo concreto

VaiVen, repo de dirección: `docs/planning/tickets/hito-4/H4-C.3.8-qa-de-la-pantalla-de-match.md` (siete casos, dos juegos de datos) y `docs/planning/tickets/hito-6/H6-A.1.1-*.md` / `H6-A.1.2-*.md` (recorrido exploratorio y ejecución del set).

## Ejemplo de uso

**Pedido:** Escribí los casos de prueba manuales de la pantalla de candidatos para que la dev los corra antes de la revisión del viernes.

**Resultado:** Devuelve la tabla cerrada de casos (estado, cómo se provoca, resultado esperado, columnas para resultado real y captura), los juegos de datos con sus comandos, lo que no se anota como bug y los criterios de aceptación del ticket de QA.
