---
name: g14-cierre-y-congelamiento
description: Genera, a partir de lo que los repositorios realmente usan (workflows con cron, secretos referenciados, variables de entorno, servidores MCP, servicios con sus hosts), el checklist de traspaso y congelamiento de un proyecto, con acción, objeto, origen, dueño y forma de comprobación por ítem, y después verifica lo comprobable sin credenciales. Acepta opcionalmente el JSON del auditor de higiene. Usala al cerrar o traspasar el proyecto a otro equipo; no rota, apaga ni transfiere nada por sí sola.
metadata:
  tipo: skill
  area:
  - gestion
  - devops
  fase:
  - mantenimiento
  tecnologias:
  - agnostico
  - git
  - python
  metodologia:
  - agnostico
  herramientas:
  - claude-code
  requiere:
  - github
  grupo: '14'
  autor:
    nombre: Macarena Alimena
    github: MackyAlimena
  colaboradores: []
  responsables:
  - MackyAlimena
  madurez: probado
  relacionados:
  - g14-auditor-de-higiene-pre-entrega
---

# Cierre y congelamiento

Un traspaso falla por lo que nadie anotó: el cron que sigue gastando minutos, el token que sigue vivo, el proyecto en la nube a nombre de una persona. El checklist se arma **de lo que el código y la configuración usan**, no de la memoria del equipo.

## Protocolo

1. **(Opcional, recomendado)** Corré antes `g14-auditor-de-higiene-pre-entrega` y guardá su JSON.
2. Generá: `python3 scripts/inventario_cierre.py generar --raiz <carpeta con los repos> [--higiene higiene.json] --salida cierre.md`. Produce `cierre.md` (tabla con casillas) y `cierre.json` (cómo se comprueba cada ítem).
   - **Con** `--higiene`: los hallazgos ALTA y MEDIA entran como ítems «resolver».
   - **Sin** `--higiene`: no inventa nada; deja un ítem previo «correr el auditor de higiene», porque sin él el checklist no sabe qué secretos filtrados hay.
3. Asigná un dueño a cada ítem (el script deja `<dueño>`). Un ítem sin persona no se hace.
4. A medida que se hace, marcá `[x]` en `cierre.md`.
5. Verificá: `python3 scripts/inventario_cierre.py verificar cierre.md [--online]`. Devuelve 1 si algo está marcado como hecho y **no lo está**.

## Qué descubre

Repos de GitHub (transferir o archivar), workflows con `schedule`/`cron` (apagar), referencias a `secrets.*` y `vars.*` (rotar y retirar), nombres de variables de los `.env.example` (entregar por canal privado o revocar; nunca lee valores), servidores de `.mcp.json`, infraestructura por archivo (Vercel, Supabase local, compose/Caddy, n8n) y hosts de servicios en la documentación (Atlassian, Supabase, Vercel, Figma, Canva, Cloud Run).

## Qué verifica y qué no

| Ítem | Verificación |
|---|---|
| Cron apagado | Automática: el workflow ya no tiene `schedule:`/`cron:` |
| Archivo sensible ya ignorado | Automática: `git check-ignore` |
| Repo archivado | Automática con `--online` (`gh`, sólo lectura) |
| Secretos, variables, MCP, servicios en la nube | **Confirmación humana**: se informa como tal, nunca como verificado |

## Límites

- Descubre lo que está escrito en los repos. Cuentas de personas, accesos a paneles y dominios que nadie documentó no aparecen: el checklist lo dice en su encabezado y hay que completarlo a mano.
- Los hosts salen de la documentación y pueden incluir servicios ya apagados; revisá la columna «Origen».

## Evidencia de uso

`salidas/cierre-y-congelamiento.md` (08/11/2026): 80 ítems sobre los 7 repos, 9 de ellos venidos del auditor de higiene. Sin el JSON de higiene se generan 72 ítems más el ítem previo. La verificación se probó sobre un repo descartable: con el cron activo falló (exit 1) y al apagarlo pasó (exit 0), ver `salidas/cierre-y-congelamiento-verificacion.txt`.

## Ejemplo de uso

**Pedido:** Armá el checklist para traspasar el proyecto a otro equipo.

**Resultado:** Descubre servicios, crons, secretos y variables en los repos, suma los hallazgos de higiene si hay JSON, genera la tabla con dueño por ítem y, cuando se marcan casillas, verifica cuáles se cumplen de verdad.
