/* perf.js — Lazy images, skeleton toggles, install prompt */
document.addEventListener('DOMContentLoaded', () => {
  // Lazy-load any image lacking loading attr
  const imgs = document.querySelectorAll('img:not([loading])');
  imgs.forEach(img => img.setAttribute('loading','lazy'));

  // IntersectionObserver to add 'is-visible' class for fade-in
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('is-visible');
          io.unobserve(e.target);
        }
      });
    }, { rootMargin: '120px 0px' });
    document.querySelectorAll('.skeleton, img').forEach(el => io.observe(el));
  }

  // PWA install: show button if available
  let deferredPrompt = null;
  const installBtn = document.getElementById('install-btn');
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    if (installBtn) installBtn.style.display = 'inline-flex';
  });
  if (installBtn) {
    installBtn.addEventListener('click', async () => {
      if (!deferredPrompt) return;
      deferredPrompt.prompt();
      await deferredPrompt.userChoice;
      deferredPrompt = null;
      installBtn.style.display = 'none';
    });
  }
});
