// static/login.js — toggle de contraseña accesible y robusto
document.addEventListener("DOMContentLoaded", function () {
  const checkbox = document.getElementById("toggleLoginPassword");
  const input = document.getElementById("loginPassword");
  if (!checkbox || !input) return;

  // Estado inicial de accesibilidad
  checkbox.setAttribute("aria-controls", "loginPassword");
  checkbox.setAttribute("aria-pressed", input.type === "text" ? "true" : "false");

  checkbox.addEventListener("change", function () {
    const show = this.checked;
    input.setAttribute("type", show ? "text" : "password");
    checkbox.setAttribute("aria-pressed", show ? "true" : "false");
    // Mantener foco en el campo al cambiar
    try { input.focus({ preventScroll: true }); } catch (_) { input.focus(); }
  });
});
// Asegurar que el campo de contraseña se actualice correctamente al cargar
document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("loginPassword");
  if (input) {
    input.setAttribute("type", "password"); // Asegurar que sea tipo password al cargar
  }
});
// Manejo de errores para evitar problemas de compatibilidad
window.addEventListener("error", function (event) {
  console.error("Error en login.js:", event.message);
  // Aquí podrías agregar lógica para manejar errores específicos si es necesario
}); 