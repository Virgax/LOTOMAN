# Bookmarklets para jugar desde el teléfono

## Por qué bookmarklet y no extensión

La extensión v4 hacía **automatización de clics dentro de la página ya
autenticada** de leidsa.com: Jaime hacía login y el 2FA a mano, y la extensión
seleccionaba los bolos y registraba las jugadas. No tocaba credenciales, no
llamaba APIs, no guardaba estado.

Esa clase de automatización se convierte en bookmarklet sin perder nada, y el
bookmarklet sí corre en iPhone y Android:

| | Escritorio | Android Chrome | iPhone Safari |
|---|---|---|---|
| Extensión de Chrome | sí | no (Kiwi sí) | imposible |
| Bookmarklet | sí | sí | sí |

Un bookmarklet corre en el origen de la pestaña abierta, así que usa la sesión
que ya tiene el navegador. No hay credenciales que guardar en ningún lado.

## Paso 1 — inspector (lo que hay ahora)

`inspector.js` SOLO LEE. No hace clic, no selecciona bolos, no compra nada.
Recorre el DOM de la página de juego y reporta:

  * los grupos de elementos cuyo texto es un número 1..80 (las bolas)
  * los botones visibles y su texto
  * los montos en pantalla (saldo, total)

Copia el reporte al portapapeles para poder escribir el bookmarklet de verdad
sobre la estructura real, en vez de adivinarla.

### Cómo instalarlo

**Escritorio:** crea un marcador nuevo y pega el contenido de
`inspector.bookmarklet.txt` como URL.

**iPhone (Safari):** marca cualquier página, luego edita el marcador y
reemplaza la URL por el contenido del .txt. Se ejecuta tocándolo desde
Favoritos con la página de juego abierta.

**Android (Chrome):** crea el marcador igual, ponle un nombre corto (ej. `insp`)
y ejecútalo escribiendo ese nombre en la barra de direcciones.

### Cómo usarlo

1. Entra a leidsa.com y haz login con tu 2FA.
2. Ve a https://www.leidsa.com/play/draw/leidsa-kinotv
3. Toca el bookmarklet.
4. Pega el reporte en el chat.

## Paso 2 — el bookmarklet de jugadas (pendiente)

Se escribe cuando llegue el reporte del inspector. Va a:

  * recibir las jugadas ya calculadas (de Athena Boletos)
  * seleccionar los bolos de cada jugada y registrarla
  * repetir hasta completar la cantidad
  * **mostrar jugadas y total, y esperar confirmación ANTES de "jugar ahora"**

Ese último punto no es negociable: un bookmarklet que compra de un toque es
plata que se va por un mal clic.

## Aviso

Automatizar compras suele ir contra los términos de servicio de un sitio de
apuestas. El riesgo concreto es que cierren la cuenta.
