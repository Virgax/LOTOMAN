const URL_DEF = "https://raw.githubusercontent.com/Virgax/LOTOMAN/" +
                "claude/lotoman-nq7rfx/data/jugadas_hoy.json";
const $ = id => document.getElementById(id);
let datos = null;

const estado = (t, cls = "") => { $("estado").textContent = t; $("estado").className = "est " + cls; };
const rd = n => "RD$" + Number(n).toLocaleString("es-DO");

chrome.storage.local.get(["url", "pausa"], v => {
  $("url").value = v.url || URL_DEF;
  if (v.pausa) $("pausa").value = v.pausa;
});

async function pestana() {
  const [t] = await chrome.tabs.query({ active: true, currentWindow: true });
  return t;
}

$("cargar").onclick = async () => {
  const url = $("url").value.trim();
  chrome.storage.local.set({ url });
  estado("Bajando…");
  try {
    // cache:no-store — si no, Chrome sirve el archivo de ayer.
    const r = await fetch(url, { cache: "no-store" });
    if (!r.ok) throw new Error("HTTP " + r.status);
    datos = await r.json();
  } catch (e) {
    datos = null; $("llenar").disabled = true;
    return estado("No pude bajar el archivo.\n" + e.message +
      "\n\nRevisa la URL, o que la rutina ya haya generado las jugadas de hoy.", "err");
  }
  const d = datos;
  $("resumen").innerHTML = [
    ["Juego", d.juego_nombre], ["Para el sorteo", d.para_sorteo],
    ["Jugadas", d.cantidad], ["Presupuesto", rd(d.presupuesto)],
    ["Modo", d.modo], ["Retorno esperado", d.retorno_esperado_pct + "%"],
    ["Pérdida esperada", rd(d.perdida_esperada)],
  ].map(([k, v]) => `<div class="kv"><span>${k}</span><b>${v}</b></div>`).join("");
  $("n").value = d.cantidad; $("n").max = d.cantidad;
  $("llenar").disabled = false;
  const viejo = d.para_sorteo !== new Date().toISOString().slice(0, 10);
  estado(`${d.cantidad} jugadas listas.` +
    (viejo ? `\n\nOJO: son del ${d.para_sorteo}, no de hoy.` : ""), viejo ? "err" : "ok");
};

$("detectar").onclick = async () => {
  if (!datos) return estado("Carga las jugadas primero.", "err");
  const t = await pestana();
  if (!/leidsa\.com\/play\//.test(t.url || ""))
    return estado("Abre primero la página del juego:\n" + datos.url_juego, "err");
  chrome.tabs.sendMessage(t.id,
    { tipo: "detectar", lo: datos.rango[0], hi: datos.rango[1] }, r => {
      if (chrome.runtime.lastError || !r)
        return estado("La página no respondió. Recárgala y reintenta.", "err");
      const bien = r.bolas >= r.esperadas && r.btnAgregar;
      estado(
        `Bolas encontradas: ${r.bolas} de ${r.esperadas}\n` +
        `Botón agregar: ${r.btnAgregar || "NO ENCONTRADO"}\n` +
        `Botón jugar: ${r.btnJugar || "no visible"}`, bien ? "ok" : "err");
    });
};

chrome.runtime.onMessage.addListener(m => {
  if (m.tipo === "progreso") estado(`Llenando… ${m.hecha} de ${m.total}`);
});

$("llenar").onclick = async () => {
  if (!datos) return;
  const n = Math.min(+$("n").value || 0, datos.cantidad);
  if (n < 1) return estado("Pon cuántas jugadas quieres.", "err");
  const t = await pestana();
  if (!/leidsa\.com\/play\//.test(t.url || ""))
    return estado("Abre primero la página del juego:\n" + datos.url_juego, "err");
  const total = n * datos.costo_por_jugada;
  if (!confirm(`Llenar ${n} jugadas de ${datos.juego_nombre}.\n` +
               `Costo si luego confirmas: ${rd(total)}\n\n` +
               `La extensión NO compra — solo llena. ¿Seguir?`)) return;

  const pausa = Math.max(40, +$("pausa").value || 140);
  chrome.storage.local.set({ pausa });
  $("llenar").disabled = true;
  estado("Llenando…");
  chrome.tabs.sendMessage(t.id, {
    tipo: "llenar",
    cfg: { jugadas: datos.jugadas.slice(0, n), lo: datos.rango[0],
           hi: datos.rango[1], pick: datos.numeros_por_jugada, pausa }
  }, r => {
    $("llenar").disabled = false;
    if (chrome.runtime.lastError || !r)
      return estado("Se perdió la conexión con la página.", "err");
    if (r.ok) estado(`Listas ${r.hechas.length} jugadas.\n\n` +
      `Revisa el total en pantalla y toca "jugar ahora" tú mismo.`, "ok");
    else estado(`Se detuvo en la jugada ${r.hechas.length + 1}.\n\n${r.error}\n\n` +
      `Las ${r.hechas.length} anteriores quedaron puestas.`, "err");
  });
};
