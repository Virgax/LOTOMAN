#!/usr/bin/env python3
"""
Sonda de fuentes — diagnóstico, no toca la base.

Para qué: desde el contenedor de Claude Code todas las fuentes de lotería están
bloqueadas por la política de egress. Desde un runner de GitHub Actions sí se
llega. Esta sonda pide las mismas URLs desde allá y vuelca lo que devuelven,
para poder escribir el parser con datos reales en la mano en vez de adivinando.

Objetivo inmediato: 2026-06-23, el único día del tramo 2026-03-25..08-25 que
quedó sin explicar.

Hallazgos de la corrida 1 (2026-08-27), que definen lo que hace la v2:
  * resuloto.com para esa fecha devuelve HTTP 200 con CERO bytes. Por eso
    update_db.py la registró como "sin resultado": el hueco es de resuloto.
  * leidsa.com/results/Leidsa/KinoTV/3_6247 devuelve 258 KB pero solo 45 chars
    de texto plano. Los números están embebidos en JavaScript, y quitar los
    <script> los borra justo a ellos. -> hay que buscar en el CRUDO.
  * api3.bolillerobingoonlinegratis.com/api/sorteos/buscar/historial da 404 en
    GET y en POST. La ruta documentada en CLAUDE.md ya no existe.
  * elboletoganador.com es un cascarón SPA de 2.5 KB sin contenido servido.

Uso:
    python scripts/probe_fuentes.py --fecha 2026-06-23 --salida probe/
"""

import argparse
import json
import re
import sys
from pathlib import Path

import requests

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
TIMEOUT = 25

# 20 números de 1-2 dígitos separados por coma, tolerando comillas y espacios
# alrededor (que es como vienen serializados dentro de JS/JSON).
SEC20 = re.compile(r"""(?:\b0?\d{1,2}\b[\s"']*,[\s"']*){19}\b0?\d{1,2}\b""")


def texto_plano(html):
    """Quita scripts/estilos/tags para poder mirar el contenido a ojo."""
    h = re.sub(r"<(script|style).*?</\1>", " ", html, flags=re.S | re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()


def numeros(txt):
    """Primera ventana de 20 números distintos en 1..80 — la misma heurística
    que usa update_db.py, para ver si habría funcionado sobre esta respuesta."""
    ns = [int(x) for x in re.findall(r"\b(\d{1,2})\b", txt) if 1 <= int(x) <= 80]
    for i in range(len(ns) - 19):
        v = ns[i:i + 20]
        if len(set(v)) == 20:
            return sorted(set(v))
    return None


def cazar_en_crudo(html, etiqueta):
    """Busca los 20 números DENTRO del HTML crudo, scripts incluidos."""
    print(f"\n  --- buscando dentro del crudo de {etiqueta} ({len(html):,} chars) ---")

    # Bloques JSON típicos de SPA (Nuxt / Next / <script type=application/json>)
    blobs = [
        (r"window\.__NUXT__\s*=\s*(.{0,800})", "__NUXT__"),
        (r'<script[^>]*id="__NEXT_DATA__"[^>]*>(.{0,800})', "__NEXT_DATA__"),
        (r'<script[^>]*type="application/json"[^>]*>(.{0,800})', "application/json"),
    ]
    for pat, nombre in blobs:
        for m in re.finditer(pat, html, re.S | re.I):
            print(f"  [{nombre}] {m.group(1)[:500]}")

    # Inventario de scripts, para saber si el contenido llega por fetch aparte
    srcs = re.findall(r'<script[^>]*src="([^"]+)"', html, re.I)
    if srcs:
        print(f"  scripts externos ({len(srcs)}): {srcs[:8]}")

    cands = []
    for m in SEC20.finditer(html):
        v = [int(x) for x in re.findall(r"\d{1,2}", m.group(0))]
        if len(v) == 20 and len(set(v)) == 20 and all(1 <= x <= 80 for x in v):
            cands.append((m.start(), sorted(v), m.group(0)[:160]))

    if not cands:
        print("  (ninguna secuencia de 20 números distintos 1..80 en el crudo)")
        return None

    print(f"  {len(cands)} candidata(s):")
    for pos, v, crudo in cands[:6]:
        ctx = re.sub(r"\s+", " ", html[max(0, pos - 220):pos])
        print(f"   @{pos}: {v}")
        print(f"      crudo    : {crudo}")
        print(f"      contexto : ...{ctx[-220:]}")
    return cands[0][1]


def intento(nombre, salida, **kw):
    """Hace una petición, la guarda cruda y reporta un resumen."""
    print(f"\n{'=' * 70}\n### {nombre}\n{kw.get('method', 'GET')} {kw['url']}")
    if kw.get("json"):
        print(f"body: {json.dumps(kw['json'])}")
    try:
        r = requests.request(kw.get("method", "GET"), kw["url"], headers=UA,
                             json=kw.get("json"), params=kw.get("params"),
                             timeout=TIMEOUT)
    except requests.RequestException as e:
        print(f"  ERROR de red: {e}")
        return

    ct = r.headers.get("content-type", "?")
    print(f"  HTTP {r.status_code}  {ct}  {len(r.content):,} bytes")

    dest = salida / f"{nombre}.{'json' if 'json' in ct else 'html'}"
    dest.write_bytes(r.content)
    print(f"  guardado -> {dest}")

    if r.status_code != 200:
        print(f"  cuerpo (300 chars): {r.text[:300]}")
        return

    if "json" in ct:
        try:
            print("  JSON (2000 chars):")
            print("  " + json.dumps(r.json(), ensure_ascii=False)[:2000])
        except ValueError:
            print(f"  no parseó como JSON: {r.text[:300]}")
        return

    txt = texto_plano(r.text)
    print(f"  texto plano ({len(txt):,} chars): {txt[:600]}")
    print(f"  heurística sobre texto plano -> {numeros(txt)}")
    cazar_en_crudo(r.text, nombre)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fecha", default="2026-06-23")
    ap.add_argument("--kino-id", type=int, default=6247,
                    help="id de la página oficial de Leidsa para esa fecha")
    ap.add_argument("--salida", default="probe")
    args = ap.parse_args()

    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)
    f, kid = args.fecha, args.kino_id
    print(f"Sonda para {f}  (kino id {kid})\n")

    # 1. Leidsa oficial — la apuesta principal. 258 KB de JS con los números
    #    adentro. Se piden 3 ids seguidos: si los tres parsean y dan sorteos
    #    distintos, el parser sirve y los ids son secuenciales por día.
    for off in (0, 1, -3):
        intento(f"leidsa_{kid + off}", salida,
                url=f"https://www.leidsa.com/results/Leidsa/KinoTV/3_{kid + off}")

    # 2. resuloto — para dejar documentado que devuelve 200 con 0 bytes.
    intento("resuloto", salida,
            url=f"https://www.resuloto.com/do/leid/super-kino-tv-amp.php?fecha={f}")

    # 3. ¿Existe alguna ruta viva en la API? La documentada da 404.
    base = "https://api3.bolillerobingoonlinegratis.com"
    for ruta in ("/api/sorteos/buscar/historial", "/api/sorteos/historial",
                 "/api/sorteos", "/api"):
        intento(f"api{ruta.replace('/', '_')}", salida,
                url=base + ruta, params={"gameId": 8, "fecha": f})

    print(f"\n{'=' * 70}\nListo. Respuestas crudas en {salida}/")


if __name__ == "__main__":
    main()
