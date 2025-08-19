// static/register.js — toggle de contraseña accesible y robusto
document.addEventListener("DOMContentLoaded", function () {
  const checkbox = document.getElementById("toggleRegisterPassword");
  const input = document.getElementById("registerPassword");
  if (!checkbox || !input) return;

  // Accesibilidad inicial
  checkbox.setAttribute("aria-controls", "registerPassword");
  checkbox.setAttribute("aria-pressed", input.type === "text" ? "true" : "false");

  checkbox.addEventListener("change", function () {
    const show = this.checked;
    input.setAttribute("type", show ? "text" : "password");
    checkbox.setAttribute("aria-pressed", show ? "true" : "false");
    // Mantener foco en el campo
    try { input.focus({ preventScroll: true }); } catch (_) { input.focus(); }
  });
});
