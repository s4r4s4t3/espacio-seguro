document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("panicForm");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // loader opcional si está definido
    if (typeof showLoader === "function") showLoader();

    setTimeout(function () {
      if (typeof hideLoader === "function") hideLoader();
      if (typeof window.showToast === "function") {
        window.showToast("🚨 ¡Alerta enviada a tus contactos de confianza!");
      }

      // Opcional: sonido si tenés alert.mp3 en /static/sounds/
      /*
      const audio = new Audio("/static/sounds/alert.mp3");
      audio.play();
      */
    }, 1200);
  });
});
