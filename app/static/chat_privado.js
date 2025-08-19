// static/chat_privado.js — DM/Chat Privado (mejorado, i18n-ready, robusto)
document.addEventListener("DOMContentLoaded", function () {
  // ---- i18n opcional (inyectá window.I18N desde los templates si querés) ----
  const T = (k, fb) => (window.I18N && window.I18N[k]) || fb || k;
  const TXT_EMPTY       = T("dm.emptyInput", "Debes escribir un mensaje o subir una imagen.");
  const TXT_SEND_FAIL   = T("dm.sendFail", "No se pudo enviar el mensaje. Intentá de nuevo.");
  const TXT_IMAGE_ALT   = T("dm.imageAlt", "Imagen");
  const TXT_PREVIEW_ALT = T("dm.previewAlt", "Vista previa de la imagen");

  // ---- refs DOM ----
  const mensajes     = document.querySelector(".chat-global-box"); // mismo contenedor que en el template
  const formulario   = document.getElementById("formularioPrivado");
  const inputMensaje = document.getElementById("mensajePrivado");
  const inputImagen  = document.getElementById("imagenPrivada");
  const preview      = document.getElementById("img-preview-priv");

  if (!mensajes || !formulario || !inputMensaje || !inputImagen) {
    // No estamos en la vista de chat privado → salir
    return;
  }
  if (typeof window.USER_ID === "undefined" || typeof window.FRIEND_ID === "undefined") {
    // Faltan IDs base (plantilla no los inyectó)
    return;
  }

  // ---- Socket.io ----
  let socket = null;
  try {
    if (typeof io === "function") {
      socket = io();
      socket.on("connect_error", () => {
        // opcional: manejo de error de conexión
      });
    }
  } catch (_) {}

  // ---- Preview de imagen (evitar fugas de memoria) ----
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

  // ---- Util: agregar burbuja al DOM ----
  function appendDM(data, isOwn) {
    const div = document.createElement("div");
    div.className = "mensaje bubble " + (isOwn ? "yo" : "otro");

    if (data.content) {
      const texto = document.createElement("div");
      texto.className = "chat-text";
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

    mensajes.appendChild(div);
    mensajes.scrollTop = mensajes.scrollHeight;

    const placeholder = document.querySelector(".placeholder-msg");
    if (placeholder) placeholder.remove();

    // animación opcional si definís .bubble-in en tu CSS
    div.classList.add("bubble-in");
    setTimeout(() => div.classList.remove("bubble-in"), 650);
  }

  // ---- Submit del formulario ----
  let sending = false;
  formulario.addEventListener("submit", async function (e) {
    e.preventDefault();
    if (sending) return;

    const mensaje = (inputMensaje.value || "").trim();
    const imagen  = inputImagen.files && inputImagen.files[0];

    if (!mensaje && !imagen) {
<<<<<<< HEAD
      // Utilizamos una cadena localizada si está disponible
      const msg = window.TRANSLATIONS && window.TRANSLATIONS.chat_no_content
        ? window.TRANSLATIONS.chat_no_content
        : "You must write a message or upload an image.";
      alert(msg);
=======
      alert(TXT_EMPTY);
>>>>>>> 6530948 (feat: i18n + PWA offline; SW v1.0.1, manifest EN y base dinámica; JS chat/toggles/previews/dark-mode)
      return;
    }

    const formData = new FormData();
    formData.append("content", mensaje);
    if (imagen) formData.append("image", imagen);
    formData.append("receiver_id", String(window.FRIEND_ID));

    const submitBtn = formulario.querySelector('button[type="submit"]');
    sending = true;
    if (submitBtn) { submitBtn.disabled = true; submitBtn.classList.add("is-sending"); }

    try {
      const response = await fetch("/send_message_privado", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) throw new Error("HTTP " + response.status);
      const result = await response.json().catch(() => ({}));

      // Emitir a través del socket si existe
      if (socket) socket.emit("mensaje_privado", result);

      // Feedback inmediato local
      appendDM(result, true);

      // Reset
      inputMensaje.value = "";
      inputImagen.value = "";
      if (lastObjectURL) URL.revokeObjectURL(lastObjectURL);
      lastObjectURL = null;
      preview.style.display = "none";
      preview.removeAttribute("src");
    } catch (err) {
      alert(TXT_SEND_FAIL);
    } finally {
      sending = false;
      if (submitBtn) { submitBtn.disabled = false; submitBtn.classList.remove("is-sending"); }
    }
  });

  // ---- Recepción de mensajes privados ----
  if (socket) {
    socket.on("mensaje_privado", function (data) {
      // Mostrar SOLO si pertenece a esta conversación (USER_ID <-> FRIEND_ID)
      const me   = String(window.USER_ID);
      const peer = String(window.FRIEND_ID);
      const sender   = String(data.sender_id);
      const receiver = String(data.receiver_id);

      const isCurrentThread =
        (sender === me && receiver === peer) ||
        (sender === peer && receiver === me);

      if (!isCurrentThread) return;

      const isOwn = sender === me;
      appendDM(data, isOwn);
    });
  }
});
