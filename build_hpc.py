"""Build the HPC tutorial from src/hpc/*.md: one web page per chapter, and one PDF.

    python build_hpc.py [--pdf]
    python build.py

Writes page fragments to src/pages/hpc-<slug>.html, which build.py wraps in the site layout, and with --pdf
writes files/HPC_tutorial_Ahmad_Ammar.pdf. A line "!include examples/x.py python" pulls in a file from
teaching/hpc/examples, so the pages show exactly the code that readers download. Needs pandoc; the PDF needs xelatex.
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "src" / "hpc"
EX = HERE / "teaching" / "hpc"
PANDOC = shutil.which("pandoc") or os.path.expandvars(r"%LOCALAPPDATA%\Pandoc\pandoc.exe")


def chapters():
    out = []
    for path in sorted(SRC.glob("[0-9]*.md")):
        _, head, body = path.read_text(encoding="utf-8").split("---\n", 2)
        meta = dict(line.split(": ", 1) for line in head.strip().splitlines())
        meta["title"] = meta["title"].strip('"')
        body = re.sub(r"^!include (\S+) (\w+)$",
                      lambda m: f"**{Path(m[1]).name}**\n\n```{m[2]}\n{(EX / m[1]).read_text(encoding='utf-8').rstrip()}\n```",
                      body, flags=re.M)
        out.append((meta, body))
    return out


def pandoc(text, *args):
    return subprocess.run([PANDOC, "-f", "markdown-smart", *args], input=text.encode("utf-8"),
                          capture_output=True, check=True).stdout.decode("utf-8")


def href(slug):
    return "{{root}}teaching/hpc/" + ("" if slug == "index" else slug + "/")


def web(items):
    for i, (meta, body) in enumerate(items):
        slug = meta["slug"]
        out = "teaching/hpc/index.html" if slug == "index" else f"teaching/hpc/{slug}/index.html"
        html = pandoc(body, "-t", "html", "--no-highlight")
        html = html.replace('href="examples/', 'href="{{root}}teaching/hpc/examples/')
        side = "\n".join(f'      <li><a href="{href(m["slug"])}"' + (' aria-current="page"' if m["slug"] == slug else "")
                         + f'>{m["title"]}</a></li>' for m, _ in items)
        prev_ = f'<a href="{href(items[i - 1][0]["slug"])}">&larr; {items[i - 1][0]["title"]}</a>' if i else "<span></span>"
        next_ = f'<a href="{href(items[i + 1][0]["slug"])}">{items[i + 1][0]["title"]} &rarr;</a>' if i + 1 < len(items) else "<span></span>"
        crumb = '<a href="{{root}}teaching.html">Teaching</a> / ' + ("HPC tutorial" if slug == "index" else '<a href="' + href("index") + '">HPC tutorial</a> / ' + meta["title"])
        page = f"""title: {meta['title']}
description: {meta['description']}
nav: teaching
out: {out}
---
<nav class="breadcrumb" aria-label="Breadcrumb">{crumb}</nav>
<header class="page-head">
  <p class="eyebrow">HPC tutorial</p>
  <h1>{meta['title']}</h1>
</header>
<button class="btn no-print" type="button" data-toc-toggle aria-expanded="true">Hide or show contents</button>
<div class="cv-layout">
  <aside class="toc" aria-label="Chapters">
    <p class="title">Chapters</p>
    <ol>
{side}
    </ol>
    <p><a href="{{{{root}}}}teaching/hpc/full/">Whole tutorial on one page</a></p>
    <p><a href="{{{{root}}}}files/HPC_tutorial_Ahmad_Ammar.pdf">Whole tutorial as a PDF</a></p>
  </aside>
  <article class="hpc-body">
{html}
<nav class="hpc-pager" aria-label="Previous and next chapter">{prev_}{next_}</nav>
<p class="hpc-licence">Text &copy; Ahmad Ammar, licensed under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Example code &copy; Ulster University, MIT licence. Data as credited in the starter kit. An independent guide, not an official NI-HPC document. Written during a PhD supported by a Vice-Chancellor's Research Scholarship (VCRS) from Ulster University.</p>
  </article>
</div>
"""
        (HERE / "src" / "pages" / f"hpc-{slug}.html").write_text(page, encoding="utf-8")
        print("wrote fragment", slug)


def full(items):
    """Every chapter on one page, with a contents panel of chapters and sections that follows the reader."""
    side, body = [], []
    for meta, text in items:
        slug = meta["slug"]
        html = pandoc(text, "-t", "html", "--no-highlight", f"--id-prefix={slug}-", "--shift-heading-level-by=1")
        html = html.replace('href="examples/', 'href="{{root}}teaching/hpc/examples/')
        html = re.sub(r'href="(concepts|shell|connect|files|software|slurm|first-jobs|arrays|practice|beyond|troubleshooting)/?"', lambda m: f'href="#ch-{m[1]}"', html)
        side.append(f'      <li><a href="#ch-{slug}">{meta["title"]}</a></li>')
        side += [f'      <li class="sub"><a href="#{i}">{re.sub("<[^>]+>", "", t)}</a></li>' for i, t in re.findall(r'<h3[^>]*id="([^"]+)"[^>]*>(.*?)</h3>', html)]
        body.append(f'<section id="ch-{slug}">\n<h2>{meta["title"]}</h2>\n{html}\n</section>')
    nl = "\n"
    page = f"""title: The whole HPC tutorial on one page
description: Every chapter of the HPC tutorial on one scrolling page, with contents that follow the reader.
nav: teaching
out: teaching/hpc/full/index.html
---
<nav class="breadcrumb" aria-label="Breadcrumb"><a href="{{{{root}}}}teaching.html">Teaching</a> / <a href="{{{{root}}}}teaching/hpc/">HPC tutorial</a> / One page</nav>
<header class="page-head">
  <p class="eyebrow">HPC tutorial</p>
  <h1>The whole tutorial on one page</h1>
</header>
<button class="btn no-print" type="button" data-toc-toggle aria-expanded="true">Hide or show contents</button>
<div class="cv-layout">
  <aside class="toc" aria-label="Contents">
    <p class="title">Contents</p>
    <ol>
{nl.join(side)}
    </ol>
    <p><a href="{{{{root}}}}files/HPC_tutorial_Ahmad_Ammar.pdf">PDF version</a></p>
  </aside>
  <article class="hpc-body">
{nl.join(body)}
  </article>
</div>
"""
    (HERE / "src" / "pages" / "hpc-full.html").write_text(page, encoding="utf-8")
    print("wrote fragment full")


def pdf(items):
    text = "\n\n".join(f"# {m['title']}\n\n{b}" for m, b in items)
    head = HERE / "src" / "hpc" / "pdf_header.tex"
    out = HERE / "files" / "HPC_tutorial_Ahmad_Ammar.pdf"
    subprocess.run([PANDOC, "-f", "markdown-smart", "-o", str(out), "--pdf-engine=xelatex", "--toc", "--number-sections", "--no-highlight",
                    "-V", "documentclass=report", "-V", "papersize=a4", "-V", "geometry:margin=2.3cm", "-V", "colorlinks=true",
                    "-V", "title=Getting started on an HPC cluster", "-V", "author=Ahmad Ammar",
                    "-V", "date=" + __import__("datetime").date.today().strftime("%B %Y"), "-H", str(head)],
                   input=text.encode("utf-8"), check=True)
    print("wrote", out)


if __name__ == "__main__":
    items = chapters()
    web(items)
    full(items)
    if "--pdf" in sys.argv:
        pdf(items)
