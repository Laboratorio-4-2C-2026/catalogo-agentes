#!/usr/bin/env python3
"""Chequea en el panel público de Lab4 KPIs si el Equipo 2 (Zest) tiene el día en estado COMPLETO.

Fuente: https://lab4-kpis.github.io/kpis/#/cumplimiento (vista pública v_public_compliance).

Uso:
    python3 check_kpis.py                 # chequea el último día evaluable cerrado (ayer o el último hábil)
    python3 check_kpis.py --date 2026-10-28
    python3 check_kpis.py --today         # chequea el día de hoy (todavía puede cambiar)

Salida: un JSON en stdout y el código de salida:
    0 = COMPLETO      -> no hay que hacer nada
    1 = NO completo   -> hay que crear el issue
    2 = no se pudo chequear (error de red, sin datos, etc.)

Opcional: si la variable de entorno LAB4_PROJECT_KEY tiene la clave **prod** del equipo,
también lista qué KPIs del catálogo no llegaron ese día.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

TEAM = 2
SITE = "https://lab4-kpis.github.io/kpis/"
DEFAULT_SUPABASE_URL = "https://rzlalzowistpiphmdqpp.supabase.co"
TZ = ZoneInfo("America/Argentina/Buenos_Aires")
LABELS = {"complete": "COMPLETO", "incomplete": "INCOMPLETO", "missing": "SIN REPORTE"}


def _ssl_context():
    """Usa los certificados de certifi si está instalado (el Python de python.org en Mac no trae los del sistema)."""
    import ssl
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


SSL_CTX = _ssl_context()


def http_get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": "zest-kpi-check", **(headers or {})})
    with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as r:
        return r.read().decode("utf-8")


def public_config():
    """URL de Supabase y clave pública: las mismas que usa el panel público en el navegador."""
    url = os.environ.get("LAB4_SUPABASE_URL")
    key = os.environ.get("LAB4_SUPABASE_PUBLISHABLE_KEY")
    if url and key:
        return url, key
    html = http_get(SITE)
    for src in re.findall(r'src="([^"]+\.js)"', html):
        js = http_get(urllib.parse.urljoin(SITE, src))
        k = re.search(r"sb_publishable_[A-Za-z0-9_\-]+", js)
        u = re.search(r"https://[a-z0-9]+\.supabase\.co", js)
        if k:
            return (url or (u.group(0) if u else DEFAULT_SUPABASE_URL)), k.group(0)
    raise RuntimeError("No encontré la clave pública en el sitio del panel.")


def rest(base, key, path, params, extra_headers=None):
    q = urllib.parse.urlencode(params, safe=".,:()")
    body = http_get(f"{base}/rest/v1/{path}?{q}", {"apikey": key, "Accept": "application/json", **(extra_headers or {})})
    return json.loads(body)


def missing_kpis(base, key, project_key, day):
    """Con la clave prod del equipo: KPIs activos del catálogo que no llegaron ese día (por recepción)."""
    h = {"X-Project-Key": project_key}
    catalog = rest(base, key, "kpi_catalog", {"select": "id,deprecated_at", "order": "id.asc"}, h)
    active = {k["id"] for k in catalog if not k.get("deprecated_at") or k["deprecated_at"] > day.isoformat()}
    start = dt.datetime.combine(day, dt.time(), TZ).astimezone(dt.timezone.utc)
    end = start + dt.timedelta(days=1)
    params = [("select", "kpi_id,reported_at"), ("env", "eq.prod"),
              ("reported_at", f"gte.{start:%Y-%m-%dT%H:%M:%SZ}"), ("reported_at", f"lt.{end:%Y-%m-%dT%H:%M:%SZ}")]
    q = urllib.parse.urlencode(params, safe=".,:")
    got = json.loads(http_get(f"{base}/rest/v1/measurement?{q}", {"apikey": key, "Accept": "application/json", **h}))
    received = {m["kpi_id"] for m in got}
    return sorted(active - received)


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group()
    g.add_argument("--date", help="Día a chequear (YYYY-MM-DD)")
    g.add_argument("--today", action="store_true", help="Chequear el día de hoy")
    args = p.parse_args()
    today = dt.datetime.now(TZ).date()

    try:
        base, key = public_config()
        rows = rest(base, key, "v_public_compliance", {
            "select": "team_number,project_name,report_date,valid_kpis,expected_kpis,status,score",
            "team_number": f"eq.{TEAM}", "order": "report_date.desc", "limit": "15"})
    except Exception as e:  # red, sitio caído, cambio en el portal
        print(json.dumps({"ok": False, "error": f"No se pudo consultar el panel: {e}"}, ensure_ascii=False))
        return 2

    if args.date:
        target = args.date
    elif args.today:
        target = today.isoformat()
    else:  # último día evaluable ya cerrado
        closed = [r["report_date"] for r in rows if r["report_date"] < today.isoformat()]
        target = closed[0] if closed else None

    row = next((r for r in rows if r["report_date"] == target), None)
    if row is None:
        print(json.dumps({"ok": False, "error": f"No hay fila del equipo {TEAM} para {target} "
                          "(día no evaluable o fuera del período)."}, ensure_ascii=False))
        return 2

    result = {
        "ok": True,
        "team": row["team_number"], "project": row["project_name"], "date": row["report_date"],
        "status": row["status"], "status_label": LABELS.get(row["status"], row["status"]),
        "valid_kpis": row["valid_kpis"], "expected_kpis": row["expected_kpis"],
        "complete": row["status"] == "complete",
        "panel": SITE + "#/cumplimiento",
    }
    pk = os.environ.get("LAB4_PROJECT_KEY")
    if pk and not result["complete"]:
        try:
            result["missing_kpis"] = missing_kpis(base, key, pk, dt.date.fromisoformat(target))
        except Exception as e:
            result["missing_kpis_error"] = str(e)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["complete"] else 1


if __name__ == "__main__":
    sys.exit(main())