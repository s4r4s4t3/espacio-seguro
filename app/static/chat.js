// static/chat.js — Chat Global (mejorado, i18n-ready, robusto)
document.addEventListener("DOMContentLoaded", function () {
  // ---- util i18n opcional (inyectá window.I18N desde los templates si querés) ----
  const T = (k, fb) => (window.I18N && window.I18N[k]) || fb || k;
  const TXT_EMPTY       = T("chat.emptyInput", "Debes escribir un mensaje o subir una imagen.");
  const TXT_NOW         = T("chat.now", "ahora");
  const TXT_SEND_FAIL   = T("chat.sendFail", "No se pudo enviar el mensaje. Intentá de nuevo.");
  const TXT_PREVIEW_ALT = T("chat.previewAlt", "Vista previa de la imagen");
  const TXT_IMAGE_ALT   = T("chat.imageAlt", "Imagen");

  // ---- refs DOM ----
  const mensajes    = document.getElementById("mensajes");
  const formulario  = document.getElementById("formulario");
  const inputMensaje= document.getElementById("mensaje");
  const inputImagen = document.getElementById("imagen");
  const preview     = document.getElementById("img-preview");

  if (!mensajes || !formulario || !inputMensaje || !inputImagen) {
    // Si no estamos en la vista de chat, salir silenciosamente
    return;
  }

  // ---- Socket.io ----
  let socket = null;
  try {
    if (typeof io === "function") {
      socket = io();
      // Opcional: manejo de errores de conexión
      socket.on("connect_error", () => {
        // console.warn("Socket.IO no pudo conectar");
      });
    }
  } catch (_) {}

  // ---- Vista previa de imagen (evita fugas de memoria) ----
  let lastObjectURL = null;
  inputImagen.addEventListener("change", function () {
    const file = this.files && this.files[0];
    if (file) {
      if (lastObjectURL) URL.revokeObjectURL(lastObjectURL);
      lastObjectURL = URL.createObjectURL(file);
      preview.src = lastObjectURL;
      preview.alt = TXT_PREVIEW_ALT;
      preview.style.display = "inline-block";
    } else {
      if (lastObjectURL) URL.revokeObjectURL(lastObjectURL);
      lastObjectURL = null;
      preview.style.display = "none";
      preview.removeAttribute("src");
    }
  });

<<<<<<< HEAD
  formulario.addEventListener("submit", async function (e) {
    e.preventDefault();
    const mensaje = inputMensaje.value.trim();
    const imagen = inputImagen.files[0];

    if (!mensaje && !imagen) {
      // Utilizamos una cadena localizada si está disponible
      const msg = window.TRANSLATIONS && window.TRANSLATIONS.chat_no_content
        ? window.TRANSLATIONS.chat_no_content
        : "You must write a message or upload an image.";
      alert(msg);
      return;
    }

    const formData = new FormData();
    formData.append("content", mensaje);
    if (imagen) {
      formData.append("image", imagen);
    }

    const response = await fetch("/send_message_global", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    socket.emit("mensaje", result);

    inputMensaje.value = "";
    inputImagen.value = "";
    preview.style.display = "none";
  });

  socket.on("mensaje", function (data) {
=======
  // ---- Crear burbuja de mensaje en el DOM ----
  function appendMessageBubble(data, isOwn) {
>>>>>>> 6530948 (feat: i18n + PWA offline; SW v1.0.1, manifest EN y base dinámica; JS chat/toggles/previews/dark-mode)
    const div = document.createElement("div");
    div.className = "mensaje-global bubble " + (isOwn ? "yo" : "otro");

    if (data.content) {
      const texto = document.createElement("div");
      texto.className = "chat-global-text";
      texto.textContent = data.content; // textContent evita XSS
      div.appendChild(texto);
    }

    if (data.image_url) {
      const img = document.createElement("img");
      img.src = data.image_url;
      img.className = "chat-image";
      img.alt = TXT_IMAGE_ALT;
      div.appendChild(img);
    }

    const meta = document.createElement("div");
    meta.className = "mensaje-meta";
<<<<<<< HEAD
    // Mostramos la hora actual formateada según la configuración regional del navegador
    const nowStr = new Date().toLocaleString();
    meta.textContent = `👤 ${data.sender_username || data.sender_id} | 🕒 ${nowStr}`;
=======
    const userLabel = data.sender_username || data.sender_id || "?";
    meta.textContent = `👤 ${userLabel} | 🕒 ${TXT_NOW}`;
>>>>>>> 6530948 (feat: i18n + PWA offline; SW v1.0.1, manifest EN y base dinámica; JS chat/toggles/previews/dark-mode)
    div.appendChild(meta);

    mensajes.appendChild(div);
    mensajes.scrollTop = mensajes.scrollHeight;

    // Remover placeholder si existía
    const placeholder = document.querySelector(".placeholder-msg");
    if (placeholder) placeholder.remove();

    // Pequeña animación (si tu CSS define .bubble-in)
    div.classList.add("bubble-in");
    setTimeout(() => div.classList.remove("bubble-in"), 650);
  }

  // ---- Envío del formulario ----
  let sending = false;
  formulario.addEventListener("submit", async function (e) {
    e.preventDefault();
    if (sending) return;
    const mensaje = (inputMensaje.value || "").trim();
    const imagen  = inputImagen.files && inputImagen.files[0];

    if (!mensaje && !imagen) {
      alert(TXT_EMPTY);
      return;
    }

    const formData = new FormData();
    formData.append("content", mensaje);
    if (imagen) formData.append("image", imagen);

    // Evitar doble submit
    sending = true;
    const submitBtn = formulario.querySelector('button[type="submit"]');
    if (submitBtn) { submitBtn.disabled = true; submitBtn.classList.add("is-sending"); }

    try {
      const response = await fetch("/send_message_global", { method: "POST", body: formData });
      if (!response.ok) throw new Error("HTTP " + response.status);
      const result = await response.json().catch(() => ({}));

      // Emitir por socket si está disponible
      if (socket) {
        socket.emit("mensaje", result);
      }

      // Añadir también localmente para feedback inmediato (por si el eco tarda)
      appendMessageBubble(result, true);

      // Reset de campos
      inputMensaje.value = "";
      inputImagen.value = "";
      if (lastObjectURL) URL.revokeObjectURL(lastObjectURL);
      lastObjectURL = null;
      preview.style.display = "none";
      preview.removeAttribute("src");
    } catch (err) {
      // console.error(err);
      alert(TXT_SEND_FAIL);
    } finally {
      sending = false;
      if (submitBtn) { submitBtn.disabled = false; submitBtn.classList.remove("is-sending"); }
    }
  });

  // ---- Recepción de mensajes (broadcast) ----
  if (socket) {
    socket.on("mensaje", function (data) {
      const isOwn = String(data.sender_id) === String(window.USER_ID);
      appendMessageBubble(data, isOwn);
    });
  }
});
