document.addEventListener("DOMContentLoaded", function () {
  const inputNP = document.getElementById("image");
  const previewNP = document.getElementById("img-preview-np");

  if (inputNP && previewNP) {
    inputNP.addEventListener("change", function () {
      const file = this.files[0];
      previewNP.style.display = file ? "block" : "none";
      if (file) previewNP.src = URL.createObjectURL(file);
    });
  }
});
