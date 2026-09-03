// Corre dentro de leidsa.com/play/*. Hace los clics; NO compra.
// El botón "jugar ahora" no se toca nunca desde aquí: eso lo hace Jaime.

const RE_AGREGAR = /agregar|añadir|anadir|registrar|guardar|listo|aceptar|siguiente/i;
const RE_JUGAR   = /jugar\s*ahora|comprar|pagar|confirmar\s*compra/i;

const visible = el => {
  const r = el.getBoundingClientRect();
  return r.width > 0 && r.height > 0 && getComputedStyle(el).visibility !== "hidden";
};

/** Los elementos-bola: hoja del DOM, texto = número en rango, visible.
 *  Se agrupan por padre y se queda el grupo más grande. Buscar por clase sería
 *  más rápido pero se rompe cada vez que Leidsa toque el CSS. */
function hallarBolas(lo, hi) {
  const porPadre = new Map();
  for (const el of document.querySelectorAll("*")) {
    if (el.children.length) continue;
    const t = (el.textContent || "").trim();
    if (!/^0?\d{1,2}$/.test(t)) continue;
    const n = parseInt(t, 10);
    if (n < lo || n > hi || !visible(el)) continue;
    const p = el.parentElement?.parentElement || el.parentElement;
    if (!p) continue;
    if (!porPadre.has(p)) porPadre.set(p, new Map());
    const m = porPadre.get(p);
    if (!m.has(n)) m.set(n, el);      // el primero gana
  }
  let mejor = null;
  for (const [, m] of porPadre) if (!mejor || m.size > mejor.size) mejor = m;
  return mejor || new Map();
}

function botonPorTexto(re) {
  const cand = [...document.querySelectorAll(
    "button,a,[role=button],input[type=button],input[type=submit],div,span")];
  return cand.find(el => {
    const t = (el.textContent || el.value || "").trim();
    return t && t.length < 40 && re.test(t) && visible(el) && !el.disabled;
  }) || null;
}

/** Click "de verdad": muchos SPA ignoran un .click() pelado. */
function clic(el) {
  el.scrollIntoView({ block: "center", behavior: "instant" });
  for (const tipo of ["pointerdown", "mousedown", "mouseup", "click"]) {
    el.dispatchEvent(new MouseEvent(tipo, { bubbles: true, cancelable: true, view: window }));
  }
}
const esperar = ms => new Promise(r => setTimeout(r, ms));

async function llenar({ jugadas, lo, hi, pick, pausa }, progreso) {
  const hechas = [];
  for (let i = 0; i < jugadas.length; i++) {
    const bolas = hallarBolas(lo, hi);
    if (bolas.size < hi - lo + 1) {
      return { ok: false, hechas, error:
        `Solo encontré ${bolas.size} bolas de ${hi - lo + 1} en la jugada ${i + 1}. ` +
        `Puede que la página haya cambiado o no haya terminado de cargar.` };
    }
    for (const n of jugadas[i]) {
      const el = bolas.get(n);
      if (!el) return { ok: false, hechas, error: `No encontré el número ${n}.` };
      clic(el);
      await esperar(pausa);
    }
    const btn = botonPorTexto(RE_AGREGAR);
    if (!btn) {
      return { ok: false, hechas, error:
        `Seleccioné los ${pick} números de la jugada ${i + 1} pero no encontré el ` +
        `botón de agregar. Revísalo a mano y dime qué dice ese botón.` };
    }
    clic(btn);
    await esperar(pausa * 3);
    hechas.push(jugadas[i]);
    progreso({ hecha: i + 1, total: jugadas.length });
  }
  return { ok: true, hechas };
}

chrome.runtime.onMessage.addListener((msg, _s, responder) => {
  if (msg.tipo === "detectar") {
    const bolas = hallarBolas(msg.lo, msg.hi);
    responder({
      url: location.href,
      bolas: bolas.size,
      esperadas: msg.hi - msg.lo + 1,
      btnAgregar: botonPorTexto(RE_AGREGAR)?.textContent?.trim() || null,
      btnJugar: botonPorTexto(RE_JUGAR)?.textContent?.trim() || null,
    });
    return true;
  }
  if (msg.tipo === "llenar") {
    llenar(msg.cfg, p => chrome.runtime.sendMessage({ tipo: "progreso", ...p }))
      .then(responder)
      .catch(e => responder({ ok: false, hechas: [], error: String(e) }));
    return true;   // respuesta asíncrona
  }
});
