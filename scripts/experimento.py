#!/usr/bin/env python3
"""
Experimento prospectivo: ¿el modelo v4 le gana al azar?

IDEA DE JAIME, y es la correcta: generar las jugadas ANTES de ver el sorteo.
Comprometerse por adelantado es la única forma de probar un modelo sin margen
para engañarse después. Los archivos quedan commiteados con fecha, así que la
prueba es auditable por cualquiera.

TRES BRAZOS, no dos:

    azar        10 números uniformes de 1..80
    modelo      muestreo sesgado HACIA los mejor puntuados por athena v4
    anti        muestreo sesgado hacia los PEOR puntuados

El brazo "anti" no es broma: dobla el tamaño del efecto. Si el modelo tiene
señal, se debe ver modelo > azar > anti. Si las tres dan ~2.5 aciertos, no
hay señal. Y si el "anti" gana, sería igual de informativo — significaría que
el modelo apunta al revés.

SIN LOOKAHEAD: los puntajes salen de score_numbers(draws, upto=N), que corta
la historia en el día anterior. El modelo nunca ve el sorteo que va a predecir.

CUÁNTOS SORTEOS HACEN FALTA: 1000 jugadas contra UN sorteo tienen la misma
potencia que 10 — todas ven el mismo resultado, así que lo que decide es una
sola variable (cuántos de los 20 favoritos salieron, SD 1.69). Para detectar
la ventaja que haría rentable el juego (+0.37 en el top-20) hacen falta ~80
sorteos. Por eso esto se corre TODOS LOS DÍAS y se acumula.

Uso:
    python scripts/experimento.py --generar          # antes del sorteo
    python scripts/experimento.py --evaluar          # después
"""

import argparse
import json
import random
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from athena import load_draws, score_numbers          # noqa: E402

DIR = Path(__file__).parent.parent / "data" / "experimentos"
N_JUGADAS = 1000
PICK, POOL = 10, 80


def jugadas_sesgadas(pesos, n, seed):
    """n jugadas DISTINTAS de 10 números, muestreadas sin reemplazo con `pesos`."""
    rng = random.Random(seed)
    nums = list(range(1, POOL + 1))
    vistas, out, guard = set(), [], 0
    while len(out) < n and guard < n * 400:
        guard += 1
        disp, w = nums[:], [pesos[x] for x in nums]
        jugada = []
        for _ in range(PICK):
            t = sum(w)
            r, acc = rng.random() * t, 0.0
            for i, x in enumerate(disp):
                acc += w[i]
                if acc >= r:
                    jugada.append(x); disp.pop(i); w.pop(i); break
            else:
                jugada.append(disp.pop()); w.pop()
        c = tuple(sorted(jugada))
        if c not in vistas:
            vistas.add(c); out.append(list(c))
    return out


def generar():
    draws = load_draws(dedupe=True)
    objetivo = draws[-1][0] + timedelta(days=1)
    DIR.mkdir(parents=True, exist_ok=True)
    dest = DIR / f"{objetivo}.json"
    if dest.exists():
        print(f"Ya existe {dest} — no se regenera (eso sería hacer trampa).")
        return

    # Puntajes SOLO con historia hasta el último sorteo conocido.
    sc = score_numbers(draws)
    vals = {n: sc[n]["score"] for n in range(1, POOL + 1)}
    lo, hi = min(vals.values()), max(vals.values())
    rango = (hi - lo) or 1.0
    # Normalizado a [0.2, 1.8]: concentra sin llegar a excluir números.
    p_mod = {n: 0.2 + 1.6 * (vals[n] - lo) / rango for n in vals}
    p_anti = {n: 2.0 - p_mod[n] for n in vals}
    p_azar = {n: 1.0 for n in vals}

    semilla = int(objetivo.strftime("%Y%m%d"))
    datos = {
        "sorteo_objetivo": objetivo.isoformat(),
        "generado_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "base_hasta": draws[-1][0].isoformat(),
        "sorteos_usados": len(draws),
        "n_jugadas": N_JUGADAS,
        "top20_modelo": sorted(vals, key=lambda n: -vals[n])[:20],
        "brazos": {
            "azar":   jugadas_sesgadas(p_azar,  N_JUGADAS, semilla + 1),
            "modelo": jugadas_sesgadas(p_mod,   N_JUGADAS, semilla + 2),
            "anti":   jugadas_sesgadas(p_anti,  N_JUGADAS, semilla + 3),
        },
    }
    dest.write_text(json.dumps(datos, indent=1))
    print(f"Sorteo objetivo: {objetivo}   (base hasta {draws[-1][0]}, "
          f"{len(draws):,} sorteos)")
    for b, js in datos["brazos"].items():
        print(f"   {b:7} {len(js):,} jugadas distintas")
    print(f"   top-20 del modelo: {datos['top20_modelo']}")
    print(f"\nGuardado: {dest}")


def evaluar():
    reales = dict(load_draws(dedupe=True))
    archivos = sorted(DIR.glob("*.json")) if DIR.exists() else []
    if not archivos:
        print("No hay experimentos guardados."); return

    acum = {b: [] for b in ("azar", "modelo", "anti")}
    top20 = []
    print(f"{'sorteo':>12} {'azar':>8} {'modelo':>8} {'anti':>8} {'top20':>7}")
    for f in archivos:
        d = json.loads(f.read_text())
        obj = date.fromisoformat(d["sorteo_objetivo"])
        if obj not in reales:
            print(f"{str(obj):>12}   (sin resultado todavía)")
            continue
        salieron = reales[obj]
        fila = {}
        for b, js in d["brazos"].items():
            m = sum(len(set(j) & salieron) for j in js) / len(js)
            acum[b].append(m); fila[b] = m
        t = len(set(d["top20_modelo"]) & salieron)
        top20.append(t)
        print(f"{str(obj):>12} {fila['azar']:>8.3f} {fila['modelo']:>8.3f} "
              f"{fila['anti']:>8.3f} {t:>7}")

    n = len(top20)
    if not n:
        print("\nNingún experimento tiene resultado todavía."); return
    print(f"\n{'='*54}\nACUMULADO sobre {n} sorteo(s)\n{'='*54}")
    print(f"   {'brazo':<8} {'aciertos/jugada':>16}   esperado por azar: 2.500")
    for b in ("modelo", "azar", "anti"):
        prom = sum(acum[b]) / n
        print(f"   {b:<8} {prom:>16.4f}")
    dif = sum(acum["modelo"])/n - sum(acum["anti"])/n
    print(f"\n   modelo - anti = {dif:+.4f}   (0.000 si el modelo no aporta)")
    print(f"   top-20: {sum(top20)/n:.3f}   esperado por azar: 5.000")
    if n < 80:
        print(f"\n   Faltan ~{80-n} sorteos para que esto pueda concluir algo.")


def retro(n):
    """El mismo experimento, pero hacia atrás sobre los últimos n sorteos.

    Estadísticamente equivalente a esperar n días, con una condición que aquí
    se respeta: para cada sorteo i los puntajes salen de score_numbers(draws,
    upto=i), o sea SOLO la historia anterior. El modelo nunca ve el sorteo que
    puntúa.

    No se generan las 3000 jugadas por día — sería la versión cara de medir lo
    mismo. Lo que decide el experimento es cuántos de los 20 favoritos del
    modelo salen contra cuántos de los 20 peores, y eso se calcula directo.
    """
    draws = load_draws(dedupe=True)
    ini = len(draws) - n
    top, bot, alto = [], [], []
    for i in range(ini, len(draws)):
        sc = score_numbers(draws, upto=i)
        orden = sorted(range(1, POOL + 1), key=lambda x: -sc[x]["score"])
        salieron = draws[i][1]
        top.append(len(set(orden[:20]) & salieron))
        bot.append(len(set(orden[-20:]) & salieron))
        alto.append(len(set(orden[:10]) & salieron))

    import math
    def resumen(v, esp, etq):
        m = sum(v) / len(v)
        sd = math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))
        se = sd / math.sqrt(len(v))
        z = (m - esp) / se
        print(f"   {etq:<22} {m:>7.3f}   esperado {esp:.3f}   "
              f"IC95 [{m-1.96*se:.3f}, {m+1.96*se:.3f}]   z={z:+.2f}")
        return m, se

    print(f"\n{'='*74}")
    print(f"WALK-FORWARD sobre los últimos {n} sorteos "
          f"({draws[ini][0]} → {draws[-1][0]})")
    print(f"{'='*74}\n")
    mt, st = resumen(top, 5.0, "top-20 del modelo")
    mb, sb = resumen(bot, 5.0, "bottom-20 (anti)")
    ma, sa = resumen(alto, 2.5, "top-10 del modelo")

    dif = mt - mb
    sed = math.sqrt(st**2 + sb**2)
    print(f"\n   modelo - anti = {dif:+.3f}   SE {sed:.3f}   z={dif/sed:+.2f}   "
          f"{'SIGNIFICATIVO' if abs(dif/sed) > 1.96 else 'no significativo'}")
    print(f"   (si el modelo tuviera la ventaja que lo haría rentable,")
    print(f"    esta diferencia sería de +0.74 y saldría z={0.74/sed:+.1f})")


def curso(w=700):
    """La diferencia modelo-anti en ventanas CONSECUTIVAS que no se solapan.

    Es el diagnóstico que decide, y nació de un error metodológico propio: al
    mirar los últimos 80 / 400 / 1600 sorteos, la diferencia se derrumbaba
    (0.463 -> 0.205 -> 0.122) mientras el z subía (1.67 -> 1.77 -> 2.09). Eso
    pasa porque las muestras están ANIDADAS —los 80 viven dentro de los 400—
    así que no son tres pruebas, es una mirada repetida al mismo dato. Elegir
    el tamaño que cruza 1.96 y reportarlo es el mecanismo exacto que fabricó
    el falso ciclo-5.

    Ventanas consecutivas sin solape sí son independientes. Resultado sobre
    5,392 sorteos, ventanas de 700:

        2012-09 -> 2014-09   -0.023     2020-10 -> 2022-09   -0.041
        2014-09 -> 2016-08   -0.130     2022-09 -> 2024-09   +0.151
        2016-08 -> 2018-08   +0.020     2024-09 -> 2026-09   +0.191
        2018-08 -> 2020-09   +0.020

    Media +0.027, cuatro de siete positivas: eso es azar. PERO las dos más
    positivas son las dos últimas, y que eso pase por casualidad tiene ~5%.
    Queda abierto, y no se puede cerrar mirando más veces estos mismos datos:
    lo resuelve el experimento sellado de --generar, que compromete las
    jugadas antes de que exista el sorteo.

    Referencia económica: +0.74 es lo que haría falta para empatar el EV.
    Incluso +0.224 solo baja la ventaja de la casa de 32.5% a 15.3%.
    """
    import math
    draws = load_draws(dedupe=True)
    N = len(draws)
    print(f"Base {N:,} sorteos. Ventanas consecutivas de {w}, sin solape:\n")
    print(f"   {'periodo':<26} {'top20':>7} {'anti':>7} {'dif':>8} {'z':>7}")
    difs = []
    i = N - (N - 300) // w * w
    while i + w <= N:
        top, bot = [], []
        for j in range(i, i + w):
            sc = score_numbers(draws, upto=j)
            o = sorted(range(1, POOL + 1), key=lambda x: -sc[x]["score"])
            s_ = draws[j][1]
            top.append(len(set(o[:20]) & s_))
            bot.append(len(set(o[-20:]) & s_))
        mt, mb = sum(top) / w, sum(bot) / w
        st = math.sqrt(sum((x - mt) ** 2 for x in top) / (w - 1)) / math.sqrt(w)
        sb = math.sqrt(sum((x - mb) ** 2 for x in bot) / (w - 1)) / math.sqrt(w)
        d = mt - mb
        se = math.sqrt(st * st + sb * sb)
        print(f"   {str(draws[i][0])+' -> '+str(draws[i+w-1][0]):<26} "
              f"{mt:>7.3f} {mb:>7.3f} {d:>+8.3f} {d/se:>+7.2f}")
        difs.append(d)
        i += w
    print(f"\n   positivas: {sum(1 for d in difs if d>0)} de {len(difs)}   "
          f"media {sum(difs)/len(difs):+.3f}")
    print(f"   (azar puro: ~la mitad positivas, media ~0.000)")
    print(f"   (para empatar el EV harían falta +0.740)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--generar", action="store_true")
    ap.add_argument("--evaluar", action="store_true")
    ap.add_argument("--retro", type=int, metavar="N",
                    help="replay walk-forward sobre los últimos N sorteos")
    ap.add_argument("--curso", type=int, nargs="?", const=700, metavar="W",
                    help="ventanas consecutivas de W, sin solape (el que decide)")
    a = ap.parse_args()
    if a.generar: generar()
    elif a.evaluar: evaluar()
    elif a.retro: retro(a.retro)
    elif a.curso: curso(a.curso)
    else: ap.print_help()
