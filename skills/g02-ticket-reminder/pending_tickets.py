#!/usr/bin/env python3
"""Tickets de los devs que vencen el jueves de esta semana y todavía no están terminados.

Uso:
    multica issue list --output json > issues.json
    multica workspace member list --output json > members.json
    python3 pending_tickets.py issues.json --members members.json --devs "usuario-dev1,usuario-dev2"
    python3 pending_tickets.py issues.json --members members.json --devs "..." --dia 2026-11-05

Por defecto toma el jueves de la semana en curso (o el próximo jueves si hoy es viernes a domingo).

Salida (JSON) y código:
    0 = no hay tickets pendientes -> no avisar nada
    1 = hay tickets pendientes    -> avisar (la lista viene agrupada por dev)
"""
import json
import os
import sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

DONE = {"done", "completed", "closed", "finalizado", "hecho", "cancelled", "canceled", "cancelado"}
TZ = ZoneInfo("America/Argentina/Buenos_Aires")


def load(path):
    with open(os.path.expanduser(path), encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        for k in ("issues", "data", "items", "members"):
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


def members(path):
    """assignee_id -> (nombre a mostrar, alias: nombre, usuario, email y parte local del email)."""
    out = {}
    for m in load(path) if path else []:
        if not isinstance(m, dict):
            continue
        user = m.get("user") if isinstance(m.get("user"), dict) else {}
        uid = m.get("user_id") or user.get("id") or m.get("id")
        if not uid:
            continue
        vals = [m.get(k) or user.get(k) for k in ("name", "display_name", "username", "handle", "email")]
        vals = [str(v).strip() for v in vals if v]
        aliases = {v.lower() for v in vals} | {v.split("@")[0].lower() for v in vals if "@" in v}
        out[uid] = (vals[0] if vals else uid, aliases)
    return out


def this_thursday(today):
    """Jueves de la semana en curso; de viernes a domingo, el jueves siguiente."""
    delta = (3 - today.weekday()) % 7
    return today + timedelta(days=delta)


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)

    def opt(name, default=None):
        return args[args.index(name) + 1] if name in args else default

    today = datetime.now(TZ).date()
    dia = date.fromisoformat(opt("--dia")) if opt("--dia") else this_thursday(today)
    names = members(opt("--members"))
    devs = {d.strip().lower() for d in (opt("--devs") or "").split(",") if d.strip()}

    pendientes = {}
    for i in load(args[0]):
        if to_date(i.get("due_date")) != dia:
            continue
        status = str(i.get("status_name") or i.get("status") or "").strip()
        if str(i.get("status_category") or "").lower() in DONE or status.lower() in DONE:
            continue
        uid = i.get("assignee_id")
        if i.get("assignee_type") not in (None, "member") or not uid:
            continue
        name, aliases = names.get(uid, (uid, {str(uid).lower()}))
        if devs and not (aliases & devs):
            continue
        pendientes.setdefault(name, {"assignee_id": uid, "tickets": []})["tickets"].append({
            "id": i.get("id"),
            "ticket": str(i.get("identifier") or i.get("number") or i.get("id")),
            "titulo": (i.get("title") or "").strip(),
            "estado": status or "sin estado",
        })

    total = sum(len(v["tickets"]) for v in pendientes.values())
    print(json.dumps({"vence": dia.isoformat(), "dias_restantes": (dia - today).days,
                      "tickets_pendientes": total, "por_dev": pendientes}, ensure_ascii=False, indent=2))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
