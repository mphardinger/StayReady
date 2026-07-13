/* Stay Ready service worker.
   Caches the app shell (HTML/CSS/JS/icons) so the app launches offline and is
   installable. API calls (/api/*) always go to the network — data is never
   served stale. Bump CACHE when shell assets change to force a refresh. */

const CACHE = 'stay-ready-v15';
const SHELL = [
  '/',
  '/css/styles.css',
  '/js/app.js',
  '/js/views/auth.js',
  '/js/views/dashboard.js',
  '/js/views/plan.js',
  '/js/views/recipes.js',
  '/js/views/pantry.js',
  '/js/views/shopping.js',
  '/js/views/balance.js',
  '/js/views/household.js',
  '/js/views/settings.js',
  '/manifest.json',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);

  // Never cache API or auth traffic — always hit the network for live data.
  if (url.pathname.startsWith('/api/')) return;

  // Navigations: network-first, fall back to the cached shell when offline.
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(() => caches.match('/'))
    );
    return;
  }

  // Static assets: cache-first, then network (and cache what we fetch).
  event.respondWith(
    caches.match(request).then((hit) => hit || fetch(request).then((resp) => {
      if (resp.ok && (url.origin === self.location.origin)) {
        const copy = resp.clone();
        caches.open(CACHE).then((c) => c.put(request, copy));
      }
      return resp;
    }).catch(() => hit))
  );
});
