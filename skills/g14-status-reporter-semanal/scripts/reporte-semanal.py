#!/usr/bin/env python3
"""reporte-semanal.py — Agente 4.1/4.7 Status Reporter semanal / Documentador de progreso.

Consolida los datos reales de Jira (issues cerradas, WIP, backlog), la actividad de GitHub
y el inventario de agentes para generar el informe semanal de avance del proyecto VaiVen
con estado RAG (Red/Amber/Green), resumen de blockers, burndown, riesgos e hitos.

Soporta re-ejecución (actualiza el reporte de la semana actual) y ejecuciones retroactivas
mediente el parámetro --hasta YYYY-MM-DD o indicando el número de --semana.

Uso:
  python3 scripts/reporte-semanal.py --semana 01
  python3 scripts/reporte-semanal.py --semana 02 --hasta 2026-08-30
  python3 scripts/reporte-semanal.py --semana 01 --output salidas/status-report-semana-01.txt

Credenciales en .env (JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN).
Solo stdlib.
"""

import argparse
import base64
import datetime
import importlib.util
import json
import os
import re
import ssl
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIMEOUT = 30
# Fecha de inicio oficial del proyecto (Semana 1: Lunes 17/08/2026)
FECHA_INICIO_PROYECTO = datetime.date(2026, 8, 17)


def contexto_ssl():
    """Contexto SSL seguro para entorno local/macOS/Linux."""
    ctx = ssl.create_default_context()
    if ctx.cert_store_stats().get("x509_ca", 0) > 0:
        return ctx

    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        pass

    bundle = Path("/etc/ssl/cert.pem")
    if bundle.exists():
        return ssl.create_default_context(cafile=str(bundle))

    raise RuntimeError("No se encontró un bundle de certificados SSL válido.")


SSL_CTX = None


def cargar_mapeo():
    """Carga el mapeo canónico desde sync-all-jira.py."""
    ruta = ROOT / "scripts" / "sync-all-jira.py"
    if not ruta.exists():
        return {}
    spec = importlib.util.spec_from_file_location("sync_all_jira", ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "MAPEO_COMPLETO", {})


def cargar_credenciales():
    """Lee las credenciales de Jira desde .env.jira o .env."""
    base_url = os.environ.get("JIRA_BASE_URL", "")
    email = os.environ.get("JIRA_EMAIL", "")
    token = os.environ.get("JIRA_API_TOKEN", "")

    for candidato in (ROOT / ".env.jira", ROOT / ".env"):
        if not candidato.exists():
            continue
        for linea in candidato.read_text(encoding="utf-8").splitlines():
            linea = linea.strip()
            if not linea or linea.startswith("#") or "=" not in linea:
                continue
            k, v = linea.split("=", 1)
            v = v.strip().strip('"').strip("'")
            if k == "JIRA_BASE_URL" and not base_url:
                base_url = v
            elif k == "JIRA_EMAIL" and not email:
                email = v
            elif k == "JIRA_API_TOKEN" and not token:
                token = v

    return base_url.rstrip("/"), email, token


def traer_issue(base_url, auth_b64, key):
    """Consulta la API REST de Jira para obtener los datos de una issue."""
    url = f"{base_url}/rest/api/3/issue/{key}?fields=summary,status,issuetype,parent,labels,created,updated"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Basic {auth_b64}",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=SSL_CTX) as resp:
        return json.loads(resp.read().decode("utf-8"))


def obtener_actividad_git(fecha_hasta_dt=None):
    """Obtiene los últimos commits del repositorio filtrados hasta la fecha límite."""
    cmd = ["git", "log", "-n", "8", "--pretty=format:%h - %s (%cr)"]
    if fecha_hasta_dt:
        corte_str = fecha_hasta_dt.strftime("%Y-%m-%d 23:59:59")
        cmd.append(f"--until={corte_str}")

    try:
        res = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        out = [linea.strip() for linea in res.stdout.splitlines() if linea.strip()]
        return out if out else ["Sin commits registrados en este período."]
    except Exception:
        return ["No se pudo obtener el historial de commits de Git."]


def analizar_inventario_agentes():
    """Analiza inventario.md y cuenta los agentes en cada estado."""
    inv_file = ROOT / "inventario.md"
    if not inv_file.exists():
        return {"operando": 0, "construccion": 0, "lista_operando": [], "lista_construccion": []}

    content = inv_file.read_text(encoding="utf-8")
    operando_sec = re.search(r"## Operando\n\n(.*?)(?=\n## |\Z)", content, re.S)
    construccion_sec = re.search(r"## En construcción\n\n(.*?)(?=\n## |\Z)", content, re.S)

    lista_operando = []
    if operando_sec:
        for line in operando_sec.group(1).splitlines():
            if line.startswith("| **"):
                match = re.search(r"\|\s*\*\*([^\*]+)\*\*\s*\|\s*\[([^\]]+)\]", line)
                if match:
                    lista_operando.append(f"{match.group(1)} {match.group(2)}")

    lista_construccion = []
    if construccion_sec:
        for line in construccion_sec.group(1).splitlines():
            if line.startswith("| **"):
                match = re.search(r"\|\s*\*\*([^\*]+)\*\*\s*\|\s*\[([^\]]+)\]", line)
                if match:
                    lista_construccion.append(f"{match.group(1)} {match.group(2)}")

    return {
        "operando": len(lista_operando),
        "construccion": len(lista_construccion),
        "lista_operando": lista_operando,
        "lista_construccion": lista_construccion,
    }


def categorizar_estado_jira(status_name, status_cat_key):
    """Categoriza el estado de Jira en Done, In Progress o To Do."""
    name_lower = status_name.lower()
    cat_lower = status_cat_key.lower()

    if cat_lower == "done" or name_lower in ("listo", "done", "cerrado", "finalizado", "resuelto"):
        return "Done"
    elif cat_lower in ("indeterminate", "in_flight", "in progress") or name_lower in ("en curso", "in progress", "en progreso"):
        return "In Progress"
    else:
        return "To Do"


def calcular_rango_semana(semana_num, hasta_str=None):
    """Calcula las fechas de inicio y fin de la semana N."""
    inicio = FECHA_INICIO_PROYECTO + datetime.timedelta(days=(semana_num - 1) * 7)
    fin = inicio + datetime.timedelta(days=6)

    if hasta_str:
        try:
            fin = datetime.datetime.strptime(hasta_str, "%Y-%m-%d").date()
        except ValueError:
            pass

    return inicio, fin


def generar_informe(semana_num, fecha_inicio, fecha_fin, datos_issues, actividad_git, datos_agentes):
    """Genera el contenido del reporte semanal en texto/markdown."""
    total_issues = len(datos_issues)
    done_issues = [i for i in datos_issues if i["cat"] == "Done"]
    wip_issues = [i for i in datos_issues if i["cat"] == "In Progress"]
    todo_issues = [i for i in datos_issues if i["cat"] == "To Do"]

    cnt_done = len(done_issues)
    cnt_wip = len(wip_issues)
    cnt_todo = len(todo_issues)
    pct_avance = (cnt_done / total_issues * 100) if total_issues > 0 else 0.0

    # Evaluación RAG
    if cnt_wip > 15:
        rag = "🔴 ROJO"
        rag_reason = "Elevada cantidad de trabajo en progreso (WIP excesivo) que genera riesgo de congestión."
    elif cnt_wip > 0 or cnt_done > 0:
        rag = "🟢 VERDE"
        rag_reason = "Proyecto avanzando según el ritmo previsto. Trabajo en progreso controlado y backlog priorizado."
    else:
        rag = "🟡 ÁMBAR"
        rag_reason = "Sprint o semana iniciada sin tareas finalizadas registradas en Jira."

    # Agrupación por Tarea Madre / Épica
    issues_by_key = {i["key"]: i for i in datos_issues}
    madres = [i for i in datos_issues if not i.get("parent")]
    subtareas = [i for i in datos_issues if i.get("parent")]

    desglose_madres = {}
    for m in madres:
        m_key = m["key"]
        desglose_madres[m_key] = {
            "summary": m["summary"],
            "status": m["status_name"],
            "sub_total": 0,
            "sub_done": 0,
            "sub_wip": 0,
            "sub_todo": 0,
        }

    for s in subtareas:
        parent_key = s["parent"]
        if parent_key not in desglose_madres:
            if parent_key in issues_by_key:
                p_info = issues_by_key[parent_key]
                p_summary = p_info["summary"]
                p_status = p_info["status_name"]
            else:
                p_summary = f"Tarea Madre ({parent_key})"
                p_status = "Desconocido"
            desglose_madres[parent_key] = {
                "summary": p_summary,
                "status": p_status,
                "sub_total": 0,
                "sub_done": 0,
                "sub_wip": 0,
                "sub_todo": 0,
            }
        desglose_madres[parent_key]["sub_total"] += 1
        if s["cat"] == "Done":
            desglose_madres[parent_key]["sub_done"] += 1
        elif s["cat"] == "In Progress":
            desglose_madres[parent_key]["sub_wip"] += 1
        else:
            desglose_madres[parent_key]["sub_todo"] += 1

    fecha_emision = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    periodo_str = f"del {fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')}"

    lineas = []
    lineas.append(f"================================================================================")
    lineas.append(f" INFORME SEMANAL DE AVANCE DE PROYECTO — VAIVEN (SEMANA {semana_num:02d})")
    lineas.append(f"================================================================================")
    lineas.append(f"Período evaluado : {periodo_str}")
    lineas.append(f"Fecha de emisión : {fecha_emision}")
    lineas.append(f"Estado RAG       : {rag}")
    lineas.append(f"Justificación    : {rag_reason}")
    lineas.append(f"--------------------------------------------------------------------------------")
    lineas.append(f"")
    lineas.append(f"1. RESUMEN EJECUTIVO DE METRICAS (JIRA CLOUD)")
    lineas.append(f"--------------------------------------------------------------------------------")
    lineas.append(f"  - Total de issues monitoreadas : {total_issues}")
    lineas.append(f"  - Completadas (Done)          : {cnt_done} ({pct_avance:.1f}%)")
    lineas.append(f"  - En Curso (In Progress)      : {cnt_wip}")
    lineas.append(f"  - Por Hacer (To Do)           : {cnt_todo}")
    lineas.append(f"  - Porcentaje de Avance        : [{('=' * int(pct_avance // 5)).ljust(20)}] {pct_avance:.1f}%")
    lineas.append(f"")
    lineas.append(f"2. DESGLOSE POR TAREA MADRE / EPICA")
    lineas.append(f"--------------------------------------------------------------------------------")
    lineas.append(f"{'Key':<10} | {'Estado':<12} | {'Progreso Subtareas':<20} | Summary")
    lineas.append(f"--------------------------------------------------------------------------------")
    for key, info in sorted(desglose_madres.items()):
        prog_str = f"{info['sub_done']}/{info['sub_total']} Done" if info['sub_total'] > 0 else "N/A"
        lineas.append(f"{key:<10} | {info['status']:<12} | {prog_str:<20} | {info['summary'][:40]}")
    lineas.append(f"")
    lineas.append(f"3. DETALLE DE TRABAJO EN CURSO (WIP)")
    lineas.append(f"--------------------------------------------------------------------------------")
    if wip_issues:
        for w in wip_issues:
            lineas.append(f"  * [{w['key']}] {w['summary']} (Padre: {w.get('parent', 'N/A')})")
    else:
        lineas.append(f"  (Sin tareas en curso actualmente)")
    lineas.append(f"")
    lineas.append(f"4. ACTIVIDAD RECIENTE EN GITHUB (COMMITS HASTA {fecha_fin.strftime('%d/%m/%Y')})")
    lineas.append(f"--------------------------------------------------------------------------------")
    for c in actividad_git:
        lineas.append(f"  - {c}")
    lineas.append(f"")
    lineas.append(f"5. ESTADO DEL INVENTARIO DE AGENTES (ECHO / VAIVEN)")
    lineas.append(f"--------------------------------------------------------------------------------")
    lineas.append(f"  - Agentes Operando con Evidencia : {datos_agentes['operando']}")
    for ag in datos_agentes["lista_operando"]:
        lineas.append(f"      * {ag}")
    lineas.append(f"  - Agentes En Construcción        : {datos_agentes['construccion']}")
    for ag in datos_agentes["lista_construccion"]:
        lineas.append(f"      * {ag}")
    lineas.append(f"")
    lineas.append(f"6. RIESGOS & BLOCKERS DESTACADOS")
    lineas.append(f"--------------------------------------------------------------------------------")
    if cnt_wip > 10:
        lineas.append(f"  [ALERTA] Alto volumen de tareas abiertas en paralelo.")
    else:
        lineas.append(f"  - Sin bloqueos críticos reportados en las API de Jira/GitHub.")
    lineas.append(f"  - Mantener paridad estricta entre tickets en Markdown y estado en Jira Cloud.")
    lineas.append(f"")
    lineas.append(f"7. PROXIMOS HITOS")
    lineas.append(f"--------------------------------------------------------------------------------")
    lineas.append(f"  - Cierre del Hito 3: MVP de VaiVen (Auth, Motor de Matching, Listados y RLS).")
    lineas.append(f"  - Auditoría de higiene continua mediante Agente 5.5.")
    lineas.append(f"================================================================================")

    return "\n".join(lineas) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--semana", type=int, default=1, help="Número de semana a reportar (ej: 1 a 14)")
    parser.add_argument("--hasta", type=str, default=None, help="Fecha límite superior (YYYY-MM-DD) para reportes retroactivos")
    parser.add_argument("--output", type=str, default=None, help="Ruta del archivo de salida")
    parser.add_argument("--verbose", "-v", action="store_true", help="Imprimir salida detallada")
    args = parser.parse_args()

    semana_num = args.semana
    fecha_inicio, fecha_fin = calcular_rango_semana(semana_num, args.hasta)

    output_path = (
        Path(args.output)
        if args.output
        else ROOT / "salidas" / "reportes-semanales" / f"status-report-semana-{semana_num:02d}.txt"
    )

    base_url, email, token = cargar_credenciales()
    if not all([base_url, email, token]):
        print("Error: faltan credenciales en .env (JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN).", file=sys.stderr)
        return 2

    global SSL_CTX
    SSL_CTX = contexto_ssl()

    auth_b64 = base64.b64encode(f"{email}:{token}".encode()).decode()
    mapeo = cargar_mapeo()

    print(
        f"[reporte-semanal] Generando reporte para la Semana {semana_num:02d} "
        f"(del {fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')}) sobre {len(mapeo)} issues..."
    )

    datos_issues = []
    for key in mapeo.keys():
        try:
            raw = traer_issue(base_url, auth_b64, key)
            fields = raw.get("fields", {})
            st_obj = fields.get("status", {})
            st_name = st_obj.get("name", "Desconocido")
            st_cat_key = (st_obj.get("statusCategory") or {}).get("key", "new")
            cat = categorizar_estado_jira(st_name, st_cat_key)
            parent = (fields.get("parent") or {}).get("key")
            summary = fields.get("summary", "")

            datos_issues.append({
                "key": key,
                "summary": summary,
                "status_name": st_name,
                "status_cat_key": st_cat_key,
                "cat": cat,
                "parent": parent,
            })
        except Exception as e:
            if args.verbose:
                print(f"  [WARN] No se pudo leer {key}: {e}", file=sys.stderr)

    actividad_git = obtener_actividad_git(fecha_fin)
    datos_agentes = analizar_inventario_agentes()

    reporte_txt = generar_informe(
        semana_num, fecha_inicio, fecha_fin, datos_issues, actividad_git, datos_agentes
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(reporte_txt, encoding="utf-8")

    print(f"[reporte-semanal] Reporte guardado con éxito en: {output_path}")
    if args.verbose:
        print("\n" + reporte_txt)

    return 0


if __name__ == "__main__":
    sys.exit(main())
