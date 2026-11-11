---
name: g14-auditor-de-higiene-pre-entrega
description: Audita con un script determinista, sin imprimir nunca un valor secreto, la higiene de uno o varios repositorios antes de entregarlos (archivos sensibles sin ignorar, secretos versionados o en el historial, .gitignore incompleto, remotes con credenciales, artefactos de build versionados, emails en datos de prueba) y deja un JSON que puede alimentar al checklist de cierre. Usala antes de un traspaso o de la entrega final; no rota credenciales ni reescribe el historial.
metadata:
  tipo: skill
  area:
  - seguridad
  fase:
  - revision
  - despliegue
  tecnologias:
  - agnostico
  - git
  - python
  metodologia:
  - agnostico
  herramientas:
  - claude-code
  requiere: []
  grupo: '14'
  autor:
    nombre: Macarena Alimena
    github: MackyAlimena
  colaboradores: []
  responsables:
  - MackyAlimena
  madurez: probado
  relacionados:
  - g14-cierre-y-congelamiento
---

# Auditor de higiene pre-entrega

Antes de entregar un repositorio, la pregunta es qué se lleva quien lo recibe sin saberlo. Esta skill la responde con un script que sólo lee.

## Cuándo usarla

Antes de transferir repos, abrirlos a otro equipo o entregar el proyecto. Se puede correr sobre un repo o sobre una carpeta con varios.

## Protocolo

1. Corré el script: `python3 scripts/auditar_higiene.py --raiz <carpeta con los repos> --json higiene.json --salida higiene.txt`. Con `--sin-historial` omite la búsqueda en el historial (más rápido). Con `--check` devuelve 1 si hay hallazgos ALTA.
2. Leé primero lo ALTA. Para cada una, decidí con una persona: **rotar** la credencial en el proveedor (siempre, si estuvo versionada), sacarla del repo, y recién después evaluar si hace falta reescribir historial.
3. Los MEDIA son «revisar a mano»: asignaciones con valor literal (puede ser un ejemplo) y `.gitignore` sin cubrir `.env`. Los BAJA son informativos (licencia, emails en datos de prueba, JWT vencidos o anon).
4. Corrigiendo lo que corresponda, volvé a correrlo hasta que no queden ALTA, y guardá la salida como evidencia.
5. Pasale el JSON a `g14-cierre-y-congelamiento` (`--higiene`) para que los hallazgos entren al checklist de cierre. La skill funciona igual sin ese paso.

## Qué comprueba

- Archivos sensibles por nombre (`.env*`, claves, `*_SA_JSON`, cuentas de servicio): versionado, ignorado, o **sin versionar y sin ignorar** (un `git add .` lo sube).
- Secretos en archivos versionados y en las líneas agregadas del historial de cualquier rama: claves privadas, tokens de GitHub/Slack/Atlassian/Google/AWS, claves de LLM, claves secretas de Supabase y JWT (decodifica el payload: `service_role` es ALTA; indica si el token ya venció).
- Cobertura mínima del `.gitignore`, credenciales embebidas en remotes, `node_modules`/`dist` versionados, archivos de más de 5 MB, emails de dominio real en datos de prueba, README y LICENSE.

## Límites

- Es una búsqueda por patrones: no encuentra secretos sin formato conocido y puede marcar ejemplos. Por eso los MEDIA piden criterio humano.
- No verifica que una credencial haya sido rotada: eso sólo lo sabe el proveedor.
- Nunca imprime ni guarda el valor: sólo tipo, ubicación, longitud y una huella sha256 corta.

## Evidencia de uso

Corrida del 08/11/2026 sobre los 7 repos del proyecto: `salidas/auditoria-higiene-pre-entrega.txt`. Encontró un archivo `VERTEX_SA_JSON` en `vaiven-app` sin versionar y sin ignorar (ALTA), `.env` sin cubrir en un repo, y 0 secretos reales en archivos versionados ni en el historial.

## Ejemplo de uso

**Pedido:** Auditá la higiene de los repos del proyecto antes de entregarlos.

**Resultado:** Corre el script sobre cada repo, informa los hallazgos ALTA/MEDIA/BAJA con archivo y línea (sin mostrar valores), propone qué rotar y qué ignorar, y deja el JSON para el checklist de cierre.
