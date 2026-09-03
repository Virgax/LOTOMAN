#!/usr/bin/env python3
"""
Genera data/jugadas_hoy.json — el archivo que lee la extensión de Chrome.

La extensión no calcula nada: solo lee este archivo y hace los clics. Toda la
lógica vive aquí, donde ya está athena, la base y las validaciones.

CÓMO SE ARMAN LAS JUGADAS
Bajo un sorteo justo —que es lo que dicen 671 pruebas sobre Kino y 274 sobre
Pool— lo único que sube P(8+ aciertos) es CUÁNTAS combinaciones distintas
juegas, no cuáles. Por eso el modo por defecto es `azar` y garantiza que no se
repita ninguna combinación.

El modo `modelo` existe para el experimento prospectivo, no porque prediga:
muestrea sesgado hacia los mejor puntuados por athena v4. Sirve para que lo
que Jaime juega de verdad sea comparable con lo que el experimento mide.

Uso:
    python scripts/jugadas_hoy.py --presupuesto 800
    python scripts/jugadas_hoy.py --presupuesto 600 --juego pool --modo modelo
"""

import argparse
import json
import random
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

DEST = Path(__file__).parent.parent / "data" / "jugadas_hoy.json"

JUEGOS = {
    "kino": {"nombre": "Super Kino TV", "lo": 1, "hi": 80, "pick": 10,
             "costo": 25, "ev": 16.88,
             "url": "https://www.leidsa.com/play/draw/leidsa-kinotv"},
    "pool": {"nombre": "Loto Pool", "lo": 1, "hi": 31, "pick": 5,
             "costo": 20, "ev": 10.67,
             "url": "https://www.leidsa.com/play/draw/leidsa-loto"},
}


def pesos_modelo(juego):
    """Pesos por número según athena v4. Solo para el juego kino."""
    if juego != "kino":
        return None
    from athena import load_draws, score_numbers
    draws = load_draws(dedupe=True)
    sc = score_numbers(draws)          # corta en el último sorteo conocido
    vals = {n: sc[n]["score"] for n in range(1, 81)}
    lo, hi = min(vals.values()), max(vals.values())
    rango = (hi - lo) or 1.0
    return {n: 0.2 + 1.6 * (vals[n] - lo) / rango for n in vals}


def generar(g, n, pesos, seed):
    """n jugadas DISTINTAS. Sin pesos = uniforme."""
    rng = random.Random(seed)
    nums = list(range(g["lo"], g["hi"] + 1))
    vistas, out, guard = set(), [], 0
    while len(out) < n and guard < n * 400:
        guard += 1
        if pesos is None:
            j = rng.sample(nums, g["pick"])
        else:
            disp, w, j = nums[:], [pesos[x] for x in nums], []
            for _ in range(g["pick"]):
                r, acc = rng.random() * sum(w), 0.0
                for i, x in enumerate(disp):
                    acc += w[i]
                    if acc >= r:
                        j.append(x); disp.pop(i); w.pop(i); break
                else:
                    j.append(disp.pop()); w.pop()
        c = tuple(sorted(j))
        if c not in vistas:
            vistas.add(c); out.append(list(c))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--juego", choices=list(JUEGOS), default="kino")
    ap.add_argument("--presupuesto", type=int, default=800)
    ap.add_argument("--modo", choices=("azar", "modelo"), default="azar")
    ap.add_argument("--salida", default=str(DEST))
    a = ap.parse_args()

    g = JUEGOS[a.juego]
    n = a.presupuesto // g["costo"]
    if n < 1:
        sys.exit(f"El presupuesto no alcanza ni para una jugada de {g['costo']}.")

    pesos = pesos_modelo(a.juego) if a.modo == "modelo" else None
    if a.modo == "modelo" and pesos is None:
        print("(modo modelo solo aplica a kino — se usa azar)")
    hoy = date.today()
    jugadas = generar(g, n, pesos, int(hoy.strftime("%Y%m%d")))

    datos = {
        "generado_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "para_sorteo": hoy.isoformat(),
        "juego": a.juego,
        "juego_nombre": g["nombre"],
        "url_juego": g["url"],
        "modo": a.modo if pesos else "azar",
        "numeros_por_jugada": g["pick"],
        "rango": [g["lo"], g["hi"]],
        "costo_por_jugada": g["costo"],
        "presupuesto": n * g["costo"],
        "cantidad": len(jugadas),
        "retorno_esperado_pct": round(g["ev"] / g["costo"] * 100, 1),
        "perdida_esperada": round((g["costo"] - g["ev"]) * len(jugadas)),
        "jugadas": jugadas,
    }
    Path(a.salida).write_text(json.dumps(datos, indent=1))
    print(f"{g['nombre']}  ·  {len(jugadas)} jugadas  ·  RD${datos['presupuesto']:,}")
    print(f"   modo {datos['modo']}  ·  retorno esperado {datos['retorno_esperado_pct']}%"
          f"  ·  pérdida esperada RD${datos['perdida_esperada']:,}")
    print(f"   -> {a.salida}")


if __name__ == "__main__":
    main()
