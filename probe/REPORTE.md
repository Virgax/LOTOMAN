# Sonda de fuentes — último resultado

Generado por `.github/workflows/probe-fuentes.yml`. Diagnóstico, no toca la base.

Criterio: una fuente solo cuenta si alguna de sus secuencias de 20 números coincide EXACTO
con un sorteo que ya está en la base (`MATCH_BASE`). Contar bytes no prueba nada.

```
[V] base: 5,606 sorteos conocidos, último 2026-08-27
[V] kino: dato más viejo hallado en el muestreo = None
[V] pool: dato más viejo hallado en el muestreo = None
[V] leidsa 3_6242: fecha=2026-06-18 OK rank=673/923
[V] leidsa 3_6243: fecha=2026-06-19 SIN MATCH (mejor solape 19/20 de 927)
[V] leidsa 3_6244: fecha=2026-06-20 SIN MATCH (mejor solape 19/20 de 922)
[V] leidsa 3_6245: fecha=2026-06-21 SIN MATCH (mejor solape 19/20 de 919)
[V] leidsa 3_6246: fecha=2026-06-21 SIN MATCH (mejor solape 19/20 de 928)
[V] leidsa 3_6247: fecha=2026-06-23 NO está en la base (927 candidatas) <- ESTA es la que falta
[V] leidsa 3_6248: fecha=2026-06-24 OK rank=31/925
[V] leidsa 3_6249: fecha=2026-06-25 SIN MATCH (mejor solape 19/20 de 922)
[V] leidsa 3_6250: fecha=2026-06-26 OK rank=591/925
[V] leidsa 3_6251: fecha=2026-06-27 OK rank=576/919
[V] leidsa 3_6252: fecha=2026-06-28 SIN MATCH (mejor solape 19/20 de 932)
[V] leidsa 3_6253: fecha=2026-06-28 SIN MATCH (mejor solape 19/20 de 920)
[V] leidsa 3_6254: fecha=2026-06-30 SIN MATCH (mejor solape 19/20 de 937)
[V] leidsa RANKS de la candidata correcta: [31, 576, 591, 673] (VARIABLE -> hace falta anclar por campo)
```

## Textos planos (para escribir el parser)
