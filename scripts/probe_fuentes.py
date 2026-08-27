#!/usr/bin/env python3
"""
Sonda de fuentes — diagnóstico, no toca la base.

Para qué: desde el contenedor de Claude Code todas las fuentes de lotería están
bloqueadas por la política de egress. Desde un runner de GitHub Actions sí se
llega. Esta sonda pide las mismas URLs desde allá y vuelca lo que devuelven,
para poder escribir el parser con datos reales en la mano en vez de adivinando.

Objetivo inmediato: 2026-06-23, el único día del tramo 2026-03-25..08-25 que
quedó sin explicar. La búsqueda web dice que Leidsa sí tiene página de
resultados para ese día (/results/Leidsa/KinoTV/3_6247), así que el sorteo se
hizo y resuloto.com fue quien falló.

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


def intento(nombre, salida, **kw):
    """Hace una petición, la guarda cruda y reporta un resumen."""
    print(f"\n{'=' * 70}\n### {nombre}\n{kw.get('method','GET')} {kw['url']}")
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

    ext = "json" if "json" in ct else "html"
    dest = salida / f"{nombre}.{ext}"
    dest.write_bytes(r.content)
    print(f"  guardado -> {dest}")

    if r.status_code != 200:
        print(f"  cuerpo (500 chars): {r.text[:500]}")
        return

    if "json" in ct:
        try:
            print("  JSON (2000 chars):")
            print("  " + json.dumps(r.json(), ensure_ascii=False)[:2000])
        except ValueError:
            print(f"  no parseó como JSON: {r.text[:500]}")
    else:
        txt = texto_plano(r.text)
        print(f"  texto plano ({len(txt):,} chars), primeros 1500:")
        print("  " + txt[:1500])
        n = numeros(txt)
        print(f"\n  heurística de 20 números -> {n}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fecha", default="2026-06-23")
    ap.add_argument("--kino-id", type=int, default=6247,
                    help="id de la página oficial de Leidsa para esa fecha")
    ap.add_argument("--salida", default="probe")
    args = ap.parse_args()

    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)
    f = args.fecha
    print(f"Sonda para {f}\n")

    # 1. resuloto — la fuente que usa update_db.py hoy. ¿Por qué falló?
    intento("resuloto", salida,
            url=f"https://www.resuloto.com/do/leid/super-kino-tv-amp.php?fecha={f}")

    # 2. Leidsa oficial — la búsqueda dice que esta página existe para el 23/6.
    intento("leidsa_oficial", salida,
            url=f"https://www.leidsa.com/results/Leidsa/KinoTV/3_{args.kino_id}")

    # 3-5. elboletoganador / API. CLAUDE.md documenta el endpoint y que `fecha`
    # es un cursor hacia atrás, pero no la forma exacta de la petición. El
    # bloqueo por CORS que menciona es cosa del navegador; desde el servidor no
    # aplica. Probamos varias formas para ver cuál responde.
    api = "https://api3.bolillerobingoonlinegratis.com/api/sorteos/buscar/historial"
    intento("api_get", salida, url=api, params={"gameId": 8, "fecha": f})
    intento("api_post_gameId", salida, method="POST", url=api,
            json={"gameId": 8, "fecha": f})
    intento("api_post_juego", salida, method="POST", url=api,
            json={"juego": 8, "fecha": f})
    intento("elboletoganador", salida, url="https://elboletoganador.com/")

    print(f"\n{'=' * 70}\nListo. Respuestas crudas en {salida}/")


if __name__ == "__main__":
    main()
