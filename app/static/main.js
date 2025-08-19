// === main.js SafeSpace Pro 2025 (mejorado) ===
// - Registro de Service Worker con flujo de actualización (SKIP_WAITING + reload controlado)
// - Botón de instalación PWA (beforeinstallprompt)
// - Modo oscuro persistente (usa botón existente #darkModeToggle si ya está en el DOM; si no, crea uno fijo)
// - Loader global showLoader/hideLoader
// - Vista previa de imágenes (revoca ObjectURL para no fugar memoria)
// - Chat: autoscroll, animación de burbuja y observer para nuevos mensajes
// - Easter eggs motivacionales (Ctrl+M => toast / Shift+M => alert) con soporte opcional de i18n vía window.I18N

(function () {
  // ----- Utilidad i18n opcional -----
  const T = (k, fallback) => (window.I18N && window.I18N[k]) || fallback || k;

<<<<<<< HEAD
  // ======= Inicialización de tema oscuro/claro =======
  const body = document.body;
  // Aplica el modo oscuro si el valor almacenado es 'on'
  if (localStorage.getItem('darkMode') === 'on') {
    body.classList.add('dark');
  }
  /**
   * Aplica el modo oscuro de forma global.  Esta función se expone
   * mediante window.applyDarkMode para que pueda ser utilizada desde
   * cualquier plantilla (por ejemplo, la página de configuración).
   *
   * @param {boolean} state - Verdadero para activar el modo oscuro,
   *                          falso para desactivarlo.  Si se omite,
   *                          se invertirá el estado actual.
   */
  window.applyDarkMode = function(state) {
    let enable;
    if (typeof state === 'undefined') {
      enable = !body.classList.contains('dark');
    } else {
      enable = !!state;
    }
    if (enable) {
      body.classList.add('dark');
    } else {
      body.classList.remove('dark');
    }
    localStorage.setItem('darkMode', enable ? 'on' : 'off');
  };
=======
  document.addEventListener('DOMContentLoaded', () => {
    // ======= Service Worker: registro + actualización =======
    if ('serviceWorker' in navigator) {
      (async () => {
        try {
          const registration = await navigator.serviceWorker.register('/static/service-worker.js');
          // console.log('[SW] Registrado', registration);

          const handleWaiting = (reg) => {
            if (!reg || !reg.waiting) return;
            const waitingSW = reg.waiting;

            let refreshed = false;
            navigator.serviceWorker.addEventListener('controllerchange', () => {
              if (refreshed) return;
              refreshed = true;
              window.location.reload();
            }, { once: true });
>>>>>>> 6530948 (feat: i18n + PWA offline; SW v1.0.1, manifest EN y base dinámica; JS chat/toggles/previews/dark-mode)

            // Forzamos activación inmediata del SW nuevo
            waitingSW.postMessage({ type: 'SKIP_WAITING' });
          };

<<<<<<< HEAD
  // ======= Vista previa imagen genérica =======
  document.querySelectorAll('input[type="file"]').forEach(input => {
    input.addEventListener('change', function(e) {
      const file = this.files[0];
      // Si no hay archivo, ocultamos la vista previa y salimos
      if (!file) {
        const preview = this.closest('form')?.querySelector('.preview-img') ||
                        document.querySelector(`img[data-preview="${this.id}"]`);
        if (preview) preview.style.display = 'none';
        return;
      }
      let preview = this.closest('form')?.querySelector('.preview-img') ||
                    document.querySelector(`img[data-preview="${this.id}"]`);
      if (preview) {
        preview.src = URL.createObjectURL(file);
        preview.style.display = 'block';
      }
    });
  });
=======
          // Si ya hay uno esperando (después de una actualización)
          handleWaiting(registration);
>>>>>>> 6530948 (feat: i18n + PWA offline; SW v1.0.1, manifest EN y base dinámica; JS chat/toggles/previews/dark-mode)

          // Detecta nuevas instalaciones
          registration.addEventListener('updatefound', () => {
            const nw = registration.installing;
            if (!nw) return;
            nw.addEventListener('statechange', () => {
              if (nw.state === 'installed' && navigator.serviceWorker.controller) {
                handleWaiting(registration);
              }
            });
          });
        } catch (err) {
          // console.error('[SW] Error de registro:', err);
        }
      })();
    }

    // ======= PWA: botón de instalación =======
    let deferredPrompt = null;
    const installEl = document.getElementById('install-btn');

    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      deferredPrompt = e;
      if (installEl) {
        installEl.style.display = 'block';
        // Evitar listeners duplicados
        const onClick = async () => {
          installEl.style.display = 'none';
          if (deferredPrompt) {
            deferredPrompt.prompt();
            try { await deferredPrompt.userChoice; } finally { deferredPrompt = null; }
          }
        };
        installEl.removeEventListener('click', onClick); // por si el navegador dispara múltiples eventos
        installEl.addEventListener('click', onClick, { once: true });
      }
    });

    // ======= Toggle modo oscuro =======
    const THEME_KEY = 'safespace_theme'; // 'dark' | 'light'
    const root = document.documentElement;

    function applyTheme(theme) {
      if (theme === 'dark') {
        root.classList.add('dark');
      } else if (theme === 'light') {
        root.classList.remove('dark');
      } else {
        // auto (preferencias del sistema)
        window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
          ? root.classList.add('dark')
          : root.classList.remove('dark');
      }
    }

    function setToggleVisual(btn) {
      const isDark = root.classList.contains('dark');
      btn.innerHTML = isDark ? '☀️' : '🌙';
      btn.setAttribute('aria-pressed', isDark ? 'true' : 'false');
      btn.title = T('toggleDarkTitle', 'Cambiar modo claro/oscuro');
    }

    (function initDarkMode() {
      try {
        // Usar botón existente (#darkModeToggle) si lo pusiste en el HTML, si no, crear uno
        let toggleBtn = document.getElementById('darkModeToggle');
        const saved = localStorage.getItem(THEME_KEY);
        applyTheme(saved || 'auto');

        if (!toggleBtn) {
          toggleBtn = document.createElement('button');
          toggleBtn.id = 'darkModeToggle';
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
        }

        setToggleVisual(toggleBtn);
        toggleBtn.addEventListener('click', () => {
          const nowDark = !root.classList.contains('dark');
          applyTheme(nowDark ? 'dark' : 'light');
          localStorage.setItem(THEME_KEY, nowDark ? 'dark' : 'light');
          setToggleVisual(toggleBtn);
        });
      } catch (_) {}
    })();

    // ======= Loader global =======
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

    // ======= Vista previa imagen genérica (sin fugas de memoria) =======
    document.querySelectorAll('input[type="file"]').forEach(input => {
      input.addEventListener('change', function () {
        const file = this.files && this.files[0];
        if (!file) return;
        const form = this.closest('form');
        const preview = (form && form.querySelector('.preview-img')) ||
                        document.querySelector(`img[data-preview="${this.id}"]`);
        if (preview) {
          const url = URL.createObjectURL(file);
          preview.onload = () => URL.revokeObjectURL(url);
          preview.src = url;
          preview.style.display = '';
        }
      });
    });

<<<<<<< HEAD
  // ======= Easter egg: motivacional (Ctrl+M) =======
  // Selección de frases motivacionales según el idioma.  Tomamos la lengua desde
  // window.APP_LANG (inyectada en base.html) o, en su defecto, del atributo
  // lang del documento.  Si no coincide con una clave conocida, usamos español.
  const currentLang = (window.APP_LANG || document.documentElement.lang || 'es').toLowerCase();
  const frasesByLang = {
    es: [
      "Hoy puede ser un gran día para comenzar de nuevo.",
      "Recuerda: aquí nunca estás solo/a. Cada paso, aunque pequeño, cuenta.",
      "Lo importante no es la meta, sino seguir caminando.",
      "Siempre hay alguien dispuesto a escucharte aquí.",
      "Tus emociones importan. Tu historia vale.",
      "Un día a la vez. Vos podés."
    ],
    en: [
      "Today could be a great day to start over.",
      "Remember: you're never alone here. Every step, even small, counts.",
      "What matters is not the goal but to keep walking.",
      "There is always someone willing to listen to you here.",
      "Your emotions matter. Your story counts.",
      "One day at a time. You can do it."
    ],
    'pt_br': [
      "Hoje pode ser um grande dia para recomeçar.",
      "Lembre-se: aqui você nunca está sozinho(a). Cada passo, mesmo pequeno, conta.",
      "O importante não é o destino, mas continuar caminhando.",
      "Sempre há alguém disposto a ouvir você aqui.",
      "Suas emoções importam. Sua história vale.",
      "Um dia de cada vez. Você consegue."
    ],
    'pt-pt': [
      "Hoje pode ser um grande dia para recomeçar.",
      "Lembra-te: aqui nunca estás sozinho/a. Cada passo, mesmo pequeno, conta.",
      "O importante não é o destino, mas continuar a caminhar.",
      "Há sempre alguém disposto a ouvir-te aqui.",
      "As tuas emoções importam. A tua história vale.",
      "Um dia de cada vez. Tu consegues."
    ],
    de: [
      "Heute könnte ein großartiger Tag sein, um neu anzufangen.",
      "Denke daran: Du bist hier nie allein. Jeder Schritt, auch ein kleiner, zählt.",
      "Wichtig ist nicht das Ziel, sondern weiterzugehen.",
      "Hier gibt es immer jemanden, der dir zuhört.",
      "Deine Gefühle sind wichtig. Deine Geschichte zählt.",
      "Ein Tag nach dem anderen. Du schaffst das."
    ],
    fr: [
      "Aujourd'hui peut être un grand jour pour recommencer.",
      "Rappelle-toi : tu n'es jamais seul(e) ici. Chaque pas, même petit, compte.",
      "Ce qui compte, ce n'est pas la destination, mais de continuer à avancer.",
      "Il y a toujours quelqu'un prêt à t'écouter ici.",
      "Tes émotions comptent. Ton histoire a de la valeur.",
      "Un jour à la fois. Tu peux le faire."
    ],
    it: [
      "Oggi può essere un grande giorno per ricominciare.",
      "Ricorda: qui non sei mai solo/a. Ogni passo, anche piccolo, conta.",
      "Non importa la meta, ma continuare a camminare.",
      "C'è sempre qualcuno disposto ad ascoltarti qui.",
      "Le tue emozioni contano. La tua storia vale.",
      "Un giorno alla volta. Ce la puoi fare."
    ]
  };
  // Normalizamos claves para que coincidan con el objeto.  pt_br, pt-br, etc.
  let frasesArray = frasesByLang[currentLang];
  if (!frasesArray) {
    // Soportamos alias: pt_BR se normaliza a pt_br
    const normalized = currentLang.replace('-', '_');
    frasesArray = frasesByLang[normalized] || frasesByLang['es'];
  }
  window.addEventListener('keydown', e => {
    if (e.ctrlKey && e.key.toLowerCase() === 'm') {
      const idx = Math.floor(Math.random() * frasesArray.length);
      showToast(frasesArray[idx]);
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
  // Muestra mensajes de inspiración en una ventana alert().  Selecciona el
  // arreglo según el idioma actual, con alias igual que en las frases.
  const frasesShiftByLang = {
    es: [
      "¡No estás solo/a! Siempre se puede empezar de nuevo.",
      "Cada pequeño paso cuenta.",
      "Aquí siempre hay alguien para escucharte.",
      "Hoy puede ser un gran día para vos. 🌟",
      "Tu historia importa. Tu valor es infinito."
    ],
    en: [
      "You're not alone! You can always start again.",
      "Every little step counts.",
      "There is always someone here to listen to you.",
      "Today could be a great day for you. 🌟",
      "Your story matters. Your worth is infinite."
    ],
    'pt_br': [
      "Você não está sozinho(a)! Sempre é possível recomeçar.",
      "Cada pequeno passo conta.",
      "Sempre há alguém aqui para te ouvir.",
      "Hoje pode ser um grande dia para você. 🌟",
      "Sua história importa. Seu valor é infinito."
    ],
    'pt-pt': [
      "Não estás sozinho/a! É sempre possível recomeçar.",
      "Cada pequeno passo conta.",
      "Há sempre alguém aqui para te ouvir.",
      "Hoje pode ser um grande dia para ti. 🌟",
      "A tua história importa. O teu valor é infinito."
    ],
    de: [
      "Du bist nicht allein! Du kannst immer wieder neu beginnen.",
      "Jeder kleine Schritt zählt.",
      "Hier ist immer jemand, der dir zuhört.",
      "Heute könnte ein großartiger Tag für dich sein. 🌟",
      "Deine Geschichte ist wichtig. Dein Wert ist unendlich."
    ],
    fr: [
      "Tu n'es pas seul(e) ! On peut toujours recommencer.",
      "Chaque petit pas compte.",
      "Il y a toujours quelqu'un ici pour t'écouter.",
      "Aujourd'hui peut être un grand jour pour toi. 🌟",
      "Ton histoire compte. Ta valeur est infinie."
    ],
    it: [
      "Non sei solo/a! Si può sempre ricominciare.",
      "Ogni piccolo passo conta.",
      "C'è sempre qualcuno qui per ascoltarti.",
      "Oggi può essere un grande giorno per te. 🌟",
      "La tua storia conta. Il tuo valore è infinito."
    ]
  };
  document.addEventListener('keydown', (e) => {
    if (e.shiftKey && e.key.toLowerCase() === 'm') {
      let arr = frasesShiftByLang[currentLang];
      if (!arr) {
        const norm = currentLang.replace('-', '_');
        arr = frasesShiftByLang[norm] || frasesShiftByLang['es'];
      }
      const msg = arr[Math.floor(Math.random() * arr.length)];
      showLoader();
=======
    // ======= Chat: autoscroll + animación =======
    const chatBox = document.querySelector('.chat-global-box') || document.querySelector('.chat-private-box');
    if (chatBox) {
>>>>>>> 6530948 (feat: i18n + PWA offline; SW v1.0.1, manifest EN y base dinámica; JS chat/toggles/previews/dark-mode)
      setTimeout(() => {
        chatBox.scrollTop = chatBox.scrollHeight;
      }, 200);

      const observer = new MutationObserver(muts => {
        for (const m of muts) {
          m.addedNodes && m.addedNodes.forEach(n => {
            if (!(n instanceof HTMLElement)) return;
            if (n.classList.contains('mensaje-global') || n.classList.contains('mensaje') || n.classList.contains('bubble')) {
              n.classList.add('bubble-in');
              setTimeout(() => n.classList.remove('bubble-in'), 650);
              chatBox.scrollTop = chatBox.scrollHeight;
            }
          });
        }
      });
      observer.observe(chatBox, { childList: true });
    }

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
      requestAnimationFrame(() => {
        toast.style.opacity = 1;
        setTimeout(() => { toast.style.opacity = 0; }, 3200);
      });
    };

<<<<<<< HEAD
  // ======= Selector de idioma: redirige a la ruta /set_language/<lang> cuando cambia =======
  // Seleccionamos todos los elementos con la clase lang-select (incluye
  // el selector en la barra lateral y en la navegación inferior móvil)
  const langSelects = document.querySelectorAll('.lang-select');
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
=======
    // ======= Easter egg: Ctrl+M => toast / Shift+M => alert con loader =======
    const MOTIVATIONAL_TOAST = (window.I18N && window.I18N.MOTIVATIONAL_TOAST) || [
      'Hoy puede ser un gran día para comenzar de nuevo.',
      'Recuerda: aquí nunca estás solo/a. Cada paso, aunque pequeño, cuenta.',
      'Lo importante no es la meta, sino seguir caminando.',
      'Siempre hay alguien dispuesto a escucharte aquí.',
      'Tus emociones importan. Tu historia vale.',
      'Un día a la vez. Vos podés.'
    ];
    const MOTIVATIONAL_ALERT = (window.I18N && window.I18N.MOTIVATIONAL_ALERT) || [
      '¡No estás solo/a! Siempre se puede empezar de nuevo.',
      'Cada pequeño paso cuenta.',
      'Aquí siempre hay alguien para escucharte.',
      'Hoy puede ser un gran día para ti. 🌟',
      'Tu historia importa. Tu valor es infinito.'
    ];

    window.addEventListener('keydown', e => {
      if (e.ctrlKey && e.key.toLowerCase() === 'm') {
        const idx = Math.floor(Math.random() * MOTIVATIONAL_TOAST.length);
        window.showToast(MOTIVATIONAL_TOAST[idx]);
      } else if (e.shiftKey && e.key.toLowerCase() === 'm') {
        const idx = Math.floor(Math.random() * MOTIVATIONAL_ALERT.length);
        const msg = MOTIVATIONAL_ALERT[idx];
        window.showLoader();
        setTimeout(() => {
          window.hideLoader();
          // Evitá textos duros: si querés i18n total, inyectá window.I18N y reemplazá alert por UI propia
          alert(msg);
        }, 600);
      }
    });

    // ======= Micro-animación para burbujas ya presentes =======
    document.querySelectorAll('.mensaje-global, .mensaje, .bubble').forEach(el => {
      el.style.animation = 'bubblein 0.35s cubic-bezier(.34,1.56,.64,1)';
    });
  });
})();
// === main.js SafeSpace Pro 2025 (mejorado) ===
// - Registro de Service Worker con flujo de actualización (SKIP_WAITING + reload controlado)
// - Botón de instalación PWA (beforeinstallprompt)
// - Modo oscuro persistente (usa botón existente #darkModeToggle si ya está en el DOM; si no, crea uno fijo)
// - Loader global showLoader/hideLoader
// - Vista previa de imágenes (revoca ObjectURL para no fugar memoria)
// - Chat: autoscroll, animación de burbuja y observer para nuevos mensajes
// - Easter eggs motivacionales (Ctrl+M => toast / Shift+M => alert)
// - Soporte opcional de i18n vía window.I18N 
>>>>>>> 6530948 (feat: i18n + PWA offline; SW v1.0.1, manifest EN y base dinámica; JS chat/toggles/previews/dark-mode)
