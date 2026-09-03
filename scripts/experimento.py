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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--generar", action="store_true")
    ap.add_argument("--evaluar", action="store_true")
    a = ap.parse_args()
    if a.generar: generar()
    elif a.evaluar: evaluar()
    else: ap.print_help()
