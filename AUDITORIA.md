# AUDITORÍA ATHENA — salida cruda y cómo reproducirla

Reproducir:

```bash
python athena.py --audit
```

El detalle interpretado está en `CLAUDE.md` sección 5. Aquí va la salida
literal del comando sobre la base actual (5,451 filas cargables), para que
Claude Code pueda comparar contra ella después de limpiar los datos.

```
====================================================================
AUDITORÍA ATHENA — ¿las señales sobreviven?
====================================================================

[1] INTEGRIDAD
    filas crudas: 5,451   filas únicas: 5,110   duplicadas: 341
    separación de los duplicados: {1: 60, 2: 32, 3: 9, 5: 230, 8: 1, 22: 1}
    año de la copia: {2010: 4, 2011: 243, 2012: 39, 2013: 6, 2014: 6, 2015: 7, 2016: 9, 2017: 8, 2018: 6, 2019: 2, 2026: 11}
    -> P(que una combinación 20-de-80 se repita) = 1 en 3.5e18.
       Estas filas son error de captura, no sorteos.

[2] CICLO-5 (peso actual 25%)
    lag |  base cruda  |  base limpia
      1 |    +3.43%    |    -0.21%
      2 |    +2.54%    |    +0.31%
      3 |    +1.06%    |    +0.06%
      4 |    -0.38%    |    -0.82%
      5 |   +12.79%    |    +0.13%   <-- el supuesto ciclo
      6 |    -0.19%    |    -0.36%
      7 |    +0.05%    |    -0.36%
      8 |    +0.77%    |    -0.07%
      9 |    +0.31%    |    +0.06%
     10 |   +13.22%    |    +0.79%
    -> El pico de lag 5/10/15 en la base cruda es el eco de los duplicados.

[3] REPETICIÓN (peso actual 45%)
    media de P(sale|salió) - P(sale|no salió) = -0.084 puntos
    desviación entre números = 1.194 puntos
    -> 0.000 significa que el sorteo NO tiene memoria de un día al otro.

[4] ¿HAY NÚMEROS 'CALIENTES' DE VERDAD?
    desviación estándar de los z observados = 0.993  (azar puro = 1.000)
    número más extremo: 59 con z = -2.54
    -> Con 80 números, un |z| de ~2.5-3.0 aparece por azar SIEMPRE.

[5] LA MÉTRICA QUE IMPORTA — aciertos del top-20
    promedio sobre 300 sorteos = 4.990
    esperado si escogieras 20 números al azar = 5.000
    -> Regla del propio sistema: >5.3 sostenido = aporta. ~5.0 = no aporta.

====================================================================
VALOR ESPERADO (esto no depende del modelo)
  RD$25 apostados devuelven ~RD$16.88 en promedio. Ventaja casa ~32.5%.
  RD$800/día = RD$24,000/mes = pérdida esperada ~RD$7,800/mes.
====================================================================
```

## Resumen en una línea

Las 341 filas duplicadas de la base (230 de ellas separadas por exactamente
5 posiciones, 243 en 2011) crearon un falso "ciclo-5" de +12.8%. Al quitarlas
cae a +0.13%. Repetición y frecuencia base son indistinguibles del azar. El
backtest del top-20 da 5.01 contra 5.00 esperado por azar.

## Qué NO prueba esto

- No prueba que el sorteo esté amañado. Prueba lo contrario: se comporta
  como un sorteo justo.
- No prueba que el código esté mal. El código está bien; los datos que
  comía tenían basura.
- No prueba que ninguna señal exista jamás. Prueba que estas tres no.


---

# ACTUALIZACIÓN — 2026-08-27, base completa hasta 2026-08-25

Se cerró el hueco `2026-03-25 → 2026-08-25`: **+151 sorteos**, traídos por la
rutina diaria (`.github/workflows/actualizar-base.yml`). Base ahora **5,602
filas crudas / 5,261 únicas**. Las 151 filas nuevas no metieron ni un
duplicado ni una fila con conteo distinto de 20.

Faltaron 3 días, correctamente dejados fuera:

| Fecha | Qué es |
|---|---|
| 2026-04-02 Jue | Jueves Santo (Pascua 2026 = 5 abril) |
| 2026-04-03 Vie | Viernes Santo |
| 2026-06-23 Mar | **sin explicar — pendiente de verificar** |

## Ojo con el [5] del `--audit`

Con la base completa, `--audit` reporta **5.263** en la métrica del top-20,
pegado al umbral de 5.3. **No es señal.** Tres pruebas:

**1. El salto viene del tramo nuevo, y ahí no hay nada raro.** Solape con el
día anterior en las 151 filas nuevas: 5.260 (z=+1.89). Probando 6 lags, el
umbral Bonferroni al 5% es |z|>2.64. No pasa. Como el modelo es 45%
repetición, un tramo donde la repetición salió alta por azar lo hace verse bien.

**2. Ventanas de 300 sorteos sin solape, walk-forward, toda la historia:**

| ventana | prom | z | | ventana | prom | z |
|---|---|---|---|---|---|---|
| 2012-01-30..2012-12-30 | 4.960 | −0.41 | | 2018-11-21..2019-09-22 | 4.997 | −0.03 |
| 2013-01-02..2013-11-06 | 4.890 | −1.13 | | 2019-09-23..2020-10-09 | 4.860 | −1.44 |
| 2013-11-07..2014-09-11 | 5.177 | +1.82 | | 2020-10-10..2021-08-12 | 5.110 | +1.13 |
| 2014-09-12..2015-07-14 | **4.727** | **−2.80** | | 2021-08-13..2022-06-15 | 4.983 | −0.17 |
| 2015-07-15..2016-05-20 | 5.053 | +0.54 | | 2022-06-16..2023-08-18 | 4.820 | −1.85 |
| 2016-05-21..2017-03-20 | 4.863 | −1.41 | | 2023-08-19..2024-06-25 | 5.010 | +0.10 |
| 2017-03-21..2018-01-22 | 5.010 | +0.10 | | 2024-06-26..2025-04-29 | 5.023 | +0.24 |
| 2018-01-23..2018-11-20 | 5.157 | +1.61 | | 2025-04-30..2026-03-14 | 5.027 | +0.28 |

RMS de los z = 1.235 (azar = 1.000), media = −0.214. La ventana más extrema
de la historia es **−2.80**, más lejos del centro que el +2.70 de ahora.
Una ventana de 300 sorteos brinca así por puro azar.

**3. El número que manda — agrupado sobre las 16 ventanas (4,800 sorteos
walk-forward, sin lookahead):**

```
promedio = 4.979   IC95 [4.931, 5.027]
```

Contiene 5.000. No llega ni cerca de 5.3. **Conclusión sin cambios: el modelo
no aporta valor.** Si acaso, apunta un pelo por debajo del azar.

## Corrección a CLAUDE.md §5.5

Decía que el backtest "se midió dándole ventaja al modelo, usando tasas de
repetición calculadas con toda la historia, incluido el futuro". **Eso no es
cierto en el código actual:** `score_numbers(draws, upto=i)` corta con
`hist = draws[:upto]`. El backtest es walk-forward limpio. Debe venir de una
versión vieja. El hallazgo no cambia — solo que es más sólido de lo que decía.
