// Nombre y versiones del caché.  Actualiza el sufijo cuando cambies archivos en producción
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
});
