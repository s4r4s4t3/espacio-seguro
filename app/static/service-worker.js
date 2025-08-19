<<<<<<< HEAD
// Nombre y versiones del caché.  Actualiza el sufijo cuando cambies archivos en producción
const OFFLINE_FALLBACK_URL = '/offline';
const CACHE_NAME = 'safespace-v1';
const urlsToCache = [
  '/',
  '/static/style.css',
  '/static/main.js',
  '/static/service-worker.js',
  '/static/icon-192x192-new.png',
  '/static/icon-512x512-new.png'
];

// Instalación: precacheamos algunos recursos clave para que la app funcione offline
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
      .catch((err) => console.error('Error caching initial files', err))
  );
  // Inmediatamente tomamos control
  self.skipWaiting();
});

// Activación: limpiamos cachés antiguos
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      );
    })
  );
  self.clients.claim();
});

// Interceptamos las peticiones: respondemos desde el caché si está disponible; de lo contrario hacemos fetch
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
=======
/* static/service-worker.js
 * SafeSpace — PWA offline support
 * Estrategias:
 * - Navegaciones (HTML): network-first con fallback a /offline (cache)
 * - Estáticos (css/js/img/font): cache-first con actualización en segundo plano
 */

const CACHE_VERSION = 'safespace-v1.0.1';
const STATIC_CACHE = `${CACHE_VERSION}-static`;
const RUNTIME_CACHE = `${CACHE_VERSION}-runtime`;
const OFFLINE_URL = '/offline';

/** Archivos a precachear */
const PRECACHE_ASSETS = [
  // Páginas
  OFFLINE_URL, // requiere ruta Flask que sirva templates/offline.html

  // Estáticos básicos
  '/static/style.css',
  '/static/main.js',
  '/static/home.js',
  '/static/landing.js',
  '/static/login.js',
  '/static/register.js',
  '/static/chat.js',
  '/static/chat_privado.js',
  '/static/panico.js',
  '/static/nueva_publicacion.js',
  '/static/profile.js',

  // PWA
  '/static/manifest.json',
  '/static/manifest.en.json', // 👈 agregado
  '/static/icon-192x192.png',
  '/static/icon-512x512.png',
  '/static/heart.png',
  '/static/icons/google.svg',
];

// -------------------- Install --------------------
self.addEventListener('install', event => {
  event.waitUntil((async () => {
    try {
      const cache = await caches.open(STATIC_CACHE);
      await Promise.all(
        PRECACHE_ASSETS.map(async (url) => {
          try {
            const req = new Request(url, { cache: 'no-cache' });
            const res = await fetch(req);
            if (res && res.ok) {
              await cache.put(url, res.clone());
            }
          } catch (_) {}
        })
      );
    } finally {
      await self.skipWaiting();
    }
  })());
});

// -------------------- Activate -------------------
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(
      keys.map(key => {
        if (!key.startsWith(CACHE_VERSION)) {
          return caches.delete(key);
        }
      })
    );

    if (self.registration.navigationPreload) {
      await self.registration.navigationPreload.enable();
    }

    await self.clients.claim();
  })());
});

// --------------- Utilidades de respuesta ----------
async function offlineResponse() {
  const cache = await caches.open(STATIC_CACHE);
  const cached = await cache.match(OFFLINE_URL);
  if (cached) return cached;
  return new Response(
    `
<!doctype html>
<html lang="es"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Offline - SafeSpace</title>
<body style="font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,'Helvetica Neue',Arial,sans-serif;padding:2rem;max-width:640px;margin:auto">
  <h2>Estás sin conexión</h2>
  <p>No pudimos conectarnos. Revisá tu conexión e intentá de nuevo.</p>
  <button onclick="location.reload()">Reintentar</button>
</body></html>
    `.trim(),
    { headers: { 'Content-Type': 'text/html; charset=UTF-8' }, status: 200 }
  );
}

async function cacheFirst(event) {
  const req = event.request;
  const cached = await caches.match(req);
  if (cached) {
    event.waitUntil((async () => {
      try {
        const res = await fetch(req, { cache: 'no-cache' });
        if (res && res.ok) {
          const runtime = await caches.open(RUNTIME_CACHE);
          await runtime.put(req, res.clone());
        }
      } catch (_) {}
    })());
    return cached;
  }
  try {
    const res = await fetch(req);
    if (res && res.ok) {
      const runtime = await caches.open(RUNTIME_CACHE);
      await runtime.put(req, res.clone());
    }
    return res;
  } catch (_) {
    return await offlineResponse();
  }
}

async function navigationNetworkFirst(event) {
  const preload = await event.preloadResponse;
  if (preload) return preload;

  try {
    const res = await fetch(event.request);
    const runtime = await caches.open(RUNTIME_CACHE);
    runtime.put(event.request, res.clone()).catch(() => {});
    return res;
  } catch (_) {
    return await offlineResponse();
  }
}

// -------------------- Fetch ----------------------
self.addEventListener('fetch', event => {
  const { request } = event;
  if (request.method !== 'GET') return;

  const dest = request.destination;

  // Navegaciones HTML → network-first con fallback offline
  if (request.mode === 'navigate' || dest === 'document') {
    event.respondWith(navigationNetworkFirst(event));
    return;
  }

  // Estáticos → cache-first
  if (dest === 'style' || dest === 'script' || dest === 'image' || dest === 'font' || dest === 'manifest') {
    event.respondWith(cacheFirst(event));
    return;
  }

  // Otros → red con fallback a cache u offline
  event.respondWith((async () => {
    try {
      return await fetch(request);
    } catch (_) {
      const cached = await caches.match(request);
      return cached || offlineResponse();
    }
  })());
>>>>>>> 6530948 (feat: i18n + PWA offline; SW v1.0.1, manifest EN y base dinámica; JS chat/toggles/previews/dark-mode)
});

// Mensajes desde la página (p. ej. forzar activación)
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
// -------------------- Push Notifications ----------------------
self.addEventListener('push', event => {  
  const data = event.data ? event.data.json() : {};
  const title = data.title || 'Notificación';
  const options = {
    body: data.body || 'Tienes una nueva notificación',
    icon: data.icon || '/static/icon-192x192.png',
    badge: data.badge || '/static/icon-192x192.png',
    vibrate: [200, 100, 200],
    data: data.url || '/',
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});
self.addEventListener('notificationclick', event => { 
  event.notification.close();
  event.waitUntil(
    clients.matchAll({ type: 'window' }).then(clientList => {
      for (const client of clientList) {
        if (client.url === event.notification.data && 'focus' in client) {
          return client.focus();
        }
      }
      return clients.openWindow(event.notification.data);
    })
  );
});
// -------------------- Background Sync ----------------------
self.addEventListener('sync', event => {
  if (event.tag === 'sync-posts') {
    event.waitUntil(
      (async () => {
        const cache = await caches.open(RUNTIME_CACHE);
        const posts = await cache.keys();
        for (const post of posts) {
          try {
            const response = await fetch(post);
            if (response.ok) {
              await cache.delete(post);
            }
          } catch (_) {}
        }
      })()
    );
  }
});
// -------------------- Periodic Sync ----------------------
self.addEventListener('periodicsync', event => {
  if (event.tag === 'sync-notifications') {
    event.waitUntil(
      (async () => {
        const cache = await caches.open(RUNTIME_CACHE);
        const notifications = await cache.keys();
        for (const notification of notifications) {
          try {
            const response = await fetch(notification);
            if (response.ok) {
              await cache.delete(notification);
            }
          } catch (_) {}
        }
      })()
    );
  }
} );
// -------------------- End of service worker ----------------------
