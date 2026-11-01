"""Build every course from src/<course>/*.md: one web page per chapter, one long page, and one PDF booklet.

    python build_courses.py [--pdf] [course ...]
    python build.py

Writes page fragments to src/pages/, which build.py wraps in the site layout, and with --pdf writes the booklets to files/. A line
"!include examples/x.py python" pulls in a file from teaching/<course>/, so the pages show exactly the code that readers download.
To add a course: make its folder in src/ and add a line to COURSES. Needs pandoc; the PDF needs xelatex.
"""
import datetime
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PANDOC = shutil.which("pandoc") or os.path.expandvars(r"%LOCALAPPDATA%\Pandoc\pandoc.exe")
CODE_TEXT = 'Text &copy; Ahmad Ammar, licensed under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Example code &copy; Ulster University, MIT licence.'
VCRS = "Written during a PhD supported by a Vice-Chancellor's Research Scholarship (VCRS) from Ulster University."
COURSES = {
    "hpc": dict(name="HPC tutorial", title="Getting started on an HPC cluster", pdf="HPC_tutorial_Ahmad_Ammar.pdf",
                note=f"{CODE_TEXT} Data as credited in the starter kit. An independent guide, not an official NI-HPC document. {VCRS}"),
    "latex": dict(name="LaTeX guide", title="LaTeX from first principles", pdf="LaTeX_guide_Ahmad_Ammar.pdf", note=f"{CODE_TEXT} {VCRS}"),
    "atmosphere": dict(pandoc=["--mathjax"], name="The Atmosphere", title="The Atmosphere: a book worked step by step", pdf="The_Atmosphere_Ahmad_Ammar.pdf",
                note='Questions and data grew out of the practicals of EGM305 at Ulster University and are reused with the permission of the module staff. <a href="{{root}}teaching/egm305/">About the course</a>. <style>.box{border:1px solid var(--line,#c8ced6);border-left-width:5px;border-radius:6px;padding:.7em 1em;margin:1.1em 0}.box-title{font-weight:700;margin:0 0 .4em}.box-answer{border-left-color:#1b7f5c}.box-question{border-left-color:#27476e}.box-key{border-left-color:#2f6fb5}.box-care{border-left-color:#b3402f}.box-ask{border-left-color:#c77700}.box-worked{border-left-color:#27476e}.box-try,.box-deriv{border-left-color:#7a828c}.hpc-body img{max-width:100%;height:auto;background:#fff;display:block;margin:1em auto;border-radius:4px}.hpc-body table{display:block;overflow-x:auto}mjx-container[display="true"]{overflow-x:auto;overflow-y:hidden;max-width:100%}.hpc-body{min-width:0;overflow-wrap:anywhere}</style><script>window.MathJax={tex:{inlineMath:[["\\\\(","\\\\)"]],displayMath:[["\\\\[","\\\\]"]],tags:"none",macros:{ensuremath:["{#1}",1]}}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml.js"></script>'),
    "git-ci": dict(name="Git and automation guide", title="Git, testing and automation for research", pdf="Git_CI_guide_Ahmad_Ammar.pdf", note=f"{CODE_TEXT} {VCRS}"),
}


def chapters(course):
    out = []
    for path in sorted((HERE / "src" / course).glob("[0-9]*.md")):
        _, head, body = path.read_text(encoding="utf-8").split("---\n", 2)
        meta = dict(line.split(": ", 1) for line in head.strip().splitlines())
        meta["title"] = meta["title"].strip('"')
        fence = lambda text: "`" * max(3, 1 + max([len(r) for r in re.findall(r"`{3,}", text)] or [0]))
        def include(m):
            text = (HERE / "teaching" / course / m[1]).read_text(encoding="utf-8").rstrip()
            return f"**{Path(m[1]).name}**\n\n{fence(text)}{m[2]}\n{text}\n{fence(text)}"
        body = re.sub(r"^!include (\S+) (\w+)$", include, body, flags=re.M)
        out.append((meta, body))
    return out


def pandoc(text, *args):
    return subprocess.run([PANDOC, "-f", "markdown-smart", *args], input=text.encode("utf-8"), capture_output=True, check=True).stdout.decode("utf-8").replace("\r\n", "\n")


def href(course, slug):
    return f"{{{{root}}}}teaching/{course}/" + ("" if slug == "index" else slug + "/")


def head_block(title, description, out, crumb, eyebrow, h1):
    return f"""title: {title}
description: {description}
nav: teaching
out: {out}
---
<nav class="breadcrumb" aria-label="Breadcrumb">{crumb}</nav>
<header class="page-head">
  <p class="eyebrow">{eyebrow}</p>
  <h1>{h1}</h1>
</header>
<button class="btn no-print" type="button" data-toc-toggle aria-expanded="true">Hide or show contents</button>
"""


def web(course, cfg, items):
    for i, (meta, body) in enumerate(items):
        slug = meta["slug"]
        out = f"teaching/{course}/index.html" if slug == "index" else f"teaching/{course}/{slug}/index.html"
        html = pandoc(body, "-t", "html", "--no-highlight", *cfg.get("pandoc", []))
        html = html.replace('href="examples/', f'href="{{{{root}}}}teaching/{course}/examples/')
        side = "\n".join(f'      <li><a href="{href(course, m["slug"])}"' + (' aria-current="page"' if m["slug"] == slug else "")
                         + f'>{m["title"]}</a></li>' for m, _ in items)
        prev_ = f'<a href="{href(course, items[i - 1][0]["slug"])}">&larr; {items[i - 1][0]["title"]}</a>' if i else "<span></span>"
        next_ = f'<a href="{href(course, items[i + 1][0]["slug"])}">{items[i + 1][0]["title"]} &rarr;</a>' if i + 1 < len(items) else "<span></span>"
        crumb = '<a href="{{root}}teaching.html">Teaching</a> / ' + (cfg["name"] if slug == "index" else f'<a href="{href(course, "index")}">{cfg["name"]}</a> / {meta["title"]}')
        page = head_block(meta["title"], meta["description"], out, crumb, cfg["name"], meta["title"]) + f"""<div class="cv-layout">
  <aside class="toc" aria-label="Chapters">
    <p class="title">Chapters</p>
    <ol>
{side}
    </ol>
    <p><a href="{{{{root}}}}teaching/{course}/full/">Whole guide on one page</a></p>
    <p><a href="{{{{root}}}}files/{cfg['pdf']}">Whole guide as a PDF</a></p>
  </aside>
  <article class="hpc-body">
{html}
<nav class="hpc-pager" aria-label="Previous and next chapter">{prev_}{next_}</nav>
<p class="hpc-licence">{cfg['note']}</p>
  </article>
</div>
"""
        (HERE / "src" / "pages" / f"{course}-{slug}.html").write_text(page, encoding="utf-8")


def full(course, cfg, items):
    """Every chapter on one page, with a contents panel of chapters and sections that follows the reader."""
    slugs = "|".join(re.escape(m["slug"]) for m, _ in items if m["slug"] != "index")
    side, body = [], []
    for meta, text in items:
        slug = meta["slug"]
        html = pandoc(text, "-t", "html", "--no-highlight", f"--id-prefix={slug}-", "--shift-heading-level-by=1", *cfg.get("pandoc", []))
        html = html.replace('href="examples/', f'href="{{{{root}}}}teaching/{course}/examples/')
        html = re.sub(rf'href="(?:\.\./)?({slugs})/?"', lambda m: f'href="#ch-{m[1]}"', html)
        html = re.sub(r'<p>Prefer one long page\?.*?</p>\n?', "", html)
        side.append(f'      <li><a href="#ch-{slug}">{meta["title"]}</a></li>')
        side += [f'      <li class="sub"><a href="#{i}">{re.sub("<[^>]+>", "", t)}</a></li>' for i, t in re.findall(r'<h3[^>]*id="([^"]+)"[^>]*>(.*?)</h3>', html)]
        body.append(f'<section id="ch-{slug}">\n<h2>{meta["title"]}</h2>\n{html}\n</section>')
    nl = "\n"
    crumb = f'<a href="{{{{root}}}}teaching.html">Teaching</a> / <a href="{href(course, "index")}">{cfg["name"]}</a> / One page'
    page = head_block(f"{cfg['title']}: whole guide", f"Every chapter of {cfg['title']} on one scrolling page, with contents that follow the reader.",
                      f"teaching/{course}/full/index.html", crumb, cfg["name"], "The whole guide on one page") + f"""<div class="cv-layout">
  <aside class="toc" aria-label="Contents">
    <p class="title">Contents</p>
    <ol>
{nl.join(side)}
    </ol>
    <p><a href="{{{{root}}}}files/{cfg['pdf']}">PDF version</a></p>
  </aside>
  <article class="hpc-body">
{nl.join(body)}
<p class="hpc-licence">{cfg['note']}</p>
  </article>
</div>
"""
    (HERE / "src" / "pages" / f"{course}-full.html").write_text(page, encoding="utf-8")


def pdf(course, cfg, items):
    text = "\n\n".join(f"# {m['title']}\n\n{b}" for m, b in items)
    subprocess.run([PANDOC, "-f", "markdown-smart", "-o", str(HERE / "files" / cfg["pdf"]), "--pdf-engine=xelatex", "--toc", "--number-sections", "--no-highlight",
                    "-V", "documentclass=report", "-V", "papersize=a4", "-V", "geometry:margin=2.3cm", "-V", "colorlinks=true",
                    "-V", f"title={cfg['title']}", "-V", "author=Ahmad Ammar", "-V", "date=" + datetime.date.today().strftime("%B %Y"), "-H", str(HERE / "src/hpc/pdf_header.tex")],
                   input=text.encode("utf-8"), check=True)
    print("wrote", cfg["pdf"])


if __name__ == "__main__":
    wanted = [a for a in sys.argv[1:] if not a.startswith("--")] or list(COURSES)
    for name in wanted:
        cfg = COURSES[name]
        items = chapters(name)
        web(name, cfg, items)
        full(name, cfg, items)
        if "--pdf" in sys.argv:
            pdf(name, cfg, items)
        print(f"{name}: {len(items)} chapters")
