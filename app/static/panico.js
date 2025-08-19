// static/panico.js — envío robusto (POST real), anti-doble click e i18n opcional
document.addEventListener("DOMContentLoaded", function () {
  const T = (k, fb) => (window.I18N && window.I18N[k]) || fb || k;
  const TXT_SENT  = T("panic.sent", "🚨 ¡Alerta enviada a tus contactos de confianza!");
  const TXT_ERR   = T("panic.error", "No se pudo enviar la alerta. Intentá de nuevo.");

  const form = document.getElementById("panicForm");
  if (!form) return;

  const btn = form.querySelector(".panic-btn");
  let sending = false;

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    if (sending) return;
    sending = true;

    // UI: loader + deshabilitar botón
    if (typeof showLoader === "function") showLoader();
    if (btn) {
      btn.disabled = true;
      btn.classList.add("is-sending");
    }

    const url = form.getAttribute("action") || window.location.pathname || "/panico";
    const formData = new FormData(form);

    try {
      // POST real al backend (sin recargar la página)
      const res = await fetch(url, { method: "POST", body: formData });
      if (!res.ok) throw new Error("HTTP " + res.status);

      // Feedback
      if (typeof window.showToast === "function") {
<<<<<<< HEAD
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
=======
        window.showToast(TXT_SENT);
      }

      // (Opcional) sonido si existe /static/sounds/alert.mp3
      /*
      try {
        const audio = new Audio("/static/sounds/alert.mp3");
        audio.play().catch(() => {});
      } catch(_) {}
      */
    } catch (_) {
      // Si falla fetch, podríamos hacer submit tradicional para no perder la acción del servidor
      try {
        form.submit(); // fallback
        return; // la navegación se hará cargo
      } catch (err) {
        if (typeof window.showToast === "function") {
          window.showToast(TXT_ERR);
        } else {
          alert(TXT_ERR);
        }
      }
    } finally {
      if (typeof hideLoader === "function") hideLoader();
      if (btn) {
        btn.disabled = false;
        btn.classList.remove("is-sending");
      }
      sending = false;
    }
>>>>>>> 6530948 (feat: i18n + PWA offline; SW v1.0.1, manifest EN y base dinámica; JS chat/toggles/previews/dark-mode)
  });
});
// Fin del script panico.js
// Este script maneja el envío de alertas de pánico con feedback visual y manejo de errores.
// Se asegura de que no se envíen múltiples alertas por accidente y proporciona mensajes traducidos si están disponibles.
// También permite un sonido opcional al enviar la alerta, aunque está comentado por defecto. 