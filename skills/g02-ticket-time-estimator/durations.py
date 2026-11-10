#!/usr/bin/env python3
"""Cuánto tardaron los tickets terminados en Multica, para estimar cuánto va a llevar uno nuevo.

Uso:
    multica issue list --output json > issues.json

    # Historial completo de tickets terminados (para elegir tickets parecidos)
    python3 durations.py issues.json

    # Resumen por persona y por label
    python3 durations.py issues.json --resumen

    # Estimación a partir de tickets parecidos (de todo el equipo o de una persona)
    python3 durations.py issues.json --ids ZEST-12,ZEST-18,ZEST-21
    python3 durations.py issues.json --ids ZEST-12,ZEST-18,ZEST-21 --persona <assignee_id>
    python3 durations.py issues.json --label backend --persona <assignee_id>

Duración de un ticket = días hábiles (lunes a viernes) entre el inicio y el cierre.
    Inicio: start_date si está cargada; si no, created_at.
    Cierre: updated_at del ticket terminado (aproximación: es la última modificación).
"""
import json
import statistics
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta

DONE = {"done", "completed", "closed", "finalizado", "hecho"}


def load(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        for k in ("issues", "data", "items"):
            if isinstance(data.get(k), list):
                return data[k]
    return data if isinstance(data, list) else []


def to_date(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00")).date()
    except ValueError:
        try:
            return date.fromisoformat(str(s)[:10])
        except ValueError:
            return None


def business_days(a, b):
    """Días hábiles entre a y b (mínimo 1 si se cerró el mismo día)."""
    if b < a:
        return None
    n, d = 0, a
    while d < b:
        d += timedelta(days=1)
        if d.weekday() < 5:
            n += 1
    return max(n, 1)


def is_done(i):
    return (str(i.get("status_category") or "").lower() in DONE
            or str(i.get("status_name") or i.get("status") or "").lower() in DONE)


def label_names(i):
    return [l.get("name", "") if isinstance(l, dict) else str(l) for l in (i.get("labels") or [])]


def finished(issues):
    rows = []
    for i in issues:
        if not is_done(i):
            continue
        start = to_date(i.get("start_date")) or to_date(i.get("created_at"))
        end = to_date(i.get("updated_at"))
        if not start or not end:
            continue
        dias = business_days(start, end)
        if dias is None:
            continue
        rows.append({
            "id": str(i.get("identifier") or i.get("number") or i.get("id")),
            "persona": i.get("assignee_id") if i.get("assignee_type") in (None, "member") else None,
            "dias": dias,
            "labels": label_names(i),
            "inicio_estimado": not i.get("start_date"),
            "titulo": (i.get("title") or "").strip(),
        })
    return rows


def stats(values):
    v = sorted(values)
    if not v:
        return None
    q = statistics.quantiles(v, n=4, method="inclusive") if len(v) >= 2 else [v[0], v[0], v[0]]
    return {"tickets": len(v), "mediana": round(statistics.median(v), 1),
            "rango_probable": [round(q[0], 1), round(q[2], 1)], "min": v[0], "max": v[-1]}


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)

    def opt(name):
        return args[args.index(name) + 1] if name in args else None

    rows = finished(load(args[0]))
    if not rows:
        sys.exit("No encontré tickets terminados con fechas.")

    ids, persona, label = opt("--ids"), opt("--persona"), opt("--label")
    if ids or label:
        sel = rows
        if ids:
            wanted = {x.strip() for x in ids.split(",") if x.strip()}
            sel = [r for r in sel if r["id"] in wanted]
        if label:
            sel = [r for r in sel if label.lower() in (l.lower() for l in r["labels"])]
        equipo = stats([r["dias"] for r in sel])
        out = {"base": [r["id"] for r in sel], "equipo": equipo}
        # Estimación para cada persona: mediana del equipo en tickets parecidos × su ritmo habitual
        todas = stats([r["dias"] for r in rows])
        por_persona = {}
        for p in sorted({r["persona"] for r in rows if r["persona"]}):
            suyas = stats([r["dias"] for r in rows if r["persona"] == p])
            parecidos = [r["dias"] for r in sel if r["persona"] == p]
            ritmo = round(suyas["mediana"] / todas["mediana"], 2) if suyas and todas and todas["mediana"] else None
            est = round(equipo["mediana"] * ritmo, 1) if equipo and ritmo else None
            por_persona[p] = {"estimacion_dias": est, "ritmo_vs_equipo": ritmo,
                              "tickets_terminados": suyas["tickets"] if suyas else 0,
                              "tickets_parecidos_propios": len(parecidos),
                              "mediana_parecidos_propios": round(statistics.median(parecidos), 1) if parecidos else None}
        out["por_persona"] = por_persona
        if persona:
            propios = [r for r in sel if r["persona"] == persona]
            out["persona"] = {"id": persona, **(stats([r["dias"] for r in propios]) or {"tickets": 0})}
            # Ritmo relativo de la persona frente al equipo, sobre TODO su historial
            todas = stats([r["dias"] for r in rows])
            suyas = stats([r["dias"] for r in rows if r["persona"] == persona])
            if todas and suyas and todas["mediana"]:
                out["persona"]["ritmo_vs_equipo"] = round(suyas["mediana"] / todas["mediana"], 2)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    if "--resumen" in args:
        out = {"equipo": stats([r["dias"] for r in rows]), "por_persona": {}, "por_label": {}}
        by_p, by_l = defaultdict(list), defaultdict(list)
        for r in rows:
            by_p[r["persona"] or "sin asignar"].append(r["dias"])
            for l in r["labels"]:
                by_l[l].append(r["dias"])
        out["por_persona"] = {k: stats(v) for k, v in by_p.items()}
        out["por_label"] = {k: stats(v) for k, v in by_l.items()}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    print("id\tdias_habiles\tpersona\tlabels\ttitulo")
    for r in sorted(rows, key=lambda r: r["dias"]):
        flag = "*" if r["inicio_estimado"] else ""
        print(f"{r['id']}\t{r['dias']}{flag}\t{r['persona'] or ''}\t{','.join(r['labels'])}\t{r['titulo']}")
    print("\n* inicio tomado de created_at (el ticket no tenía start_date).")


if __name__ == "__main__":
    main()
