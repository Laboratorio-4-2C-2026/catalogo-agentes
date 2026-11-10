#!/usr/bin/env python3
"""Carga el status semanal de Zest (Equipo 02) en el Tablero de Estado del Proyecto.

Uso:
    python3 update_status.py propuesta.json --dry-run     # muestra qué celdas cambiaría, sin escribir
    python3 update_status.py propuesta.json               # escribe
    python3 update_status.py propuesta.json --fecha 2026-11-12   # simula otro día (pruebas)

Requisitos: `pip install gspread` y la cuenta de servicio en ~/.config/zest/google-sa.json
(o la ruta en GOOGLE_SA_KEY). La cuenta tiene que tener acceso de edición a la planilla.

Qué escribe (y nada más), solo en la pestaña "Equipo 02":
  * Semáforo: la columna de la semana en curso, filas de Alcance a Riesgos.
  * Motivo / Acción tomada: AGREGA una línea "Sem-NN (dd/mm): texto" al final de la celda del área.
  * Cronograma: Estado Tarea, Avance %, F. Fin Estimado, F. Fin Real y Comentarios de las actividades que
    figuran en la propuesta (los comentarios se agregan, no se reemplazan).
  * Incidentes: filas nuevas en la primera fila libre de la tabla, y cierre de los que se indiquen.

Lo que NUNCA toca: General, Desvío y Vencido (son fórmulas de la planilla), otras pestañas, otras semanas,
ni texto de semanas anteriores. Se niega a escribir una semana que ya tiene valores.

Códigos de salida: 0 ok · 2 propuesta o datos inválidos · 3 la semana ya está cargada · 4 sin acceso a la planilla.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
from zoneinfo import ZoneInfo

SHEET_ID = "1tA2CFxUesISCr39-MmhhdxwmitZKZBhTdOjfpSGjCec"
PESTANA = "Equipo 02"
SEM01 = dt.date(2026, 8, 10)  # lunes de la Sem-01
AREAS = ["Alcance", "Cronograma", "Incidentes", "Calidad", "Riesgos"]
COLORES = {"Verde", "Amarillo", "Rojo"}
ESTADOS = {"Finaliz.", "En curso", "Pend."}
CRITICIDADES = {"Baja", "Media", "Alta"}
COL_MOTIVO, COL_ACCION = "Motivo", "Acción tomada"
TZ = ZoneInfo("America/Argentina/Buenos_Aires")


class Error(Exception):
    def __init__(self, msg, codigo=2):
        super().__init__(msg)
        self.codigo = codigo


# ---------- utilidades de celdas ----------

def col_letra(n):
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def a1(fila, col):
    return f"{col_letra(col)}{fila}"


def get(valores, fila, col):
    try:
        return valores[fila - 1][col - 1]
    except IndexError:
        return ""


def es_formula(formulas, fila, col):
    return str(get(formulas, fila, col)).startswith("=")


def fecha(texto, campo):
    """dd/mm/aa o dd/mm/aaaa -> date."""
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{2}|\d{4})", str(texto or "").strip())
    if not m:
        raise Error(f"{campo}: la fecha '{texto}' debe tener formato dd/mm/aa")
    d, mo, y = int(m[1]), int(m[2]), int(m[3])
    try:
        return dt.date(y + 2000 if y < 100 else y, mo, d)
    except ValueError:
        raise Error(f"{campo}: la fecha '{texto}' no existe")


def fmt(d):
    return d.strftime("%d/%m/%Y")


# ---------- ubicar celdas en la planilla ----------

def ubicar(valores, hoy):
    """Encuentra, leyendo los rótulos, todas las celdas que el script usa."""
    semana = (hoy - SEM01).days // 7 + 1
    if semana < 1:
        raise Error(f"La fecha {hoy} es anterior a la Sem-01")
    etiqueta = f"Sem-{semana:02d}"
    fila_enc = next((i + 1 for i, f in enumerate(valores) if any(f"Sem-01" in str(c) for c in f)), None)
    if not fila_enc:
        raise Error("No encontré la fila de encabezados con las semanas")
    col_sem = next((j + 1 for j, c in enumerate(valores[fila_enc - 1]) if etiqueta in str(c)), None)
    if not col_sem:
        raise Error(f"La planilla no tiene columna para {etiqueta}")
    filas_area = {}
    for i, f in enumerate(valores[fila_enc:], fila_enc + 1):
        nombre = str(f[0]).strip() if f else ""
        if nombre in AREAS and nombre not in filas_area:
            filas_area[nombre] = i
    faltan = [a for a in AREAS if a not in filas_area]
    if faltan:
        raise Error("No encontré en la planilla las áreas: " + ", ".join(faltan))
    enc = valores[fila_enc - 1]
    col_motivo = next((j + 1 for j, c in enumerate(enc) if str(c).strip().startswith(COL_MOTIVO)), None)
    col_accion = next((j + 1 for j, c in enumerate(enc) if str(c).strip().startswith(COL_ACCION)), None)
    if not (col_motivo and col_accion):
        raise Error("No encontré las columnas Motivo y Acción tomada")

    def tabla(titulo_enc, fin):
        """Devuelve (fila_encabezado, {rotulo: columna}) de la tabla con ese primer rótulo."""
        for i, f in enumerate(valores, 1):
            if any(titulo_enc in str(c).replace("\n", " ") for c in f) and i > fila_enc + 6:
                cols = {str(c).replace("\n", " ").strip(): j + 1 for j, c in enumerate(f) if str(c).strip()}
                return i, cols
        raise Error(f"No encontré la tabla de {fin}")

    f_cron, c_cron = tabla("Actividades Clave", "Cronograma")
    f_inc, c_inc = tabla("Criticidad", "Incidentes")
    f_inc_sec = f_inc
    return {
        "semana": semana, "etiqueta": etiqueta, "lunes": SEM01 + dt.timedelta(days=7 * (semana - 1)),
        "col_sem": col_sem, "filas_area": filas_area, "col_motivo": col_motivo, "col_accion": col_accion,
        "f_cron": f_cron, "c_cron": c_cron, "f_inc": f_inc_sec, "c_inc": c_inc,
    }


def limites_tablas(valores, formulas, u):
    """Rangos de filas de datos de cada tabla: Cronograma hasta el rótulo INCIDENTES; Incidentes hasta PRODUCTO.

    En Incidentes solo cuentan las filas que ya tienen la fórmula de Vencido (la parte formateada de la tabla)."""
    def fila_de(texto, desde):
        return next((i for i, f in enumerate(valores, 1) if i > desde and any(str(c).strip() == texto for c in f)), None)
    fin_cron = (fila_de("INCIDENTES", u["f_cron"]) or u["f_cron"] + 22) - 1
    fin_inc = (fila_de("PRODUCTO", u["f_inc"]) or u["f_inc"] + 32) - 1
    inc = range(u["f_inc"] + 1, fin_inc + 1)
    col_venc = u["c_inc"].get("Vencido")
    con_formula = [f for f in inc if col_venc and es_formula(formulas, f, col_venc)]
    return range(u["f_cron"] + 1, fin_cron + 1), (con_formula or list(inc))


# ---------- plan ----------

def planificar(valores, formulas, propuesta, hoy):
    """Decide qué celdas cambian. Función pura: no usa la red. Devuelve (cambios, avisos).

    cambios: lista de dicts {celda, fila, col, antes, despues, que}
    """
    u = ubicar(valores, hoy)
    cambios, avisos = [], []
    etiqueta_linea = f"{u['etiqueta']} ({u['lunes'].strftime('%d/%m')})"

    def poner(fila, col, nuevo, que):
        if es_formula(formulas, fila, col):
            raise Error(f"Voy a pisar una fórmula en {a1(fila, col)} ({que}). Frenado: la planilla la calcula sola.")
        cambios.append({"celda": a1(fila, col), "fila": fila, "col": col, "antes": get(valores, fila, col),
                        "despues": nuevo, "que": que})

    def agregar(fila, col, texto, que):
        previo = str(get(valores, fila, col)).rstrip()
        linea = f"{etiqueta_linea}: {texto.strip()}"
        poner(fila, col, f"{previo}\n{linea}" if previo else linea, que)

    # --- semáforo ---
    sem = propuesta.get("semaforo") or {}
    faltan = [a for a in AREAS if a not in sem]
    if faltan:
        raise Error("El semáforo de la propuesta no incluye: " + ", ".join(faltan))
    for a in AREAS:
        fila = u["filas_area"][a]
        if str(get(valores, fila, u["col_sem"])).strip():
            raise Error(f"La {u['etiqueta']} ya está cargada ({a} = {get(valores, fila, u['col_sem'])}). "
                        "No se sobrescribe.", 3)
    for a in AREAS:
        d = sem[a]
        color = d.get("color")
        if color not in COLORES:
            raise Error(f"{a}: color '{color}' inválido (usar Verde, Amarillo o Rojo)")
        if color != "Verde" and not (d.get("motivo") and d.get("accion")):
            raise Error(f"{a} está en {color}: la propuesta necesita 'motivo' y 'accion'")
        fila = u["filas_area"][a]
        poner(fila, u["col_sem"], color, f"Semáforo {a}")
        if color != "Verde":
            agregar(fila, u["col_motivo"], d["motivo"], f"Motivo {a}")
            agregar(fila, u["col_accion"], d["accion"], f"Acción {a}")

    cron_filas, inc_filas = limites_tablas(valores, formulas, u)
    c = u["c_cron"]
    col_act = min(c.values())

    # --- cronograma ---
    for act in propuesta.get("cronograma") or []:
        nombre = (act.get("actividad") or "").strip()
        coinc = [f for f in cron_filas if str(get(valores, f, col_act)).strip() == nombre]
        if len(coinc) != 1:
            raise Error(f"Cronograma: la actividad '{nombre}' aparece {len(coinc)} veces en la planilla "
                        "(tiene que haber exactamente una). Las actividades nuevas no se agregan.")
        f = coinc[0]
        if act.get("estado") not in ESTADOS:
            raise Error(f"Cronograma '{nombre}': estado '{act.get('estado')}' inválido (Finaliz., En curso, Pend.)")
        av = act.get("avance")
        if not isinstance(av, (int, float)) or not 0 <= av <= 100:
            raise Error(f"Cronograma '{nombre}': avance debe ser un número entre 0 y 100")
        poner(f, c["Estado Tarea"], act["estado"], f"Estado {nombre}")
        poner(f, c["Avance [%]"], f"{round(av)}%", f"Avance {nombre}")
        if act.get("f_fin_estimado"):
            poner(f, c["F. Fin Estimado"], fmt(fecha(act["f_fin_estimado"], f"'{nombre}' f_fin_estimado")), f"F. Fin Estimado {nombre}")
        if act["estado"] == "Finaliz.":
            if not act.get("f_fin_real"):
                raise Error(f"Cronograma '{nombre}': si está Finaliz. hay que indicar 'f_fin_real'")
            poner(f, c["F. Fin Real"], fmt(fecha(act["f_fin_real"], f"'{nombre}' f_fin_real")), f"F. Fin Real {nombre}")
        elif act.get("f_fin_real"):
            raise Error(f"Cronograma '{nombre}': 'f_fin_real' solo se completa si la actividad está Finaliz.")
        if act.get("comentario"):
            agregar(f, c["Comentarios"], act["comentario"], f"Comentario {nombre}")

    # --- incidentes ---
    ci = u["c_inc"]
    col_desc = min(ci.values())
    inc = propuesta.get("incidentes") or {}
    filas_con_dato = [f for f in inc_filas if str(get(valores, f, col_desc)).strip()]
    libres = [f for f in inc_filas if f not in filas_con_dato and not str(get(valores, f, ci["Estado"])).strip()]
    for x in inc.get("cerrar") or []:
        frag = (x.get("descripcion") or "").strip().lower()
        coinc = [f for f in filas_con_dato if frag and frag in str(get(valores, f, col_desc)).lower()]
        if len(coinc) != 1:
            raise Error(f"Incidentes: '{x.get('descripcion')}' coincide con {len(coinc)} filas (tiene que ser exactamente una)")
        f = coinc[0]
        if str(get(valores, f, ci["Estado"])).strip() != "Abierto":
            avisos.append(f"Incidente de la fila {f} ya no estaba Abierto: no se modificó.")
            continue
        poner(f, ci["Estado"], "Cerrado", f"Cerrar incidente fila {f}")
        poner(f, ci["F. Cierre"], fmt(fecha(x.get("f_cierre"), "cerrar f_cierre")), f"F. Cierre fila {f}")
        if x.get("resolucion"):
            poner(f, ci["Resolución"], x["resolucion"].strip(), f"Resolución fila {f}")
    for x in inc.get("nuevos") or []:
        desc = (x.get("descripcion") or "").strip()
        if not desc:
            raise Error("Incidentes: un incidente nuevo no tiene 'descripcion'")
        if any(desc.lower() == str(get(valores, f, col_desc)).strip().lower() for f in filas_con_dato):
            avisos.append(f"El incidente '{desc[:50]}…' ya está en la planilla: no se agregó de nuevo.")
            continue
        if x.get("criticidad") not in CRITICIDADES:
            raise Error(f"Incidentes '{desc[:40]}…': criticidad inválida (Baja, Media o Alta)")
        if not libres:
            raise Error("La tabla de Incidentes no tiene filas libres. Agregá filas a mano y volvé a correr.")
        f = libres.pop(0)
        alta = fecha(x.get("f_alta"), "f_alta") if x.get("f_alta") else hoy
        limite = fecha(x["f_limite"], "f_limite") if x.get("f_limite") else alta + dt.timedelta(days=7)
        poner(f, col_desc, desc, f"Nuevo incidente fila {f}")
        poner(f, ci["Estado"], "Abierto", f"Estado fila {f}")
        poner(f, ci["Criticidad"], x["criticidad"], f"Criticidad fila {f}")
        poner(f, ci["F. Alta"], fmt(alta), f"F. Alta fila {f}")
        poner(f, ci["F. Límite"], fmt(limite), f"F. Límite fila {f}")
        if x.get("resolucion"):
            poner(f, ci["Resolución"], x["resolucion"].strip(), f"Resolución fila {f}")

    celdas = [c_["celda"] for c_ in cambios]
    repetidas = {x for x in celdas if celdas.count(x) > 1}
    if repetidas:
        raise Error("La propuesta modifica dos veces la misma celda: " + ", ".join(sorted(repetidas)))
    return u, cambios, avisos


# ---------- entrada/salida ----------

def abrir_planilla():
    try:
        import gspread
    except ImportError:
        raise Error("Falta gspread: pip install gspread", 4)
    clave = os.environ.get("GOOGLE_SA_KEY") or os.path.expanduser("~/.config/zest/google-sa.json")
    try:
        ws = gspread.service_account(filename=clave).open_by_key(SHEET_ID).worksheet(PESTANA)
        return ws
    except Exception as e:  # sin permisos, sin red, clave inexistente...
        raise Error(f"No pude abrir la planilla ({type(e).__name__}: {str(e)[:150]})", 4)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("propuesta")
    p.add_argument("--dry-run", action="store_true", help="no escribe: solo muestra los cambios")
    p.add_argument("--fecha", help="AAAA-MM-DD: simula otro día (por defecto, hoy en Buenos Aires)")
    a = p.parse_args(argv)
    try:
        hoy = dt.date.fromisoformat(a.fecha) if a.fecha else dt.datetime.now(TZ).date()
        try:
            propuesta = json.load(open(a.propuesta, encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            raise Error(f"No pude leer {a.propuesta}: {e}")
        ws = abrir_planilla()
        valores = ws.get_all_values(value_render_option="FORMATTED_VALUE")
        formulas = ws.get_all_values(value_render_option="FORMULA")
        u, cambios, avisos = planificar(valores, formulas, propuesta, hoy)
    except Error as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return e.codigo

    print(f"Semana {u['etiqueta']} (lunes {u['lunes'].strftime('%d/%m/%Y')}) · pestaña '{PESTANA}' · "
          f"{len(cambios)} celdas {'(simulación, no se escribió nada)' if a.dry_run else ''}")
    for c in cambios:
        antes = str(c["antes"]).replace("\n", "⏎")
        despues = str(c["despues"]).replace("\n", "⏎")
        print(f"  {c['celda']:>5}  {c['que']:<38} {('[' + antes[:40] + '] → ') if antes else ''}{despues[:90]}")
    for av in avisos:
        print(f"AVISO: {av}")
    if a.dry_run:
        return 0
    ws.batch_update([{"range": c["celda"], "values": [[c["despues"]]]} for c in cambios], value_input_option="USER_ENTERED")
    print(f"Listo: {len(cambios)} celdas escritas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
