document.addEventListener("DOMContentLoaded", function () {
  const toggleRegisterPassword = document.getElementById("toggleRegisterPassword");
  const registerPassword = document.getElementById("registerPassword");

  if (toggleRegisterPassword) {
    toggleRegisterPassword.addEventListener("change", function () {
      registerPassword.type = this.checked ? "text" : "password";
    });
  }
});
