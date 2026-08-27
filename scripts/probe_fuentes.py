#!/usr/bin/env python3
"""
Sonda de fuentes — diagnóstico, no toca la base.

Desde el contenedor de Claude Code todas las fuentes de lotería están
bloqueadas por egress. Desde un runner de Actions sí se llega.

Historia de lo aprendido (2026-08-27):

  v1  resuloto.com para 2026-06-23 devuelve HTTP 200 con CERO bytes -> el
      hueco es de resuloto, no de Leidsa. El sorteo se hizo.
      La API de elboletoganador que documenta CLAUDE.md §7 da 404 en las 4
      rutas probadas; el sitio es un cascarón SPA de 2.5 KB.
  v2  leidsa.com trae los números embebidos en JavaScript.
  v3  Contrastado contra la base: 3_6248 (24/6) parseó EXACTA, pero 3_6244
      (20/6) dio solape 5/20. Cada página tiene ~102 secuencias de 20 números
      distintos: "la primera" es una moneda al aire. La heurística de
      update_db.py no sirve en páginas ricas.
      elboletoganador dio timeout de conexión — segunda falla seguida.
  v4  13 páginas de Leidsa bajadas para cruzarlas contra la base.

Esta v5 agrega conectate.com, que es lo que pidió Jaime, y mantiene la regla
que sacamos a golpes: NADA se da por bueno si no coincide exacto con un sorteo
que ya está en la base. Verdad de campo o no se usa.

Uso:
    python scripts/probe_fuentes.py --salida probe/
"""

import argparse
import re
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urljoin

import requests
from openpyxl import load_workbook

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
SEC20 = re.compile(r"""(?:\b0?\d{1,2}\b[\s"']*,[\s"']*){19}\b0?\d{1,2}\b""")
DB = Path(__file__).parent.parent / "data" / "kino_2010_a_hoy_COMPLETO.xlsx"

ANCLA_ID, ANCLA_FECHA = 6248, date(2026, 6, 24)   # confirmado por <title> en v3
VEREDICTO = []


def veredicto(linea):
    VEREDICTO.append(linea)
    print(f"  >> {linea}")


def base_conocida():
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


def candidatas(txt):
    """Todas las ventanas de 20 números distintos 1..80, SOLAPADAS.

    OJO — aquí estaba el bug de las v3/v5: se usaba re.finditer con un patrón
    de 20 números, que NO solapa. Si el sorteo real no empezaba justo en el
    borde de un match, el regex devolvía una ventana corrida un lugar: 19 de
    los 20 números buenos más un vecino. De ahí salían los "SIN MATCH (mejor
    solape 19/20)" y las "102 candidatas". No era la fuente: era el parser.

    Deslizar una ventana sobre TODOS los números en orden lo resuelve, y de
    paso sirve igual si vienen separados por coma o por espacios (conectate
    los pinta en elementos HTML sueltos, sin comas).
    """
    ns = [(m.start(), int(m.group()))
          for m in re.finditer(r"\d{1,2}", txt) if 1 <= int(m.group()) <= 80]
    out = []
    for i in range(len(ns) - 19):
        v = [n for _, n in ns[i:i + 20]]
        if len(set(v)) == 20:
            out.append((ns[i][0], sorted(v)))
    return out


def texto(html):
    h = re.sub(r"<(script|style).*?</\1>", " ", html, flags=re.S | re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()


def bajar(url, salida, nombre, timeout=30):
    try:
        r = requests.get(url, headers=UA, timeout=timeout)
    except requests.RequestException as e:
        print(f"  ERROR de red: {type(e).__name__}")
        return None
    print(f"  HTTP {r.status_code}  {len(r.content):,} bytes")
    (salida / f"{nombre}.html").write_bytes(r.content)
    return r


def cotejar(html, base, etiqueta):
    """¿Alguna secuencia de la página coincide EXACTO con un sorteo conocido?

    Esta es la única prueba que vale. Si una página trae sorteos reales, al
    menos uno tiene que dar match perfecto contra la base.
    """
    cands = candidatas(html)
    conocidos = {tuple(v): d for d, v in base.items()}
    hits = []
    for pos, v in cands:
        d = conocidos.get(tuple(v))
        if d:
            hits.append((d, pos, v))
    print(f"  {len(cands)} secuencias de 20 | {len(hits)} coinciden con la base")
    for d, pos, v in hits[:8]:
        print(f"     {d} @{pos}: {v}")
    return cands, hits


# ---------------------------------------------------------------------------
def sondear_conectate(salida, base):
    print(f"\n{'=' * 70}\n## CONECTATE.COM\n{'=' * 70}")
    urls = [
        ("cnt_indice", "https://loterias.conectate.com.do/leidsa/"),
        ("cnt_kino", "https://www.conectate.com.do/loterias/leidsa/super-kino-tv"),
        ("cnt_kino_sub", "https://loterias.conectate.com.do/leidsa/super-kino-tv/"),
        ("cnt_pool", "https://www.conectate.com.do/loterias/leidsa/loto-pool"),
        ("cnt_pool_sub", "https://loterias.conectate.com.do/leidsa/loto-pool/"),
        ("cnt_leidsa", "https://www.conectate.com.do/loterias/leidsa"),
    ]
    for nombre, url in urls:
        print(f"\n### {nombre}\n{url}")
        r = bajar(url, salida, nombre)
        if r is None or r.status_code != 200:
            veredicto(f"{nombre}: HTTP {r.status_code if r else 'ERROR'}")
            continue
        t = texto(r.text)
        print(f"  texto plano: {len(t):,} chars")
        print(f"\n  --- texto plano de {nombre} (primeros 2200 chars) ---")
        print("  " + t[:2200])
        print("  --- fin ---\n")
        print("  [sobre HTML crudo]")
        cands, hits = cotejar(r.text, base, nombre)
        print("  [sobre texto plano]")
        cands_t, hits_t = cotejar(t, base, nombre + "/texto")
        if hits_t and not hits:
            cands, hits = cands_t, hits_t
        veredicto(f"{nombre}: {len(r.content):,}B texto={len(t):,} "
                  f"secuencias={len(cands)} MATCH_BASE={len(hits)}"
                  + (f" fechas={[str(d) for d, _, _ in hits[:5]]}" if hits else ""))

        # ¿Hay historial? Enlaces con fecha o con pinta de archivo.
        enlaces = sorted(set(re.findall(r'href="([^"]*(?:loteria|resultado|histor|fecha|20\d\d)[^"]*)"',
                                        r.text, re.I)))
        if enlaces:
            print(f"  {len(enlaces)} enlaces con pinta de historial:")
            for e in enlaces[:20]:
                print(f"     {urljoin(url, e)}")
            veredicto(f"{nombre}: {len(enlaces)} enlaces candidatos a historial")


def sondear_leidsa(salida, base, dias):
    print(f"\n{'=' * 70}\n## LEIDSA — ¿en qué posición cae la candidata correcta?\n{'=' * 70}")
    ranks = []
    for off in range(-dias, dias + 1):
        kid = ANCLA_ID + off
        url = f"https://www.leidsa.com/results/Leidsa/KinoTV/3_{kid}"
        print(f"\n### 3_{kid}")
        r = bajar(url, salida, f"leidsa_{kid}")
        if r is None or r.status_code != 200:
            continue
        mt = re.search(r"<title>\s*Leidsa KinoTV Resultados \|\s*(\d+)/(\d+)/(\d+)", r.text)
        if not mt:
            print("  sin título parseable")
            continue
        dd, mm, yy = (int(x) for x in mt.groups())
        real = date(yy, mm, dd)
        cands = candidatas(r.text)
        conocido = base.get(real)
        if not conocido:
            veredicto(f"leidsa 3_{kid}: fecha={real} NO está en la base "
                      f"({len(cands)} candidatas) <- ESTA es la que falta")
            continue
        hit = [i for i, (_, v) in enumerate(cands) if v == conocido]
        if hit:
            ranks.append(hit[0])
            pos = cands[hit[0]][0]
            ctx = re.sub(r"\s+", " ", r.text[max(0, pos - 200):pos])[-200:]
            veredicto(f"leidsa 3_{kid}: fecha={real} OK rank={hit[0]}/{len(cands)}")
            print(f"     contexto: ...{ctx}")
        else:
            mejor = max((len(set(v) & set(conocido)) for _, v in cands), default=0)
            veredicto(f"leidsa 3_{kid}: fecha={real} SIN MATCH "
                      f"(mejor solape {mejor}/20 de {len(cands)})")
    if ranks:
        veredicto(f"leidsa RANKS de la candidata correcta: {sorted(set(ranks))} "
                  + ("(CONSTANTE -> parser posicional sirve)"
                     if len(set(ranks)) == 1 else "(VARIABLE -> hace falta anclar por campo)"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default="probe")
    ap.add_argument("--dias", type=int, default=3)
    ap.add_argument("--saltar-leidsa", action="store_true")
    args = ap.parse_args()

    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)
    base = base_conocida()
    veredicto(f"base: {len(base):,} sorteos conocidos, último {max(base)}")

    sondear_conectate(salida, base)
    if not args.saltar_leidsa:
        sondear_leidsa(salida, base, args.dias)

    # El veredicto va al final Y se guarda aparte, para no tener que paginar
    # 300 líneas de log por tres datos.
    txt = "\n".join(f"[V] {l}" for l in VEREDICTO)
    Path("veredicto.txt").write_text(txt + "\n")
    print(f"\n{'=' * 70}\n@@ VEREDICTO @@\n{'=' * 70}\n{txt}\n{'=' * 70}")

    # Reporte al repo: paginar logs de GitHub para leer 15 líneas sale caro.
    rep = salida / "REPORTE.md"
    rep.write_text(
        "# Sonda de fuentes — último resultado\n\n"
        "Generado por `.github/workflows/probe-fuentes.yml`. Diagnóstico, no "
        "toca la base.\n\n"
        "Criterio: una fuente solo cuenta si alguna de sus secuencias de 20 "
        "números coincide EXACTO\ncon un sorteo que ya está en la base "
        "(`MATCH_BASE`). Contar bytes no prueba nada.\n\n"
        "```\n" + txt + "\n```\n")
    print(f"reporte -> {rep}")


if __name__ == "__main__":
    main()
