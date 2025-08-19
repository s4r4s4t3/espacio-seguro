// static/profile.js — vista previa de foto de perfil (robusta, sin fugas)
document.addEventListener("DOMContentLoaded", function () {
  const fileInput  = document.getElementById("profile_picture");
  const previewImg = document.getElementById("profileImage");
  const form       = document.querySelector(".profile-form");
  if (!fileInput || !previewImg) return;

  let lastObjectURL = null;

  function clearPreview() {
    if (lastObjectURL) {
      URL.revokeObjectURL(lastObjectURL);
      lastObjectURL = null;
    }
    // No quitamos el src actual: el servidor decidirá el valor final tras el POST.
  }

  fileInput.addEventListener("change", function (event) {
    const file = event.target.files && event.target.files[0];
    if (!file) {
      clearPreview();
      return;
    }
    // Solo previsualizar imágenes
    if (file.type && !file.type.startsWith("image/")) {
      clearPreview();
      return;
    }
    if (lastObjectURL) URL.revokeObjectURL(lastObjectURL);

    const url = URL.createObjectURL(file);
    lastObjectURL = url;

    previewImg.onload = () => {
      // Revoca cuando el <img> ya usó la URL
      URL.revokeObjectURL(url);
    };
    previewImg.src = url;
  });

  // Limpieza defensiva al enviar el formulario
  if (form) {
    form.addEventListener("submit", () => {
      clearPreview();
    });
  }
});
