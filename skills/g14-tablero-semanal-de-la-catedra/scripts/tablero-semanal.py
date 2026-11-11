#!/usr/bin/env python3
"""tablero-semanal.py — Agente Tablero semanal de la cátedra (parte determinista).

Junta los datos para cargar la pestaña «Equipo 14» del tablero de la cátedra:
qué semanas faltan, qué filas del cronograma hay que agregar o actualizar y con
qué fechas, y qué PRs de vaiven-app cayeron en cada semana. Calcula el desvío y,
si se le pasan los colores de las cinco áreas, el «General».

No escribe en la planilla. Nunca. Lee el CSV que publica el link compartido.

Reglas que aplica (las mismas que usa el equipo al cargar a mano):
  - Una tarea está terminada cuando quedó lista para revisión: la fecha real es el día en
    que se abrió el último PR de sus subtareas. Si no hay PR, la primera entrada a
    «Testing/Pruebas» en Jira, o a «Done/Finalizada» si no pasó por revisión.
  - F. Fin L. Base es lo comprometido al planificar y no se mueve. Si la fila ya está en la
    planilla, se usa la de la planilla. Si es nueva, se propone el fin del sprint de Jira
    marcado «(confirmar)»: las fechas de sprint en Jira se editaron después de planificar.
    Desvío = L. Base − Real, en días.
  - General: Rojo si hay ≥1 rojo o ≥3 amarillos; Amarillo si hay ≥1 amarillo; Verde en el resto.

Uso:
  python3 scripts/tablero-semanal.py                      # semanas vacías hasta hoy
  python3 scripts/tablero-semanal.py --hoy 2026-10-15
  python3 scripts/tablero-semanal.py --general Verde,Amarillo,Verde,Verde,Verde

Credenciales: JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN (entorno o .env).
PRs: CLI `gh` autenticado con lectura sobre vaiven-austral/vaiven-app.
Solo stdlib.
"""

import argparse
import base64
import csv
import difflib
import datetime as dt
import io
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIMEOUT = 30

PLANILLA = "1tA2CFxUesISCr39-MmhhdxwmitZKZBhTdOjfpSGjCec"
GID_EQUIPO_14 = "627974951"
REPO_APP = "vaiven-austral/vaiven-app"
REPO_DIRECCION = "vaiven-austral/vaiven-direccion"
AREAS = ["Alcance", "Cronograma", "Incidentes", "Calidad", "Riesgos"]
ESTADOS_REVISION = {"testing", "pruebas"}
ESTADOS_HECHO = {"done", "finalizada"}


# ---------- utilidades ----------

def credenciales():
    vals = {k: os.environ.get(k, "") for k in ("JIRA_BASE_URL", "JIRA_EMAIL", "JIRA_API_TOKEN")}
    env = ROOT / ".env"
    if env.exists():
        for linea in env.read_text(encoding="utf-8").splitlines():
            if "=" in linea and not linea.strip().startswith("#"):
                k, v = linea.split("=", 1)
                if k.strip() in vals and not vals[k.strip()]:
                    vals[k.strip()] = v.strip().strip('"').strip("'")
    if not all(vals.values()):
        sys.exit("Faltan credenciales de Jira (JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN).")
    return vals


def jira(cred, ruta, params=None):
    url = cred["JIRA_BASE_URL"].rstrip("/") + ruta
    if params:
        url += "?" + urllib.parse.urlencode(params)
    auth = base64.b64encode(f'{cred["JIRA_EMAIL"]}:{cred["JIRA_API_TOKEN"]}'.encode()).decode()
    req = urllib.request.Request(url, headers={"Authorization": f"Basic {auth}", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8"))


ARGENTINA = dt.timezone(dt.timedelta(hours=-3))


def fecha_iso(s):
    """Fecha de Jira (con zona o en UTC) -> fecha en hora argentina."""
    if not s:
        return None
    s = s.replace("Z", "+00:00")
    if len(s) > 5 and s[-5] in "+-" and s[-3] != ":":  # -0300 -> -03:00
        s = s[:-2] + ":" + s[-2:]
    return dt.datetime.fromisoformat(s).astimezone(ARGENTINA).date()


def ddmmaa(d):
    return d.strftime("%d/%m/%y") if d else ""


def calcular_general(colores):
    colores = [c.strip().capitalize() for c in colores]
    if colores.count("Rojo") >= 1 or colores.count("Amarillo") >= 3:
        return "Rojo"
    if colores.count("Amarillo") >= 1:
        return "Amarillo"
    return "Verde"


# ---------- planilla ----------

def leer_planilla():
    url = f"https://docs.google.com/spreadsheets/d/{PLANILLA}/export?format=csv&gid={GID_EQUIPO_14}"
    with urllib.request.urlopen(url, timeout=TIMEOUT) as r:
        filas = list(csv.reader(io.StringIO(r.read().decode("utf-8"))))

    semanas, areas, cronograma, incidentes = [], {}, [], []
    seccion = None
    for fila in filas:
        celdas = [c.strip() for c in fila]
        if not any(celdas):
            continue
        if celdas[0] == "ÁREA":
            for i, c in enumerate(celdas[1:21], start=1):
                partes = c.split()
                if len(partes) == 2 and partes[1].startswith("Sem-"):
                    semanas.append({"col": i, "nombre": partes[1], "dd_mm": partes[0]})
            seccion = "estado"
            continue
        if seccion == "estado" and celdas[0] in AREAS + ["General"]:
            areas[celdas[0]] = celdas
            continue
        if len(celdas) > 1 and celdas[1] == "Actividades Clave":
            seccion = "cronograma"
            continue
        if len(celdas) > 1 and celdas[1] == "Descripción":
            seccion = "incidentes"
            continue
        if len(celdas) > 1 and celdas[1] in ("INCIDENTES", "PRODUCTO", "CRONOGRAMA"):
            seccion = None
            continue
        if seccion == "cronograma" and len(celdas) > 12 and celdas[1]:
            cronograma.append({"actividad": celdas[1], "estado": celdas[7], "avance": celdas[8],
                               "l_base": celdas[9], "estimado": celdas[10], "real": celdas[11],
                               "desvio": celdas[12]})
        elif seccion == "incidentes" and len(celdas) > 7 and celdas[1]:
            incidentes.append({"descripcion": celdas[1], "estado": celdas[7], "criticidad": celdas[8]})
    return semanas, areas, cronograma, incidentes


def lunes_de(sem, anio):
    d, m = sem["dd_mm"].split("/")
    return dt.date(anio, int(m), int(d))


# ---------- jira ----------

def tareas_del_rango(cred, desde, hasta):
    """Tareas (no subtareas) cuyo sprint termina dentro de [desde, hasta]."""
    jql = ('project = SCRUM AND issuetype not in subTaskIssueTypes() AND issuetype != Epic '
           f'AND updated >= "{(desde - dt.timedelta(days=45)).isoformat()}" ORDER BY key ASC')
    datos = jira(cred, "/rest/api/3/search/jql", {
        "jql": jql, "maxResults": 100,
        "fields": "summary,status,issuetype,customfield_10020,assignee"})
    tareas = []
    for issue in datos.get("issues", []):
        f = issue["fields"]
        sprints = f.get("customfield_10020") or []
        if not sprints:
            continue
        sp = sprints[-1]
        fin = fecha_iso(sp.get("endDate", ""))
        if not fin or not (desde <= fin <= hasta):
            continue
        tareas.append({"key": issue["key"], "resumen": f["summary"], "estado_jira": f["status"]["name"],
                       "sprint": sp.get("name", ""), "l_base": fin,
                       "responsable": (f.get("assignee") or {}).get("displayName", "")})
    return tareas


def fecha_real(cred, key):
    """Primera entrada a revisión, o a hecho si nunca pasó por revisión."""
    log = jira(cred, f"/rest/api/3/issue/{key}/changelog", {"maxResults": 100})
    revision = hecho = None
    for h in log.get("values", []):
        for it in h["items"]:
            if it["field"] != "status":
                continue
            destino = (it.get("toString") or "").lower()
            if destino in ESTADOS_REVISION and not revision:
                revision = fecha_iso(h["created"])
            if destino in ESTADOS_HECHO and not hecho:
                hecho = fecha_iso(h["created"])
    return revision or hecho


def subtareas(cred, key):
    datos = jira(cred, "/rest/api/3/search/jql", {"jql": f"parent = {key}", "fields": "summary", "maxResults": 100})
    return [i["key"] for i in datos.get("issues", [])]


def fecha_ultimo_pr(claves, prs):
    """Día en que se abrió el último PR que nombra alguna de las claves (rama o título)."""
    import re
    patrones = [re.compile(rf"\b{re.escape(k)}\b", re.I) for k in claves]
    fechas = [fecha_iso(p["createdAt"]) for p in prs if "error" not in p
              and any(pt.search(p["title"]) or pt.search(p["headRefName"]) for pt in patrones)]
    return max(fechas) if fechas else None


def estado_planilla(estado_jira):
    e = estado_jira.lower()
    if e in ESTADOS_HECHO:
        return "Finaliz.", "100%"
    if e in ESTADOS_REVISION:
        return "En revisión", ""
    if e in ("en curso", "in progress"):
        return "En curso", ""
    return "Sin iniciar", "0%"


def base_de(previa, tarea):
    """L. Base de la planilla si la fila existe; si no, el fin del sprint de Jira."""
    if previa and previa["l_base"]:
        return dt.datetime.strptime(previa["l_base"], "%d/%m/%y").date()
    return tarea["l_base"]


# ---------- github ----------

def prs_del_rango(desde, hasta):
    cmd = ["gh", "pr", "list", "-R", REPO_APP, "--state", "all", "--limit", "300",
           "--search", f"updated:>={desde.isoformat()}" + (f" created:<={hasta.isoformat()}" if hasta else ""),
           "--json", "number,title,state,createdAt,mergedAt,headRefName"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=60)
        return json.loads(res.stdout)
    except Exception as e:  # sin gh o sin permiso: se avisa, no se inventa
        return [{"error": f"No se pudieron leer los PRs de {REPO_APP}: {e}"}]


def novedades_direccion(desde, hasta):
    """Commits de vaiven-direccion en la semana: de ahí salen incidentes y riesgos."""
    cmd = ["gh", "api", "-X", "GET", f"repos/{REPO_DIRECCION}/commits",
           "-f", f"since={desde.isoformat()}T00:00:00-03:00",
           "-f", f"until={hasta.isoformat()}T23:59:59-03:00", "-f", "per_page=100",
           "--jq", ".[] | [.commit.author.date, .commit.message] | @tsv"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=60)
    except Exception as e:
        return [f"⚠️ No se pudo leer {REPO_DIRECCION}: {e}"]
    return [f"{l.split(chr(9))[0][:10]} · {l.split(chr(9))[1].split(chr(92) + 'n')[0]}"
            for l in res.stdout.splitlines() if chr(9) in l]


def avance_global(cred):
    """Horas estimadas de tareas finalizadas sobre el total de tareas con sprint."""
    datos = jira(cred, "/rest/api/3/search/jql", {
        "jql": "project = SCRUM AND issuetype = Tarea AND sprint is not EMPTY",
        "fields": "status,timeoriginalestimate,customfield_10020", "maxResults": 100})
    total = hecho = 0.0
    fin = None
    for i in datos.get("issues", []):
        h = (i["fields"].get("timeoriginalestimate") or 0) / 3600
        total += h
        if i["fields"]["status"]["name"].lower() in ESTADOS_HECHO:
            hecho += h
        for sp in i["fields"].get("customfield_10020") or []:
            d = fecha_iso(sp.get("endDate", ""))
            fin = max(fin, d) if fin and d else (d or fin)
    return (round(100 * hecho / total) if total else None), hecho, total, fin


# ---------- salida ----------

def fuente(f):
    if f["real_pr"] and f["real_jira"] and f["real_pr"] != f["real_jira"]:
        return (f"Último PR abierto el {ddmmaa(f['real_pr'])}; en Jira pasó a revisión el "
                f"{ddmmaa(f['real_jira'])}. Con la fecha de Jira, el desvío sería "
                f"{(f['base'] - f['real_jira']).days}.")
    return "Fecha del último PR abierto." if f["real_pr"] else "Fecha de Jira: la tarea no tiene PR asociado."


def imprimir(salida, objetivo, menciones):
    out = []
    w = out.append
    if menciones:
        w(" ".join("@" + m for m in menciones) + "\n")
    w(f"**Corte:** {ddmmaa(dt.date.fromisoformat(salida['hoy']))} · "
      f"[planilla](https://docs.google.com/spreadsheets/d/{PLANILLA}/edit#gid={GID_EQUIPO_14}) · "
      "este issue **no escribe en la planilla**: la carga el PM y después lo cierra.\n")
    if not objetivo:
        w("✅ No hay semanas vacías hasta hoy.")
        return "\n".join(out)
    nombres = ", ".join(s["semana"] for s in salida["semanas"])
    w(f"> ⚠️ **Semanas sin cargar:** {nombres}.\n")
    ag = salida["avance_global"]
    w("## Encabezado del cronograma\n")
    w(f"- **Avance Global [%]:** {ag[0]} % ({ag[1]:.0f} de {ag[2]:.0f} h estimadas en Jira, tareas finalizadas)")
    w(f"- **Fecha de Fin Prevista:** {ddmmaa(ag[3])} (fin del último sprint de Jira)\n")
    for s in salida["semanas"]:
        w(f"## {s['semana']} ({ddmmaa(dt.date.fromisoformat(s['desde']))} a {ddmmaa(dt.date.fromisoformat(s['hasta']))})\n")
        w("### Estado semanal — decidís vos\n")
        w("Elegí un color por área con la evidencia de abajo. El General no se elige: "
          "Rojo si hay ≥1 rojo o ≥3 amarillos; Amarillo si hay ≥1 amarillo; Verde en el resto. "
          "Motivo y acción se escriben «Sem-NN: …» sólo si el área no es Verde.\n")
        w("| Área | Color | Motivo | Acción |\n|---|---|---|---|")
        for a in AREAS:
            w(f"| {a} | | | |")
        w("| **General** | (calculado) | | |\n")
        w("### Cronograma\n")
        w("| Actividad | Estado | Avance | F. Fin L. Base | F. Fin Estimado | F. Fin Real | Desvío | Comentarios | Jira | ¿Ya está en la planilla? |")
        w("|---|---|---|---|---|---|---|---|---|---|")
        for f in s["cronograma"]:
            lb = f["l_base_planilla"] or f"{ddmmaa(f['l_base'])} (confirmar)"
            desvio = "" if f["desvio"] is None else str(f["desvio"])
            w(f"| {f['resumen']} | {f['estado']} | {f['avance']} | {lb} | {lb.split()[0]} | "
              f"{ddmmaa(f['real'])} | {desvio} | {fuente(f)} | {f['key']} | "
              f"{('sí: «' + f['ya_en_planilla'] + '»') if f['ya_en_planilla'] else 'no, fila nueva'} |")
        if not s["cronograma"]:
            w("| Ninguna tarea de Jira cierra su sprint en esta semana | | | | | | | | | |")
        w("\nF. Fin Estimado = L. Base salvo que haya un cambio de pronóstico. Desvío = L. Base − Real.\n")
        w("### Evidencia de la semana\n")
        w("**PRs de vaiven-app**\n")
        for p in s["prs"] or [{"error": "ninguno"}]:
            if "error" in p:
                w(f"- {p['error']}")
                continue
            cuando = f"mergeado {ddmmaa(fecha_iso(p['mergedAt']))}" if p.get("mergedAt") else ("abierto" if p["state"] == "OPEN" else p["state"].lower())
            w(f"- #{p['number']} {p['title']} ({cuando})")
        w("\n**Novedades en vaiven-direccion** (de acá salen incidentes y riesgos)\n")
        for n in s["direccion"] or ["sin commits en la semana"]:
            w(f"- {n}")
        w("")
    w("## Incidentes\n")
    w("Columnas: Descripción · Estado · Criticidad · F. Alta · F. Límite · F. Cierre · Vencido · Resolución. "
      "Si en la evidencia hay un incidente nuevo, se agrega una fila; los abiertos se actualizan.\n")
    if salida["incidentes_abiertos"]:
        for i in salida["incidentes_abiertos"]:
            w(f"- Abierto en la planilla: {i['descripcion']} ({i['criticidad']})")
    else:
        w("- No hay incidentes abiertos en la planilla.")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hoy", help="fecha de corte YYYY-MM-DD (por defecto, hoy)")
    ap.add_argument("--semana", action="append", help="forzar una semana, p. ej. Sem-09 (repetible)")
    ap.add_argument("--general", help="cinco colores en orden Alcance,Cronograma,Incidentes,Calidad,Riesgos")
    ap.add_argument("--mencionar", default="", help="usuarios de GitHub separados por coma")
    ap.add_argument("--json", action="store_true", help="salida en JSON en vez de Markdown")
    args = ap.parse_args()

    if args.general:
        colores = args.general.split(",")
        if len(colores) != 5:
            sys.exit("--general pide exactamente cinco colores.")
        print(calcular_general(colores))
        return

    hoy = dt.date.fromisoformat(args.hoy) if args.hoy else dt.datetime.now(ARGENTINA).date()
    cred = credenciales()
    semanas, areas, cronograma, incidentes = leer_planilla()

    general = areas.get("General", [])
    if args.semana:
        objetivo = [s for s in semanas if s["nombre"] in args.semana]
    else:
        objetivo = [s for s in semanas
                    if lunes_de(s, hoy.year) <= hoy and not (general[s["col"]] if s["col"] < len(general) else "")]

    def buscar_en_planilla(resumen):
        """La planilla reescribe los nombres a mano: se acepta un parecido alto, y se avisa."""
        mejor, puntaje = None, 0.0
        for c in cronograma:
            r = difflib.SequenceMatcher(None, resumen.lower(), c["actividad"].lower()).ratio()
            if r > puntaje:
                mejor, puntaje = c, r
        return mejor if puntaje >= 0.6 else None

    salida = {"hoy": hoy.isoformat(), "semanas": [], "avance_global": avance_global(cred),
              "incidentes_abiertos": [i for i in incidentes if i["estado"].lower() != "cerrado"]}

    for sem in objetivo:
        desde = lunes_de(sem, hoy.year)
        hasta = desde + dt.timedelta(days=6)
        filas = []
        prs_amplio = prs_del_rango(desde - dt.timedelta(days=21), hasta)
        for t in tareas_del_rango(cred, desde, hasta):
            real_jira = fecha_real(cred, t["key"])
            real_pr = fecha_ultimo_pr([t["key"]] + subtareas(cred, t["key"]), prs_amplio)
            real = real_pr or real_jira
            estado, avance = estado_planilla(t["estado_jira"])
            previa = buscar_en_planilla(t["resumen"])
            base = base_de(previa, t)
            filas.append({
                **t, "estado": estado, "avance": avance, "real": real, "base": base,
                "real_pr": real_pr, "real_jira": real_jira,
                "desvio": (base - real).days if real else None,
                "ya_en_planilla": previa["actividad"] if previa else "",
                "l_base_planilla": previa["l_base"] if previa else "",
            })
        salida["semanas"].append({
            "semana": sem["nombre"], "desde": desde.isoformat(), "hasta": hasta.isoformat(),
            "cronograma": filas, "direccion": novedades_direccion(desde, hasta),
            "prs": [p for p in prs_amplio if "error" in p or
                    desde <= fecha_iso(p.get("mergedAt") or p["createdAt"]) <= hasta]})

    if args.json:
        print(json.dumps(salida, ensure_ascii=False, indent=2, default=str))
        return
    menciones = [m.strip() for m in args.mencionar.split(",") if m.strip()]
    print(imprimir(salida, objetivo, menciones))


if __name__ == "__main__":
    main()
