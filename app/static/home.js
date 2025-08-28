document.addEventListener("DOMContentLoaded", function () {
  const langSelect = document.getElementById("language-select");
  const form = document.getElementById("language-form");

  langSelect.addEventListener("change", function () {
    const selected = this.value;
    form.action = `/set_language/${selected}`;
    form.submit();
  });
});
