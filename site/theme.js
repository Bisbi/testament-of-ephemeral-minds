/* theme.js — the three controls in the strip, and nothing else.

   Reads `toem-lang` and `toem-theme` from localStorage and writes `data-lang`
   and `data-theme` on <html> before the first paint, so the page never flashes
   the wrong language or the wrong palette. On DOMContentLoaded it wires the
   language buttons, the palette button and the copy button of the install
   block. Every storage access is guarded: a browser that refuses storage still
   renders the page and still switches, it just forgets between visits. No
   network, no cookie, no third party. */

(function () {
  var root = document.documentElement;
  var LANG_KEY = "toem-lang";
  var THEME_KEY = "toem-theme";

  function read(key) {
    try {
      return localStorage.getItem(key);
    } catch (e) {
      return null;
    }
  }

  function write(key, value) {
    try {
      localStorage.setItem(key, value);
    } catch (e) {
      /* private mode, blocked storage: the choice lasts for this page only */
    }
  }

  root.setAttribute("data-lang", read(LANG_KEY) === "it" ? "it" : "en");
  var savedTheme = read(THEME_KEY);
  if (savedTheme === "light" || savedTheme === "dark") {
    root.setAttribute("data-theme", savedTheme);
  }

  function currentTheme() {
    var set = root.getAttribute("data-theme");
    if (set) {
      return set;
    }
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches
      ? "light"
      : "dark";
  }

  function syncButtons() {
    var lang = root.getAttribute("data-lang");
    Array.prototype.forEach.call(document.querySelectorAll("[data-lang-btn]"), function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-lang-btn") === lang ? "true" : "false");
    });
    var t = document.querySelector("[data-theme-btn]");
    if (t) {
      t.setAttribute("aria-pressed", currentTheme() === "light" ? "true" : "false");
    }
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var area = document.createElement("textarea");
      area.value = text;
      area.setAttribute("readonly", "");
      area.style.position = "fixed";
      area.style.opacity = "0";
      document.body.appendChild(area);
      area.select();
      var done = false;
      try {
        done = document.execCommand("copy");
      } catch (e) {
        done = false;
      }
      document.body.removeChild(area);
      done ? resolve() : reject();
    });
  }

  function wire() {
    Array.prototype.forEach.call(document.querySelectorAll("[data-lang-btn]"), function (b) {
      b.addEventListener("click", function () {
        var next = b.getAttribute("data-lang-btn");
        root.setAttribute("data-lang", next);
        write(LANG_KEY, next);
        syncButtons();
      });
    });

    var themeBtn = document.querySelector("[data-theme-btn]");
    if (themeBtn) {
      themeBtn.addEventListener("click", function () {
        var next = currentTheme() === "dark" ? "light" : "dark";
        root.setAttribute("data-theme", next);
        write(THEME_KEY, next);
        syncButtons();
      });
    }

    Array.prototype.forEach.call(document.querySelectorAll("[data-copy]"), function (b) {
      b.addEventListener("click", function () {
        var target = document.getElementById(b.getAttribute("data-copy"));
        if (!target) {
          return;
        }
        copyText(target.textContent.trim()).then(
          function () {
            b.classList.add("is-done");
            window.setTimeout(function () {
              b.classList.remove("is-done");
            }, 1600);
          },
          function () {
            /* nothing to say: the commands are on screen and selectable */
          }
        );
      });
    });

    syncButtons();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wire);
  } else {
    wire();
  }
})();
