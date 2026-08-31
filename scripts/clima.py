#!/usr/bin/env python3
"""
Prueba directa de la hipótesis de Jaime: ¿el clima a la hora del sorteo
influye en qué números salen?

La hipótesis física NO es tonta: la densidad del aire cambia con presión,
temperatura y humedad, y eso afecta cómo flotan y rebotan las bolas. Es la
razón por la que las loterías serias pesan las bolas y rotan los sets.

Lo que se mide, por número (1..80 en Kino, 1..31 en Pool):

    ¿La temperatura media de los días en que SALIÓ ese número es distinta
    de la de los días en que NO salió?

Bajo la hipótesis nula (el clima no influye) las dos medias son iguales.
Se usa la t de Welch, que no exige varianzas iguales ni grupos del mismo
tamaño. Igual para presión y humedad.

Son 80 números x 3 variables = 240 pruebas en Kino. Con alfa 0.05 se esperan
12 con p<0.05 por PURO AZAR. Todo pasa por Benjamini-Hochberg — reportar esas
12 como hallazgos sería repetir exactamente el error del falso ciclo-5.

Fuente del clima: Open-Meteo ERA5 (archivo histórico, gratis, sin API key).
Coordenadas de Santo Domingo. Hora del sorteo: 20:55 local, salvo domingos
que es 15:55 — se toma la hora redondeada correspondiente.

Uso:
    python scripts/clima.py --bajar        # descarga y cachea el clima
    python scripts/clima.py                # corre las pruebas
"""

import argparse
import csv
import math
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from hipotesis import benjamini_hochberg, norm_sf   # noqa: E402

CACHE = Path(__file__).parent.parent / "data" / "clima_santo_domingo.csv"
LAT, LON = 18.4861, -69.9312          # Santo Domingo
VARS = ["temperature_2m", "surface_pressure", "relative_humidity_2m"]
NOMBRES = {"temperature_2m": "temperatura",
           "surface_pressure": "presion",
           "relative_humidity_2m": "humedad"}


def hora_sorteo(d):
    """20:55 todos los días; domingos 15:55. Se redondea a la hora entera."""
    return 15 if d.weekday() == 6 else 20


def bajar(desde=2010, hasta=2026):
    """Descarga el clima horario y cachea SOLO la hora del sorteo por día."""
    import requests
    filas = {}
    for anio in range(desde, hasta + 1):
        fin = f"{anio}-12-31" if anio < hasta else date.today().isoformat()
        url = ("https://archive-api.open-meteo.com/v1/archive"
               f"?latitude={LAT}&longitude={LON}"
               f"&start_date={anio}-01-01&end_date={fin}"
               f"&hourly={','.join(VARS)}"
               "&timezone=America%2FSanto_Domingo")
        print(f"  {anio}...", end=" ", flush=True)
        r = requests.get(url, timeout=120)
        r.raise_for_status()
        h = r.json()["hourly"]
        for i, t in enumerate(h["time"]):
            f = date.fromisoformat(t[:10])
            if int(t[11:13]) != hora_sorteo(f):
                continue
            vals = [h[v][i] for v in VARS]
            if any(v is None for v in vals):
                continue
            filas[f] = vals
        print(f"{len(filas):,} días acumulados")

    CACHE.parent.mkdir(parents=True, exist_ok=True)
    with CACHE.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["fecha"] + VARS)
        for f in sorted(filas):
            w.writerow([f.isoformat()] + filas[f])
    print(f"\nGuardado: {CACHE}  ({len(filas):,} días)")


def leer_clima():
    if not CACHE.exists():
        sys.exit(f"No existe {CACHE}. Corre primero con --bajar")
    out = {}
    with CACHE.open() as fh:
        for row in csv.DictReader(fh):
            try:
                out[date.fromisoformat(row["fecha"])] = \
                    {v: float(row[v]) for v in VARS}
            except (ValueError, TypeError):
                continue
    return out


def welch(a, b):
    """t de Welch -> (t, p). Grupos de tamaños y varianzas distintas."""
    na, nb = len(a), len(b)
    if na < 30 or nb < 30:
        return 0.0, 1.0
    ma, mb = sum(a) / na, sum(b) / nb
    va = sum((x - ma) ** 2 for x in a) / (na - 1)
    vb = sum((x - mb) ** 2 for x in b) / (nb - 1)
    se = math.sqrt(va / na + vb / nb)
    if se == 0:
        return 0.0, 1.0
    t = (ma - mb) / se
    return t, 2 * norm_sf(abs(t))      # n grande -> t ~ normal


def correr(nombre, sorteos, lo, hi, clima):
    emparejados = [(f, nums) for f, nums in sorteos if f in clima]
    print(f"\n{'='*70}\n{nombre}\n{'='*70}")
    print(f"sorteos con clima disponible: {len(emparejados):,} de {len(sorteos):,}")
    if len(emparejados) < 500:
        print("!! muy pocos para probar nada"); return []

    pruebas, detalle = [], {}
    for var in VARS:
        serie = {f: clima[f][var] for f, _ in emparejados}
        for n in range(lo, hi + 1):
            con = [serie[f] for f, nums in emparejados if n in nums]
            sin = [serie[f] for f, nums in emparejados if n not in nums]
            t, p = welch(con, sin)
            clave = f"{NOMBRES[var]}/{n:02d}"
            pruebas.append((clave, p))
            if con and sin:
                detalle[clave] = (sum(con)/len(con), sum(sin)/len(sin), t)

    res = benjamini_hochberg(pruebas)
    sig = [r for r in res if r[3]]
    crudas = [r for r in res if r[1] < 0.05]
    print(f"\npruebas: {len(res)}   p<0.05 sin corregir: {len(crudas)} "
          f"(esperadas por azar: {len(res)*0.05:.1f})   sobreviven BH: {len(sig)}")

    print(f"\nlas 6 más extremas:")
    print(f"   {'prueba':<18} {'salió':>9} {'no salió':>10} {'dif':>8} "
          f"{'p':>9} {'q(BH)':>9}")
    for nom, p, q, s in res[:6]:
        if nom in detalle:
            a, b, t = detalle[nom]
            print(f"   {nom:<18} {a:>9.2f} {b:>10.2f} {a-b:>+8.3f} "
                  f"{p:>9.4f} {q:>9.4f}  {'** SIG **' if s else ''}")

    if sig:
        print(f"\n>>> {len(sig)} sobreviven. Investigar una por una.")
    else:
        print(f"\n>>> NINGUNA sobrevive. El clima a la hora del sorteo no")
        print(f"    predice qué números salen.")
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bajar", action="store_true")
    args = ap.parse_args()

    if args.bajar:
        bajar(); return

    clima = leer_clima()
    print(f"clima cacheado: {len(clima):,} días  "
          f"({min(clima)} -> {max(clima)})")

    from athena import load_draws
    correr("KINO vs CLIMA", load_draws(dedupe=True), 1, 80, clima)

    from update_pool import leer_base
    b = leer_base()
    pool = sorted((d, frozenset(int(x) for x in s.split(", ")))
                  for d, s in b.items() if d >= date(2017, 2, 1))
    correr("LOTO POOL vs CLIMA (2017+)", pool, 1, 31, clima)


if __name__ == "__main__":
    main()
