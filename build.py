"""Assemble the site: wraps every fragment in src/pages with the shared layout.

    python build.py

Each fragment starts with a header block of `key: value` lines, ended by a line
holding only `---`:

    title: Teaching
    description: One sentence for search engines and link previews.
    nav: teaching
    out: teaching.html
    ---
    <section>...</section>

Inside fragments, `{{root}}` expands to the relative path back to the site root
and `{{icon:name}}` to an inline SVG icon from ICONS below.
"""

from datetime import date
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
PAGES = HERE / "src" / "pages"
SITE_URL = "https://ahmadammar.github.io"
UPDATED = date.today().strftime("%B %Y")

NAV = [
    ("about", "About", "index.html"),
    ("research", "Research", "research.html"),
    ("teaching", "Teaching", "teaching.html"),
    ("projects", "Projects", "projects.html"),
    ("writing", "Writing", "writing.html"),
    ("cv", "CV", "cv.html"),
]

_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{}</svg>'
_SVG_FILL = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">{}</svg>'

ICONS = {
    "mail": _SVG.format('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
    "pin": _SVG.format('<path d="M12 21s-7-6.1-7-11.5A7 7 0 0 1 19 9.5C19 14.9 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>'),
    "building": _SVG.format('<path d="M4 21V5l8-3v19M12 8l8 3v10M8 8h.01M8 12h.01M8 16h.01M16 14h.01M16 18h.01M2 21h20"/>'),
    "cap": _SVG.format('<path d="m2 9 10-5 10 5-10 5z"/><path d="M6 11v5c3 2.5 9 2.5 12 0v-5M22 9v6"/>'),
    "book": _SVG.format('<path d="M4 5a2 2 0 0 1 2-2h14v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5M8 7h8"/>'),
    "external": _SVG.format('<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>'),
    "download": _SVG.format('<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>'),
    "arrow": _SVG.format('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "print": _SVG.format('<path d="M7 9V3h10v6M7 17H5a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2h-2"/><rect x="7" y="14" width="10" height="7"/>'),
    "globe": _SVG.format('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.8 3 2.8 15 0 18M12 3c-2.8 3-2.8 15 0 18"/>'),
    "sun": _SVG.format('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>'),
    "menu": _SVG.format('<path d="M4 7h16M4 12h16M4 17h16"/>'),
    "github": _SVG_FILL.format('<path d="M12 2a10 10 0 0 0-3.2 19.5c.5.1.7-.2.7-.5v-1.7c-2.8.6-3.4-1.3-3.4-1.3-.5-1.2-1.1-1.5-1.1-1.5-.9-.6.1-.6.1-.6 1 .1 1.5 1 1.5 1 .9 1.5 2.4 1.1 2.9.8.1-.7.4-1.1.6-1.3-2.2-.3-4.6-1.1-4.6-5 0-1.1.4-2 1-2.7-.1-.3-.4-1.3.1-2.7 0 0 .8-.3 2.8 1a9.6 9.6 0 0 1 5 0c1.9-1.3 2.8-1 2.8-1 .5 1.4.2 2.4.1 2.7.6.7 1 1.6 1 2.7 0 3.9-2.4 4.7-4.6 5 .4.3.7.9.7 1.9V21c0 .3.2.6.7.5A10 10 0 0 0 12 2z"/>'),
    "linkedin": _SVG_FILL.format('<path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.5h4V21H3zM9.5 9.5h3.8v1.6h.1c.5-1 1.8-2 3.8-2 4 0 4.8 2.6 4.8 6V21h-4v-5.2c0-1.3 0-2.9-1.8-2.9s-2 1.4-2 2.8V21h-4z"/>'),
    "substack": _SVG_FILL.format('<path d="M4 3h16v2.6H4zM4 7.4h16V10H4zM4 11.8h16V21l-8-4.5L4 21z"/>'),
}

HEAD = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="author" content="Ahmad Ammar">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&display=swap">
<link rel="stylesheet" href="{root}assets/css/site.css">
<script src="{root}assets/js/site.js"></script>
{extra_head}</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="site-header">
  <div class="bar">
    <a class="brand" href="{root}index.html">Ahmad <span>Ammar</span></a>
    <button class="icon-btn menu-btn" type="button" data-menu-toggle aria-controls="site-nav" aria-expanded="false" aria-label="Menu">{icon_menu}</button>
    <nav class="nav" id="site-nav" aria-label="Main">
{nav}
    </nav>
    <button class="icon-btn" type="button" data-theme-toggle aria-label="Switch between light and dark theme">{icon_sun}</button>
  </div>
</header>
<main id="content">
"""

FOOT = """</main>
<footer class="site-footer">
  <div class="bar">
    <div>&copy; <span data-year>{year}</span> Ahmad Ammar &middot; School of Geography and Environmental Sciences, Ulster University &middot; Updated {updated}</div>
    <div class="social">
      <a href="mailto:ahmadammargeo@gmail.com" aria-label="Email">{icon_mail}</a>
      <a href="https://github.com/AhmadAmmar" aria-label="GitHub">{icon_github}</a>
      <a href="https://www.linkedin.com/in/ahmadammar/" aria-label="LinkedIn">{icon_linkedin}</a>
      <a href="https://ammarastan.substack.com/" aria-label="Substack">{icon_substack}</a>
    </div>
  </div>
</footer>
</body>
</html>
"""


def parse(path):
    text = path.read_text(encoding="utf-8")
    header, body = text.split("\n---\n", 1)
    meta = {}
    for line in header.strip().splitlines():
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, body


def render(meta, body):
    out = meta["out"]
    depth = out.count("/")
    root = "../" * depth
    nav = "\n".join(
        '      <a href="{}{}"{}>{}</a>'.format(
            root, href, ' aria-current="page"' if key == meta.get("nav") else "", label
        )
        for key, label, href in NAV
    )
    canonical = SITE_URL + "/" + ("" if out == "index.html" else out.replace("index.html", ""))
    title = meta["title"] if meta.get("nav") == "about" else meta["title"] + " | Ahmad Ammar"
    head = HEAD.format(
        title=title, description=meta["description"], canonical=canonical, root=root,
        nav=nav, extra_head=meta.get("head", ""),
        icon_menu=ICONS["menu"], icon_sun=ICONS["sun"],
    )
    foot = FOOT.format(
        year=date.today().year, updated=UPDATED,
        **{"icon_" + k: ICONS[k] for k in ("mail", "github", "linkedin", "substack")},
    )
    body = body.replace("{{root}}", root)
    body = re.sub(r"\{\{icon:(\w+)\}\}", lambda m: ICONS[m.group(1)], body)
    return out, head + body.strip("\n") + "\n" + foot


# pages on this host that are not built here: the EGM305 atlas and the sites of other repositories
# (GitHub Pages serves them under this domain, so this sitemap may list them)
EXTRA_URLS = ["teaching/egm305/atlas/", "GBEM/", "marxist-economics/"]


def sitemap(outs):
    paths = [o.replace("index.html", "") for o in sorted(outs) if o != "404.html"] + EXTRA_URLS
    urls = "\n".join("  <url><loc>{}/{}</loc></url>".format(SITE_URL, p) for p in paths)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n"


def robots():
    """robots.txt for the whole host (also read for /GBEM/ and /marxist-economics/): allow all, point to the sitemap"""
    return f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"


def main():
    outs = []
    for path in sorted(PAGES.glob("*.html")):
        out, html = render(*parse(path))
        target = HERE / out
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8", newline="\n")
        outs.append(out)
        print("wrote", out)
    (HERE / "sitemap.xml").write_text(sitemap(outs), encoding="utf-8", newline="\n")
    (HERE / "robots.txt").write_text(robots(), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
