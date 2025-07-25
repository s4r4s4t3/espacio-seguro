document.addEventListener("DOMContentLoaded", function () {
  const socket = io();
  const mensajes = document.querySelector(".chat-global-box");
  const formulario = document.getElementById("formularioPrivado");
  const inputMensaje = document.getElementById("mensajePrivado");
  const inputImagen = document.getElementById("imagenPrivada");
  const preview = document.getElementById("img-preview-priv");

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
    if (imagen) formData.append("image", imagen);
    formData.append("receiver_id", window.FRIEND_ID);

    const response = await fetch("/send_message_privado", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    socket.emit("mensaje_privado", result);

    inputMensaje.value = "";
    inputImagen.value = "";
    preview.style.display = "none";
    preview.src = "";
  });

  socket.on("mensaje_privado", function (data) {
    if (
      parseInt(data.receiver_id) === Number(window.USER_ID) ||
      parseInt(data.sender_id) === Number(window.USER_ID)
    ) {
      const div = document.createElement("div");
      div.className =
        "mensaje bubble " +
        (parseInt(data.sender_id) === Number(window.USER_ID) ? "yo" : "otro");

      if (data.content) {
        const texto = document.createElement("div");
        texto.className = "chat-text";
        texto.textContent = data.content;
        div.appendChild(texto);
      }

      if (data.image_url) {
        const img = document.createElement("img");
        img.src = data.image_url;
        img.className = "chat-image";
        div.appendChild(img);
      }

      mensajes.appendChild(div);
      mensajes.scrollTop = mensajes.scrollHeight;

      const placeholder = document.querySelector(".placeholder-msg");
      if (placeholder) placeholder.remove();
    }
  });
});
