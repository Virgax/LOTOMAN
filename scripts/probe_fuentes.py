#!/usr/bin/env python3
"""
Sonda de fuentes — diagnóstico, no toca la base.

Desde el contenedor de Claude Code todas las fuentes de lotería están
bloqueadas por la política de egress. Desde un runner de Actions sí se llega,
así que la investigación se hace allá.

Lo que ya quedó establecido en las corridas 1 y 2 (2026-08-27):
  * resuloto.com para 2026-06-23 devuelve HTTP 200 con CERO bytes. Por eso
    update_db.py lo anotó "sin resultado": el hueco es de resuloto, no de
    Leidsa. El sorteo se hizo.
  * leidsa.com devuelve 258 KB con solo 45 chars de texto plano: los números
    van embebidos en JavaScript.
  * api3.bolillerobingoonlinegratis.com da 404 en /api, /api/sorteos,
    /api/sorteos/historial y /api/sorteos/buscar/historial. La ruta que
    documenta CLAUDE.md §7 ya no existe.
  * elboletoganador.com es un cascarón SPA de 2.5 KB.

Esta v3 va por tres cosas:
  1. Confirmar si los números de Kino se sacan del crudo de leidsa.com y si
     los ids son secuenciales por día.
  2. Encontrar la URL de Loto Pool en leidsa.com (Jaime lo pidió; el CLAUDE.md
     lo tenía descartado).
  3. Descubrir la API REAL de elboletoganador leyendo sus bundles de
     JavaScript, en vez de adivinar rutas. Jaime dice que ese sitio tiene más
     historia para Kino y Pool — hay que verificarlo, no asumirlo.

Uso:
    python scripts/probe_fuentes.py --salida probe/
"""

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urljoin

import requests

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
TIMEOUT = 25

SEC20 = re.compile(r"""(?:\b0?\d{1,2}\b[\s"']*,[\s"']*){19}\b0?\d{1,2}\b""")
RESUMEN = []          # (seccion, detalle) -> se imprime al final


def anotar(seccion, detalle):
    RESUMEN.append((seccion, detalle))
    print(f"  >> {detalle}")


def pedir(url, salida, nombre, **kw):
    try:
        r = requests.request(kw.pop("method", "GET"), url, headers=UA,
                             timeout=TIMEOUT, **kw)
    except requests.RequestException as e:
        anotar(nombre, f"ERROR de red: {e}")
        return None
    ct = r.headers.get("content-type", "?")
    print(f"  HTTP {r.status_code}  {ct}  {len(r.content):,} bytes")
    ext = "json" if "json" in ct else ("js" if "javascript" in ct else "html")
    (salida / f"{nombre}.{ext}").write_bytes(r.content)
    return r


def secuencias20(txt):
    """Todas las secuencias de 20 números distintos 1..80, con su posición."""
    out = []
    for m in SEC20.finditer(txt):
        v = [int(x) for x in re.findall(r"\d{1,2}", m.group(0))]
        if len(v) == 20 and len(set(v)) == 20 and all(1 <= x <= 80 for x in v):
            out.append((m.start(), sorted(v)))
    return out


# ---------------------------------------------------------------------------
# 1 y 2 — LEIDSA OFICIAL
# ---------------------------------------------------------------------------
def sondear_leidsa(salida, kino_ids):
    print(f"\n{'=' * 70}\n## LEIDSA OFICIAL\n{'=' * 70}")

    # Mapa del sitio: qué juegos publica y con qué patrón de URL.
    print("\n### portada /results")
    r = pedir("https://www.leidsa.com/results", salida, "leidsa_results")
    if r is not None and r.status_code == 200:
        enlaces = sorted(set(re.findall(r'href="(/results/[^"]+)"', r.text)))
        anotar("leidsa/mapa", f"{len(enlaces)} enlaces /results/: {enlaces[:25]}")
        pool = [e for e in enlaces if re.search(r"pool", e, re.I)]
        anotar("leidsa/pool", f"enlaces que mencionan Pool: {pool[:10] or 'NINGUNO'}")

    # Kino: tres ids seguidos. Si los tres dan sorteos distintos, el parser
    # sirve y los ids son secuenciales por día.
    for kid in kino_ids:
        print(f"\n### KinoTV 3_{kid}")
        r = pedir(f"https://www.leidsa.com/results/Leidsa/KinoTV/3_{kid}",
                  salida, f"leidsa_kino_{kid}")
        if r is None or r.status_code != 200:
            anotar(f"leidsa/kino/{kid}", f"HTTP {r.status_code if r else '-'}")
            continue
        titulo = re.search(r"<title>(.{0,80})", r.text, re.S)
        cands = secuencias20(r.text)
        anotar(f"leidsa/kino/{kid}",
               f"titulo={(titulo.group(1).strip() if titulo else '?')!r} "
               f"candidatas={len(cands)} "
               f"primera={cands[0][1] if cands else None}")
        for pos, v in cands[:3]:
            ctx = re.sub(r"\s+", " ", r.text[max(0, pos - 200):pos])[-200:]
            print(f"     @{pos} {v}\n        contexto: ...{ctx}")


# ---------------------------------------------------------------------------
# 3 — ELBOLETOGANADOR: encontrar la API real leyendo sus bundles
# ---------------------------------------------------------------------------
def sondear_elboleto(salida):
    print(f"\n{'=' * 70}\n## ELBOLETOGANADOR — descubrir la API real\n{'=' * 70}")
    base = "https://elboletoganador.com/"
    r = pedir(base, salida, "ebg_shell")
    if r is None or r.status_code != 200:
        anotar("ebg/shell", "no se pudo bajar la portada")
        return

    srcs = re.findall(r'<script[^>]*src="([^"]+)"', r.text, re.I)
    links = re.findall(r'<link[^>]*href="([^"]+\.js)"', r.text, re.I)
    bundles = sorted(set(srcs + links))
    anotar("ebg/shell", f"{len(bundles)} bundles JS: {bundles[:12]}")

    # Patrones que delatan endpoints dentro del JS minificado
    pat_url = re.compile(r"""https?://[A-Za-z0-9._-]+(?:/[A-Za-z0-9._~%/-]*)?""")
    pat_ruta = re.compile(r"""["'`](/api/[A-Za-z0-9._~%/-]{2,60})["'`]""")

    hosts, rutas = set(), set()
    for i, b in enumerate(bundles[:12]):
        url = urljoin(base, b)
        print(f"\n### bundle {i}: {url}")
        rb = pedir(url, salida, f"ebg_bundle_{i}")
        if rb is None or rb.status_code != 200:
            continue
        js = rb.text
        for m in pat_url.finditer(js):
            u = m.group(0)
            if re.search(r"api|sorteo|histor|lot|bolillero", u, re.I):
                hosts.add(u)
        for m in pat_ruta.finditer(js):
            rutas.add(m.group(1))

    anotar("ebg/urls", f"URLs con pinta de API ({len(hosts)}): {sorted(hosts)[:25]}")
    anotar("ebg/rutas", f"rutas /api/* ({len(rutas)}): {sorted(rutas)[:25]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default="probe")
    ap.add_argument("--kino-ids", default="6247,6248,6244",
                    help="ids de Leidsa a pedir (23, 24 y 20 de junio 2026)")
    args = ap.parse_args()

    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)

    sondear_leidsa(salida, [int(x) for x in args.kino_ids.split(",")])
    sondear_elboleto(salida)

    print(f"\n{'=' * 70}\n@@ RESUMEN @@\n{'=' * 70}")
    for seccion, detalle in RESUMEN:
        print(f"[{seccion}] {detalle}")
    print(f"{'=' * 70}\nCrudos en {salida}/")


if __name__ == "__main__":
    main()
