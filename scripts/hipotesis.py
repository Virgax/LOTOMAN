#!/usr/bin/env python3
"""
Batería de hipótesis con corrección por comparaciones múltiples.

Tarea #6 del CLAUDE.md. La pregunta que contesta NO es "¿qué números van a
salir?" — eso no tiene respuesta en un sorteo justo. La pregunta es:

    ¿Se comporta esta tómbola como una tómbola justa?

Si la respuesta fuera NO, ahí sí habría algo explotable. Kino ya dio "justo"
en cuatro pruebas distintas. Loto Pool (3,720 sorteos) nunca se ha auditado.

POR QUÉ LA CORRECCIÓN NO ES OPCIONAL
Esta batería corre ~200 pruebas. Con alfa 0.05 y ninguna señal real, se
esperan ~10 con p<0.05 por PURO AZAR. Reportar esas 10 como hallazgos es
exactamente el error que fabricó el "ciclo-5". Por eso todo pasa por
Benjamini-Hochberg, que controla la tasa de falsos descubrimientos.

Uso:
    python scripts/hipotesis.py                # los dos juegos
    python scripts/hipotesis.py --juego pool
"""

import argparse
import math
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))


# --------------------------------------------------------------------------
# Estadística — sin scipy, para no romper la regla de "solo openpyxl"
# --------------------------------------------------------------------------
def norm_sf(z):
    """P(Z > z) para la normal estándar."""
    return 0.5 * math.erfc(z / math.sqrt(2))


def p_dos_colas(z):
    return 2 * norm_sf(abs(z))


def chi2_sf(x, k):
    """P(X > x) para chi-cuadrado con k grados de libertad.

    Wilson-Hilferty: transforma a normal. Error <1% para k>=3, que es todo
    lo que se usa aquí. Suficiente para decidir si algo merece mirarse.
    """
    if x <= 0:
        return 1.0
    t = (x / k) ** (1 / 3) - (1 - 2 / (9 * k))
    return norm_sf(t / math.sqrt(2 / (9 * k)))


def benjamini_hochberg(pruebas, alfa=0.05):
    """[(nombre, p)] -> [(nombre, p, q, significativa)] ordenado por p.

    BH controla la FDR: la proporción esperada de falsos positivos ENTRE los
    rechazados. Es lo correcto aquí — Bonferroni sería tan estricto que
    escondería un sesgo real de máquina si lo hubiera.
    """
    ordenadas = sorted(pruebas, key=lambda t: t[1])
    m = len(ordenadas)
    out, q_min = [], 1.0
    for i in range(m - 1, -1, -1):          # de atrás hacia adelante
        nombre, p = ordenadas[i]
        q_min = min(q_min, p * m / (i + 1))
        out.append((nombre, p, min(q_min, 1.0)))
    out.reverse()
    return [(n, p, q, q <= alfa) for n, p, q in out]


# --------------------------------------------------------------------------
# Las pruebas
# --------------------------------------------------------------------------
def pruebas_frecuencia(sorteos, lo, hi, extraidas):
    """Una prueba por número: ¿sale con la frecuencia que le toca?"""
    n = len(sorteos)
    p0 = extraidas / (hi - lo + 1)
    esperado, sd = n * p0, math.sqrt(n * p0 * (1 - p0))
    cuenta = Counter()
    for _, nums in sorteos:
        cuenta.update(nums)
    return [(f"frecuencia/{x:02d}", p_dos_colas((cuenta[x] - esperado) / sd))
            for x in range(lo, hi + 1)]


def prueba_pares_impares(sorteos, lo, hi, extraidas):
    """¿La cantidad de pares por sorteo sigue la hipergeométrica?"""
    pares_pool = sum(1 for x in range(lo, hi + 1) if x % 2 == 0)
    total = hi - lo + 1
    obs = Counter(sum(1 for v in nums if v % 2 == 0) for _, nums in sorteos)
    n = len(sorteos)
    chi = gl = 0
    for k in range(extraidas + 1):
        e = n * (math.comb(pares_pool, k) * math.comb(total - pares_pool, extraidas - k)
                 / math.comb(total, extraidas))
        if e >= 5:
            chi += (obs.get(k, 0) - e) ** 2 / e
            gl += 1
    return [("pares_impares", chi2_sf(chi, max(gl - 1, 1)))]


def prueba_suma(sorteos):
    """¿La suma del sorteo se desvía de lo que da el azar?

    Se compara la media observada contra la teórica por remuestreo analítico:
    media y varianza de una suma sin reemplazo son cerradas.
    """
    sumas = [sum(nums) for _, nums in sorteos]
    n = len(sumas)
    obs = sum(sumas) / n
    return obs, sumas, n


def pruebas_lags(sorteos, lo, hi, extraidas, max_lag=20):
    """¿Salir hace k sorteos cambia la probabilidad de salir hoy?

    Esta es la familia donde vivía el falso ciclo-5. Se prueban 20 lags, así
    que sin corrección uno daría p<0.05 por azar aproximadamente siempre.
    """
    p0 = extraidas / (hi - lo + 1)
    out = []
    for lag in range(1, max_lag + 1):
        hit = tot = 0
        for i in range(lag, len(sorteos)):
            pasado, hoy = sorteos[i - lag][1], sorteos[i][1]
            for v in pasado:
                tot += 1
                hit += v in hoy
        if tot == 0:
            continue
        p = hit / tot
        z = (p - p0) / math.sqrt(p0 * (1 - p0) / tot)
        out.append((f"lag/{lag:02d}", p_dos_colas(z)))
    return out


def pruebas_decenas(sorteos, lo, hi, extraidas):
    """¿Alguna franja del rango sale más de la cuenta?"""
    ancho = 10
    franjas = defaultdict(int)
    for _, nums in sorteos:
        for v in nums:
            franjas[v // ancho] += 1
    total_bolas = len(sorteos) * extraidas
    tam = Counter((v // ancho) for v in range(lo, hi + 1))
    out = []
    for f, cuantos in sorted(tam.items()):
        p0 = cuantos / (hi - lo + 1)
        e = total_bolas * p0
        sd = math.sqrt(total_bolas * p0 * (1 - p0))
        out.append((f"franja/{f*ancho:02d}-{f*ancho+ancho-1:02d}",
                    p_dos_colas((franjas[f] - e) / sd)))
    return out


def pruebas_dow(sorteos, lo, hi, extraidas):
    """Día de la semana. Jaime ya la botó por esotérica — va como CONTROL
    NEGATIVO: si el método es honesto, esto NO debe dar significativo."""
    por_dia = defaultdict(Counter)
    n_dia = Counter()
    for f, nums in sorteos:
        por_dia[f.weekday()].update(nums)
        n_dia[f.weekday()] += 1
    p0 = extraidas / (hi - lo + 1)
    out = []
    for d in range(7):
        if n_dia[d] < 30:
            continue
        for v in range(lo, hi + 1):
            e = n_dia[d] * p0
            sd = math.sqrt(n_dia[d] * p0 * (1 - p0))
            out.append((f"dow/{d}/{v:02d}",
                        p_dos_colas((por_dia[d][v] - e) / sd)))
    return out


# --------------------------------------------------------------------------
def correr(nombre, sorteos, lo, hi, extraidas):
    """lo..hi es el rango REAL de números. Kino 1..80, Pool 00..31.

    No colapsar esto en un solo "pool": la primera versión lo hizo y probó el
    número 32 en Loto Pool, que no existe. Frecuencia cero, z infinito, y 40
    pruebas "significativas" que eran puro artefacto del código.
    """
    print(f"\n{'='*70}\n{nombre}  —  {len(sorteos):,} sorteos, "
          f"{extraidas} de {hi-lo+1} (números {lo:02d}..{hi:02d})\n{'='*70}")

    # Guardia: ningún número fuera del rango declarado.
    fuera = {v for _, nums in sorteos for v in nums if not lo <= v <= hi}
    if fuera:
        print(f"!! ABORTADO: números fuera de {lo}..{hi} en los datos: {sorted(fuera)}")
        return []

    pruebas = []
    pruebas += pruebas_frecuencia(sorteos, lo, hi, extraidas)
    pruebas += prueba_pares_impares(sorteos, lo, hi, extraidas)
    pruebas += pruebas_lags(sorteos, lo, hi, extraidas)
    pruebas += pruebas_decenas(sorteos, lo, hi, extraidas)
    pruebas += pruebas_dow(sorteos, lo, hi, extraidas)

    obs, sumas, n = prueba_suma(sorteos)
    med = sum(sumas) / n
    var = sum((s - med) ** 2 for s in sumas) / (n - 1)
    esperada = extraidas * (lo + hi) / 2
    z_suma = (med - esperada) / math.sqrt(var / n)
    pruebas.append(("suma_media", p_dos_colas(z_suma)))

    res = benjamini_hochberg(pruebas)
    sig = [r for r in res if r[3]]
    crudas = [r for r in res if r[1] < 0.05]

    print(f"\npruebas corridas:              {len(res)}")
    print(f"p<0.05 SIN corregir:          {len(crudas)}   "
          f"(esperadas por azar: {len(res)*0.05:.1f})")
    print(f"sobreviven Benjamini-Hochberg: {len(sig)}")

    print(f"\nlas 8 más extremas:")
    print(f"   {'prueba':<22} {'p':>10} {'q (BH)':>10}  veredicto")
    for nom, p, q, s in res[:8]:
        print(f"   {nom:<22} {p:>10.4f} {q:>10.4f}  "
              f"{'** SIGNIFICATIVA **' if s else 'ruido'}")

    print(f"\nsuma del sorteo: observada {med:.2f}  esperada {esperada:.2f}  "
          f"z={z_suma:+.2f}")

    if sig:
        print(f"\n>>> {len(sig)} prueba(s) sobreviven la corrección. "
              f"Hay que investigarlas una por una.")
    else:
        print(f"\n>>> NINGUNA sobrevive. La tómbola se comporta como justa.")
        print(f"    Las {len(crudas)} con p<0.05 son exactamente las que produce")
        print(f"    mirar {len(res)} pruebas a la vez. No son hallazgos.")
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--juego", choices=("kino", "pool", "ambos"), default="ambos")
    ap.add_argument("--desde", help="YYYY-MM-DD: recortar la serie desde esta fecha")
    args = ap.parse_args()
    corte = date.fromisoformat(args.desde) if args.desde else None

    if args.juego in ("kino", "ambos"):
        from athena import load_draws
        d = load_draws(dedupe=True)
        if corte:
            d = [r for r in d if r[0] >= corte]
        correr("SUPER KINO TV", d, 1, 80, 20)

    if args.juego in ("pool", "ambos"):
        from update_pool import leer_base
        b = leer_base()
        sorteos = sorted((d, frozenset(int(x) for x in s.split(", ")))
                         for d, s in b.items())
        if corte:
            sorteos = [r for r in sorteos if r[0] >= corte]
        # OJO: la tómbola cambió. En 2016 era 1..27; el 28 aparece por primera
        # vez el 2017-01-09 y desde ahí los 28-31 salen a su tasa. Analizar la
        # serie entera mezcla dos juegos distintos y produce un falso sesgo
        # en la cola alta (z hasta -4.28) que NO es de la máquina.
        lo, hi = (1, 27) if (corte and corte.year < 2017) else (1, 31)
        correr("LOTO POOL", sorteos, lo, hi, 5)


if __name__ == "__main__":
    main()
