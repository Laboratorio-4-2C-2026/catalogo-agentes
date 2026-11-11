---
name: g14-status-reporter-semanal
description: Genera el informe interno semanal de avance con estado RAG consolidando el estado actual de Jira, la actividad de Git y el inventario de agentes. Se puede re-ejecutar; el corte histórico (--hasta) limita Git pero no reconstruye Jira, que siempre se lee como está hoy.
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
  requiere:
  - jira
  - github
  grupo: '14'
  autor:
    nombre: Macarena Alimena
    github: MackyAlimena
  colaboradores: []
  responsables:
  - MackyAlimena
  madurez: usado-en-proyecto
  relacionados: []
---

# Status Reporter semanal / Documentador de progreso

Consolida los datos reales de Jira Cloud (`vaiven-app.atlassian.net`), la actividad reciente de Git y el inventario de agentes para generar el reporte semanal de avance con evaluación RAG (Red/Amber/Green).

## Antes de correr nada

```bash
cp .env.example .env    # completar JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN
```

Se requieren credenciales válidas en `.env` para consultar la API REST v3 de Jira. `scripts/sync-all-jira.py` viaja sólo porque el reporte lee de ahí el mapeo de tareas madre (`MAPEO_COMPLETO`); adaptalo a tu backlog.

## El protocolo

**1. Generar o actualizar el reporte semanal.**

```bash
# Para la semana en curso (o re-ejecución de actualización)
python3 scripts/reporte-semanal.py --semana 01 --output salidas/reportes-semanales/status-report-semana-01.txt

# Para una semana pasada o corrida retroactiva con fecha límite
python3 scripts/reporte-semanal.py --semana 02 --hasta 2026-08-30
```

El script realiza lo siguiente:
- Consulta las 37 issues del backlog (`SCRUM-9`…`SCRUM-45`) en Jira Cloud.
- Clasifica las tareas en *Done*, *In Progress* y *To Do*.
- Calcula el rango de fechas que abarca la semana (ej: *del 17/08/2026 al 23/08/2026*).
- Calcula el porcentaje de avance y asigna el semáforo RAG: Rojo si hay más de 15 issues en curso; Verde si hay alguna en curso o terminada; Ámbar si no hay ninguna. No evalúa blockers: los riesgos de la sección 6 los completa una persona.
- Incorpora la actividad de commits de Git (`git log --until=...`).
- Lee `inventario.md` para incluir el conteo de agentes operando y en construcción.
- Escribe o **refresca** el reporte estructurado en `salidas/status-report-semana-XX.txt`.

**2. Verificar el archivo generado.**

Abrir `salidas/status-report-semana-XX.txt` y verificar que contenga el período evaluado y las 7 secciones del reporte:
1. Resumen Ejecutivo de Métricas.
2. Desglose por Tarea Madre / Épica.
3. Detalle de Trabajo en Curso (WIP).
4. Actividad Reciente en GitHub.
5. Estado del Inventario de Agentes.
6. Riesgos & Blockers Destacados.
7. Próximos Hitos.

**3. Registrar la evidencia en el inventario.**

Tras generar el reporte de la semana, actualizar `inventario.md` agregando o actualizando la fila correspondiente al Agente 4.1 en la tabla `## Operando`.

```markdown
| **4.1** | [Status Reporter semanal](agentes/4.1-status-reporter-semanal.md) | 🟡 `humano` | Dirección → `vaiven-app.atlassian.net` | [`salidas/reportes-semanales/status-report-semana-01.txt`](salidas/reportes-semanales/status-report-semana-01.txt) · 23/08 · 37 issues procesadas |
```

## Comportamiento ante re-ejecución y reportes pasados

- **Re-ejecución**: Correr el script sobre una semana existente sobreescribe/refresca el archivo con los datos más recientes.
- **Reportes retroactivos**: Pasar `--hasta YYYY-MM-DD` acota la actividad de commits e indica la fecha de corte histórica en la cabecera. **No reconstruye Jira**: los estados, el avance y el RAG son los de hoy.

## Ejemplo de uso

**Pedido:** Generá el status report de la semana 5.

**Resultado:** Consulta Jira y Git, calcula el estado RAG y deja el reporte en salidas/reportes-semanales/.
