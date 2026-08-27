#!/usr/bin/env python3
"""
Sonda de fuentes — diagnóstico, no toca la base.

Desde el contenedor de Claude Code todas las fuentes de lotería están
bloqueadas por egress. Desde un runner de Actions sí se llega.

Historia de lo aprendido (2026-08-27):

  v1  resuloto.com para 2026-06-23 devuelve HTTP 200 con CERO bytes -> el
      hueco es de resuloto, no de Leidsa. El sorteo se hizo.
      La API de CLAUDE.md §7 da 404 en las 4 rutas probadas.
      elboletoganador.com es un cascarón SPA de 2.5 KB.
  v2  leidsa.com trae los números embebidos en JavaScript.
  v3  Contrastado contra la base: la página 3_6248 (24/6) parseó EXACTA, pero
      la 3_6244 (20/6) dio un solape de 5/20 — puro azar. Cada página tiene
      ~102 secuencias de 20 números distintos, así que "la primera" es una
      moneda al aire. La heurística de update_db.py NO SIRVE aquí.

Esta v4 no adivina: usa la base como verdad de campo. Para cada página cuya
fecha YA está en la base, busca cuál de las ~102 candidatas es la correcta y
reporta su posición y su contexto. Si todas caen en el mismo campo, ese es el
parser que hay que escribir.

Uso:
    python scripts/probe_fuentes.py --salida probe/
"""

import argparse
import re
from datetime import date, timedelta
from pathlib import Path

import requests
from openpyxl import load_workbook

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
SEC20 = re.compile(r"""(?:\b0?\d{1,2}\b[\s"']*,[\s"']*){19}\b0?\d{1,2}\b""")
DB = Path(__file__).parent.parent / "data" / "kino_2010_a_hoy_COMPLETO.xlsx"

# Ancla confirmada por título en la corrida v3: id 6248 = 2026-06-24.
ANCLA_ID, ANCLA_FECHA = 6248, date(2026, 6, 24)
RESUMEN = []


def anotar(s, d):
    RESUMEN.append((s, d))
    print(f"  >> {d}")


def base_conocida():
    """{date: [20 números]} de lo que ya está guardado."""
    wb = load_workbook(DB, read_only=True, data_only=True)
    out = {}
    for hoja in wb.sheetnames:
        if not hoja.strip().isdigit():
            continue
        for a, b in wb[hoja].iter_rows(min_col=1, max_col=2, values_only=True):
            if not a or not b or not isinstance(b, str):
                continue
            try:
                d = date.fromisoformat(str(a).strip()[:10])
            except ValueError:
                continue
            out[d] = sorted(int(x) for x in b.replace(" ", "").split(",") if x)
    wb.close()
    return out


def candidatas(html):
    """[(posicion, [20 numeros])] — todas, en orden de aparición."""
    out = []
    for m in SEC20.finditer(html):
        v = [int(x) for x in re.findall(r"\d{1,2}", m.group(0))]
        if len(v) == 20 and len(set(v)) == 20 and all(1 <= x <= 80 for x in v):
            out.append((m.start(), sorted(v)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default="probe")
    ap.add_argument("--dias", type=int, default=6,
                    help="cuántos días alrededor del ancla pedir")
    args = ap.parse_args()

    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)
    base = base_conocida()
    anotar("base", f"{len(base):,} sorteos conocidos, último {max(base)}")

    print(f"\n{'=' * 70}\n## LEIDSA — hallar el campo correcto usando la base\n{'=' * 70}")
    aciertos = []
    for off in range(-args.dias, args.dias + 1):
        kid = ANCLA_ID + off
        esperada = ANCLA_FECHA + timedelta(days=off)
        url = f"https://www.leidsa.com/results/Leidsa/KinoTV/3_{kid}"
        print(f"\n### 3_{kid}  (se espera {esperada})")
        try:
            r = requests.get(url, headers=UA, timeout=30)
        except requests.RequestException as e:
            anotar(f"leidsa/{kid}", f"ERROR de red: {e}")
            continue
        if r.status_code != 200:
            anotar(f"leidsa/{kid}", f"HTTP {r.status_code}")
            continue
        (salida / f"leidsa_{kid}.html").write_bytes(r.content)

        # La fecha REAL la dice el título, no mi suposición.
        mt = re.search(r"<title>\s*Leidsa KinoTV Resultados \|\s*(\d+)/(\d+)/(\d+)",
                       r.text)
        if not mt:
            anotar(f"leidsa/{kid}", "sin título parseable")
            continue
        dd, mm, yy = (int(x) for x in mt.groups())
        real = date(yy, mm, dd)

        cands = candidatas(r.text)
        conocido = base.get(real)
        if not conocido:
            anotar(f"leidsa/{kid}",
                   f"fecha={real} (esperada {esperada}) NO está en la base — "
                   f"{len(cands)} candidatas, es la que hay que recuperar")
            continue

        # ¿Cuál de las candidatas es la buena?
        hit = [(i, pos) for i, (pos, v) in enumerate(cands) if v == conocido]
        if not hit:
            mejor = max((len(set(v) & set(conocido)), i)
                        for i, (_, v) in enumerate(cands)) if cands else (0, -1)
            anotar(f"leidsa/{kid}",
                   f"fecha={real} coincide_exacta=NINGUNA de {len(cands)} "
                   f"(mejor solape {mejor[0]}/20) -> el dato NO está en la página")
            continue

        i, pos = hit[0]
        ctx = re.sub(r"\s+", " ", r.text[max(0, pos - 260):pos])[-260:]
        aciertos.append((real, i, len(cands), ctx))
        anotar(f"leidsa/{kid}",
               f"fecha={real} ok=SI rank={i}/{len(cands)} @{pos}")
        print(f"     contexto: ...{ctx}")

    print(f"\n{'=' * 70}\n@@ RESUMEN @@\n{'=' * 70}")
    for s, d in RESUMEN:
        print(f"[{s}] {d}")
    if aciertos:
        ranks = sorted({i for _, i, _, _ in aciertos})
        print(f"\n[VEREDICTO] {len(aciertos)} páginas verificadas contra la base.")
        print(f"[VEREDICTO] ranks de la candidata correcta: {ranks}")
        print("[VEREDICTO] rank constante => el parser es posicional y sirve.")
        print("[VEREDICTO] contextos:")
        for real, i, n, ctx in aciertos:
            print(f"   {real} rank {i}/{n}: ...{ctx[-160:]}")
    else:
        print("\n[VEREDICTO] ninguna página se pudo verificar contra la base.")
    print("=" * 70)


if __name__ == "__main__":
    main()
