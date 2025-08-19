// static/nueva_publicacion.js — vista previa robusta sin fugas
document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("image");
  const preview = document.getElementById("img-preview-np");
  const form = document.querySelector(".nueva-publicacion-form");

  if (!input || !preview) return;

  let lastObjectURL = null;

  function clearPreview() {
    if (lastObjectURL) {
      URL.revokeObjectURL(lastObjectURL);
      lastObjectURL = null;
    }
    preview.removeAttribute("src");
    preview.style.display = "none";
  }

  input.addEventListener("change", function () {
    const file = this.files && this.files[0];
    if (!file) {
      clearPreview();
      return;
    }
    // Revoca la URL anterior para evitar fugas de memoria
    if (lastObjectURL) URL.revokeObjectURL(lastObjectURL);

    const url = URL.createObjectURL(file);
    lastObjectURL = url;

    preview.onload = () => {
      // Revoca cuando la imagen ya fue cargada por el <img>
      URL.revokeObjectURL(url);
      // No seteamos lastObjectURL a null acá porque el usuario podría
      // querer limpiar después; la referencia viva es la de preview.src
    };
    preview.src = url;
    preview.style.display = "block";
  });

  // Limpieza al enviar (por si el back redirige rápido)
  if (form) {
    form.addEventListener("submit", () => {
      // No llamamos preventDefault aquí: el back procesa el POST.
      clearPreview();
    });
  }

  // Extra: permitir limpiar la imagen si el usuario borra manualmente el input
  // (por ejemplo, con un script externo que haga input.value = '')
  const observer = new MutationObserver(() => {
    if (!input.value) clearPreview();
  });
  observer.observe(input, { attributes: true, attributeFilter: ["value"] });
});
// Extra: limpiar al cambiar de página (por si el usuario navega rápido)
window.addEventListener("beforeunload", () => {
  if (lastObjectURL) {
    URL.revokeObjectURL(lastObjectURL);
    lastObjectURL = null;
  }
});
// También limpiar al cerrar la pestaña (para evitar fugas de memoria)
window.addEventListener("unload", () => {
  if (lastObjectURL) {
    URL.revokeObjectURL(lastObjectURL);
    lastObjectURL = null;
  }
});   