// Macwan Apps — shared behaviors: scroll reveals, nav surface on scroll, stat count-up

// ?noanim=1 disables entrance animations (debugging / screenshots)
if (new URLSearchParams(location.search).has('noanim')) {
  document.documentElement.classList.add('noanim');
}

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll('.fade-in, .fade-in-left').forEach(el => observer.observe(el));

// Nav gains background + border once the page is scrolled
const navEl = document.querySelector('nav');
const updateNav = () => navEl.classList.toggle('scrolled', window.scrollY > 8);
window.addEventListener('scroll', updateNav, { passive: true });
updateNav();

// Count-up for elements like <span data-count="9" data-suffix="+">
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const countObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    countObserver.unobserve(entry.target);
    const el = entry.target;
    const target = parseInt(el.dataset.count, 10);
    const suffix = el.dataset.suffix || '';
    if (reducedMotion || !Number.isFinite(target)) {
      el.textContent = el.dataset.count + suffix;
      return;
    }
    el.textContent = '0' + suffix;
    const duration = 1200;
    const start = performance.now();
    const ease = t => 1 - Math.pow(1 - t, 3);
    const tick = now => {
      const p = Math.min((now - start) / duration, 1);
      el.textContent = Math.round(ease(p) * target) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
    // rAF can stall (backgrounded tab); guarantee the final value lands
    setTimeout(() => { el.textContent = target + suffix; }, duration + 100);
  });
}, { threshold: 0.4 });

document.querySelectorAll('[data-count]').forEach(el => countObserver.observe(el));
