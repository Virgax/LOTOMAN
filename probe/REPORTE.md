# Sonda de fuentes — último resultado

Generado por `.github/workflows/probe-fuentes.yml`. Diagnóstico, no toca la base.

Criterio: una fuente solo cuenta si alguna de sus secuencias de 20 números coincide EXACTO
con un sorteo que ya está en la base (`MATCH_BASE`). Contar bytes no prueba nada.

```
[V] base: 5,604 sorteos conocidos, último 2026-08-25
[V] pool patrón loto-pool-amp.php: HTTP 200 33,587B texto=1,204
[V] pool patrón loto-pool.php: HTTP 200 22,583B texto=1,108
[V] pool patrón pool-amp.php: HTTP 404 73,633B texto=207
[V] pool: patrón vivo -> https://www.resuloto.com/do/leid/loto-pool.php?fecha={}
[V] pool 2026-08-17 Lun: texto=1,084 numeros=9 en_rango_00_31=[17, 17, 17, 6, 13, 14, 22, 26, 3]
[V] pool 2026-08-18 Mar: texto=1,087 numeros=9 en_rango_00_31=[18, 18, 18, 2, 5, 6, 17, 25, 3]
[V] pool 2026-08-19 Mié: texto=1,117 numeros=9 en_rango_00_31=[19, 19, 19, 3, 8, 14, 18, 24, 3]
[V] pool 2026-08-20 Jue: texto=1,087 numeros=9 en_rango_00_31=[20, 20, 20, 17, 23, 25, 28, 30, 3]
[V] pool 2026-08-21 Vie: texto=1,090 numeros=9 en_rango_00_31=[21, 21, 21, 6, 8, 20, 22, 28, 3]
[V] pool 2026-08-22 Sáb: texto=1,108 numeros=9 en_rango_00_31=[22, 22, 22, 9, 15, 22, 29, 31, 3]
[V] pool 2026-08-23 Dom: texto=1,090 numeros=9 en_rango_00_31=[23, 23, 23, 2, 12, 14, 25, 27, 3]
[V] pool 2026-08-24 Lun: texto=1,084 numeros=9 en_rango_00_31=[24, 24, 24, 8, 9, 11, 16, 19, 3]
[V] pool 2026-08-25 Mar: texto=1,087 numeros=9 en_rango_00_31=[25, 25, 25, 6, 7, 15, 3]
[V] cnt_indice: 64,264B texto=4,050 secuencias=5 MATCH_BASE=0
[V] cnt_indice: 9 enlaces candidatos a historial
[V] cnt_kino: 67,692B texto=4,669 secuencias=5 MATCH_BASE=0
[V] cnt_kino: 8 enlaces candidatos a historial
[V] cnt_kino_sub: 67,692B texto=4,669 secuencias=5 MATCH_BASE=0
[V] cnt_kino_sub: 8 enlaces candidatos a historial
[V] cnt_pool: 66,896B texto=4,195 secuencias=5 MATCH_BASE=0
[V] cnt_pool: 8 enlaces candidatos a historial
[V] cnt_pool_sub: 66,896B texto=4,195 secuencias=5 MATCH_BASE=0
[V] cnt_pool_sub: 8 enlaces candidatos a historial
[V] cnt_leidsa: 64,264B texto=4,050 secuencias=5 MATCH_BASE=0
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

### pool_amp_2026-08-22 (1,204 chars)

```
Loto Pool - Resultado del S&aacute;bado 22 de Agosto de 2026 - resuloto.com Resuloto.com Menú Otros juegos Super Palé Loto Pool Pega 3 Más Super Kino TV Quiniela Leidsa Loto Más Organismos Lotería Nacional RD Leidsa Loto Real Loteka Loto Pool S&aacute;bado 22 de Agosto de 2026 Loto Pool S&aacute;bado 22 Ago 09 15 22 29 31 &#9668;&nbsp;Anterior Siguiente&nbsp;&#9658; Otros juegos Super Palé Loto Pool Pega 3 Más Super Kino TV Quiniela Leidsa Loto Más Organismos Lotería Nacional RD Leidsa Loto Real Loteka Calendario Días de sorteo Últimos resultados Compártenos en redes sociales Aplicacion móvil de Resuloto Bájate nuestra APP ResuLoto y comprueba todos los resultados de las loterías con la cámara de tu móvil . No tendrás que meter los resultados manualmente. Sólo enfoca el código de barras del boleto y te diremos si está premiado Más info Esta página web no está vinculada con, ni afiliada a, ni aprobada por ningún organismo oficial. El propósito de está Web es únicamente informar de los resultados y de noticias relacionadas con los sorteos de loterías. Para obtener más información o comprobar los resultados oficiales contacte con la entidad organizadora de los juegos Aviso Legal Contactar
```

### pool_plano_2026-08-22 (1,108 chars)

```
Loto Pool - Resultado del S&aacute;bado 22 de Agosto de 2026 - resuloto.com Resuloto.com Loto Pool S&aacute;bado 22 de Agosto de 2026 Loto Pool S&aacute;bado 22 Ago 09 15 22 29 31 &#9668;&nbsp;Anterior Siguiente&nbsp;&#9658; Otros juegos Super Palé Loto Pool Pega 3 Más Super Kino TV Quiniela Leidsa Loto Más Organismos Lotería Nacional RD Leidsa Loto Real Loteka Calendario Días de sorteo Últimos resultados Compártenos en redes sociales Aplicacion móvil de Resuloto Bájate nuestra APP ResuLoto y comprueba todos los resultados de las loterías con la cámara de tu móvil . No tendrás que meter los resultados manualmente. Sólo enfoca el código de barras del boleto y te diremos si está premiado Más info Favoritos Juegos Buscar Configuración Compartir Esta página web no está vinculada con, ni afiliada a, ni aprobada por ningún organismo oficial. El propósito de está Web es únicamente informar de los resultados y de noticias relacionadas con los sorteos de loterías. Para obtener más información o comprobar los resultados oficiales contacte con la entidad organizadora de los juegos Aviso Legal Contactar
```

### cnt_indice (4,050 chars)

```
Leidsa: Resultados, Horarios, Estadísticas y Guía Loterías Portada Lotería Nacional Leidsa Lotería Real Loteka La Primera La Suerte Lotedom Americanas (New York) Anguila King Lottery Quinielas Gana Más Lotería Nacional Quiniela Leidsa Quiniela Real Quiniela Loteka New York Tarde New York Noche Florida Día Florida Noche La Primera Día La Primera Noche La Suerte Día La Suerte Tarde Lotedom Anguila (Todas) Haiti Bolet (Todas) King Lottery Día King Lottery Noche Lotos Loto Leidsa Loto Real Mega Lotto Loteka Loto 5 La Primera Mega Millions Powerball DP Powerball Estadísticas Quinielas Años Anteriores Números Calientes Números Fríos Pronósticos Consultar Números Leidsa: Resultados, Horarios, Estadísticas y Guía Leidsa es una de las compañías de lotería más populares de República Dominicana y ofrece sorteos diarios de quinielas, lotos y juegos electrónicos. En esta página encontrarás información organizada sobre resultados, horarios, estadísticas y juegos como Quiniela Leidsa, Loto Leidsa, Pega 3 Más, Loto Pool y Súper Kino TV. Juegos de Leidsa Quiniela Leidsa Sorteo diario de quiniela donde se publican números ganadores en primera, segunda y tercera posición. Es uno de los juegos más populares entre los jugadores dominicanos. Pega 3 Más Juego electrónico diario donde los participantes deben acertar números de tres cifras en diferentes modalidades de apuesta. Loto Pool Juego diario donde los jugadores seleccionan cinco números para participar en el sorteo. Súper Kino TV Juego electrónico donde se extraen 20 números ganadores en cada sorteo. Loto Leidsa Uno de los sorteos más conocidos de República Dominicana, realizado semanalmente con premios acumulativos millonarios. Horarios de Sorteos Leidsa Quiniela Leidsa: 8:55 PM Pega 3 Más: 8:55 PM Loto Pool: 8:55 PM Súper Kino TV: 8:55 PM Domingos: 3:55 PM Loto Leidsa: miércoles y sábados 8:55 PM ¿Cómo Jugar los Juegos de Leidsa? Los juegos de Leidsa permiten participar en diferentes modalidades de apuestas diarias y sorteos acumulativos en República Dominicana.Los sorteos de Leidsa pueden jugarse en bancas de lotería autorizadas y puntos de venta disponibles en diferentes provincias y ciudades del país. ¿Cómo se Juega? Leidsa ofrece diferentes modalidades de juegos y sorteos diarios en República Dominicana, incluyendo quinielas, lotos y juegos electrónicos. Cada sorteo cuenta con reglas, horarios y modalidades de juego diferentes. Para conocer cómo jugar, tipos de apuestas, premios y detalles de cada juego, selecciona el sorteo correspondiente dentro de esta página. ¿Cuánto Cuesta Jugar? El monto de las apuestas puede variar dependiendo del juego, la modalidad seleccionada y el valor apostado por el jugador. Las bancas de lotería permiten realizar apuestas desde montos bajos hasta jugadas de mayor valor dependiendo del sorteo. Sorteos Especiales de Leidsa Además de sus sorteos diarios, Leidsa también realiza diferentes sorteos especiales y promociones durante el año en República Dominicana, como el Sorteo de Navidad y el Sorteo de las Madres. Estos sorteos suelen incluir premios millonarios, vehículos, bonos y promociones especiales para los jugadores de Leidsa. Los sorteos especiales pueden variar cada año dependiendo de las promociones y actividades anunciadas por la compañía. Información de Leidsa Página Web Oficial: Leidsa.com Teléfono: (809) 683-9393 Dirección: Av. Abraham Lincoln #1059, Santo Domingo, República Dominicana Dónde Ver los Sorteos Leidsa, “Tu Única Loto”, realiza sorteos diarios a 
```

### cnt_kino (4,669 chars)

```
Super Kino TV Leidsa: Resultados de Hoy Loterías Portada Lotería Nacional Leidsa Lotería Real Loteka La Primera La Suerte Lotedom Americanas (New York) Anguila King Lottery Quinielas Gana Más Lotería Nacional Quiniela Leidsa Quiniela Real Quiniela Loteka New York Tarde New York Noche Florida Día Florida Noche La Primera Día La Primera Noche La Suerte Día La Suerte Tarde Lotedom Anguila (Todas) Haiti Bolet (Todas) King Lottery Día King Lottery Noche Lotos Loto Leidsa Loto Real Mega Lotto Loteka Loto 5 La Primera Mega Millions Powerball DP Powerball Estadísticas Quinielas Años Anteriores Números Calientes Números Fríos Pronósticos Consultar Números Super Kino TV Leidsa: Resultados de Hoy, Números Ganadores y Premios Consulta los resultados de hoy de Super Kino TV Leidsa, verifica los números ganadores más recientes, revisa sorteos anteriores y accede a estadísticas actualizadas. También encontrarás información sobre premios, horarios de los sorteos, costos de participación y la forma de jugar este popular sorteo de Leidsa. Super Kino TV | Leidsa ¿Qué es Super Kino TV Leidsa? Super Kino TV Leidsa es un juego de lotería que ofrece múltiples formas de ganar mediante la selección de números. En cada sorteo se extraen 20 bolos de un total de 80 números, mientras que los jugadores deben elegir 10 números para participar. Dependiendo de la cantidad de aciertos obtenidos, es posible ganar desde premios menores hasta un premio mayor de RD$25 millones. Gracias a sus diferentes categorías de premios, Super Kino TV es una de las modalidades más atractivas para quienes buscan múltiples oportunidades de ganar en un solo sorteo. ¿Cómo se juega Super Kino TV Leidsa? Para participar en Super Kino TV, los jugadores deben: Seleccionar 10 números del 1 al 80 Durante cada sorteo se extraen: 20 números ganadores Los premios se determinan según la cantidad de coincidencias entre los números seleccionados por el jugador y los números sorteados. Las apuestas pueden realizarse en cualquiera de los puntos de venta autorizados de Leidsa en todo el territorio nacional. Horario del Sorteo Super Kino TV Los sorteos se realizan: Todos los días: 8:55 p.m. Los resultados son publicados inmediatamente después de finalizar cada sorteo. Estadísticas de Super Kino TV Leidsa Consulta cuáles han sido los números más sorteados durante: Último mes Últimos 3 meses Últimos 6 meses También puedes analizar: Números más frecuentes Números menos frecuentes Números más atrasados Historial de apariciones Estas estadísticas ayudan a conocer el comportamiento histórico de los números ganadores y las tendencias de los sorteos. ¿Cuánto cuesta jugar Super Kino TV? El costo de participación es de: RD$25 por jugada Cada apuesta permite seleccionar una combinación de 10 números para participar en el sorteo. Probabilidades de ganar en Super Kino TV Los premios dependen de la cantidad de números acertados entre los 20 números sorteados. 10 números acertados Premio mayor del sorteo. 9 números acertados Premio de segunda categoría. 8 números acertados Premio de tercera categoría. 7 números acertados Premio de cuarta categoría. 6 números acertados Premio de quinta categoría. 5 números acertados Premio de sexta categoría. 0 números acertados Premio especial por no acertar ninguno de los números sorteados. ¿Cuánto paga Super Kino TV Leidsa? Los premios de Super Kino TV se distribuyen según la cantidad de números acertados: 10 números acertados RD$25,000,000 9 números acertados RD$150,000 8 números acer
```

### cnt_kino_sub

Idéntico a `cnt_kino`.

### cnt_pool (4,195 chars)

```
Loto Pool Leidsa - Resultados de Hoy Lotería Leidsa Loterías Portada Lotería Nacional Leidsa Lotería Real Loteka La Primera La Suerte Lotedom Americanas (New York) Anguila King Lottery Quinielas Gana Más Lotería Nacional Quiniela Leidsa Quiniela Real Quiniela Loteka New York Tarde New York Noche Florida Día Florida Noche La Primera Día La Primera Noche La Suerte Día La Suerte Tarde Lotedom Anguila (Todas) Haiti Bolet (Todas) King Lottery Día King Lottery Noche Lotos Loto Leidsa Loto Real Mega Lotto Loteka Loto 5 La Primera Mega Millions Powerball DP Powerball Estadísticas Quinielas Años Anteriores Números Calientes Números Fríos Pronósticos Consultar Números Loto Pool Leidsa: Resultados de Hoy, Números Ganadores y Premios Consulta los resultados de hoy de Loto Pool Leidsa, verifica los números ganadores más recientes, revisa sorteos anteriores y accede a estadísticas actualizadas. También encontrarás información sobre premios, horarios de los sorteos, costos de participación y la forma de jugar este popular juego de Leidsa. Loto Pool | Leidsa ¿Qué es Loto Pool Leidsa? Loto Pool Leidsa es uno de los sorteos más populares de Leidsa en República Dominicana. El juego se realiza con una tómbola compuesta por bolos numerados del 00 al 31, donde los jugadores deben seleccionar 5 números para participar por premios en efectivo. Gracias a sus múltiples categorías de aciertos y su accesible costo de participación, Loto Pool se ha convertido en una de las opciones favoritas de los jugadores dominicanos. ¿Cómo se juega Loto Pool Leidsa? Para participar en Loto Pool Leidsa, los jugadores deben: Seleccionar 5 números del 00 al 31 Durante el sorteo se extraen los números ganadores que determinan las diferentes categorías de premios. Los jugadores pueden realizar sus apuestas en cualquiera de las agencias y puntos de venta autorizados de Leidsa en todo el territorio nacional. Horario del Sorteo Loto Pool Los sorteos se realizan: Miércoles: 8:55 p.m. Sábados: 8:55 p.m. Los resultados son publicados inmediatamente después de finalizar cada sorteo. Estadísticas de Loto Pool Leidsa Consulta cuáles han sido los números más sorteados durante: Último mes Últimos 3 meses Últimos 6 meses También puedes analizar: Números más frecuentes Números menos frecuentes Números más atrasados Historial de apariciones Estas estadísticas permiten conocer el comportamiento histórico de los números ganadores y las tendencias de los sorteos. ¿Cuánto cuesta jugar Loto Pool? El costo mínimo para participar en Loto Pool es de: RD$20 por jugada Los jugadores pueden realizar apuestas superiores según las opciones disponibles en los puntos de venta autorizados. Probabilidades de ganar en Loto Pool Leidsa Las probabilidades de ganar dependen de la cantidad de números acertados durante el sorteo. 5 números acertados Premio mayor del sorteo. 4 números acertados Premio secundario. 3 números acertados Premio de tercera categoría. Loto Pool ofrece varias oportunidades de ganar gracias a sus diferentes niveles de premios. ¿Cuánto paga Loto Pool Leidsa? Los premios de Loto Pool se distribuyen según la cantidad de números acertados: 5 números acertados RD$1,000,000 4 números acertados RD$5,000 3 números acertados RD$50 Los premios están sujetos a las reglas y condiciones vigentes establecidas por Leidsa. Aciertos Ganadores en Loto Pool Premio Mayor Acertar los 5 números sorteados. Segundo Premio Acertar 4 de los 5 números sorteados. Tercer Premio Acertar 3 de los 5 números sorteados. Resultad
```

### cnt_pool_sub

Idéntico a `cnt_pool`.

### cnt_leidsa

Idéntico a `cnt_indice`.
