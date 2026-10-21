(function () {
  var root = document.documentElement;

  function storedTheme() {
    try { return localStorage.getItem('theme'); } catch (e) { return null; }
  }
  function saveTheme(value) {
    try { localStorage.setItem('theme', value); } catch (e) { /* storage unavailable */ }
  }
  function currentTheme() {
    var set = root.getAttribute('data-theme');
    if (set) return set;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  var saved = storedTheme();
  if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved);

  document.addEventListener('DOMContentLoaded', function () {
    var toggle = document.querySelector('[data-theme-toggle]');
    if (toggle) {
      toggle.addEventListener('click', function () {
        var next = currentTheme() === 'dark' ? 'light' : 'dark';
        root.setAttribute('data-theme', next);
        saveTheme(next);
      });
    }

    var menu = document.querySelector('[data-menu-toggle]');
    var nav = document.getElementById('site-nav');
    if (menu && nav) {
      menu.addEventListener('click', function () {
        var open = nav.classList.toggle('open');
        menu.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    }

    var year = document.querySelector('[data-year]');
    if (year) year.textContent = new Date().getFullYear();

    // highlight the section of a long page that is currently in view
    var tocLinks = document.querySelectorAll('.toc a[href^="#"]');
    if (tocLinks.length && 'IntersectionObserver' in window) {
      var byId = {};
      tocLinks.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting && byId[entry.target.id]) {
            tocLinks.forEach(function (a) { a.classList.remove('active'); });
            byId[entry.target.id].classList.add('active');
          }
        });
      }, { rootMargin: '-90px 0px -70% 0px' });
      Object.keys(byId).forEach(function (id) {
        var el = document.getElementById(id);
        if (el) observer.observe(el);
      });
    }

    var printBtn = document.querySelector('[data-print]');
    if (printBtn) printBtn.addEventListener('click', function () { window.print(); });
  });
})();
