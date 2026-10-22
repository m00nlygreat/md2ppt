(() => {
  "use strict";

  const revealRoot = document.getElementById("reveal");
  const slidesRoot = revealRoot?.querySelector(".slides");
  const status = document.getElementById("player-status");
  const speakerButton = document.getElementById("speaker-view");
  const fullscreenButton = document.getElementById("fullscreen");
  if (!revealRoot || !slidesRoot) return;

  const slides = Array.from(slidesRoot.querySelectorAll(":scope > section"));
  const receiverView = new URLSearchParams(window.location.search).has("receiver");
  if (receiverView) document.body.classList.add("notes-receiver");

  function stageDimension(name, fallback) {
    const value = getComputedStyle(revealRoot).getPropertyValue(name).trim();
    const match = value.match(/^(\d+(?:\.\d+)?|\.\d+)px$/i);
    const parsed = match ? Number(match[1]) : NaN;
    return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
  }

  function normalizeLocation() {
    const total = Math.max(1, slides.length);
    const hash = window.location.hash;
    const legacy = hash.match(/^#slide=(\d+)$/i);
    const current = hash.match(/^#\/?slide-(\d+)$/i);
    const number = legacy ? Number(legacy[1]) : current ? Number(current[1]) : 1;
    const safeNumber = Math.max(1, Math.min(total, Number.isFinite(number) ? number : 1));
    const canonicalHash = `#/slide-${safeNumber}`;

    if (hash !== canonicalHash) {
      const url = `${window.location.pathname}${window.location.search}${canonicalHash}`;
      window.history.replaceState(window.history.state, "", url);
    }
  }

  normalizeLocation();

  function isInteractiveTarget(target) {
    return target instanceof Element && Boolean(
      target.closest("a, button, input, textarea, select, [contenteditable='true'], [role='textbox']"),
    );
  }

  function keyboardAllowed(event) {
    return !isInteractiveTarget(event?.target) && !isInteractiveTarget(document.activeElement);
  }

  function slideOverflows(slide) {
    const frame = slide.querySelector(".slide-inner, .toc-content, .cover-content");
    if (frame && frame.scrollHeight > frame.clientHeight + 2) return true;
    const regions = slide.querySelectorAll(".placeholder, .table-scroll, pre.code, .toc-content nav");
    return Array.from(regions).some((region) =>
      region.scrollHeight > region.clientHeight + 2 || region.scrollWidth > region.clientWidth + 2,
    );
  }

  function fitSlide(slide) {
    if (!slide || !slide.isConnected || slide.getClientRects().length === 0) return;
    const warning = slide.querySelector(".overflow-warning");
    slide.style.setProperty("--fit-scale", "1");
    if (!slideOverflows(slide)) {
      warning?.classList.remove("visible");
      return;
    }

    let low = 0.25;
    let high = 1;
    slide.style.setProperty("--fit-scale", String(low));
    if (slideOverflows(slide)) {
      warning?.classList.add("visible");
      return;
    }

    for (let attempt = 0; attempt < 12; attempt += 1) {
      const middle = (low + high) / 2;
      slide.style.setProperty("--fit-scale", String(middle));
      if (slideOverflows(slide)) high = middle;
      else low = middle;
    }
    slide.style.setProperty("--fit-scale", String(low));
    warning?.classList.remove("visible");
  }

  let fitFrame = 0;
  function scheduleFit() {
    cancelAnimationFrame(fitFrame);
    fitFrame = requestAnimationFrame(() => {
      fitFrame = requestAnimationFrame(() => {
        fitSlide(window.Reveal?.getCurrentSlide());
      });
    });
  }

  function announceSlide(event) {
    const index = event?.indexh ?? window.Reveal.getIndices().h;
    if (status) status.textContent = `슬라이드 ${index + 1} / ${window.Reveal.getTotalSlides()}`;
    scheduleFit();
  }

  async function startPresentation() {
    if (!window.Reveal || !window.RevealNotes) {
      if (status) status.textContent = "Reveal.js 리소스를 불러오지 못했습니다. 서버 설치 파일을 확인하세요.";
      return;
    }

    const config = {
      width: stageDimension("--stage-width", 1280),
      height: stageDimension("--stage-height", 720),
      controls: true,
      controlsTutorial: false,
      progress: true,
      slideNumber: "c/t",
      hash: true,
      hashOneBasedIndex: true,
      transition: "none",
      backgroundTransition: "none",
      scrollActivationWidth: null,
      keyboardCondition: keyboardAllowed,
      plugins: [window.RevealNotes],
    };

    try {
      await window.Reveal.initialize(config);
      window.Reveal.on("ready", announceSlide);
      window.Reveal.on("slidechanged", announceSlide);
      window.Reveal.on("overviewhidden", scheduleFit);
      window.Reveal.on("resumed", scheduleFit);

      fullscreenButton?.addEventListener("click", async () => {
        try {
          if (document.fullscreenElement) await document.exitFullscreen();
          else await revealRoot.requestFullscreen();
        } catch (error) {
          if (status) status.textContent = `전체 화면을 시작할 수 없습니다: ${error.message}`;
        }
      });

      speakerButton?.addEventListener("click", () => {
        const notesPlugin = window.Reveal.getPlugin("notes");
        if (typeof notesPlugin?.open === "function") {
          try {
            notesPlugin.open();
            if (status) status.textContent = "발표자 화면이 열리지 않으면 브라우저에서 팝업을 허용한 뒤 다시 누르세요.";
          } catch (error) {
            if (status) status.textContent = "발표자 화면 팝업이 차단되었습니다. 브라우저에서 팝업을 허용한 뒤 다시 누르세요.";
          }
        } else if (status) {
          status.textContent = "발표자 화면 플러그인을 사용할 수 없습니다.";
        }
      });

      window.addEventListener("resize", scheduleFit, { passive: true });
      document.addEventListener("fullscreenchange", scheduleFit);
      document.addEventListener("load", (event) => {
        if (event.target instanceof HTMLImageElement) scheduleFit();
      }, true);
      if ("ResizeObserver" in window) {
        new ResizeObserver(scheduleFit).observe(revealRoot);
      }
      if (document.fonts?.ready) document.fonts.ready.then(scheduleFit);
      announceSlide();
      scheduleFit();

      if (receiverView) {
        document.querySelector(".presentation-tools")?.remove();
        document.querySelector(".diagnostics")?.remove();
      }
    } catch (error) {
      console.error("Reveal.js initialization failed", error);
      if (status) status.textContent = `발표 화면을 시작할 수 없습니다: ${error.message}`;
    }
  }

  startPresentation();
})();
