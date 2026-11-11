#!/usr/bin/env python3
"""tablero-ia.py — Agente 4.8, parte con criterio: propuesta de colores por IA.

Toma el texto que arma tablero-semanal.py (datos ya calculados) y le pide a
Gemini una propuesta de color por área, con motivo, acción y evidencia,
más una revisión de lo calculado. El General NO lo decide el modelo: se calcula
acá con la regla de la planilla.

Si el modelo no responde o devuelve algo inválido, imprime un aviso y sale con 0:
el issue se abre igual, sin propuesta. Nunca escribe en la planilla.

Uso (en el workflow):
  python3 scripts/tablero-ia.py issue.md >> issue.md
Necesita GEMINI_API_KEY (key gratuita de Google AI Studio). Solo stdlib.
"""

import importlib.util
import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
import time
import urllib.error

# Si un modelo está saturado (503) o sin cupo (429), se reintenta y después se pasa al siguiente.
MODELOS = os.environ.get("MODELOS_TABLERO",
                         "gemini-flash-latest,gemini-2.5-flash,gemini-flash-lite-latest").split(",")
ESPERAS = (0, 15, 45)
URL = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent"
MODELO = MODELOS[0]
COLORES = {"Verde", "Amarillo", "Rojo"}

spec = importlib.util.spec_from_file_location("tablero", ROOT / "scripts" / "tablero-semanal.py")
tablero = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tablero)

INSTRUCCIONES = """Sos el asistente del PM de un proyecto universitario. Proponés el estado semanal \
del tablero de la cátedra a partir de DATOS ya calculados. Reglas:
- Un color por área (Alcance, Cronograma, Incidentes, Calidad, Riesgos): Verde, Amarillo o Rojo.
  VERDE: no hay inconvenientes. AMARILLO: hay alertas que pueden derivar en desvíos.
  ROJO: hay situaciones críticas que ya están derivando en desvíos.
- Cronograma: algún desvío negativo, o una tarea sin terminar a un día del cierre, es Amarillo.
- Cada color no Verde lleva motivo y acción con el formato «Sem-NN: …», en pasado, una o dos frases.
- La evidencia SOLO puede citar elementos que aparezcan en los DATOS (SCRUM-n, PR #n, un commit).
  Si no hay evidencia suficiente para un área, el color es "a confirmar". No inventes.
- No calcules el General: lo calcula otro programa.
- En "revision", señalá lo calculado que convenga confirmar (fechas que no coinciden, L. Base
  marcada «confirmar», PRs sin ticket). Frases cortas.
Respondé SOLO con JSON con esta forma:
{"semanas":[{"semana":"Sem-NN","areas":[{"area":"Alcance","color":"Verde","motivo":"","accion":"","evidencia":""}]}],
 "revision":["..."]}"""


def pedir(datos):
    """Prueba cada modelo con reintentos. Devuelve (propuesta, modelo que respondió)."""
    global MODELO
    ultimo = None
    for modelo in MODELOS:
        for espera in ESPERAS:
            time.sleep(espera)
            try:
                MODELO = modelo.strip()
                return pedir_a(MODELO, datos), MODELO
            except urllib.error.HTTPError as e:
                ultimo = e
                if e.code in (429, 500, 503):
                    continue
                if e.code == 404:
                    break
                raise
            except (TimeoutError, urllib.error.URLError) as e:
                ultimo = e  # tardó demasiado: el modelo está saturado, se pasa al siguiente
                break
    raise ultimo


def pedir_a(modelo, datos):
    cuerpo = json.dumps({
        "systemInstruction": {"parts": [{"text": INSTRUCCIONES}]},
        "contents": [{"role": "user", "parts": [{"text": "DATOS:\n\n" + datos}]}],
        "generationConfig": {"temperature": 0, "responseMimeType": "application/json"},
    }).encode()
    req = urllib.request.Request(URL.format(modelo), data=cuerpo, headers={
        "x-goog-api-key": os.environ["GEMINI_API_KEY"], "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        respuesta = json.loads(r.read().decode())
    return json.loads(respuesta["candidates"][0]["content"]["parts"][0]["text"])


def main():
    datos = Path(sys.argv[1]).read_text(encoding="utf-8")
    if "No hay semanas vacías" in datos:
        return
    print("\n---\n\n## Propuesta de colores (IA, para que decida el PM)\n")
    try:
        prop, _ = pedir(datos)
    except Exception as e:
        detalle = ""
        if hasattr(e, "read"):  # HTTPError: Google explica el motivo en el cuerpo (sin la key)
            try:
                detalle = " — " + json.loads(e.read().decode()).get("error", {}).get("message", "")[:300]
            except Exception:
                pass
        print(f"> ⚠️ No se pudo pedir la propuesta a Gemini ({type(e).__name__}: {e}{detalle}). "
              "Los datos de arriba siguen valiendo; los colores los elige el PM o la skill.")
        return
    print(f"Modelo: `{MODELO}`. Cada color cita evidencia de los datos de arriba; "
          "el General lo calcula el script con la regla de la planilla, no el modelo.\n")
    for sem in prop.get("semanas", []):
        print(f"### {sem.get('semana', '?')}\n")
        print("| Área | Color | Motivo | Acción | Evidencia |\n|---|---|---|---|---|")
        colores = []
        for a in sem.get("areas", []):
            color = str(a.get("color", "")).strip().capitalize()
            colores.append(color)
            print(f"| {a.get('area', '')} | {color or 'a confirmar'} | {a.get('motivo', '')} | "
                  f"{a.get('accion', '')} | {a.get('evidencia', '')} |")
        if len(colores) == 5 and all(c in COLORES for c in colores):
            print(f"| **General** | **{tablero.calcular_general(colores)}** | calculado | | |\n")
        else:
            print("| **General** | sin calcular | hay áreas «a confirmar» | | |\n")
    if prop.get("revision"):
        print("### Para confirmar antes de cargar\n")
        for r in prop["revision"]:
            print(f"- {r}")


if __name__ == "__main__":
    main()
