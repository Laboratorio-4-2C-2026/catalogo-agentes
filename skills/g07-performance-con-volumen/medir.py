"""Mide latencia de endpoints a distintos volúmenes de datos (g07-performance-con-volumen).

Sin dependencias externas. Dos subcomandos:

  medir    -> pide cada endpoint N veces (secuencial, sin concurrencia) y agrega filas a un CSV
  comparar -> arma la tabla volumen x endpoint y estima cómo crece la latencia

Ejemplos:
  python3 -I medir.py medir --base http://localhost:8080 --endpoints endpoints.txt \
      --volumen 10000 --reps 30 --csv resultados.csv --token-env STUDY_TOKEN
  python3 -I medir.py comparar --csv resultados.csv

endpoints.txt: una línea por endpoint, "METODO /ruta [cuerpo-json]". Líneas con # se ignoran.
  GET /api/rankings/global?page=0&size=20
  POST /api/rooms/search {"query": "fisica"}
"""
import argparse
import csv
import json
import math
import os
import statistics
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict


def leer_endpoints(ruta):
    eps = []
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            partes = linea.split(" ", 2)
            metodo, path = partes[0].upper(), partes[1]
            cuerpo = partes[2] if len(partes) > 2 else None
            eps.append((metodo, path, cuerpo))
    return eps


def pedir(base, metodo, path, cuerpo, headers, timeout):
    datos = cuerpo.encode() if cuerpo else None
    req = urllib.request.Request(base.rstrip("/") + path, data=datos, method=metodo, headers=headers)
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            contenido = r.read()
            estado = r.status
    except urllib.error.HTTPError as e:
        contenido, estado = e.read(), e.code
    except Exception as e:  # timeout, conexión rechazada
        return (time.perf_counter() - t0) * 1000, f"ERR:{type(e).__name__}", 0
    return (time.perf_counter() - t0) * 1000, estado, len(contenido)


def percentil(valores, p):
    v = sorted(valores)
    if not v:
        return float("nan")
    k = (len(v) - 1) * p / 100
    f, c = math.floor(k), math.ceil(k)
    return v[f] if f == c else v[f] + (v[c] - v[f]) * (k - f)


def cmd_medir(a):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if a.token_env:
        token = os.environ.get(a.token_env)
        if not token:
            sys.exit(f"Falta la variable de entorno {a.token_env}")
        headers["Authorization"] = f"Bearer {token}"
    nuevo = not os.path.exists(a.csv)
    with open(a.csv, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if nuevo:
            w.writerow(["volumen", "metodo", "ruta", "n", "p50_ms", "p95_ms", "max_ms", "bytes", "estados"])
        for metodo, path, cuerpo in leer_endpoints(a.endpoints):
            for _ in range(a.warmup):
                pedir(a.base, metodo, path, cuerpo, headers, a.timeout)
            tiempos, estados, tam = [], defaultdict(int), 0
            for _ in range(a.reps):
                ms, est, b = pedir(a.base, metodo, path, cuerpo, headers, a.timeout)
                tiempos.append(ms)
                estados[str(est)] += 1
                tam = max(tam, b)
            fila = [a.volumen, metodo, path, a.reps, round(percentil(tiempos, 50), 1),
                    round(percentil(tiempos, 95), 1), round(max(tiempos), 1), tam,
                    " ".join(f"{k}x{v}" for k, v in sorted(estados.items()))]
            w.writerow(fila)
            print(f"{metodo:6} {path:50} p50={fila[4]:>8}ms p95={fila[5]:>8}ms bytes={tam:>8} {fila[8]}")


def crecimiento(puntos):
    """Pendiente log-log entre el menor y el mayor volumen > 0: ~0 constante, ~1 lineal, ~2 cuadrático."""
    pts = [(v, t) for v, t in puntos if v > 0 and t > 0]
    if len(pts) < 2:
        return None
    (v1, t1), (v2, t2) = pts[0], pts[-1]
    if v1 == v2:
        return None
    return math.log(t2 / t1) / math.log(v2 / v1)


def cmd_comparar(a):
    datos = defaultdict(dict)
    vols = set()
    with open(a.csv, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            v = int(r["volumen"])
            vols.add(v)
            datos[(r["metodo"], r["ruta"])][v] = (float(r["p50_ms"]), float(r["p95_ms"]), int(r["bytes"]), r["estados"])
    vols = sorted(vols)
    cab = "| Endpoint | " + " | ".join(f"p95 @ {v:,}".replace(",", ".") for v in vols) + " | Crecimiento | Bytes máx |"
    print(cab)
    print("|" + "---|" * (len(vols) + 3))
    for (m, r), por_vol in sorted(datos.items(), key=lambda kv: -max(x[1] for x in kv[1].values())):
        celdas = []
        for v in vols:
            if v in por_vol:
                p95 = por_vol[v][1]
                estados = por_vol[v][3].split()
                todo_ok = all(e.startswith("2") for e in estados)
                marca = "" if todo_ok else " ⚠️"  # alguna respuesta no-2xx o error de conexión
                celdas.append(f"{p95:.0f} ms{marca}")
            else:
                celdas.append("–")
        k = crecimiento([(v, por_vol[v][1]) for v in vols if v in por_vol])
        if k is None:
            etiqueta = "?"
        elif k < 0.2:
            etiqueta = f"🟢 constante (k={k:.2f})"
        elif k < 0.6:
            etiqueta = f"🟡 sublineal (k={k:.2f})"
        elif k < 1.3:
            etiqueta = f"🟠 lineal (k={k:.2f})"
        else:
            etiqueta = f"🔴 superlineal (k={k:.2f})"
        bytes_max = max(x[2] for x in por_vol.values())
        print(f"| `{m} {r}` | " + " | ".join(celdas) + f" | {etiqueta} | {bytes_max:,} |".replace(",", "."))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("medir")
    m.add_argument("--base", required=True)
    m.add_argument("--endpoints", required=True)
    m.add_argument("--volumen", type=int, required=True, help="etiqueta numérica del volumen cargado")
    m.add_argument("--reps", type=int, default=30)
    m.add_argument("--warmup", type=int, default=5)
    m.add_argument("--timeout", type=float, default=30)
    m.add_argument("--csv", default="resultados.csv")
    m.add_argument("--token-env", help="nombre de la variable de entorno con el JWT (nunca el token en sí)")
    c = sub.add_parser("comparar")
    c.add_argument("--csv", default="resultados.csv")
    a = ap.parse_args()
    cmd_medir(a) if a.cmd == "medir" else cmd_comparar(a)


if __name__ == "__main__":
    main()
