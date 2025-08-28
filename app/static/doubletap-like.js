/* doubletap-like.js */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.feed-card img').forEach(img => {
    let lastTap = 0;
    img.addEventListener('click', () => {
      const now = Date.now();
      if (now - lastTap < 300) {
        // Double tap detected
        const likeBtn = img.closest('.feed-card').querySelector('.like-btn');
        if (likeBtn) likeBtn.click();
        img.classList.add('liked');
        setTimeout(()=>img.classList.remove('liked'), 600);
      }
      lastTap = now;
    });
  });
});
