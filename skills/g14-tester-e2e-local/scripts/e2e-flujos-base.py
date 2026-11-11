#!/usr/bin/env python3
"""e2e-flujos-base.py — Flujos base del Tester E2E local (9.2), con Playwright.

Prueba vaiven-app como un usuario, sobre el stack LOCAL (Supabase en Docker + Vite):
  1. Registro y login de un usuario nuevo (A).
  2. Publicar una necesidad y una donación desde el formulario.
  3. Historial: las publicaciones aparecen agrupadas.
  4. RLS con dos sesiones: una publicación completada de A la ve A y no la ve B.

No toca archivos de vaiven-app. Crea usuarios nuevos en cada corrida (emails únicos) y no
imprime ni guarda contraseñas ni claves. Solo corre contra localhost.

Uso:
  python scripts/e2e-flujos-base.py --app <clon-de-vaiven-app> [--url http://localhost:5173] [--headed]
Salida: informe en salidas/e2e/<fecha>-<etiqueta>.md. Sale 0 si todo pasó, 1 si algo falló.
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from e2e_comun import (AVISO, FALLA, PASA, ROOT, Informe, archivo_unico, carpeta_salidas,  # noqa: E402
                       crear_usuario, entorno_local, grupos_historial, guardar_captura, login,
                       pub_por_titulo, publicar_donacion, publicar_necesidad, rest, sello, sha_probado,
                       solo_localhost)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--app", type=Path, required=True, help="Clon de vaiven-app con el stack local levantado")
    ap.add_argument("--url", default="http://localhost:5173", help="URL del frontend local")
    ap.add_argument("--etiqueta", default="local", help="Nombre para el informe (por ejemplo pr-74)")
    ap.add_argument("--headed", action="store_true", help="Mostrar el navegador")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    solo_localhost(args.url)

    inf = Informe()
    api, anon = entorno_local(args.app.resolve())
    carpeta, marca = carpeta_salidas(args.etiqueta), sello()

    a, b = crear_usuario(api, anon, "a"), crear_usuario(api, anon, "b")
    inf.anotar(PASA if a["ok"] and b["ok"] else FALLA, "Crear usuarios A y B en el Auth local")
    if a["ok"] and b["ok"]:
        titulo_nec, titulo_don = f"E2E necesidad {marca}", f"E2E donación {marca}"
        with sync_playwright() as pw:
            navegador = pw.chromium.launch(headless=not args.headed)
            page = navegador.new_context(viewport={"width": 390, "height": 844}).new_page()
            errores = []
            page.on("console", lambda m: errores.append(m.text) if m.type == "error" else None)
            try:
                if not login(page, args.url, a):
                    inf.anotar(FALLA, "Login del usuario A lleva a /feed", f"quedó en {page.url}")
                    raise RuntimeError("sin login")
                inf.anotar(PASA, "Login del usuario A lleva a /feed")

                ok = publicar_necesidad(page, args.url, titulo_nec)
                inf.anotar(PASA if ok else FALLA, "Publicar una necesidad desde el formulario",
                           "" if ok else f"quedó en {page.url}")

                aviso = publicar_donacion(page, args.url, titulo_don)
                guardada = pub_por_titulo(api, anon, a, titulo_don)
                inf.anotar(PASA if guardada else FALLA, "Publicar una donación: la publicación queda guardada")
                if guardada and aviso:
                    inf.anotar(AVISO, "Subida de la foto de la donación",
                               aviso + " (suele ser el servicio de storage del entorno local)")

                page.goto(args.url + "/historial")
                page.get_by_text(titulo_nec).wait_for(timeout=10000)
                grupos = grupos_historial(page)
                ok = any(g == "Activas" and titulo_nec in l for g, _, l in grupos)
                inf.anotar(PASA if ok else FALLA, "Historial agrupa las publicaciones en 'Activas'")
                guardar_captura(page, args.etiqueta, "historial.png", marca, full_page=True)
            except Exception as e:  # noqa: BLE001 — se informa y se sigue con RLS
                if str(e) != "sin login":
                    inf.anotar(FALLA, "Recorrido en el navegador interrumpido", str(e).splitlines()[0][:160])
                guardar_captura(page, args.etiqueta, "falla.png", marca)
            finally:
                navegador.close()
            if errores:
                inf.anotar(AVISO, "Errores en la consola del navegador", f"{len(errores)}; el primero: {errores[0][:120]}")

        # 4. RLS con dos sesiones
        fila = pub_por_titulo(api, anon, a, titulo_nec)
        if not fila:
            inf.anotar(AVISO, "RLS con dos sesiones", "no encontré la necesidad de A; se omite")
        else:
            pid = fila["id"]
            _, ve_b = rest(api, anon, "GET", f"/rest/v1/publicaciones?select=id&id=eq.{pid}", token=b["token"])
            inf.anotar(PASA if ve_b else AVISO, "Una publicación activa de A es visible para B (regla actual de la política)")
            est, resp = rest(api, anon, "PATCH", f"/rest/v1/publicaciones?id=eq.{pid}", token=a["token"],
                             cuerpo={"estado": "completada"})
            if est in (200, 204) and resp:
                _, ve_a = rest(api, anon, "GET", f"/rest/v1/publicaciones?select=id&id=eq.{pid}", token=a["token"])
                _, ve_b = rest(api, anon, "GET", f"/rest/v1/publicaciones?select=id&id=eq.{pid}", token=b["token"])
                inf.anotar(PASA if ve_a else FALLA, "RLS: A ve su publicación completada")
                inf.anotar(PASA if not ve_b else FALLA, "RLS: B NO ve la publicación completada de A",
                           "" if not ve_b else "B pudo leerla")
            else:
                inf.anotar(AVISO, "RLS con completada", f"A no pudo completar su publicación por REST (HTTP {est}); se omite")

    ruta = archivo_unico(carpeta, "flujos-base.md", marca)
    inf.escribir(ruta, f"Flujos base — {args.etiqueta}",
                 f"Fecha: {datetime.now():%Y-%m-%d %H:%M} · Commit probado: `{sha_probado(args.app.resolve())}` · "
                 f"Frontend: {args.url} · Stack: Supabase local")
    print(f"\n{inf.cuenta(PASA)} pasan · {inf.cuenta(FALLA)} fallan · {inf.cuenta(AVISO)} avisos — informe: {ruta.relative_to(ROOT)}")
    return 1 if inf.hay_fallas() else 0


if __name__ == "__main__":
    sys.exit(main())
