/* 「两衡之间」共享 UI 增强层
 * - html.js 门控：滚动入场动效
 * - 顶栏滚动态（is-scrolled）
 * - 页面内锚点 scrollspy（aria-current）
 * - 返回顶部按钮（.to-top）
 * 全部尊重 prefers-reduced-motion；无 JS 时页面保持完整可见。 */
(() => {
  'use strict';
  const root = document.documentElement;
  root.classList.add('js');

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const topbar = document.querySelector('.topbar');

  /* 返回顶部 */
  const toTop = document.createElement('button');
  toTop.type = 'button';
  toTop.className = 'to-top';
  toTop.setAttribute('aria-label', '返回顶部');
  toTop.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5m-6 6 6-6 6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  toTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
  });
  document.body.appendChild(toTop);

  /* scrollspy：仅处理导航里的页内锚点 */
  const spyLinks = [...document.querySelectorAll('nav a[href^="#"]')];
  const spyTargets = spyLinks
    .map((link) => {
      let el = null;
      try {
        el = document.querySelector(link.getAttribute('href'));
      } catch (err) {
        el = null;
      }
      return { link, el };
    })
    .filter((entry) => entry.el);

  let ticking = false;
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(() => {
      const y = window.scrollY;
      if (topbar) topbar.classList.toggle('is-scrolled', y > 8);
      toTop.classList.toggle('is-visible', y > 560);

      const probe = y + Math.min(window.innerHeight * 0.35, 360);
      let current = null;
      for (const entry of spyTargets) {
        if (entry.el.getBoundingClientRect().top <= probe) current = entry.link;
      }
      spyLinks.forEach((link) => {
        if (current && link === current) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
      ticking = false;
    });
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* 滚动入场：进入视口一次即显示 */
  const reveals = [...document.querySelectorAll('[data-reveal]')];
  if (!reduceMotion && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-revealed');
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -8% 0px' }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add('is-revealed'));
  }
})();
