// ---------------------------
// main.js
//
// Main JavaScript code for the static site.
// ---------------------------

(function () {
  "use strict";
  // ---------------------------
  // Tiny helpers
  // ---------------------------
  const qs = (sel, root = document) => root.querySelector(sel);
  const qsa = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const throttle = (fn, wait = 150) => {
    let last = 0, t;
    return (...args) => {
      const now = Date.now();
      if (now - last >= wait) {
        last = now; fn(...args);
      } else {
        clearTimeout(t);
        t = setTimeout(() => { last = Date.now(); fn(...args); }, wait - (now - last));
      }
    };
  };
  const prefersReduced = () =>
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ===========================
  // Fixed header: keep page offset in sync with real header height
  // ===========================  
  document.addEventListener("DOMContentLoaded", () => {
    const header = qs(".site-header");
    const setHeaderVar = () => {
      if (!header) return;
      const h = header.offsetHeight || 72; // fallback
      document.documentElement.style.setProperty("--header-h", `${h}px`);
    };
    setHeaderVar();
    window.addEventListener("resize", throttle(setHeaderVar, 150));
    if ("ResizeObserver" in window && header) {
      const ro = new ResizeObserver(setHeaderVar);
      ro.observe(header);
    }

    // ===========================
    // Tabs (with keyboard support)
    // ===========================
    qsa(".tabs").forEach((tablist) => {
      const tabs = qsa(".tab", tablist);
      const section = tablist.closest("section") || document;

      tablist.setAttribute("role", "tablist");

      const activate = (t) => {
        const pid = t.dataset.tab;
        const panel = pid ? section.querySelector(`#${pid}`) : null;

        tabs.forEach((x) => {
          x.classList.remove("active");
          x.setAttribute("aria-selected", "false");
          x.setAttribute("tabindex", "-1");
        });
        qsa(".panel", section).forEach((p) => p.classList.remove("active"));

        t.classList.add("active");
        t.setAttribute("aria-selected", "true");
        t.setAttribute("tabindex", "0");
        if (panel) panel.classList.add("active");
        t.focus();
      };

      tabs.forEach((tab) => {
        const panelId = tab.dataset.tab;
        const panel = panelId ? section.querySelector(`#${panelId}`) : null;

        tab.setAttribute("role", "tab");
        tab.setAttribute("tabindex", tab.classList.contains("active") ? "0" : "-1");
        tab.setAttribute("aria-selected", tab.classList.contains("active") ? "true" : "false");
        if (panel) {
          panel.setAttribute("role", "tabpanel");
          panel.setAttribute("aria-labelledby", tab.id || `tab-${panelId}`);
          if (!tab.classList.contains("active")) panel.classList.remove("active");
        }

        tab.addEventListener("click", () => activate(tab));
        tab.addEventListener("keydown", (e) => {
          const idx = tabs.indexOf(tab);
          if (e.key === "ArrowRight" || e.key === "ArrowDown") {
            e.preventDefault();
            activate(tabs[(idx + 1) % tabs.length]);
          } else if (e.key === "ArrowLeft" || e.key === "ArrowUp") {
            e.preventDefault();
            activate(tabs[(idx - 1 + tabs.length) % tabs.length]);
          } else if (e.key === "Home") {
            e.preventDefault();
            activate(tabs[0]);
          } else if (e.key === "End") {
            e.preventDefault();
            activate(tabs[tabs.length - 1]);
          } else if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            activate(tab);
          }
        });
      });
    });

    // ===========================
    // Awards Vertical Scroller
    // ===========================
    const initAwardsScroller = (scroller) => {
      const track = qs(".awards-track", scroller);
      if (!track) return;

      // duplicate once for infinite effect
      if (track.dataset._duplicated !== "1") {
        const items = qsa(":scope > li", track);
        if (items.length) {
          const frag = document.createDocumentFragment();
          items.forEach((li) => frag.appendChild(li.cloneNode(true)));
          track.appendChild(frag);
          track.dataset._duplicated = "1";
        }
      }

      const speed = Number(scroller.dataset.speed || 60); // px/sec

      const setDuration = () => {
        if (prefersReduced()) {
          track.style.animation = "none";
          return;
        }
        const total = track.scrollHeight;
        const distance = total / 2; // animates half (due to duplication)
        const duration = Math.max(12, distance / speed);
        track.style.animationDuration = `${duration.toFixed(2)}s`;
      };

      if ("IntersectionObserver" in window) {
        const io = new IntersectionObserver((entries) => {
          entries.forEach((ent) => {
            track.style.animationPlayState = ent.isIntersecting ? "running" : "paused";
          });
        });
        io.observe(scroller);
      }

      if ("ResizeObserver" in window) {
        const ro = new ResizeObserver(setDuration);
        ro.observe(track);
      } else {
        window.addEventListener("resize", throttle(setDuration, 150));
      }

      window.addEventListener("load", setDuration);
      setDuration();
    };

    qsa(".awards-scroller").forEach(initAwardsScroller);
  });

})();