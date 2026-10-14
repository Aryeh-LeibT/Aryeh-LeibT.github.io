// site.js: small helpers for every main page. No libraries needed.
// It is loaded with `defer`, so it runs after the HTML has been read.

// 1. Footer year: put the current year inside <span id="year"></span>,
//    so the copyright line never goes out of date.
const yearSpan = document.getElementById("year");
if (yearSpan) {
  yearSpan.textContent = new Date().getFullYear();
}

// 2. Current page in the nav: if no link already has aria-current,
//    find the link whose address matches this page and mark it.
//    Screen readers announce it as "current page", and the CSS makes it bold.
const navLinks = document.querySelectorAll(".nav nav a");
const alreadyMarked = document.querySelector('.nav nav a[aria-current]');
if (!alreadyMarked) {
  const here = location.pathname.replace(/index\.html$/, "");
  navLinks.forEach(function (link) {
    const target = new URL(link.href).pathname.replace(/index\.html$/, "");
    if (target === here) {
      link.setAttribute("aria-current", "page");
    }
  });
}

// Hebrew pages (<html lang="he">) get Hebrew labels on the buttons below.
const isHebrew = document.documentElement.lang === "he";

// 3. Back-to-top button: create it here (so the HTML stays clean),
//    show it after the reader scrolls down, and scroll up when clicked.
const topButton = document.createElement("button");
topButton.type = "button";
topButton.className = "back-to-top";
topButton.textContent = isHebrew ? "↑ למעלה" : "↑ Top";
topButton.setAttribute("aria-label", isHebrew ? "חזרה לראש העמוד" : "Back to top");
document.body.appendChild(topButton);

function updateTopButton() {
  // "is-visible" is a CSS class in styles.css that fades the button in.
  topButton.classList.toggle("is-visible", window.scrollY > 400);
}
window.addEventListener("scroll", updateTopButton, { passive: true });
updateTopButton();

topButton.addEventListener("click", function () {
  // Smooth scroll, unless the reader asked their system for less motion.
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" });
});

// ---------------------------------------------------------------------------
// 4. App support (PWA): the offline helper and the "Install app" button.
// ---------------------------------------------------------------------------

// 4a. Start the offline helper (sw.js). Browsers that don't support it
//     simply skip this, and the site works exactly as before.
//     We wait for "load" so it never slows down the first view of the page.
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker.register("/sw.js").catch(function (error) {
      // Not fatal: the site still works, just without offline reading.
      console.warn("Offline helper could not start:", error);
    });
  });
}

// Is the site already running as an installed app (no browser bar)?
// iPhone uses navigator.standalone; other browsers use the display-mode query.
const runningAsApp =
  window.matchMedia("(display-mode: standalone)").matches ||
  window.navigator.standalone === true;

// 4b. Android, Chrome and Edge: the browser fires "beforeinstallprompt"
//     when the site can be installed. We keep that event, and show our own
//     small "Install app" button. Clicking it opens the browser's install box.
let installEvent = null;
const installButton = document.createElement("button");
installButton.type = "button";
installButton.className = "install-app";
installButton.hidden = true; // hidden until the browser says we can install
installButton.innerHTML =
  '<i class="fa-solid fa-download" aria-hidden="true"></i>' + (isHebrew ? "התקנת האפליקציה" : "Install app");
document.body.appendChild(installButton);

window.addEventListener("beforeinstallprompt", function (event) {
  event.preventDefault(); // stop the browser's own mini-bar; we use our button
  installEvent = event;
  installButton.hidden = false;
});

installButton.addEventListener("click", function () {
  if (!installEvent) return;
  installEvent.prompt(); // the browser's real "Install?" box
  installEvent.userChoice.finally(function () {
    installEvent = null; // the event can only be used once
    installButton.hidden = true;
  });
});

window.addEventListener("appinstalled", function () {
  installButton.hidden = true;
});

// 4c. iPhone and iPad: Safari has no install event, so we show a small
//     one-time tip instead. "localStorage" is a little notebook the browser
//     keeps for this site; we write in it so the tip only appears once.
const TIP_KEY = "altIosInstallTipSeen";
const isIOS =
  /iPhone|iPad|iPod/.test(navigator.userAgent) ||
  // iPads on iPadOS 13+ say "Macintosh", but have a touch screen:
  (navigator.userAgent.includes("Macintosh") && navigator.maxTouchPoints > 1);

function tipAlreadySeen() {
  try {
    return localStorage.getItem(TIP_KEY) === "1";
  } catch (e) {
    return true; // storage blocked (private mode): don't nag
  }
}

function rememberTip() {
  try {
    localStorage.setItem(TIP_KEY, "1");
  } catch (e) {
    /* storage blocked: nothing to do */
  }
}

if (isIOS && !runningAsApp && !tipAlreadySeen()) {
  const tip = document.createElement("div");
  tip.className = "ios-install-tip";
  tip.setAttribute("role", "note");
  tip.innerHTML =
    "<p><strong>Install:</strong> tap Share " +
    '<i class="fa-solid fa-arrow-up-from-bracket" aria-hidden="true"></i>, ' +
    "then <strong>Add to Home Screen</strong>.</p>" +
    '<button type="button" class="ios-install-tip-close" aria-label="Dismiss install tip">×</button>';
  document.body.appendChild(tip);
  rememberTip(); // shown once: it won't come back on the next page

  // Fade in on the next frame (CSS skips the fade for "reduce motion").
  requestAnimationFrame(function () {
    tip.classList.add("is-visible");
  });

  tip.querySelector("button").addEventListener("click", function () {
    tip.remove();
  });
}
