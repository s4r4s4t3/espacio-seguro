// static/landing.js — selector de idioma (compatible con tu setup Babel)
// Normaliza códigos y navega con ?lang=<code> (el servidor setea la cookie)

document.addEventListener("DOMContentLoaded", function () {
  const select = document.getElementById("language-select");
  if (!select) return;

  // Normaliza a los códigos que configuramos en Babel:
  // es, en, pt_PT, pt_BR, de, fr, it
  function normalize(code) {
    if (!code) return "es";
    const c = String(code).replace("-", "_");
    const map = {
      pt: "pt_PT",
      br: "pt_BR",
      es_ES: "es",
      en_US: "en",
      en_GB: "en",
    };
    return map[c] || c;
  }

  select.addEventListener("change", function () {
    const wanted = normalize(this.value);

    // Navegamos a la misma URL agregando ?lang=wanted
    // (tu after_request en __init__.py setea la cookie automáticamente)
    const url = new URL(window.location.href);
    url.searchParams.set("lang", wanted);
    window.location.assign(url.toString());
  });
});
