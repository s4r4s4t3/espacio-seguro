document.addEventListener("DOMContentLoaded", function () {
  const socket = io();
  const mensajes = document.getElementById("mensajes");
  const formulario = document.getElementById("formulario");
  const inputMensaje = document.getElementById("mensaje");
  const inputImagen = document.getElementById("imagen");
  const preview = document.getElementById("img-preview");

  inputImagen.addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
      preview.src = URL.createObjectURL(file);
      preview.style.display = "inline-block";
    } else {
      preview.style.display = "none";
      preview.src = "";
    }
  });

  formulario.addEventListener("submit", async function (e) {
    e.preventDefault();
    const mensaje = inputMensaje.value.trim();
    const imagen = inputImagen.files[0];

    if (!mensaje && !imagen) {
      alert("Debes escribir un mensaje o subir una imagen.");
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
    const div = document.createElement("div");
    div.className = "mensaje-global bubble " + (data.sender_id == window.USER_ID ? "yo" : "otro");

    if (data.content) {
      const texto = document.createElement("div");
      texto.className = "chat-global-text";
      texto.textContent = data.content;
      div.appendChild(texto);
    }

    if (data.image_url) {
      const img = document.createElement("img");
      img.src = data.image_url;
      img.className = "chat-image";
      div.appendChild(img);
    }

    const meta = document.createElement("div");
    meta.className = "mensaje-meta";
    meta.textContent = `👤 ${data.sender_username || data.sender_id} | 🕒 ahora`;
    div.appendChild(meta);

    mensajes.appendChild(div);
    mensajes.scrollTop = mensajes.scrollHeight;

    const placeholder = document.querySelector(".placeholder-msg");
    if (placeholder) placeholder.remove();
  });
});
