#!/usr/bin/env python3
"""Valida demo-data/seed-data.json contra el esquema y las reglas reales del repo de Zest.

Uso:
    python3 validate_seed.py --repo ~/zest-agentes/zest --data ./entrega/demo-data

Lee del repo, en cada corrida:
  - backend/prisma/schema.prisma            -> valores válidos de los enums
  - backend/prisma/seed-data/ingredients.json -> catálogo de ingredientes
Reglas de los DTO: título <= 100, descripción <= 500, pasos <= 500, cantidad <= 12,
porciones 1..100, minutos 1..59, horas 1..23, color hexadecimal, imágenes jpg/png/webp.

Código de salida: 0 = válido, 1 = hay errores (se listan todos).
"""
import argparse
import json
import os
import re
import sys

HEX = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
HANDLE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
IMG = (".jpg", ".jpeg", ".png", ".webp")


def enums(schema_text):
    out = {}
    for name, body in re.findall(r"enum\s+(\w+)\s*\{([^}]*)\}", schema_text):
        out[name] = {v.strip() for v in body.split() if v.strip() and not v.strip().startswith("//")}
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True)
    p.add_argument("--data", required=True, help="Carpeta demo-data con seed-data.json e images/")
    a = p.parse_args()
    repo, data_dir = os.path.expanduser(a.repo), os.path.expanduser(a.data)

    with open(os.path.join(repo, "backend/prisma/schema.prisma"), encoding="utf-8") as f:
        en = enums(f.read())
    with open(os.path.join(repo, "backend/prisma/seed-data/ingredients.json"), encoding="utf-8") as f:
        catalogo = {n for grupo in json.load(f).values() for n in grupo}
    with open(os.path.join(data_dir, "seed-data.json"), encoding="utf-8") as f:
        data = json.load(f)

    errs = []
    E = errs.append

    def img_ok(where, rel):
        if not rel.lower().endswith(IMG):
            E(f"{where}: la imagen {rel} tiene que ser jpg, png o webp")
        elif not os.path.isfile(os.path.join(data_dir, rel)):
            E(f"{where}: no existe el archivo {rel}")
        elif os.path.getsize(os.path.join(data_dir, rel)) > 5 * 1024 * 1024:
            E(f"{where}: {rel} pesa más de 5 MB; achicarla")

    users = data.get("users", [])
    handles, emails = set(), set()
    for u in users:
        h = u.get("handle", "")
        w = f"usuario {h or '?'}"
        if not HANDLE.match(h): E(f"{w}: handle inválido (minúsculas, números, punto, guion)")
        if h in handles: E(f"{w}: handle repetido")
        handles.add(h)
        if not u.get("name"): E(f"{w}: falta name")
        em = u.get("email", "")
        if not EMAIL.match(em): E(f"{w}: email inválido")
        if em in emails: E(f"{w}: email repetido")
        emails.add(em)
        if not em.endswith(("@example.com", "@example.org", "@example.net")):
            E(f"{w}: usar un dominio reservado (@example.com) para no apuntar a casillas reales")
        if u.get("avatarUrl") and not str(u["avatarUrl"]).startswith("https://"):
            E(f"{w}: avatarUrl tiene que ser https")

    slugs = set()
    for r in data.get("recipes", []):
        s = r.get("slug", "")
        w = f"receta {s or '?'}"
        if not HANDLE.match(s): E(f"{w}: slug inválido")
        if s in slugs: E(f"{w}: slug repetido")
        slugs.add(s)
        if r.get("author") not in handles: E(f"{w}: autor desconocido {r.get('author')}")
        t = r.get("title", "")
        if not t or len(t) > 100: E(f"{w}: title vacío o de más de 100 caracteres")
        d = r.get("description", "")
        if not d or len(d) > 500: E(f"{w}: description vacía o de más de 500 caracteres")
        for campo, enum in (("category", "RecipeCategory"), ("timeUnit", "RecipeTimeUnit"), ("difficulty", "RecipeDifficulty")):
            if r.get(campo) not in en.get(enum, set()):
                E(f"{w}: {campo}={r.get(campo)!r} no es válido ({', '.join(sorted(en.get(enum, [])))})")
        tm = r.get("time")
        tope = {"MINUTOS": 59, "HORAS": 23}.get(r.get("timeUnit"))
        if not isinstance(tm, int) or tm < 1 or (tope and tm > tope):
            E(f"{w}: time={tm!r} fuera de rango (minutos 1..59, horas 1..23)")
        sv = r.get("servings")
        if not isinstance(sv, int) or not 1 <= sv <= 100: E(f"{w}: servings tiene que ser 1..100")
        ings = r.get("ingredients", [])
        if not ings: E(f"{w}: necesita al menos un ingrediente")
        vistos = set()
        for i in ings:
            n = i.get("name")
            if n not in catalogo: E(f"{w}: ingrediente fuera del catálogo: {n!r}")
            if n in vistos: E(f"{w}: ingrediente repetido: {n!r}")
            vistos.add(n)
            am = str(i.get("amount", ""))
            if not am or len(am) > 12: E(f"{w}: amount {am!r} vacío o de más de 12 caracteres")
            if i.get("unit") not in en.get("IngredientUnit", set()):
                E(f"{w}: unit {i.get('unit')!r} no es válida")
        steps = r.get("steps", [])
        if not steps: E(f"{w}: necesita al menos un paso")
        for k, st in enumerate(steps, 1):
            if not st or len(st) > 500: E(f"{w}: el paso {k} está vacío o tiene más de 500 caracteres")
        if not r.get("images"): E(f"{w}: no tiene imágenes")
        for img in r.get("images", []): img_ok(w, img)

    cslugs = set()
    for c in data.get("collections", []):
        s = c.get("slug", "")
        w = f"colección {s or '?'}"
        if s in cslugs: E(f"{w}: slug repetido")
        cslugs.add(s)
        if c.get("owner") not in handles: E(f"{w}: dueño desconocido {c.get('owner')}")
        if not c.get("name"): E(f"{w}: falta name")
        if not HEX.match(str(c.get("accentColor", ""))): E(f"{w}: accentColor tiene que ser hexadecimal (#RRGGBB)")
        if c.get("cover"): img_ok(w, c["cover"])
        for rs in c.get("recipes", []):
            if rs not in slugs: E(f"{w}: receta desconocida {rs}")

    resumen = {"usuarios": len(users), "recetas": len(data.get("recipes", [])),
               "colecciones": len(data.get("collections", [])), "errores": len(errs)}
    print(json.dumps(resumen, ensure_ascii=False))
    for e in errs:
        print(" -", e)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
