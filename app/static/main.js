// === main.js SafeSpace Pro 2025 ===
// Creado por Eze, modular, pro, y documentado

document.addEventListener('DOMContentLoaded', () => {
  // PWA install button and service worker registration
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/service-worker.js').then(function(reg) {
      console.log('Service Worker registrado', reg);
    }).catch(function(err) { console.error(err); });
  }
  let deferredPrompt;
  const installEl = document.getElementById('install-btn');
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    if (installEl) installEl.style.display = 'block';
    if (installEl) installEl.addEventListener('click', async () => {
      installEl.style.display = 'none';
      deferredPrompt.prompt();
      await deferredPrompt.userChoice;
      deferredPrompt = null;
    });
  });

  // ======= Toggle modo oscuro (único y funcional) =======
  const body = document.body;
  const toggleBtn = document.createElement('button');
  toggleBtn.id = 'darkModeToggle';
  toggleBtn.title = 'Cambiar modo claro/oscuro';
  toggleBtn.innerHTML = localStorage.getItem('darkMode') === 'on' ? '☀️' : '🌙';
  toggleBtn.style.position = 'fixed';
  toggleBtn.style.top = '22px';
  toggleBtn.style.right = '26px';
  toggleBtn.style.zIndex = '1100';
  toggleBtn.style.background = 'rgba(34,34,34,0.08)';
  toggleBtn.style.border = 'none';
  toggleBtn.style.borderRadius = '50%';
  toggleBtn.style.fontSize = '2.1em';
  toggleBtn.style.cursor = 'pointer';
  toggleBtn.style.boxShadow = '0 2px 10px rgba(34,139,94,0.12)';
  document.body.appendChild(toggleBtn);

  // Estado inicial
  if (localStorage.getItem('darkMode') === 'on') body.classList.add('dark');

  toggleBtn.onclick = () => {
    body.classList.toggle('dark');
    localStorage.setItem('darkMode', body.classList.contains('dark') ? 'on' : 'off');
    toggleBtn.innerHTML = body.classList.contains('dark') ? '☀️' : '🌙';
  };

  // ======= Loader animado global =======
  window.showLoader = () => {
    if (document.getElementById('globalLoader')) return;
    const loader = document.createElement('div');
    loader.id = 'globalLoader';
    loader.innerHTML = `<div class="loader"></div>`;
    loader.style.position = 'fixed';
    loader.style.top = 0;
    loader.style.left = 0;
    loader.style.width = '100vw';
    loader.style.height = '100vh';
    loader.style.display = 'flex';
    loader.style.alignItems = 'center';
    loader.style.justifyContent = 'center';
    loader.style.background = 'rgba(0,0,0,0.21)';
    loader.style.zIndex = '9999';
    document.body.appendChild(loader);
  };
  window.hideLoader = () => {
    const loader = document.getElementById('globalLoader');
    if (loader) loader.remove();
  };

  // ======= Vista previa imagen genérica =======
  document.querySelectorAll('input[type="file"]').forEach(input => {
    input.addEventListener('change', function(e) {
      const file = this.files[0];
      if (!file) return;
      let preview = this.closest('form')?.querySelector('.preview-img') ||
                    document.querySelector(`img[data-preview="${this.id}"]`);
      if (preview) preview.src = URL.createObjectURL(file);
    });
  });

  // ======= Chat: burbujas estilo Messenger, scroll animado =======
  const chatBox = document.querySelector('.chat-global-box, .chat-private-box');
  if (chatBox) {
    setTimeout(() => {
      chatBox.scrollTop = chatBox.scrollHeight;
    }, 200);
    const observer = new MutationObserver(muts => {
      muts.forEach(m => {
        m.addedNodes.forEach(n => {
          if (n.classList && n.classList.contains('mensaje-global')) {
            n.classList.add('bubble-in');
            setTimeout(() => n.classList.remove('bubble-in'), 650);
            chatBox.scrollTop = chatBox.scrollHeight;
          }
        });
      });
    });
    observer.observe(chatBox, { childList: true });
  }

  // ======= Easter egg: motivacional (Ctrl+M) =======
  const frases = [
    "Hoy puede ser un gran día para comenzar de nuevo.",
    "Recuerda: aquí nunca estás solo/a. Cada paso, aunque pequeño, cuenta.",
    "Lo importante no es la meta, sino seguir caminando.",
    "Siempre hay alguien dispuesto a escucharte aquí.",
    "Tus emociones importan. Tu historia vale.",
    "Un día a la vez. Vos podés."
  ];
  window.addEventListener('keydown', e => {
    if (e.ctrlKey && e.key.toLowerCase() === 'm') {
      const idx = Math.floor(Math.random() * frases.length);
      showToast(frases[idx]);
    }
  });

  // ======= Toast motivacional =======
  window.showToast = (text) => {
    let toast = document.getElementById('motivationalToast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'motivationalToast';
      toast.style.position = 'fixed';
      toast.style.bottom = '44px';
      toast.style.left = '50%';
      toast.style.transform = 'translateX(-50%)';
      toast.style.background = 'rgba(33,145,80,0.94)';
      toast.style.color = '#fff';
      toast.style.padding = '17px 34px';
      toast.style.borderRadius = '15px';
      toast.style.boxShadow = '0 2px 16px rgba(50,130,90,0.18)';
      toast.style.fontSize = '1.13em';
      toast.style.zIndex = '10001';
      toast.style.opacity = 0;
      toast.style.transition = 'opacity 0.36s';
      document.body.appendChild(toast);
    }
    toast.textContent = text;
    toast.style.opacity = 1;
    setTimeout(() => { toast.style.opacity = 0; }, 3200);
  };

  // ======= Shift+M motivacional clásico con alert() + loader =======
  document.addEventListener('keydown', (e) => {
    if (e.shiftKey && e.key.toLowerCase() === 'm') {
      const frases = [
        "¡No estás solo/a! Siempre se puede empezar de nuevo.",
        "Cada pequeño paso cuenta.",
        "Aquí siempre hay alguien para escucharte.",
        "Hoy puede ser un gran día para ti. 🌟",
        "Tu historia importa. Tu valor es infinito."
      ];
      const msg = frases[Math.floor(Math.random() * frases.length)];
      showLoader();
      setTimeout(() => {
        hideLoader();
        alert(msg);
      }, 600);
    }
  });

  // ======= Micro-animación burbuja chat (Messenger style) =======
  document.querySelectorAll('.mensaje-global, .mensaje, .bubble').forEach(el => {
    el.style.animation = 'bubblein 0.35s cubic-bezier(.34,1.56,.64,1)';
  });

  // ======= Selector de idioma: redirige a la ruta /set_language/<lang> cuando cambia =======
  const langSelects = document.querySelectorAll('#language-select');
  langSelects.forEach(sel => {
    sel.addEventListener('change', function() {
      const lang = this.value;
      // Redirigimos al endpoint que guarda la cookie y recarga la página
      window.location.href = `/set_language/${lang}`;
    });
  });

  // ======= Vista de imágenes de publicaciones a pantalla completa =======
  const postImages = document.querySelectorAll('.post-image');
  const modal = document.getElementById('imgModal');
  const modalImg = document.getElementById('imgModalContent');
  const modalCloseBtn = document.getElementById('imgModalClose');
  if (postImages.length && modal && modalImg && modalCloseBtn) {
    postImages.forEach(img => {
      img.style.cursor = 'pointer';
      img.addEventListener('click', () => {
        modal.style.display = 'block';
        modalImg.src = img.src;
      });
    });
    modalCloseBtn.addEventListener('click', () => {
      modal.style.display = 'none';
    });
    // Cerrar modal al hacer clic fuera de la imagen
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.style.display = 'none';
      }
    });
  }

});
