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
