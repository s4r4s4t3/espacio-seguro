// === main.js SafeSpace Pro 2025 ===
// Creado por Eze, modular, pro, y documentado

document.addEventListener('DOMContentLoaded', () => {
  // ======= Toggle modo oscuro =======
  const body = document.body;
  const toggleBtn = document.createElement('button');
  toggleBtn.id = 'darkModeToggle';
  toggleBtn.innerHTML = '🌙';
  toggleBtn.title = 'Cambiar modo claro/oscuro';
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

  // Aplica el modo preferido al cargar
  let darkMode = localStorage.getItem('darkMode');
  if (darkMode === 'on') body.classList.add('dark-mode');

  toggleBtn.onclick = () => {
    body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', body.classList.contains('dark-mode') ? 'on' : 'off');
  };

  // Cambia el ícono según modo
  const updateToggleIcon = () => {
    toggleBtn.innerHTML = body.classList.contains('dark-mode') ? '☀️' : '🌙';
  };
  updateToggleIcon();
  body.addEventListener('transitionend', updateToggleIcon);
  toggleBtn.addEventListener('click', updateToggleIcon);

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
      // Encuentra la img previa asociada (debe tener data-preview o class 'preview-img')
      let preview = this.closest('form')?.querySelector('.preview-img') ||
                    document.querySelector(`img[data-preview="${this.id}"]`);
      if (preview) preview.src = URL.createObjectURL(file);
    });
  });

  // ======= Chat: burbujas estilo Messenger, scroll animado =======
  const chatBox = document.querySelector('.chat-global-box, .chat-private-box');
  if (chatBox) {
    // Scroll automático suave al fondo
    setTimeout(() => {
      chatBox.scrollTop = chatBox.scrollHeight;
    }, 200);

    // Efecto de "bubble" a los mensajes nuevos (agregá clase 'bubble-in' en tu backend si querés)
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

});
// ===== SafeSpace main.js =====

// --- Loader Pro ---
function showLoader() {
  if (!document.getElementById('globalLoader')) {
    const loaderBg = document.createElement('div');
    loaderBg.id = 'globalLoader';
    loaderBg.style = `
      position:fixed;top:0;left:0;width:100vw;height:100vh;
      background:rgba(40,50,55,0.36);z-index:9999;display:flex;align-items:center;justify-content:center;
    `;
    loaderBg.innerHTML = `<div class="loader"></div>`;
    document.body.appendChild(loaderBg);
  }
}
function hideLoader() {
  const loader = document.getElementById('globalLoader');
  if (loader) loader.remove();
}

// --- Modo Oscuro Toggle ---
function setDarkMode(enable) {
  if (enable) {
    document.documentElement.classList.add('dark-mode');
    localStorage.setItem('darkMode', 'on');
  } else {
    document.documentElement.classList.remove('dark-mode');
    localStorage.setItem('darkMode', 'off');
  }
}
function toggleDarkMode() {
  setDarkMode(!document.documentElement.classList.contains('dark-mode'));
}
document.addEventListener('DOMContentLoaded', () => {
  // Toggle UI
  let toggle = document.getElementById('darkModeToggle');
  if (!toggle) {
    toggle = document.createElement('button');
    toggle.id = 'darkModeToggle';
    toggle.title = 'Modo claro/oscuro';
    toggle.innerHTML = '🌙';
    toggle.style = `
      position:fixed;top:18px;right:24px;z-index:10000;
      font-size:1.6em;padding:7px 14px;border:none;background:#fff;
      border-radius:7px;box-shadow:0 2px 12px rgba(34,139,94,0.13);
      color:#219150;cursor:pointer;transition:background 0.17s;
    `;
    document.body.appendChild(toggle);
  }
  // Estado inicial
  if (localStorage.getItem('darkMode') === 'on') setDarkMode(true);
  toggle.onclick = toggleDarkMode;
});

// --- Easter Egg: Frase motivacional con Shift+M ---
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

// --- Vista Previa de Imagen (perfil, nueva publicación, chat, etc) ---
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('input[type="file"]').forEach(input => {
    input.addEventListener('change', function(e) {
      const file = e.target.files[0];
      if (!file) return;
      // Buscar previsualización junto al input
      let preview = e.target.parentElement.querySelector('.preview-img');
      if (!preview) {
        preview = document.createElement('img');
        preview.className = 'preview-img';
        preview.style = 'margin-top:12px;max-width:140px;max-height:140px;display:block;border-radius:10px;box-shadow:0 2px 10px rgba(34,139,94,0.07);';
        e.target.parentElement.appendChild(preview);
      }
      preview.src = URL.createObjectURL(file);
    });
  });
});

// --- Micro-animación burbuja chat (Messenger style) ---
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.mensaje-global, .mensaje, .bubble').forEach(el => {
    el.style.animation = 'bubblein 0.35s cubic-bezier(.34,1.56,.64,1)';
  });
});
