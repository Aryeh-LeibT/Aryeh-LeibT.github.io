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

// 3. Back-to-top button: create it here (so the HTML stays clean),
//    show it after the reader scrolls down, and scroll up when clicked.
const topButton = document.createElement("button");
topButton.type = "button";
topButton.className = "back-to-top";
topButton.textContent = "↑ Top";
topButton.setAttribute("aria-label", "Back to top");
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
