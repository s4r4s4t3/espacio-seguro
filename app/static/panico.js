document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("panicForm");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // loader opcional si está definido
    if (typeof showLoader === "function") showLoader();

    setTimeout(function () {
      if (typeof hideLoader === "function") hideLoader();
      if (typeof window.showToast === "function") {
        // Utilizamos la traducción disponible o una alternativa en inglés
        const msg = window.TRANSLATIONS && window.TRANSLATIONS.panic_alert_sent
          ? window.TRANSLATIONS.panic_alert_sent
          : "🚨 Alert sent to your trusted contacts!";
        window.showToast(msg);
      }
      // Reproducimos un breve tono usando la API Web Audio para reforzar la notificación.
      try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(880, ctx.currentTime);
        osc.connect(ctx.destination);
        osc.start();
        setTimeout(() => osc.stop(), 600);
      } catch (err) {
        // Si AudioContext no está soportado, ignoramos el error silenciosamente
      }
    }, 1200);
  });
});
