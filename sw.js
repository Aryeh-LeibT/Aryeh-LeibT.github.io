// sw.js: the "service worker", a small helper the browser runs in the
// background for this site. It is what makes the site work like an app:
//   - it saves the basic pages and files the first time you visit,
//   - it saves each essay or PDF you open, so it opens again with no internet,
//   - and when you are offline and ask for a page you never opened,
//     it shows /offline.html instead of the browser's error page.
//
// It must live at the root of the site (/sw.js) so it can look after every
// page under "/". js/site.js is what asks the browser to start it.
//
// HOW UPDATES WORK (please read before changing this file):
// GitHub Pages tells browsers to keep files for about 10 minutes, and we
// cannot change that. The reliable way to push an update to people who
// installed the app is to change VERSION below (for example to
// 'v2-20261020'). The browser notices sw.js changed, installs the new
// version, and the "activate" step deletes the old saved copies.
// Rule of thumb: change VERSION whenever you change the files in SHELL_FILES,
// or whenever you want everyone to get fresh copies right away.

const VERSION = "v12-20261018"; // v12: drop a removed writing page from caches

// Two "caches" (named boxes of saved files). The names include VERSION,
// so a new version gets fresh boxes and the old ones can be thrown away.
const SHELL_CACHE = "shell-" + VERSION;     // the basic files, saved at install
const RUNTIME_CACHE = "runtime-" + VERSION; // pages, essays and PDFs saved as you read

// How many pages/essays/PDFs to keep in the runtime box. When there are
// more than this, the oldest saved ones are removed first.
const RUNTIME_MAX_ENTRIES = 60;

// The "app shell": what we save straight away at install time.
const SHELL_FILES = [
  "/",
  "/writing/",
  "/offline.html",
  "/css/styles.css",
  "/js/site.js",
  "/manifest.webmanifest",
  "/favicon.png",
  "/images/favicon.png",
  "/images/aryeh.jpg", // the homepage photo (about 60 KB)
  "/icons/icon-192.png",
  "/icons/icon-512.png",
  "/icons/icon-maskable-512.png",
  "/icons/apple-touch-icon-180.png",
];

// ---------------------------------------------------------------------------
// 1. INSTALL: runs once per VERSION. Save the shell files.
// ---------------------------------------------------------------------------
self.addEventListener("install", function (event) {
  event.waitUntil(
    caches
      .open(SHELL_CACHE)
      .then(function (cache) {
        // cache: "reload" skips the browser's own short-term copy, so we
        // save what is really on the server right now.
        return cache.addAll(
          SHELL_FILES.map(function (url) {
            return new Request(url, { cache: "reload" });
          })
        );
      })
      // Take over straight away instead of waiting for every tab to close.
      .then(function () {
        return self.skipWaiting();
      })
  );
});

// ---------------------------------------------------------------------------
// 2. ACTIVATE: runs after install. Delete boxes from older versions,
//    then start looking after pages that are already open.
// ---------------------------------------------------------------------------
self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches
      .keys()
      .then(function (names) {
        return Promise.all(
          names
            .filter(function (name) {
              return name !== SHELL_CACHE && name !== RUNTIME_CACHE;
            })
            .map(function (name) {
              return caches.delete(name);
            })
        );
      })
      .then(function () {
        return self.clients.claim();
      })
  );
});

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

// Keep the runtime box small: remove the oldest entries beyond the limit.
// (Entries are listed in the order they were saved, oldest first.)
function trimCache(cacheName, maxEntries) {
  return caches.open(cacheName).then(function (cache) {
    return cache.keys().then(function (keys) {
      const extra = keys.length - maxEntries;
      if (extra <= 0) return;
      return Promise.all(
        keys.slice(0, extra).map(function (request) {
          return cache.delete(request);
        })
      );
    });
  });
}

// Only save complete, successful answers from our own site.
// (Status 200 only: not 404 pages, not partial "206" PDF pieces.)
function isSaveable(response) {
  return response && response.status === 200 && response.type === "basic";
}

// Save a copy of a response in a box (and trim the runtime box).
function saveCopy(cacheName, request, response) {
  if (!isSaveable(response)) return Promise.resolve();
  const copy = response.clone();
  return caches.open(cacheName).then(function (cache) {
    return cache.put(request, copy).then(function () {
      if (cacheName === RUNTIME_CACHE) {
        return trimCache(RUNTIME_CACHE, RUNTIME_MAX_ENTRIES);
      }
    });
  });
}

// The offline page, for when there is no network and nothing saved.
function offlinePage() {
  return caches.match("/offline.html");
}

// STRATEGY A: "network first" (used for ordinary pages).
// Try the internet. If it answers, show that and save a copy.
// If the internet fails, show the saved copy, or else offline.html.
function networkFirst(event) {
  const request = event.request;
  return fetch(request)
    .then(function (response) {
      event.waitUntil(saveCopy(RUNTIME_CACHE, request, response));
      return response;
    })
    .catch(function () {
      // ignoreSearch: "/?source=pwa" (the app's start page) matches "/".
      return caches.match(request, { ignoreSearch: true }).then(function (saved) {
        return saved || offlinePage();
      });
    });
}

// STRATEGY B: "stale while revalidate" (used for essays, PDFs, CSS and JS).
// If we have a saved copy, show it right away (fast, and works offline),
// and quietly fetch a fresh copy in the background for next time.
// If nothing is saved yet, wait for the internet.
function staleWhileRevalidate(event, cacheName) {
  const request = event.request;
  return caches.match(request).then(function (saved) {
    const fresh = fetch(request)
      .then(function (response) {
        return saveCopy(cacheName, request, response).then(function () {
          return response;
        });
      })
      .catch(function () {
        return null; // offline: we just keep the saved copy
      });

    if (saved) {
      // Let the background update finish even after we have answered.
      event.waitUntil(fresh);
      return saved;
    }
    return fresh.then(function (response) {
      if (response) return response;
      // Offline and never saved: for a page, show offline.html.
      if (request.mode === "navigate") return offlinePage();
      return Response.error();
    });
  });
}

// ---------------------------------------------------------------------------
// 3. FETCH: runs for every request a page makes. Decide what to do.
// ---------------------------------------------------------------------------
self.addEventListener("fetch", function (event) {
  const request = event.request;

  // Only plain "GET" requests (reading). Anything else goes straight through.
  if (request.method !== "GET") return;

  const url = new URL(request.url);

  // Other websites (Font Awesome on cdnjs, Substack, X...) are left alone:
  // the browser fetches them normally. That means Font Awesome icons may
  // not show while offline; the text labels still do. (Self-hosting the
  // icons is planned for phase 2.)
  if (url.origin !== self.location.origin) return;

  // Partial downloads ("Range" requests, used by some PDF viewers) are left
  // to the network; we only ever save whole files.
  if (request.headers.has("range")) return;

  const path = url.pathname;

  // PDFs anywhere on the site (e.g. /printables/... or /writing/...).
  if (path.toLowerCase().endsWith(".pdf")) {
    event.respondWith(staleWhileRevalidate(event, RUNTIME_CACHE));
    return;
  }

  // Essays: /writing/<something>.html
  if (path.startsWith("/writing/") && path.endsWith(".html")) {
    event.respondWith(staleWhileRevalidate(event, RUNTIME_CACHE));
    return;
  }

  // Every other page the reader opens (homepage, About, Torah...).
  if (request.mode === "navigate") {
    event.respondWith(networkFirst(event));
    return;
  }

  // Styles and scripts: show saved copy fast, refresh in the background.
  if (path.endsWith(".css") || path.endsWith(".js")) {
    event.respondWith(staleWhileRevalidate(event, SHELL_CACHE));
    return;
  }

  // Anything else (images, icons, the manifest): use a saved copy if we
  // have one, otherwise the network. Nothing new is saved here.
  event.respondWith(
    caches.match(request).then(function (saved) {
      return saved || fetch(request);
    })
  );
});
