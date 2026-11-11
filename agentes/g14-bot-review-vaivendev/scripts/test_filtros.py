"""Chequeo del filtro de comentarios: python3 scripts/test_filtros.py"""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("gr", Path(__file__).with_name("generar-review.py"))
gr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gr)

lineas = {"src/FactorBars.tsx": {10: "  <span>{factor.value.toFixed(2)}</span>", 11: "}"}}
fuente = "[+10]   <span>{factor.value.toFixed(2)}</span>"


def c(tipo="suggestion", evidencia="factor.value.toFixed(2)", msg="revisá el null", path="src/FactorBars.tsx", line=10):
    return {"path": path, "line": line, "type": tipo, "evidencia": evidencia, "message": msg}


# Caso real, PR #46: cita una línea de otro archivo que no existe.
ok, _, desc = gr.filtrar_comentarios([c(msg="En ScoreRing se usó `factores?.f1_resolucion ?? 0`")], lineas, fuente)
assert ok == [] and "cita código" in desc[0], desc

# Evidencia inventada o ausente, archivo fuera del diff.
assert gr.filtrar_comentarios([c(evidencia="value ?? 0")], lineas, fuente)[0] == []
assert gr.filtrar_comentarios([c(evidencia="")], lineas, fuente)[0] == []
assert gr.filtrar_comentarios([c(path="src/Otro.tsx")], lineas, fuente)[0] == []

# Un comentario válido pasa, con cierre de reacción y conceptos entre backticks permitidos.
ok, _, desc = gr.filtrar_comentarios([c(msg="usá `try/finally` alrededor de `factor.value.toFixed(2)`")], lineas, fuente)
assert len(ok) == 1 and gr.CIERRE_REACCION in ok[0]["body"] and not desc, desc

# Topes: 1 praise, 2 nitpick; los issue nunca se cortan.
lote = [c("praise")] * 3 + [c("nitpick")] * 3 + [c("issue")] * 9
ok, _, desc = gr.filtrar_comentarios(lote, lineas, fuente)
tipos = [x["body"].split(":")[0] for x in ok]
assert tipos.count("praise") == 1 and tipos.count("nitpick") == 2 and tipos.count("issue") == 9, tipos

print("ok")
