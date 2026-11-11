---
name: g14-auditor-de-tickets-contra-codigo
description: "Auditoría técnica previa a estimar o publicar un lote de tickets: verifica contra origin/main del repo de producto que lo que cada ticket da por existente exista, que lo que pide no esté ya hecho y que el kit de los devs no contradiga al código, y entrega evidencia reutilizable por el revisor final. Usala en cada emisión de tickets, en sólo lectura; no reescribe tickets ni revisa su legibilidad."
metadata:
  tipo: skill
  area:
  - gestion
  - qa
  fase:
  - planificacion
  - revision
  tecnologias:
  - agnostico
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - github
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

# Auditor de tickets contra el código

Un ticket escrito contra el plan envejece cuando el producto avanza. En VaiVen, un hito llegó con 42 h estimadas en 24 fichas y buena parte ya existía en `main`; y el kit de los devs afirmaba una librería que no estaba instalada. **Ninguna de las dos cosas se detectó leyendo documentos: se detectaron leyendo el código.**

## Entrada

- El lote de tickets a emitir (Markdown en el repo de dirección).
- Un clon del repo de producto actualizado: `git -C <clon> fetch origin`. Se lee **siempre** `origin/main`, nunca una rama de feature sin mergear (un PR abierto no es base para un ticket).
- Los documentos del kit que esos tickets citan.

## Pasos por ticket

1. **Extraé las afirmaciones verificables**: archivos y rutas a tocar, componentes, funciones, hooks, tablas, columnas, nodos del workflow, dependencias, contratos de payload y comandos.
2. **Comprobá cada una contra `origin/main`**, sin hacer checkout:
   ```bash
   git -C <clon> show origin/main:<ruta>
   git -C <clon> grep -n '<símbolo>' origin/main -- <carpeta>
   git -C <clon> show origin/main:package.json
   ```
   Para un workflow exportado (n8n), leé el JSON y buscá el nodo por nombre o tipo.
3. **Clasificá** cada afirmación:
   - ✅ existe como dice el ticket;
   - ❌ **no existe** o tiene otro nombre/forma → el ticket se corrige;
   - ⚠ **ya está hecho** lo que el ticket manda construir → se reconvierte («ya existe como MVP» no es terminado: queda llevarlo al diseño, validar errores y probar) y se re-estima;
   - ↔ **duplica lógica** que ya vive en otra capa (por ejemplo, recomponer en la app un puntaje que el workflow ya compone) → se saca.
4. **Leé el kit contra el mismo commit.** Cada afirmación del kit que el ticket usa (stack, entorno, contrato) se verifica igual. Si el código difiere, **gana el código**: se corrige el kit en el mismo cambio y el documento declara la fecha del barrido.
5. **Detectá falsos tickets**: un paso de verificación sin código nuevo no es un ticket, es un criterio de aceptación del ticket que produce el código.

## Salida

```
Auditoría contra <repo> origin/main <sha corto> — <fecha>

| Ticket | Afirmación | Estado | Evidencia (ruta:línea o comando) | Corrección |
|--------|------------|--------|----------------------------------|------------|

Kit: <doc> — <afirmación> — difiere del código: <evidencia>
Resumen: N tickets, M correcciones, K re-estimaciones.
```

Las correcciones se aplican en los tickets antes de publicarlos, y el commit del repo de dirección nombra el SHA auditado (ejemplo real: «carril A auditado contra el código antes de emitirse», ocho tickets contra `de92576`, seis correcciones).

## Reglas

- Solo lectura sobre el repo de producto: no checkout de ramas ajenas, no commits, no PRs.
- Toda afirmación del reporte lleva su evidencia de esta sesión; lo no verificado se marca `[por-verificar]` y no se hornea en el ticket.
- No se agrega alcance al corregir: si falta algo, va como ticket nuevo y pasa por la estimación.

Evidencia en VaiVen: commit `13f288c` (18/09) y `docs/bitacora/2026-09-18-el-kit-envejecio-porque-nadie-lo-leyo-contra-el-codigo.md`; antecedente en `docs/bitacora/2026-09-16-un-ticket-se-estima-contra-el-codigo-no-contra-el-plan.md`.

## Ejemplo de uso

**Pedido:** Antes de publicar en Jira los ocho tickets del carril de frontend de la semana 8, auditalos contra `vaiven-app` main.

**Resultado:** Devuelve una tabla por ticket con cada afirmación (archivo, componente, contrato) marcada como existe / no existe / ya hecho / duplica, con la evidencia de `origin/main` y la corrección propuesta, más las afirmaciones del kit que el código contradice.
