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

    // hide or show a contents panel, starting hidden on small screens; the choice is remembered
    var tocToggle = document.querySelector('[data-toc-toggle]');
    var layout = document.querySelector('.cv-layout');
    if (tocToggle && layout) {
      var setToc = function (hidden) {
        layout.classList.toggle('toc-hidden', hidden);
        tocToggle.setAttribute('aria-expanded', hidden ? 'false' : 'true');
      };
      var savedToc = null;
      try { savedToc = localStorage.getItem('toc'); } catch (e) { /* storage unavailable */ }
      setToc(savedToc ? savedToc === 'hidden' : window.innerWidth <= 900);
      tocToggle.addEventListener('click', function () {
        var hidden = !layout.classList.contains('toc-hidden');
        setToc(hidden);
        try { localStorage.setItem('toc', hidden ? 'hidden' : 'shown'); } catch (e) { /* storage unavailable */ }
      });
    }

    var printBtn = document.querySelector('[data-print]');
    if (printBtn) printBtn.addEventListener('click', function () { window.print(); });
  });
})();

// Admin edit bar: ?admin=on shows it on this browser, ?admin=off hides it again. Saving still needs a GitHub login.
(function () {
  try {
    var q = new URLSearchParams(location.search).get('admin');
    if (q === 'on') localStorage.setItem('admin', '1');
    if (q === 'off') localStorage.removeItem('admin');
    if (localStorage.getItem('admin') !== '1') return;
  } catch (e) { return; }
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-admin-edit]').forEach(function (el) { el.hidden = false; });
  });
})();
