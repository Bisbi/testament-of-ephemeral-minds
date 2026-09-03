/* booklet.js — the motion of the one-page booklet, and nothing else.

   Three effects, all transform and opacity only: a leaf rises into place the
   first time it crosses the viewport, the cover tilts a few degrees under a
   mouse, and the curation chapter turns its stack of cards as the page scrolls
   through it. Under `prefers-reduced-motion: reduce` the file returns at once
   and every leaf stays plainly visible, which is also what happens when the
   script does not run at all: the hidden state is applied by the class this
   file adds, never by the stylesheet on its own. No library, no network. */

(function () {
  var root = document.documentElement;
  var mq = window.matchMedia;
  var WIDE = 940;

  if (mq && mq("(prefers-reduced-motion: reduce)").matches) {
    return;
  }
  root.classList.add("booklet-motion");

  /* --- a leaf enters once, when its top crosses 80 % of the viewport ------ */

  var leaves = document.querySelectorAll(".leaf");
  function showAll() {
    Array.prototype.forEach.call(leaves, function (leaf) {
      leaf.classList.add("is-in");
    });
  }
  if ("IntersectionObserver" in window) {
    var seen = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            seen.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -20% 0px" }
    );
    Array.prototype.forEach.call(leaves, function (leaf) {
      seen.observe(leaf);
    });
  } else {
    showAll();
  }

  /* --- the cover tilts under a mouse, never under a finger ---------------- */

  var cover = document.querySelector("[data-tilt]");
  if (cover && mq && mq("(hover: hover) and (pointer: fine)").matches) {
    cover.addEventListener("mousemove", function (event) {
      var box = cover.getBoundingClientRect();
      var dx = (event.clientX - box.left) / box.width - 0.5;
      var dy = (event.clientY - box.top) / box.height - 0.5;
      cover.style.setProperty("--tilt-y", (dx * 6).toFixed(2) + "deg");
      cover.style.setProperty("--tilt-x", (-dy * 6).toFixed(2) + "deg");
    });
    cover.addEventListener("mouseleave", function () {
      cover.style.setProperty("--tilt-y", "0deg");
      cover.style.setProperty("--tilt-x", "0deg");
    });
  }

  /* --- the curation deck: scroll position chooses the card in front ------- */

  var deck = document.querySelector("[data-deck]");
  var track = document.querySelector(".deck-track");
  if (deck && track) {
    var cards = deck.querySelectorAll(".deck-card");
    var current = -1;

    function place(index) {
      if (index === current) {
        return;
      }
      current = index;
      Array.prototype.forEach.call(cards, function (card, n) {
        var delta = n - index;
        var state = "now";
        if (delta < 0) {
          state = "past";
        } else if (delta > 3) {
          state = "far";
        } else if (delta > 0) {
          state = "next";
        }
        card.setAttribute("data-state", state);
        card.style.setProperty("--d", String(delta));
      });
    }

    function fromScroll() {
      if (window.innerWidth < WIDE) {
        return;
      }
      var box = track.getBoundingClientRect();
      var travel = box.height - window.innerHeight;
      if (travel <= 0) {
        return;
      }
      var done = Math.min(1, Math.max(0, -box.top / travel));
      place(Math.min(cards.length - 1, Math.floor(done * cards.length)));
    }

    Array.prototype.forEach.call(cards, function (card, n) {
      card.addEventListener("focus", function () {
        place(n);
      });
    });

    place(0);
    fromScroll();
    window.addEventListener("scroll", fromScroll, { passive: true });
    window.addEventListener("resize", fromScroll);
  }
})();
