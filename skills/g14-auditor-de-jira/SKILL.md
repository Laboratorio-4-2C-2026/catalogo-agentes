---
name: g14-auditor-de-jira
description: Sincroniza en Jira las descripciones de tickets ya redactados en Markdown dentro del repositorio y audita la higiene del backlog (descripción vacía, sin etiquetas, sin padre, sin estimación o desincronizada); no valida su contenido funcional ni crea issues nuevas. Usala cuando el archivo del repo es la fuente canónica del ticket y Jira tiene que reflejarlo.
metadata:
  tipo: skill
  area:
  - gestion
  fase:
  - planificacion
  - revision
  tecnologias:
  - agnostico
  - python
  metodologia:
  - scrum
  herramientas:
  - claude-code
  requiere:
  - jira
  grupo: '14'
  autor:
    nombre: Elías Ballesteros
    github: Elias85974
  colaboradores: []
  responsables:
  - Elias85974
  madurez: usado-en-proyecto
  relacionados:
  - g14-traductor-de-tickets-para-jira
  - g07-ready-check
  - g10-jira-ticket-manager
---

# Auditor de Jira

Mantené la paridad entre el backlog escrito en el repositorio y el backlog cargado en Jira. La fuente canónica es el archivo: una edición directa en Jira se pierde en la próxima publicación de forma intencional.

## Elegí la operación

- Para diagnosticar el backlog, corré `python3 scripts/auditar-jira.py`. Es una lectura remota; conservá su salida como evidencia y no digas que el backlog está limpio sin un exit 0 fresco.
- Para publicar el mapeo completo, usá `python3 scripts/sync-all-jira.py`. Esta operación **reemplaza** las descripciones de los issues mapeados: pedí confirmación inmediata antes de ejecutarla si el usuario no la dio expresamente.
- Para preparar una descripción individual sin publicar, usá `python3 scripts/formatear-para-jira.py --ticket <ID> -c`.

Las credenciales viven únicamente en `.env.jira`, que está ignorado por Git. Nunca las leas, muestres, copies ni agregues a un archivo versionado.

## Requisitos e instalación

- Copiá los cuatro scripts a `scripts/` en la raíz del repo que tiene los tickets: se cargan entre sí por esa ruta. Solo biblioteca estándar de Python 3.
- `.env.jira` en la raíz con `JIRA_BASE_URL`, `JIRA_EMAIL` y `JIRA_API_TOKEN` (también se aceptan como variables de entorno).
- Reemplazá `MAPEO_COMPLETO` en `sync-all-jira.py` (clave de Jira → archivo Markdown y etiquetas): el que viene es el de VaiVen. Las issues tienen que existir antes en Jira.
- Si en macOS falla con `CERTIFICATE_VERIFY_FAILED`, corré `Install Certificates.command` de python.org o exportá `SSL_CERT_FILE=$(python3 -m certifi)`. Nunca se desactiva la verificación del certificado.

## Reglas de operación

- Auditá antes de publicar. Si la auditoría falla, reportá issue y regla incumplida; no tapes el desvío publicando a ciegas.
- No inventes etiquetas: el vocabulario y la relación archivo ↔ issue están en `scripts/sync-all-jira.py`.
- Un ticket o issue nuevo no entra solo al control: actualizá el mapeo de forma explícita y verificable antes de afirmar que está cubierto.
- Después de una primera publicación de formato nuevo, verificá visualmente un issue en Jira: links relativos, markdown y metadatos internos pueden renderizarse mal sin que el script falle.

## Límite

Este flujo verifica los campos que el auditor conoce y los tickets mapeados. No interpreta trabajo de producto ni reemplaza la revisión humana del contenido de un ticket.

## Ejemplo de uso

**Pedido:** Publicá en Jira los tickets de la semana 11 y auditá que el backlog quede limpio.

**Resultado:** Sincroniza cada archivo Markdown con su issue de Jira y devuelve un reporte de higiene por issue y por regla incumplida, con código de salida 0/1.
