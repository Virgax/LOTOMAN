# Sonda de fuentes — último resultado

Generado por `.github/workflows/probe-fuentes.yml`. Diagnóstico, no toca la base.

Criterio: una fuente solo cuenta si alguna de sus secuencias de 20 números coincide EXACTO
con un sorteo que ya está en la base (`MATCH_BASE`). Contar bytes no prueba nada.

```
[V] base: 5,606 sorteos conocidos, último 2026-08-27
[V] kino 1998: 0/14 (~0.0/semana) dias=-
[V] kino 2001: 0/14 (~0.0/semana) dias=-
[V] kino 2004: 0/14 (~0.0/semana) dias=-
[V] kino 2007: 0/14 (~0.0/semana) dias=-
[V] kino 2009: 0/14 (~0.0/semana) dias=-
[V] kino 2010: 0/14 (~0.0/semana) dias=-
[V] kino 2012: 0/14 (~0.0/semana) dias=-
[V] kino 2014: 0/14 (~0.0/semana) dias=-
[V] kino 2016: 12/14 (~6.0/semana) dias=JVSDLMXJVLMX
[V] kino 2019: 14/14 (~7.0/semana) dias=DLMXJVSDLMXJVS
[V] kino 2022: 14/14 (~7.0/semana) dias=JVSDLMXJVSDLMX
[V] kino 2025: 14/14 (~7.0/semana) dias=LMXJVSDLMXJVSD
[V] pool 1998: 0/14 (~0.0/semana) dias=-
[V] pool 2001: 0/14 (~0.0/semana) dias=-
[V] pool 2004: 0/14 (~0.0/semana) dias=-
[V] pool 2007: 0/14 (~0.0/semana) dias=-
[V] pool 2009: 0/14 (~0.0/semana) dias=-
[V] pool 2010: 0/14 (~0.0/semana) dias=-
[V] pool 2012: 0/14 (~0.0/semana) dias=-
[V] pool 2014: 0/14 (~0.0/semana) dias=-
[V] pool 2016: 12/14 (~6.0/semana) dias=JVSDLMXJVLMX
[V] pool 2019: 14/14 (~7.0/semana) dias=DLMXJVSDLMXJVS
[V] pool 2022: 14/14 (~7.0/semana) dias=JVSDLMXJVSDLMX
[V] pool 2025: 14/14 (~7.0/semana) dias=LMXJVSDLMXJVSD
[V] leidsa 3_6242: fecha=2026-06-18 OK rank=673/924
[V] leidsa 3_6243: fecha=2026-06-19 SIN MATCH (mejor solape 19/20 de 926)
[V] leidsa 3_6244: fecha=2026-06-20 SIN MATCH (mejor solape 19/20 de 922)
[V] leidsa 3_6245: fecha=2026-06-21 SIN MATCH (mejor solape 19/20 de 919)
[V] leidsa 3_6246: fecha=2026-06-21 SIN MATCH (mejor solape 19/20 de 929)
[V] leidsa 3_6247: fecha=2026-06-23 NO está en la base (928 candidatas) <- ESTA es la que falta
[V] leidsa 3_6248: fecha=2026-06-24 OK rank=31/925
[V] leidsa 3_6249: fecha=2026-06-25 SIN MATCH (mejor solape 19/20 de 924)
[V] leidsa 3_6250: fecha=2026-06-26 OK rank=591/937
[V] leidsa 3_6251: fecha=2026-06-27 OK rank=579/922
[V] leidsa 3_6252: fecha=2026-06-28 SIN MATCH (mejor solape 19/20 de 933)
[V] leidsa 3_6253: fecha=2026-06-28 SIN MATCH (mejor solape 19/20 de 921)
[V] leidsa 3_6254: fecha=2026-06-30 SIN MATCH (mejor solape 19/20 de 919)
[V] leidsa RANKS de la candidata correcta: [31, 579, 591, 673] (VARIABLE -> hace falta anclar por campo)
```

## Textos planos (para escribir el parser)
