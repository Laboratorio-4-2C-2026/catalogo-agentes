#!/usr/bin/env python3
"""scrum_88.py — Criterios de aceptación del SCRUM-88 «Historial: mis publicaciones», uno por uno.

Los criterios salen de la sección «3. Criterios de aceptación» del ticket (scripts/e2e-ticket.py SCRUM-88).
Cada criterio queda como PASA / FALLA / NO PROBADO, con los pasos que se ejecutaron. Los estados
«en proceso», «completada» y «vencida» no se pueden fijar desde la interfaz sin pasar por otras
pantallas, así que A los cambia por la API con su propia sesión (lo que su RLS le permite).

Uso:
  python e2e/tickets/scrum_88.py --app <clon-de-vaiven-app> [--url http://localhost:5173] [--etiqueta pr-74]
"""

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from e2e_comun import (FALLA, GRUPOS, NO_PROBADO, PASA, ROOT, InformeCriterios, archivo_unico,  # noqa: E402
                       carpeta_salidas, crear_usuario, entorno_local, etiquetas_de_tipo, grupos_historial,
                       guardar_captura, login, pub_por_titulo, publicar_donacion, publicar_necesidad, rest,
                       sello, sha_probado, solo_localhost)

TEXTOS = {
    1: "/historial lista todas las publicaciones del usuario, de los dos tipos, incluidas completadas y vencidas.",
    2: "Los grupos aparecen en el orden Activas, En proceso, Vencidas, Completadas, con su cantidad, y un grupo vacío no se muestra.",
    3: "Una publicación activa o en proceso con vence_en pasado aparece en Vencidas.",
    4: "Cada tarjeta del historial muestra su tipo; las de /mis-donaciones y /mis-necesidades no.",
    5: "MyPublications y HistorialPage usan fetchMisPublicaciones; no queda otra consulta a publicaciones en esas dos pantallas.",
    6: "Un usuario sin publicaciones ve el estado vacío con la acción a /publicar.",
    7: "El historial de un usuario no muestra publicaciones de otro.",
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--app", type=Path, required=True)
    ap.add_argument("--url", default="http://localhost:5173")
    ap.add_argument("--etiqueta", default="scrum-88")
    ap.add_argument("--headed", action="store_true")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    solo_localhost(args.url)

    api, anon = entorno_local(args.app.resolve())
    carpeta, marca = carpeta_salidas(args.etiqueta), sello()
    a, b = crear_usuario(api, anon, "a"), crear_usuario(api, anon, "b")
    if not (a["ok"] and b["ok"]):
        raise SystemExit("No pude crear los usuarios de prueba en el Auth local.")

    t = {k: f"T88 {marca} {k}" for k in ("activa", "en proceso", "completada", "activa vencida", "en proceso vencida")}
    pasado = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    res = {}  # número de criterio -> (estado, pasos, detalle)

    with sync_playwright() as pw:
        navegador = pw.chromium.launch(headless=not args.headed)
        ctx_a = navegador.new_context(viewport={"width": 390, "height": 844})
        ctx_b = navegador.new_context(viewport={"width": 390, "height": 844})
        pa, pb = ctx_a.new_page(), ctx_b.new_page()

        # ---- Preparación: A publica desde los formularios y fija estados por la API -----------------------
        prep, prep_ok = [], True
        try:
            assert login(pa, args.url, a), "no pude entrar como A"
            for clave in ("activa", "completada", "activa vencida", "en proceso vencida"):
                assert publicar_necesidad(pa, args.url, t[clave]), f"no se publicó la necesidad «{clave}»"
            publicar_donacion(pa, args.url, t["en proceso"])
            prep.append("A publica 4 necesidades y 1 donación desde los formularios de la app")

            def fijar(clave, cuerpo):
                fila = pub_por_titulo(api, anon, a, t[clave])
                est, resp = rest(api, anon, "PATCH", f"/rest/v1/publicaciones?id=eq.{fila['id']}",
                                 token=a["token"], cuerpo=cuerpo) if fila else (0, None)
                assert est in (200, 204) and resp, f"la API no dejó cambiar «{clave}» (HTTP {est})"

            fijar("en proceso", {"estado": "en_proceso"})
            fijar("completada", {"estado": "completada"})
            fijar("activa vencida", {"vence_en": pasado})
            fijar("en proceso vencida", {"estado": "en_proceso", "vence_en": pasado})
            prep.append("A deja una en proceso, una completada, una activa vencida y una en proceso vencida (por la API, con su sesión)")
        except Exception as e:  # noqa: BLE001
            prep_ok = False
            motivo = str(e).splitlines()[0][:160] if str(e) else type(e).__name__
            for n in (1, 2, 3, 4, 7):
                res[n] = (NO_PROBADO, prep, f"no se pudo preparar el escenario: {motivo}")

        # ---- B: usuario sin publicaciones (criterios 6 y 7) ------------------------------------------------
        try:
            assert login(pb, args.url, b), "no pude entrar como B"
            pb.goto(args.url + "/historial")
            pb.get_by_text("Todavía no publicaste nada").wait_for(timeout=10000)
            pasos = ["Registrar a B (usuario nuevo, sin publicaciones) y entrar", "Abrir /historial",
                     "Ver «Todavía no publicaste nada»", "Tocar «Crear una publicación»"]
            pb.get_by_role("button", name="Crear una publicación").click()
            pb.wait_for_url("**/publicar", timeout=8000)
            res[6] = (PASA, pasos, "")
            if prep_ok:
                pb.goto(args.url + "/historial")
                pb.get_by_text("Todavía no publicaste nada").wait_for(timeout=10000)
                visibles = [k for k, v in t.items() if v in pb.locator("main").inner_text()]
                res[7] = (PASA if not visibles else FALLA,
                          ["Con las publicaciones de A ya creadas (incluida la completada), entrar como B",
                           "Abrir /historial de B", "Buscar los títulos de A"],
                          "" if not visibles else "B ve publicaciones de A: " + ", ".join(visibles))
        except Exception as e:  # noqa: BLE001
            for n in (6, 7):
                if n not in res:
                    res[n] = (FALLA, [], str(e).splitlines()[0][:200])

        # ---- A: historial completo (criterios 1 a 4) -------------------------------------------------------
        if prep_ok:
            try:
                pa.goto(args.url + "/historial")
                pa.get_by_text(t["activa"]).first.wait_for(timeout=15000)
                texto = pa.locator("main").inner_text()
                grupos = grupos_historial(pa)
                guardar_captura(pa, args.etiqueta, "scrum-88-historial.png", marca, full_page=True)

                faltan = [k for k, v in t.items() if v not in texto]
                tipos = {l.strip() for l in texto.splitlines()} & {"NECESIDAD", "DONACIÓN"}
                res[1] = (PASA if not faltan and tipos == {"NECESIDAD", "DONACIÓN"} else FALLA,
                          ["Entrar como A (con 5 publicaciones: activa, en proceso, completada y dos vencidas)",
                           "Abrir /historial", "Buscar cada título y las etiquetas de tipo"],
                          ("Faltan: " + ", ".join(faltan)) if faltan else
                          ("" if tipos == {"NECESIDAD", "DONACIÓN"} else f"tipos vistos: {sorted(tipos)}"))

                orden = [g for g, _, _ in grupos]
                cantidades = {g: n for g, n, _ in grupos}
                esperado = {"Activas": 1, "En proceso": 1, "Vencidas": 2, "Completadas": 1}
                ok_orden = orden == list(GRUPOS) and cantidades == esperado
                res[2] = (PASA if ok_orden else FALLA,
                          ["Abrir /historial de A", "Leer los encabezados «Grupo · cantidad» en el orden en que aparecen",
                           "Comparar con Activas 1, En proceso 1, Vencidas 2, Completadas 1"],
                          "" if ok_orden else f"vistos: {[(g, n) for g, n, _ in grupos]}")

                def en(grupo, clave):
                    # Línea completa: «…activa» está contenido en «…activa vencida».
                    return any(g == grupo and t[clave] in l for g, _, l in grupos)
                ok3 = en("Vencidas", "activa vencida") and en("Vencidas", "en proceso vencida") \
                    and en("Activas", "activa") and en("En proceso", "en proceso") \
                    and not en("Vencidas", "activa") and not en("Vencidas", "en proceso")
                res[3] = (PASA if ok3 else FALLA,
                          ["A tiene una activa y una en proceso con vence_en pasado, y otras dos sin vencer",
                           "Abrir /historial", "Comprobar en qué grupo cae cada una"],
                          "" if ok3 else f"grupos: {[(g, [x for x in l if x.startswith('T88')]) for g, _, l in grupos]}")

                n_hist = etiquetas_de_tipo(pa)
                pa.goto(args.url + "/mis-necesidades")
                pa.wait_for_timeout(2500)
                en_nec = etiquetas_de_tipo(pa)
                hay_nec = any(v in pa.locator("main").inner_text() for v in t.values())
                pa.goto(args.url + "/mis-donaciones")
                pa.wait_for_timeout(2500)
                en_don = etiquetas_de_tipo(pa)
                hay_don = t["en proceso"] in pa.locator("main").inner_text()
                pasos4 = ["Contar las etiquetas de tipo en /historial (5 tarjetas)",
                          "Abrir /mis-necesidades y /mis-donaciones y contar sus etiquetas de tipo"]
                if not (hay_nec and hay_don):
                    res[4] = (NO_PROBADO, pasos4, "esas pantallas no mostraron las publicaciones de prueba; no hay tarjetas que mirar")
                else:
                    ok4 = n_hist == 5 and en_nec == 0 and en_don == 0
                    res[4] = (PASA if ok4 else FALLA, pasos4,
                              "" if ok4 else f"historial={n_hist} (esperado 5), mis-necesidades={en_nec}, mis-donaciones={en_don} (esperado 0)")
            except Exception as e:  # noqa: BLE001
                for n in (1, 2, 3, 4):
                    res.setdefault(n, (FALLA, [], "se interrumpió: " + str(e).splitlines()[0][:200]))

        # ---- B publica una sola: el grupo vacío no se muestra (resto del criterio 2) -----------------------
        try:
            assert publicar_necesidad(pb, args.url, f"T88 {marca} B"), "B no pudo publicar"
            pb.goto(args.url + "/historial")
            pb.get_by_text(f"T88 {marca} B").first.wait_for(timeout=10000)
            visibles = [g for g, _, _ in grupos_historial(pb)]
            ok = visibles == ["Activas"]
            previo = res.get(2, (NO_PROBADO, [], ""))
            estado = FALLA if (previo[0] == FALLA or not ok) else (PASA if previo[0] == PASA else NO_PROBADO)
            detalle = previo[2] + ("" if ok else f" Con una sola activa se vieron los grupos {visibles}.")
            res[2] = (estado, previo[1] + ["B (sin otras publicaciones) publica una sola necesidad activa",
                                           "Abrir /historial de B y comprobar que solo aparece «Activas»"], detalle.strip())
        except Exception as e:  # noqa: BLE001
            previo = res.get(2, (NO_PROBADO, [], ""))
            res[2] = (previo[0] if previo[0] == FALLA else NO_PROBADO, previo[1],
                      (previo[2] + " No pude comprobar el grupo vacío: " + str(e).splitlines()[0][:120]).strip())

        navegador.close()

    res[5] = (NO_PROBADO, ["—"], "criterio de código (qué consulta usa cada pantalla), no de comportamiento: "
                                 "no se puede ver desde la app. Lo cubre el code-reviewer-de-prs (8.1) leyendo el diff")

    inf = InformeCriterios()
    for n in sorted(res):
        estado, pasos, detalle = res[n]
        inf.criterio(n, TEXTOS[n], estado, pasos, detalle)
    ruta = archivo_unico(carpeta, "scrum-88-criterios.md", marca)
    inf.escribir(ruta, f"Criterios del SCRUM-88 — {args.etiqueta}",
                 f"Fecha: {datetime.now():%Y-%m-%d %H:%M} · Commit probado: `{sha_probado(args.app.resolve())}` · "
                 f"Frontend: {args.url} · Stack: Supabase local")
    print(f"\n{inf.cuenta(PASA)} pasan · {inf.cuenta(FALLA)} fallan · {inf.cuenta(NO_PROBADO)} no probados — informe: {ruta.relative_to(ROOT)}")
    return 1 if inf.hay_fallas() else 0


if __name__ == "__main__":
    sys.exit(main())
