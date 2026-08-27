# Sonda de fuentes — último resultado

Generado por `.github/workflows/probe-fuentes.yml`. Diagnóstico, no toca la base.

Criterio: una fuente solo cuenta si alguna de sus secuencias de 20 números coincide EXACTO
con un sorteo que ya está en la base (`MATCH_BASE`). Contar bytes no prueba nada.

```
[V] base: 5,604 sorteos conocidos, último 2026-08-25
[V] cnt_indice: 64,264B texto=4,143 secuencias=5 MATCH_BASE=0
[V] cnt_indice: 9 enlaces candidatos a historial
[V] cnt_kino: 67,692B texto=4,777 secuencias=5 MATCH_BASE=0
[V] cnt_kino: 8 enlaces candidatos a historial
[V] cnt_kino_sub: 67,692B texto=4,777 secuencias=5 MATCH_BASE=0
[V] cnt_kino_sub: 8 enlaces candidatos a historial
[V] cnt_pool: 66,896B texto=4,279 secuencias=5 MATCH_BASE=0
[V] cnt_pool: 8 enlaces candidatos a historial
[V] cnt_pool_sub: 66,896B texto=4,279 secuencias=5 MATCH_BASE=0
[V] cnt_pool_sub: 8 enlaces candidatos a historial
[V] cnt_leidsa: 64,264B texto=4,143 secuencias=5 MATCH_BASE=0
[V] cnt_leidsa: 9 enlaces candidatos a historial
[V] leidsa 3_6242: fecha=2026-06-18 OK rank=658/918
[V] leidsa 3_6243: fecha=2026-06-19 SIN MATCH (mejor solape 19/20 de 917)
[V] leidsa 3_6244: fecha=2026-06-20 SIN MATCH (mejor solape 19/20 de 916)
[V] leidsa 3_6245: fecha=2026-06-21 SIN MATCH (mejor solape 19/20 de 911)
[V] leidsa 3_6246: fecha=2026-06-21 SIN MATCH (mejor solape 19/20 de 918)
[V] leidsa 3_6247: fecha=2026-06-23 NO está en la base (925 candidatas) <- ESTA es la que falta
[V] leidsa 3_6248: fecha=2026-06-24 OK rank=31/916
[V] leidsa 3_6249: fecha=2026-06-25 SIN MATCH (mejor solape 19/20 de 914)
[V] leidsa 3_6250: fecha=2026-06-26 OK rank=572/915
[V] leidsa 3_6251: fecha=2026-06-27 OK rank=557/910
[V] leidsa 3_6252: fecha=2026-06-28 SIN MATCH (mejor solape 19/20 de 924)
[V] leidsa 3_6253: fecha=2026-06-28 SIN MATCH (mejor solape 19/20 de 911)
[V] leidsa 3_6254: fecha=2026-06-30 SIN MATCH (mejor solape 19/20 de 912)
[V] leidsa RANKS de la candidata correcta: [31, 557, 572, 658] (VARIABLE -> hace falta anclar por campo)
```
