// static/home.js — selector de idioma (normalizado, sin endpoint extra)
// Usa ?lang=<code> para que el servidor (after_request) setee la cookie.
// Códigos soportados: es, en, pt_PT, pt_BR, de, fr, it

document.addEventListener("DOMContentLoaded", function () {
  const select = document.getElementById("language-select");
  if (!select) return;

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
    const url = new URL(window.location.href);
    url.searchParams.set("lang", wanted);
    window.location.assign(url.toString());
  });
});
