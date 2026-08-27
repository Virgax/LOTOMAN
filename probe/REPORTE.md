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

## Textos planos (para escribir el parser)

### cnt_indice (4,143 chars)

```
Leidsa: Resultados, Horarios, EstadÃ­sticas y GuÃ­a LoterÃ­as Portada LoterÃ­a Nacional Leidsa LoterÃ­a Real Loteka La Primera La Suerte Lotedom Americanas (New York) Anguila King Lottery Quinielas Gana MÃ¡s LoterÃ­a Nacional Quiniela Leidsa Quiniela Real Quiniela Loteka New York Tarde New York Noche Florida DÃ­a Florida Noche La Primera DÃ­a La Primera Noche La Suerte DÃ­a La Suerte Tarde Lotedom Anguila (Todas) Haiti Bolet (Todas) King Lottery DÃ­a King Lottery Noche Lotos Loto Leidsa Loto Real Mega Lotto Loteka Loto 5 La Primera Mega Millions Powerball DP Powerball EstadÃ­sticas Quinielas AÃ±os Anteriores NÃºmeros Calientes NÃºmeros FrÃ­os PronÃ³sticos Consultar NÃºmeros Leidsa: Resultados, Horarios, EstadÃ­sticas y GuÃ­a Leidsa es una de las compaÃ±Ã­as de loterÃ­a mÃ¡s populares de RepÃºblica Dominicana y ofrece sorteos diarios de quinielas, lotos y juegos electrÃ³nicos. En esta pÃ¡gina encontrarÃ¡s informaciÃ³n organizada sobre resultados, horarios, estadÃ­sticas y juegos como Quiniela Leidsa, Loto Leidsa, Pega 3 MÃ¡s, Loto Pool y SÃºper Kino TV. Juegos de Leidsa Quiniela Leidsa Sorteo diario de quiniela donde se publican nÃºmeros ganadores en primera, segunda y tercera posiciÃ³n. Es uno de los juegos mÃ¡s populares entre los jugadores dominicanos. Pega 3 MÃ¡s Juego electrÃ³nico diario donde los participantes deben acertar nÃºmeros de tres cifras en diferentes modalidades de apuesta. Loto Pool Juego diario donde los jugadores seleccionan cinco nÃºmeros para participar en el sorteo. SÃºper Kino TV Juego electrÃ³nico donde se extraen 20 nÃºmeros ganadores en cada sorteo. Loto Leidsa Uno de los sorteos mÃ¡s conocidos de RepÃºblica Dominicana, realizado semanalmente con premios acumulativos millonarios. Horarios de Sorteos Leidsa Quiniela Leidsa: 8:55 PM Pega 3 MÃ¡s: 8:55 PM Loto Pool: 8:55 PM SÃºper Kino TV: 8:55 PM Domingos: 3:55 PM Loto Leidsa: miÃ©rcoles y sÃ¡bados 8:55 PM Â¿CÃ³mo Jugar los Juegos de Leidsa? Los juegos de Leidsa permiten participar en diferentes modalidades de apuestas diarias y sorteos acumulativos en RepÃºblica Dominicana.Los sorteos de Leidsa pueden jugarse en bancas de loterÃ­a autorizadas y puntos de venta disponibles en diferentes provincias y ciudades del paÃ­s. Â¿CÃ³mo se Juega? Leidsa ofrece diferentes modalidades de juegos y sorteos diarios en RepÃºblica Dominicana, incluyendo quinielas, lotos y juegos electrÃ³nicos. Cada sorteo cuenta con reglas, horarios y modalidades de juego diferentes. Para conocer cÃ³mo jugar, tipos de apuestas, premios y detalles de cada juego, selecciona el sorteo correspondiente dentro de esta pÃ¡gina. Â¿CuÃ¡nto Cuesta Jugar? El monto de las apuestas puede variar dependiendo del juego, la modalidad seleccionada y el valor apostado por el jugador. Las bancas de loterÃ­a permiten realizar apuestas desde montos bajos hasta jugadas de mayor valor dependiendo del sorteo. Sorteos Especiales de Leidsa AdemÃ¡s de sus sorteos diarios, Leidsa tambiÃ©n realiza diferentes sorteos especiales y promociones durante el aÃ±o en RepÃºblica Dominicana, como el Sorteo de Navidad y el Sorteo de las Madres. Estos sorteos suelen incluir premios millonarios, vehÃ­culos, bonos y promociones especiales para los jugadores de Leidsa. Los sorteos especiales pueden variar cada aÃ±o dependiendo de las promociones y actividades anunciadas por la compaÃ±Ã­a. InformaciÃ³n de Leidsa PÃ¡gina Web Oficial: Leidsa.com TelÃ©fono: (809) 683-9393 DirecciÃ³n: Av. Abraham Lincoln #1059, Santo Domingo, RepÃºblica Dominican
```

### cnt_kino (4,777 chars)

```
Super Kino TV Leidsa: Resultados de Hoy LoterÃ­as Portada LoterÃ­a Nacional Leidsa LoterÃ­a Real Loteka La Primera La Suerte Lotedom Americanas (New York) Anguila King Lottery Quinielas Gana MÃ¡s LoterÃ­a Nacional Quiniela Leidsa Quiniela Real Quiniela Loteka New York Tarde New York Noche Florida DÃ­a Florida Noche La Primera DÃ­a La Primera Noche La Suerte DÃ­a La Suerte Tarde Lotedom Anguila (Todas) Haiti Bolet (Todas) King Lottery DÃ­a King Lottery Noche Lotos Loto Leidsa Loto Real Mega Lotto Loteka Loto 5 La Primera Mega Millions Powerball DP Powerball EstadÃ­sticas Quinielas AÃ±os Anteriores NÃºmeros Calientes NÃºmeros FrÃ­os PronÃ³sticos Consultar NÃºmeros Super Kino TV Leidsa: Resultados de Hoy, NÃºmeros Ganadores y Premios Consulta los resultados de hoy de Super Kino TV Leidsa, verifica los nÃºmeros ganadores mÃ¡s recientes, revisa sorteos anteriores y accede a estadÃ­sticas actualizadas. TambiÃ©n encontrarÃ¡s informaciÃ³n sobre premios, horarios de los sorteos, costos de participaciÃ³n y la forma de jugar este popular sorteo de Leidsa. Super Kino TV | Leidsa Â¿QuÃ© es Super Kino TV Leidsa? Super Kino TV Leidsa es un juego de loterÃ­a que ofrece mÃºltiples formas de ganar mediante la selecciÃ³n de nÃºmeros. En cada sorteo se extraen 20 bolos de un total de 80 nÃºmeros, mientras que los jugadores deben elegir 10 nÃºmeros para participar. Dependiendo de la cantidad de aciertos obtenidos, es posible ganar desde premios menores hasta un premio mayor de RD$25 millones. Gracias a sus diferentes categorÃ­as de premios, Super Kino TV es una de las modalidades mÃ¡s atractivas para quienes buscan mÃºltiples oportunidades de ganar en un solo sorteo. Â¿CÃ³mo se juega Super Kino TV Leidsa? Para participar en Super Kino TV, los jugadores deben: Seleccionar 10 nÃºmeros del 1 al 80 Durante cada sorteo se extraen: 20 nÃºmeros ganadores Los premios se determinan segÃºn la cantidad de coincidencias entre los nÃºmeros seleccionados por el jugador y los nÃºmeros sorteados. Las apuestas pueden realizarse en cualquiera de los puntos de venta autorizados de Leidsa en todo el territorio nacional. Horario del Sorteo Super Kino TV Los sorteos se realizan: Todos los dÃ­as: 8:55 p.m. Los resultados son publicados inmediatamente despuÃ©s de finalizar cada sorteo. EstadÃ­sticas de Super Kino TV Leidsa Consulta cuÃ¡les han sido los nÃºmeros mÃ¡s sorteados durante: Ãltimo mes Ãltimos 3 meses Ãltimos 6 meses TambiÃ©n puedes analizar: NÃºmeros mÃ¡s frecuentes NÃºmeros menos frecuentes NÃºmeros mÃ¡s atrasados Historial de apariciones Estas estadÃ­sticas ayudan a conocer el comportamiento histÃ³rico de los nÃºmeros ganadores y las tendencias de los sorteos. Â¿CuÃ¡nto cuesta jugar Super Kino TV? El costo de participaciÃ³n es de: RD$25 por jugada Cada apuesta permite seleccionar una combinaciÃ³n de 10 nÃºmeros para participar en el sorteo. Probabilidades de ganar en Super Kino TV Los premios dependen de la cantidad de nÃºmeros acertados entre los 20 nÃºmeros sorteados. 10 nÃºmeros acertados Premio mayor del sorteo. 9 nÃºmeros acertados Premio de segunda categorÃ­a. 8 nÃºmeros acertados Premio de tercera categorÃ­a. 7 nÃºmeros acertados Premio de cuarta categorÃ­a. 6 nÃºmeros acertados Premio de quinta categorÃ­a. 5 nÃºmeros acertados Premio de sexta categorÃ­a. 0 nÃºmeros acertados Premio especial por no acertar ninguno de los nÃºmeros sorteados. Â¿CuÃ¡nto paga Super Kino TV Leidsa? Los premios de Super Kino TV se distribuyen segÃºn la cantidad de nÃºmeros acertad
```

### cnt_kino_sub

Idéntico a `cnt_kino`.

### cnt_pool (4,279 chars)

```
Loto Pool Leidsa - Resultados de Hoy LoterÃ­a Leidsa LoterÃ­as Portada LoterÃ­a Nacional Leidsa LoterÃ­a Real Loteka La Primera La Suerte Lotedom Americanas (New York) Anguila King Lottery Quinielas Gana MÃ¡s LoterÃ­a Nacional Quiniela Leidsa Quiniela Real Quiniela Loteka New York Tarde New York Noche Florida DÃ­a Florida Noche La Primera DÃ­a La Primera Noche La Suerte DÃ­a La Suerte Tarde Lotedom Anguila (Todas) Haiti Bolet (Todas) King Lottery DÃ­a King Lottery Noche Lotos Loto Leidsa Loto Real Mega Lotto Loteka Loto 5 La Primera Mega Millions Powerball DP Powerball EstadÃ­sticas Quinielas AÃ±os Anteriores NÃºmeros Calientes NÃºmeros FrÃ­os PronÃ³sticos Consultar NÃºmeros Loto Pool Leidsa: Resultados de Hoy, NÃºmeros Ganadores y Premios Consulta los resultados de hoy de Loto Pool Leidsa, verifica los nÃºmeros ganadores mÃ¡s recientes, revisa sorteos anteriores y accede a estadÃ­sticas actualizadas. TambiÃ©n encontrarÃ¡s informaciÃ³n sobre premios, horarios de los sorteos, costos de participaciÃ³n y la forma de jugar este popular juego de Leidsa. Loto Pool | Leidsa Â¿QuÃ© es Loto Pool Leidsa? Loto Pool Leidsa es uno de los sorteos mÃ¡s populares de Leidsa en RepÃºblica Dominicana. El juego se realiza con una tÃ³mbola compuesta por bolos numerados del 00 al 31, donde los jugadores deben seleccionar 5 nÃºmeros para participar por premios en efectivo. Gracias a sus mÃºltiples categorÃ­as de aciertos y su accesible costo de participaciÃ³n, Loto Pool se ha convertido en una de las opciones favoritas de los jugadores dominicanos. Â¿CÃ³mo se juega Loto Pool Leidsa? Para participar en Loto Pool Leidsa, los jugadores deben: Seleccionar 5 nÃºmeros del 00 al 31 Durante el sorteo se extraen los nÃºmeros ganadores que determinan las diferentes categorÃ­as de premios. Los jugadores pueden realizar sus apuestas en cualquiera de las agencias y puntos de venta autorizados de Leidsa en todo el territorio nacional. Horario del Sorteo Loto Pool Los sorteos se realizan: MiÃ©rcoles: 8:55 p.m. SÃ¡bados: 8:55 p.m. Los resultados son publicados inmediatamente despuÃ©s de finalizar cada sorteo. EstadÃ­sticas de Loto Pool Leidsa Consulta cuÃ¡les han sido los nÃºmeros mÃ¡s sorteados durante: Ãltimo mes Ãltimos 3 meses Ãltimos 6 meses TambiÃ©n puedes analizar: NÃºmeros mÃ¡s frecuentes NÃºmeros menos frecuentes NÃºmeros mÃ¡s atrasados Historial de apariciones Estas estadÃ­sticas permiten conocer el comportamiento histÃ³rico de los nÃºmeros ganadores y las tendencias de los sorteos. Â¿CuÃ¡nto cuesta jugar Loto Pool? El costo mÃ­nimo para participar en Loto Pool es de: RD$20 por jugada Los jugadores pueden realizar apuestas superiores segÃºn las opciones disponibles en los puntos de venta autorizados. Probabilidades de ganar en Loto Pool Leidsa Las probabilidades de ganar dependen de la cantidad de nÃºmeros acertados durante el sorteo. 5 nÃºmeros acertados Premio mayor del sorteo. 4 nÃºmeros acertados Premio secundario. 3 nÃºmeros acertados Premio de tercera categorÃ­a. Loto Pool ofrece varias oportunidades de ganar gracias a sus diferentes niveles de premios. Â¿CuÃ¡nto paga Loto Pool Leidsa? Los premios de Loto Pool se distribuyen segÃºn la cantidad de nÃºmeros acertados: 5 nÃºmeros acertados RD$1,000,000 4 nÃºmeros acertados RD$5,000 3 nÃºmeros acertados RD$50 Los premios estÃ¡n sujetos a las reglas y condiciones vigentes establecidas por Leidsa. Aciertos Ganadores en Loto Pool Premio Mayor Acertar los 5 nÃºmeros sorteados. Segundo Premio Acertar 4 de los 5 nÃº
```

### cnt_pool_sub

Idéntico a `cnt_pool`.

### cnt_leidsa

Idéntico a `cnt_indice`.
