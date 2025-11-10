/* /static/js/slider.js
   Fade Cross-dissolve Carousel with button-based dots
   - Autoplay delay from data-autoplay (ms)
   - Fade duration from data-transition (ms)
   - Accessible (ARIA), keyboard
   - Dots are numbered buttons (clear to users)
   - NO hover/focus pause; pauses only on user Pause, offscreen, or tab hidden
*/
(function(){
  "use strict";
  const $$ = (sel, root=document) => Array.from(root.querySelectorAll(sel));
  const $  = (sel, root=document) => root.querySelector(sel);
  const prefersReduced = () => matchMedia?.("(prefers-reduced-motion: reduce)")?.matches;

  $$(".banner-slider").forEach((root, idx) => {
    const slider = $(".slider", root);
    if (!slider) return;

    const SHOW_MS = Math.max(0, parseInt(slider.dataset.autoplay || "4000", 10) || 0);
    const FADE_MS = Math.max(150, parseInt(slider.dataset.transition || "700", 10) || 700);

    const slides = $$(".slide", slider);
    if (!slides.length) return;

    // Region & fade var
    const carouselId = root.id || `fade-carousel-${idx}`;
    root.id = carouselId;
    root.setAttribute("role", "region");
    root.setAttribute("aria-label", "Image carousel");
    root.setAttribute("aria-live", "off");
    slider.style.setProperty("--fade-dur", `${FADE_MS}ms`);

    // Give each slide an id so dots can aria-controls it
    slides.forEach((s, i) => { if (!s.id) s.id = `${carouselId}-slide-${i}`; });

    // Dots (buttons)
    const dotsWrap = $(".dots", root);
    const dots = [];
    if (dotsWrap && slides.length > 1){
      slides.forEach((_, i) => {
        const b = document.createElement("button");
        b.className = "dot";
        b.type = "button";
        b.textContent = String(i+1);                 // numbered for visibility
        b.setAttribute("role", "tab");
        b.setAttribute("aria-controls", slides[i].id);
        b.setAttribute("aria-label", `Go to slide ${i+1}`);
        dotsWrap.appendChild(b);
        dots.push(b);
      });
    }

    // Controls
    const btnPrev  = $(".prev", root);
    const btnNext  = $(".next", root);
    const btnPause = $(".pause", root);

    // State
    let index = 0;
    let pausedByButton = false;
    let offscreenPause = false;
    let timer = null;

    function effectivePaused(){ return pausedByButton || offscreenPause || prefersReduced(); }

    function setAria(i){
      slides.forEach((s, n) => {
        const active = n === i;
        s.classList.toggle("is-active", active);
        s.setAttribute("aria-hidden", active ? "false" : "true");
      });
      dots.forEach((d, n) => d.setAttribute("aria-current", String(n === i)));
    }

    function goTo(i){
      index = (i + slides.length) % slides.length;
      setAria(index);
    }

    function step(){ goTo(index + 1); }

    function stop(){ if (timer){ clearTimeout(timer); timer=null; } }
    function start(){
      stop();
      if (SHOW_MS > 0 && slides.length > 1 && !effectivePaused()){
        timer = setTimeout(function tick(){ step(); start(); }, SHOW_MS);
      }
    }

    // Init (decode first image to avoid flash)
    (async function init(){
      const firstImg = slides[0]?.querySelector("img");
      if (firstImg && !firstImg.complete) { try{ await firstImg.decode(); } catch{} }
      setAria(0);

      if (slides.length <= 1) {
        $(".slider-controls", root)?.style?.setProperty("display","none");
        dotsWrap?.style?.setProperty("display","none");
      }

      if (!prefersReduced()) start();
    })();

    // Events
    btnPrev?.addEventListener("click", () => goTo(index - 1), {passive:true});
    btnNext?.addEventListener("click", () => goTo(index + 1), {passive:true});

    if (btnPause){
      btnPause.addEventListener("click", () => {
        pausedByButton = !pausedByButton;
        btnPause.setAttribute("aria-pressed", String(pausedByButton));
        btnPause.textContent = pausedByButton ? "▶" : "❚❚";
        pausedByButton ? stop() : start();
      });
      btnPause.addEventListener("keydown", (e)=>{
        if (e.key === " " || e.key === "Enter") { e.preventDefault(); btnPause.click(); }
      });
    }

    // Dot clicks
    dots.forEach((d, n) => d.addEventListener("click", () => goTo(n), {passive:true}));

    // Keyboard arrows on focused carousel
    root.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft")  goTo(index - 1);
      if (e.key === "ArrowRight") goTo(index + 1);
    });

    // Offscreen pause
    if ("IntersectionObserver" in window){
      const io = new IntersectionObserver((entries) => {
        entries.forEach((ent) => {
          offscreenPause = !ent.isIntersecting;
          offscreenPause ? stop() : start();
        });
      }, { threshold: 0.05 });
      io.observe(slider);
    }

    // Tab visibility
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) stop(); else start();
    });

    // Resize: reassert active state
    addEventListener("resize", () => setAria(index), {passive:true});
  });
})();