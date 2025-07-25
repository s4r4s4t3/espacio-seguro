document.addEventListener("DOMContentLoaded", function () {
  const fileInput = document.getElementById("profile_picture");
  const previewImg = document.getElementById("profileImage");

  fileInput.addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (file) {
      previewImg.src = URL.createObjectURL(file);
    }
  });
});
