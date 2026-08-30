# ATHENA ANALYTICS — Contexto completo del proyecto

> Este archivo es el traspaso completo del proyecto a Claude Code.
> Léelo entero antes de tocar nada. Contiene el estado real del sistema,
> incluyendo una auditoría que invalida parte del modelo anterior.

---

## 0. LO PRIMERO QUE DEBES SABER

Antes de ayudar a Jaime a "mejorar el modelo", corre esto:

```bash
python athena.py --audit
```

Encontrarás que **las tres señales del modelo v4 no sobreviven una prueba
estadística honesta**. El detalle está en la sección 5. No escondas esto ni
lo suavices: Jaime construyó este sistema con el criterio explícito de
eliminar señales sin fundamento estadístico (ya botó DOW, estacionalidad y
"números atrasados" por esa razón). Esta es la continuación de ese mismo
criterio, no una contradicción.

Si Jaime quiere seguir jugando de todas formas, ayúdalo con la parte
operativa sin fingir que el modelo predice. Son cosas separadas.

---

## 1. EL JUEGO

**Super Kino TV** — Leidsa, República Dominicana.

| Concepto | Valor |
|---|---|
| Pool | números 1 al 80 |
| Bolas extraídas por sorteo | 20 |
| Números que escoge el jugador | 10 |
| Precio por jugada | RD$ 25 |
| Jugadas por boleto | 3 |
| Horario | Lun–Sáb 8:55 PM · Dom 3:55 PM |
| P(un número específico salga) | 20/80 = **0.25** |

### Tabla de premios

| Aciertos | Premio |
|---|---|
| 10 de 10 | RD$ 25,000,000 |
| 9 de 10 | RD$ 150,000 |
| 8 de 10 | RD$ 10,000 |
| 7 de 10 | RD$ 1,000 |
| 6 de 10 | RD$ 300 |
| 5 de 10 | RD$ 60 |
| 1–4 | sin premio |
| 0 de 10 | RD$ 80 devueltos |

P(10 aciertos) = 1 en 1,646,492,110,120.
**Valor esperado ≈ RD$16.88 por cada RD$25.** Ventaja de la casa ≈ 32.5%.
Esto es estructural y no depende del modelo.

### Reglas operativas conocidas
- **Días sin sorteo — son SEIS al año, no dos** (medido sobre Loto Pool
  2016–2018, tres años seguidos, y coincide con los huecos de Kino):

  | Días | Qué son |
  |---|---|
  | Jueves y Viernes Santo | 2016-03-24/25 · 2017-04-13/14 · 2018-03-29/30 |
  | 24 y 25 de diciembre | Nochebuena y Navidad |
  | 31 de diciembre y 1 de enero | Fin de año y Año Nuevo |

  Aplica a los dos juegos. El resto del año se sortea **todos los días**,
  domingos incluidos. Los actualizadores NO rellenan estos días: los dejan
  como hueco y los reportan.
- Jaime juega junto a **Irvin**.
- **Loto Pool: Jaime lo retomó el 2026-08-27**, ya no está descartado. Ojo: lo
  que se descartó fue *jugarlo* (márgenes malos, sin recuperación por cero
  aciertos como la de Kino). Eso sigue en pie. Lo que se hace ahora es
  **recolectar sus datos**, que es otra cosa. El `LotoPool_20260325.csv` que
  mencionaba este archivo NO existe en el repo.

---

## 2. OBJETIVO DECLARADO DEL SISTEMA

No es ganar todos los días. Es **maximizar la probabilidad de un evento de
7–10 aciertos** — un solo golpe grande — aceptando pérdida diaria.

Eso da forma a toda la estructura de jugadas: en vez de diversificar, se
**concentra** masa de probabilidad alrededor de un núcleo de 10 números.

> Nota honesta: esta estrategia es correcta *dado* que el modelo identifique
> números con probabilidad superior a 0.25. Si todos los números son iguales
> (que es lo que dice la auditoría), concentrar vs. diversificar no cambia
> P(8+ aciertos) — solo cambia la varianza. Ver sección 5.

---

## 3. ARCHIVOS DEL PAQUETE

```
athena/
├── .github/workflows/
│   └── actualizar-base.yml            <- rutina diaria (trae y commitea sola)
├── CLAUDE.md                          <- este archivo
├── AUDITORIA.md                       <- el hallazgo, en detalle
├── athena.py                          <- motor v4 completo y ejecutable
├── scripts/
│   ├── update_db.py                   <- actualizador de Kino
│   ├── update_pool.py                 <- actualizador de Loto Pool
│   └── probe_fuentes.py               <- sonda de fuentes (diagnóstico)
├── probe/REPORTE.md                   <- último resultado de la sonda
└── data/
    ├── kino_2010_a_hoy_COMPLETO.xlsx  <- base histórica de Kino
    ├── loto_pool.xlsx                 <- base de Loto Pool (desde 2026-07-28)
    └── KinoTV_Tabla_Premios.xlsx      <- tabla de premios
```

### Formato de la base histórica
Workbook con una hoja por año (`2010` … `2026`) más una hoja `📊 Resumen`.
Cada fila de datos:

| Col A | Col B |
|---|---|
| `2026-03-24  Mar` | `04, 07, 09, 10, 11, 13, 16, 18, 19, 21, 24, 32, 35, 36, 42, 58, 60, 62, 64, 69` |

Las primeras 1–2 filas de cada hoja son títulos; el cargador las salta solo.

**Estado de esta copia:** 5,729 filas crudas / 5,388 únicas,
`2010-07-19 → 2026-08-28`. Completa desde 2016.

Dos huecos grandes que se investigaron y resultaron ser cosas distintas:

| Hueco | Veredicto |
|---|---|
| 2020-03-19 → 06-02 (76 días) | **suspensión real** (COVID). resuloto tampoco los tiene. |
| 2023-03-30 → 07-29 (122 días) | **agujero de captura**. Rellenado: +125 sorteos. |

De 2023 solo quedan fuera el 6 y 7 de abril — Jueves y Viernes Santo.
Ver AUDITORIA.md.

⚠️ **Existe una versión más nueva** que Jaime bajó en una sesión posterior:
5,512 sorteos hasta el **24 de mayo de 2026**, más el workbook
`Athena_v4_Lunes25Mayo2026.xlsx`. Esos archivos no quedaron guardados en el
proyecto. Si Jaime los tiene, que reemplace `data/kino_2010_a_hoy_COMPLETO.xlsx`
y corra `python scripts/update_db.py` para completar hasta hoy.

---

## 4. EL MOTOR (`athena.py`)

### Comandos

```bash
python athena.py                        # recomendación para el próximo sorteo
python athena.py --budget 800           # escalar al presupuesto
python athena.py --export salida.xlsx   # workbook de 4 pestañas
python athena.py --audit                # auditoría de señales  <-- CORRE ESTO
python athena.py --validate             # tasas de repetición + escaneo de lags
python athena.py --backtest 300         # aciertos del top-20 vs azar
python athena.py --simulate 100         # simula jugadas reales y las cobra
python athena.py --raw                  # NO deduplicar (reproduce el bug viejo)
```

Solo necesita `openpyxl`. Sin pandas, sin numpy.

### Las 3 señales del modelo v4 (tal como estaban)

| Señal | Peso | Definición |
|---|---|---|
| **Repetición** | 45% | P(n sale hoy \| n salió ayer), por número |
| **Ciclo-5** | 25% | boost si n salió exactamente 5 sorteos atrás |
| **Momentum** | 30% | frecuencia en ventanas de 7/14/30 sorteos vs 0.25 |

Pesos derivados de v2 (35/20/25) renormalizados al eliminar DOW (15%) y
co-ocurrencia (5%). **Señales ya eliminadas por Jaime y que no deben volver:**
día de la semana, estacionalidad, "números atrasados"/gap. Fueron
correctamente identificadas como ruido esotérico.

### Estructura de jugadas (concentración-jackpot)
1. **NÚCLEO** — el top-10 exacto, 1 jugada
2. **ROTACIÓN-1** — núcleo con 1 sustitución desde ranks 11–15
3. **ROTACIÓN-2** — núcleo con 2 sustituciones
4. **COBERTURA** — 2–3 sustituciones usando ranks 16–20

### Sistema de confianza
Score 0–100 de tres métricas: precisión reciente del top-20 (50%),
consistencia de repetición (20%), convergencia de señales (30%).
Regla dura del sistema: **confianza <40% → no jugar ese día.**

### Formato de salida
Workbook de 4 pestañas: Jugadas · Scores · Cobertura · Referencia.
Las jugadas van como números separados por coma, con `---` cada 3 líneas
(un boleto = 3 jugadas).

---

## 5. AUDITORÍA — POR QUÉ EL MODELO NO PREDICE

Corrida original sobre las 5,451 filas de la base vieja. Re-corrida sobre la
base completa (5,602 filas) el 2026-08-27: **el hallazgo no cambia**. Ver el
apartado final de AUDITORIA.md — ahí está el detalle de por qué el `--audit`
ahora muestra 5.263 en la métrica [5] y por qué eso sigue siendo azar.

### 5.1 La base tiene 341 filas corruptas

341 filas repiten exactamente un conjunto de 20 números que ya aparecía antes.
La probabilidad natural de que una combinación 20-de-80 se repita es
**1 en 3.5 × 10¹⁸**. Son errores de captura, no sorteos.

Su distribución delata el origen:

| Separación entre la fila y su copia | Casos |
|---|---|
| 5 filas | **230** |
| 1 fila | 60 |
| 2 filas | 32 |
| otras | 19 |

Concentradas en **2011 (243 casos)**, con 39 en 2012 y 11 en 2026.

### 5.2 El "ciclo-5" era esas filas

Escaneo de lags, lift sobre la base 0.25:

| lag | base cruda | base limpia |
|---|---|---|
| 1 | +3.43% | −0.21% |
| 2 | +2.54% | +0.31% |
| 3 | +1.06% | +0.06% |
| 4 | −0.38% | −0.82% |
| **5** | **+12.79%** | **+0.13%** |
| 6 | −0.19% | −0.36% |
| 10 | +13.22% | +0.79% |
| 15 | +12.15% | — |

Los picos aparecen exactamente en múltiplos de 5 — la firma de un artefacto,
no de un fenómeno físico. Al quitar las filas duplicadas, el ciclo-5 cae a
**+0.13%**. El "+3.2% confirmado en 5,453 sorteos" era el eco de un error de
captura de 2011.

### 5.3 La repetición tampoco existe

Sobre base limpia, promedio de `P(sale | salió ayer) − P(sale | no salió ayer)`
= **−0.084 puntos porcentuales**. Cero. El sorteo no tiene memoria.

El famoso "#79 se repite 33.7% de las veces" es sesgo de selección: si ordenas
80 números por su tasa observada y miras el primero, siempre habrá uno arriba.

### 5.4 No hay números calientes

Frecuencia base de los 80 números vs. lo esperado por azar:
desviación estándar de los z-scores observados = **0.993** (azar puro = 1.000).
El número más extremo es el 59 con z = −2.54 — exactamente lo que produce
mirar 80 números al azar. La distribución es indistinguible de la aleatoria.

### 5.5 La métrica que el propio sistema definió

Regla escrita por Jaime en v2: *"Medir hits en top-20 por día. Esperado
aleatorio = 5. Si promedio > 6 en días de confianza alta = modelo funciona.
Si promedio ≈ 5 = el modelo no está añadiendo valor."*

Resultado sobre los últimos 300 sorteos:

| | promedio top-20 |
|---|---|
| base cruda | 5.037 (IC95 ±0.18) |
| base limpia | 5.013 (IC95 ±0.18) |
| azar | 5.000 |

**El modelo puntúa 5.01. El criterio que el propio sistema fijó dice que no
aporta valor.**

> **Corrección (2026-08-27):** este párrafo decía antes que el backtest le daba
> ventaja al modelo usando tasas calculadas con el futuro incluido. Es falso en
> el código actual: `score_numbers(draws, upto=i)` corta con `hist =
> draws[:upto]`. El backtest es walk-forward limpio, sin lookahead.
>
> Sobre la base completa, agrupando 16 ventanas de 300 sorteos sin solape
> (**4,800 sorteos walk-forward**): promedio **4.979**, IC95 **[4.931, 5.027]**.
> Contiene 5.000, no llega a 5.3. Una ventana suelta de 300 brinca entre 4.727
> y 5.177 por puro azar, así que no le hagas caso al número de una sola corrida
> del `--audit`.

### 5.6 Lo que sí es cierto

- La base es buena una vez limpia (5,110 sorteos reales, 2010–2026).
- El código funciona y es rápido.
- La estructura de concentración es la correcta *si* hubiera señal.
- El sorteo de Leidsa se comporta como un sorteo justo. Eso es información
  real: dice que no hay sesgo de máquina explotable.

---

## 6. TAREAS ABIERTAS PARA CLAUDE CODE

**Prioridad alta — integridad de datos**
1. Limpiar la base de forma permanente (ya se hace en memoria con `dedupe=True`)
   y regenerar el workbook sin las 341 filas.
2. Revisar las 3 filas con conteo anómalo: `2010-09-15` (21 números),
   `2012-10-29` (23), `2015-01-03` (18). Verificar contra la fuente.
3. Reconstruir 2011 desde resuloto.com — es el año más comprometido.
4. ~~Cerrar el hueco 2026-03-25 → hoy.~~ **HECHO** (2026-08-27, +151 sorteos).
   Queda un solo día sin explicar: **2026-06-23**. Los otros dos que faltan
   (2026-04-02 y 04-03) son Jueves y Viernes Santo.

**Prioridad media — verificación**
5. ~~Correr `--audit` sobre la base reconstruida.~~ **HECHO.** No cambia nada:
   4.979 agrupado sobre 4,800 sorteos. Detalle en AUDITORIA.md.
6. Probar el resto del espacio de hipótesis con corrección por comparaciones
   múltiples: pares/impares, suma del sorteo, distribución por decenas,
   co-ocurrencia. Si se prueban 200 hipótesis, ~10 darán p<0.05 por puro azar —
   corregir con Bonferroni o Benjamini-Hochberg antes de creer nada.

**Loto Pool — hecho el 2026-08-27**
9. ~~Encontrar fuente para Pool.~~ **HECHO.** `scripts/update_pool.py` sobre
   resuloto, enganchado a la rutina diaria. Base arrancada con 28 sorteos.
10. Verificado con datos, no con el texto de las webs: **Pool es DIARIO**
    (9 días corridos, y 4 sorteos por cada día de la semana en 28 filas).
    Es **5 números del 00 al 31**, RD$20 la jugada.
11. **La regla anti-duplicados de Kino NO se aplica a Pool.** C(32,5)=201,376,
    así que en 5,600 sorteos se esperan **78 repeticiones legítimas**. Pool
    deduplica por FECHA, nunca por números.
    Comprobado sobre los primeros 1,101 sorteos: **3 combinaciones repetidas,
    contra 3.0 esperadas por azar.** Clavado. Copiar la regla de Kino habría
    borrado esos 3 sorteos reales.
12. **Pool era DIARIO en 2016–2018**, no miércoles y sábados: 357 sorteos por
    año, ~6.88/semana, repartidos parejo entre los 7 días. Si hubo una época de
    2 por semana fue antes de 2016, y ahí no hay fuente.
13. ~~Relleno de Pool hacia atrás.~~ **HECHO** (2026-08-30, 4 tandas vía
    `workflow_dispatch` con `desde_pool` y `hasta`). **3,720 sorteos**,
    2016-01-02 → hoy. 0 filas inválidas. Frontera de resuloto: 2016-01-02.
14. **Integridad de Pool verificada con la misma prueba que delató las 341
    filas falsas de Kino.** 49 combinaciones repetidas contra 34.4 esperadas
    (z=+2.50, ruido de Poisson). Lo decisivo es la separación: **0 de 50 a
    ≤10 filas de distancia**, mediana 1,108 filas, la más cercana a 11. En
    Kino 2011 había 230 casos a exactamente 5 filas. Repartidas así son
    repeticiones legítimas, no errores de captura.
15. Tramos largos sin sorteo en Pool, contrastados contra Kino:

    | Tramo | Pool | Kino | Lectura |
    |---|---|---|---|
    | 2020-03-19 → 06-02 (76d) | 0 | 0 | COVID, suspensión real |
    | 2020-10-17 → 19 | 0/3 | 3/3 | falta solo en Pool |
    | 2025-10-22 → 25 | 0/4 | 0/4 | falta en los dos |
    | 2026-06-25 → 27 | 0/3 | 3/3 | falta solo en Pool |

    Pendiente: los 5 días sueltos de 2016–2018 (2016-05-14/15 — que también
    falta en Kino —, 2016-10-11, 2017-09-07, 2017-09-21, 2018-07-05/06).

**Si Jaime decide seguir jugando**
7. La parte útil pasa a ser operativa, no predictiva: control de gasto,
   registro de resultados reales, cálculo del retorno efectivo mes a mes,
   y la extensión de Chrome para no llenar boletos a mano.
8. Bajo azar puro, para P(8+ aciertos) lo único que mueve la aguja es el
   número de jugadas distintas, no cuáles. Vale la pena calcularle
   explícitamente qué compra cada nivel de gasto.

---

## 7. EXTENSIÓN DE CHROME (v4)

Automatiza el llenado de jugadas en leidsa.com.
- Construida para Chrome de escritorio.
- En Android funciona vía **Yandex Browser** o **Quetta Browser** (ambos
  soportan extensiones de Chrome en modo desarrollador).

### ⚠️ Estado real de las fuentes (verificado 2026-08-27)

Se sondearon las cuatro desde un runner de Actions. Solo una sirve:

| Fuente | Veredicto |
|---|---|
| **resuloto.com** | ✅ **la única que ha dado datos verificados** — Kino y Pool |
| leidsa.com | resultados embebidos en JS; extracción acierta 4 de 10 fechas |
| conectate.com | el HTML servido es artículo SEO, cero resultados; van por JS |
| elboletoganador.com | cascarón SPA de 2.5 KB; su API da 404; una vez timeout |

Ninguna ofrece descarga masiva de histórico: son 1 día por petición. Cerrar
el hueco de Kino fueron 155 peticiones.

**La sección de abajo quedó obsoleta.** Las 4 rutas documentadas dan 404, y
lo del CORS es incorrecto: CORS solo existe en el navegador — desde un
servidor no aplica, y aun así responde 404. Se deja como registro histórico.

### API alternativa (elboletoganador.com) — OBSOLETA, da 404
```
api3.bolillerobingoonlinegratis.com/api/sorteos/buscar/historial
```
- `fecha` es un **cursor hacia atrás**, no un número de página
- devuelve 15 resultados por llamada
- Game IDs: Kino = 8, Pool = 7, Pega3 = 23, Quiniela = 5
- requiere inyección de content script en una pestaña abierta de
  elboletoganador.com (las peticiones desde el origen de la extensión están
  bloqueadas)
- **firma obligatoria:** `apiFetchViaTab(tabId, gameId, fecha, cb)` —
  agregar un parámetro `page` rompe el callback

---

## 8. HISTORIAL DE VERSIONES

| Versión | Qué cambió |
|---|---|
| v1–v2 | 5 señales: repetición 35%, ciclo-5 20%, momentum 25%, DOW 15%, co-ocurrencia 5%. 80 jugadas a 90% de confianza. |
| v3 | Se eliminan DOW, estacionalidad y gap/atrasados por falta de fundamento estadístico. |
| v4 | 3 señales renormalizadas (45/25/30). Formato concentración-jackpot. Escalado por presupuesto. Última corrida: 25 mayo 2026, 32 jugadas, RD$800. |
| **auditoría** | **Ciclo-5 identificado como artefacto de datos. Repetición y momentum indistinguibles del azar. Backtest = 5.01 vs 5.00 esperado.** |

---

## 9. CÓMO TRABAJAR CON JAIME

- Escribe en español dominicano, directo, sin rodeos.
- Le gustan los números concretos y las tablas, no las generalidades.
- **Ya botó tres señales él mismo por no tener base estadística.** Prefiere
  la verdad incómoda a la validación. Trátalo así.
- Cuando una cifra sea supuesto tuyo y no dato verificado, dilo.
