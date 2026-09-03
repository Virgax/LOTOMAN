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

---

# Extensión de Chrome v5 (lo que se usa)

Jaime prefiere la extensión sobre el bookmarklet, y con razón: en escritorio es
más cómoda y no hay que pegar nada en la barra. El bookmarklet y el inspector
de arriba quedan como alternativa para el teléfono.

## Arquitectura

    rutina diaria (GitHub Actions)
        -> scripts/jugadas_hoy.py
        -> data/jugadas_hoy.json   (commiteado al repo)
                |
                | raw.githubusercontent.com  (repo publico, sin token)
                v
    extension  -> popup.js baja el archivo
               -> content.js hace los clics en leidsa.com

**La extensión no calcula nada.** Toda la lógica vive en el repo, donde ya
están athena, la base de 5,392 sorteos y las validaciones. La extensión se
mantiene tonta a propósito: menos cosas que se rompan cuando Leidsa cambie
el CSS.

## Instalar

1. `chrome://extensions` -> activar "Modo de desarrollador"
2. "Cargar descomprimida" -> elegir la carpeta `extension/`

## Usar

1. Entrar a leidsa.com, login y 2FA a mano.
2. Ir a la página del juego (`/play/draw/leidsa-kinotv`).
3. Abrir la extensión -> **Cargar jugadas** (baja el archivo del día).
4. **Revisar página** — confirma que encuentra las 80 bolas y el botón de
   agregar. Si algo falta, lo dice antes de tocar nada.
5. **Llenar jugadas** -> pide confirmación con el costo, y llena.
6. **El botón de jugar lo tocas tú**, después de ver el total en pantalla.

## Lo que NO hace

* No compra. Nunca toca "jugar ahora".
* No guarda credenciales. Usa la sesión que ya tiene el navegador.
* No adivina selectores por clase CSS: busca los elementos-hoja cuyo texto es
  un número en rango y se queda con el grupo más grande. Sobrevive a un
  rediseño; buscar por clase no.

## Si se rompe

"Revisar página" es el diagnóstico. Si reporta menos bolas de las esperadas o
no encuentra el botón de agregar, la página cambió — manda ese reporte y se
ajusta `content.js`.

Subir la pausa (140 ms por defecto) ayuda si la página va lenta: cada clic
necesita que el framework procese el estado antes del siguiente.
