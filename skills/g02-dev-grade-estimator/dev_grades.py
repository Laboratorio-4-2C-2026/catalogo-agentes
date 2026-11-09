#!/usr/bin/env python3
"""Nota orientativa por dev: cumplimiento de tickets de Multica + dificultad de lo terminado.

Uso:
    multica issue list --output json > issues.json
    multica workspace member list --output json > members.json
    python3 dev_grades.py issues.json --members members.json --desde 2026-10-01 --hasta 2026-10-29 \
        [--dificultad ~/.config/zest/dificultad.json] [--solo "Nombre 1,Nombre 2"]

Flujo:
  1. Si hay tickets terminados sin dificultad clasificada, el script los lista en "sin_clasificar"
     y termina con código 3. El agente los clasifica (1 = Baja, 2 = Media, 3 = Alta), los agrega
     al archivo de dificultad y vuelve a correr el script.
  2. Con todo clasificado, devuelve la nota de cada dev con su desglose (código 0).

Archivo de dificultad (JSON): {"ZEST-12": {"nivel": 2, "motivo": "front + back con formulario"}, ...}
"""
import json
import os
import sys
from datetime import date, datetime

DONE = {"done", "completed", "closed", "finalizado", "hecho"}
NIVELES = {1: "Baja", 2: "Media", 3: "Alta"}

# Rúbrica (mantener igual que rubrica.md)
PESO_CUMPLIMIENTO = 0.5
PESO_DIFICULTAD = 0.5


def load(path):
    with open(os.path.expanduser(path), encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        for k in ("issues", "data", "items", "members"):
            if isinstance(data.get(k), list):
                return data[k]
    return data


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


def is_done(i):
    return (str(i.get("status_category") or "").lower() in DONE
            or str(i.get("status_name") or i.get("status") or "").lower() in DONE)


def member_names(path):
    """assignee_id -> (nombre a mostrar, alias aceptados: nombre, usuario, email y parte local del email)."""
    names = {}
    if not path:
        return names
    for m in load(path) or []:
        if not isinstance(m, dict):
            continue
        user = m.get("user") if isinstance(m.get("user"), dict) else {}
        uid = m.get("user_id") or user.get("id") or m.get("id")
        if not uid:
            continue
        vals = [m.get(k) or user.get(k) for k in ("name", "display_name", "username", "handle", "email")]
        vals = [str(v).strip() for v in vals if v]
        aliases = {v.lower() for v in vals} | {v.split("@")[0].lower() for v in vals if "@" in v}
        names[uid] = (vals[0] if vals else uid, aliases)
    return names


def clamp(x, lo=1.0, hi=10.0):
    return max(lo, min(hi, x))


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)

    def opt(name, default=None):
        return args[args.index(name) + 1] if name in args else default

    hoy = date.today()
    desde = date.fromisoformat(opt("--desde")) if opt("--desde") else None
    hasta = date.fromisoformat(opt("--hasta")) if opt("--hasta") else hoy
    dif_path = os.path.expanduser(opt("--dificultad", "~/.config/zest/dificultad.json"))
    dificultad = load(dif_path) if os.path.exists(dif_path) else {}
    names = member_names(opt("--members"))
    solo = {s.strip().lower() for s in opt("--solo", "").split(",") if s.strip()}

    devs, sin_clasificar = {}, []
    for i in load(args[0]):
        if i.get("assignee_type") not in (None, "member") or not i.get("assignee_id"):
            continue
        name, aliases = names.get(i["assignee_id"], (i["assignee_id"], {str(i["assignee_id"]).lower()}))
        if solo and not (aliases & solo):
            continue
        due = to_date(i.get("due_date"))
        ref = due or to_date(i.get("created_at"))
        if ref is None or (desde and ref < desde) or ref > hasta:
            continue
        ident = str(i.get("identifier") or i.get("number") or i.get("id"))
        d = devs.setdefault(name, {"a_tiempo": [], "tarde": [], "vencidos": [], "en_curso": [], "terminados": []})
        if is_done(i):
            fin = to_date(i.get("updated_at"))  # aproximación de la fecha de cierre
            d["terminados"].append(ident)
            if due and fin and fin > due:
                d["tarde"].append(f"{ident} ({(fin - due).days} días tarde)")
            else:
                d["a_tiempo"].append(ident)
            if ident not in dificultad:
                sin_clasificar.append({"id": ident, "titulo": i.get("title"), "dev": name,
                                       "labels": [l.get("name", "") if isinstance(l, dict) else str(l)
                                                  for l in (i.get("labels") or [])],
                                       "descripcion": (i.get("description") or "")[:600]})
        elif due and due < hoy:
            d["vencidos"].append(f"{ident} (vencía {due:%d/%m})")
        else:
            d["en_curso"].append(ident)

    if sin_clasificar:
        print(json.dumps({"estado": "faltan_clasificar", "archivo_dificultad": dif_path,
                          "sin_clasificar": sin_clasificar}, ensure_ascii=False, indent=2))
        return 3

    # Dificultad total de cada dev y promedio del equipo
    totales = {n: sum(int(dificultad[t]["nivel"]) for t in d["terminados"]) for n, d in devs.items()}
    con_trabajo = [v for v in totales.values() if v > 0]
    promedio = sum(con_trabajo) / len(con_trabajo) if con_trabajo else 0

    out = {"periodo": {"desde": str(desde) if desde else None, "hasta": str(hasta)},
           "promedio_dificultad_equipo": round(promedio, 1), "devs": {}}
    for n, d in sorted(devs.items()):
        evaluables = len(d["a_tiempo"]) + len(d["tarde"]) + len(d["vencidos"])
        if evaluables:
            pct = (len(d["a_tiempo"]) + 0.5 * len(d["tarde"])) / evaluables
            p_cump = clamp(10 * pct)
        else:
            p_cump = None

        total = totales[n]
        ratio = total / promedio if promedio else None
        p_dif = clamp(8 + 5 * (ratio - 1)) if ratio is not None else None
        niveles = [int(dificultad[t]["nivel"]) for t in d["terminados"]]

        partes = [(p_cump, PESO_CUMPLIMIENTO), (p_dif, PESO_DIFICULTAD)]
        validas = [(p, w) for p, w in partes if p is not None]
        nota = sum(p * w for p, w in validas) / sum(w for _, w in validas) if validas else None

        out["devs"][n] = {
            "nota": round(nota * 2) / 2 if nota is not None else None,
            "cumplimiento": {
                "puntaje": round(p_cump, 1) if p_cump is not None else None,
                "a_tiempo": d["a_tiempo"], "tarde": d["tarde"], "vencidos_abiertos": d["vencidos"],
                "en_curso_sin_vencer": d["en_curso"],
            },
            "dificultad": {
                "puntaje": round(p_dif, 1) if p_dif is not None else None,
                "puntos": total, "vs_promedio_equipo": round(ratio, 2) if ratio is not None else None,
                "tickets": {NIVELES[k]: niveles.count(k) for k in (3, 2, 1)},
            },
        }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
