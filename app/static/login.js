document.addEventListener("DOMContentLoaded", function () {
  const toggleLoginPassword = document.getElementById("toggleLoginPassword");
  const loginPassword = document.getElementById("loginPassword");

  if (toggleLoginPassword) {
    toggleLoginPassword.addEventListener("change", function () {
      loginPassword.type = this.checked ? "text" : "password";
    });
  }
});
