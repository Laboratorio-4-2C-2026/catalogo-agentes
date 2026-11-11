#!/usr/bin/env python3
"""Genera la semilla de `zonas` desde la API pública de Georef.

Dirección corre las consultas y entrega la tabla curada (D-19 / ADR-0002 § 2 bis:
la migración que la inserta la escribe el dev — ver H3-B.2).

Criterio de curación:
  - `region = 'AMBA'` para las 15 comunas de CABA y los 24 partidos del conurbano
    bonaerense (ADR-0002 § 2 bis / D-63). Todo el resto conserva el nombre de su provincia.
  - Una fila por localidad, más una fila por partido con `localidad` vacía
    (el selector en cascada y el techo de 2/3 de la proximidad la necesitan).
  - `id_indec` es el `id` que devuelve Georef para la unidad de cada fila.
  - Cuando una misma localidad figura en más de una categoría de Georef (las
    cabeceras, p. ej. Bahía Blanca), se conserva la de mayor jerarquía:
    Entidad > Localidad simple > Componente de localidad compuesta.
  - `activa` en `true` sólo para AMBA; el resto entra deshabilitado por etapas.

Salida: docs/planning/tickets/hito-3/datos/zonas-georef.csv
Uso:   python3 scripts/generar-semilla-zonas.py [--stdout]
"""
import argparse
import csv
import json
import ssl
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path


def contexto_ssl():
    """Mismo criterio que scripts/auditar-jira.py: nunca se desactiva la verificación."""
    ctx = ssl.create_default_context()
    if ctx.cert_store_stats().get("x509_ca", 0) > 0:
        return ctx
    bundle = Path("/etc/ssl/cert.pem")
    if bundle.exists():
        return ssl.create_default_context(cafile=str(bundle))
    raise RuntimeError("No se encontró un bundle de certificados.")


SSL_CTX = contexto_ssl()

BASE = "https://apis.datos.gob.ar/georef/api"
ROOT = Path(__file__).resolve().parent.parent
SALIDA = ROOT / "docs/planning/tickets/hito-3/datos/zonas-georef.csv"

CONURBANO = [
    "Almirante Brown", "Avellaneda", "Berazategui", "Esteban Echeverría", "Ezeiza",
    "Florencio Varela", "General San Martín", "Hurlingham", "Ituzaingó", "José C. Paz",
    "La Matanza", "Lanús", "Lomas de Zamora", "Malvinas Argentinas", "Merlo", "Moreno",
    "Morón", "Quilmes", "San Fernando", "San Isidro", "San Miguel", "Tigre",
    "Tres de Febrero", "Vicente López",
]
CABA = "ciudad autonoma de buenos aires"
PROV_BSAS = "buenos aires"
CONECTORES = {"de", "del", "e", "y"}


def nombre_propio(s: str) -> str:
    """Georef devuelve nombres con casing correcto ('Comuna 6', 'Gregorio de
    Laferrere'): pasan tal cual. Si algún registro viniera todo en mayúsculas,
    se re-casea respetando los conectores ('Santiago del Estero' no se rompe)."""
    if not s.isupper():
        return s
    palabras = [p.casefold() for p in s.split()]
    out = []
    for i, p in enumerate(palabras):
        out.append(p if (p in CONECTORES and i > 0) else p.capitalize())
    return " ".join(out)


def normal(s: str) -> str:
    """Clave de comparación: sin acentos, sin mayúsculas, sin espacios de más."""
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return " ".join(s.casefold().split())


def fetch(endpoint: str, **params) -> dict:
    url = f"{BASE}/{endpoint}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=90, context=SSL_CTX) as resp:
        return json.load(resp)


def fetch_todos(endpoint: str, campos: str, **extra) -> list:
    resultados, inicio = [], 0
    while True:
        data = fetch(endpoint, campos=campos, max=2000, inicio=inicio, **extra)
        lote = data.get(endpoint, [])
        resultados.extend(lote)
        total = data.get("total", len(resultados))
        inicio += len(lote)
        if not lote or inicio >= total:
            return resultados
        time.sleep(0.3)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stdout", action="store_true", help="no escribir el CSV, imprimirlo")
    args = parser.parse_args()

    provincias = fetch_todos("provincias", "id,nombre")
    departamentos = fetch_todos("departamentos", "id,nombre,provincia.nombre")

    # Georef clasifica las localidades en tres categorías: 'Entidad' (partes de
    # aglomeraciones, p. ej. los barrios de CABA o las villas de Berisso),
    # 'Localidad simple' (el interior) y 'Componente de localidad compuesta', que
    # repite nombres (Berisso entidad + Berisso componente; y las cabeceras figuran
    # a la vez como Entidad y como Localidad simple, p. ej. Bahía Blanca). Regla:
    # una fila por nombre de localidad en el partido, con prioridad
    # Entidad > Localidad simple > Componente.
    todas = fetch_todos("localidades", "id,nombre,categoria,departamento.nombre,provincia.nombre")
    prioridad = {"Entidad": 0, "Localidad simple": 1, "Componente de localidad compuesta": 2}
    todas.sort(key=lambda l: prioridad.get(l.get("categoria"), 3))
    vistas, localidades = set(), []
    for loc in todas:
        dep = loc.get("departamento")
        if not dep or not dep.get("nombre"):
            continue
        clave = (normal(loc["provincia"]["nombre"]), normal(dep["nombre"]), normal(loc["nombre"]))
        if clave in vistas:
            continue
        vistas.add(clave)
        localidades.append(loc)

    conurbanizado = {normal(p) for p in CONURBANO}

    filas = []

    def agregar(region: str, partido: str, localidad, id_indec: str, activa: bool) -> None:
        filas.append({
            "region": region, "partido": partido,
            "localidad": localidad if localidad else "",
            "id_indec": id_indec, "activa": "true" if activa else "false",
        })

    # --- partido por partido: fila con localidad vacía + una por localidad ---
    for dep in departamentos:
        prov = dep["provincia"]["nombre"]
        n_prov = normal(prov)
        n_dep = normal(dep["nombre"])
        partido = nombre_propio(dep["nombre"])

        if n_prov == CABA:
            region, activa = "AMBA", True
        elif n_prov == PROV_BSAS and n_dep in conurbanizado:
            region, activa = "AMBA", True
        else:
            region, activa = nombre_propio(prov), False

        agregar(region, partido, None, dep["id"], activa)

    for loc in localidades:
        dep = loc.get("departamento")
        if not dep or not dep.get("nombre"):
            continue
        prov = loc["provincia"]["nombre"]
        n_prov = normal(prov)
        n_dep = normal(dep["nombre"])

        if n_prov == CABA:
            region, activa = "AMBA", True
        elif n_prov == PROV_BSAS and n_dep in conurbanizado:
            region, activa = "AMBA", True
        else:
            region, activa = nombre_propio(prov), False

        agregar(region, nombre_propio(dep["nombre"]), nombre_propio(loc["nombre"]), loc["id"], activa)

    # --- verificación del criterio, antes de escribir ---
    partidos_amba = {(f["region"], f["partido"]) for f in filas if f["region"] == "AMBA"}
    comunas = {p for _, p in partidos_amba if normal(p).startswith("comuna")}
    conurbano_en_amba = {p for _, p in partidos_amba if normal(p) in conurbanizado}
    errores = []
    if len(comunas) != 15:
        errores.append(f"comunas de CABA: {len(comunas)} (esperado 15)")
    if len(conurbano_en_amba) != 24:
        faltan = sorted(conurbanizado - {normal(p) for p in conurbano_en_amba})
        errores.append(f"partidos del conurbano: {len(conurbano_en_amba)} de 24; faltan {faltan}")
    la_matanza = [f for f in filas if normal(f["partido"]) == "la matanza"]
    if not la_matanza or any(f["region"] != "AMBA" for f in la_matanza):
        errores.append("La Matanza no figura como partido del AMBA")
    duplicados = [
        k for k, n in __import__("collections").Counter(
            (f["region"], f["partido"], f["localidad"]) for f in filas
        ).items() if n > 1
    ]
    if duplicados:
        errores.append(f"(region, partido, localidad) duplicados: {duplicados[:5]}")
    sin_id = [f for f in filas if not f["id_indec"]]
    if sin_id:
        errores.append(f"{len(sin_id)} filas sin id_indec")

    if errores:
        print("La curación no pasa la verificación:", file=sys.stderr)
        for e in errores:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    if args.stdout:
        writer = csv.DictWriter(sys.stdout, fieldnames=["region", "partido", "localidad", "id_indec", "activa"])
        writer.writeheader()
        writer.writerows(filas)
    else:
        SALIDA.parent.mkdir(parents=True, exist_ok=True)
        with SALIDA.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["region", "partido", "localidad", "id_indec", "activa"])
            writer.writeheader()
            writer.writerows(filas)

    amba = sum(1 for f in filas if f["region"] == "AMBA")
    print(f"OK: {len(filas)} filas ({amba} del AMBA, {len(filas) - amba} del resto, activa=false).")
    print(f"    15 comunas + 24 partidos del conurbano verificados; La Matanza es partido del AMBA.")
    if not args.stdout:
        print(f"    Escrito: {SALIDA.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
