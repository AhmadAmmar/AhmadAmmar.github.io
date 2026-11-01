"""Test the course pages in a real browser, and prove that their examples work.

    python tools/check_courses.py             exit code 1 on any failure

Compiles every LaTeX example, runs the Git practice script and the pytest examples in temporary folders, checks local links and anchors,
and opens each course page on desktop and phone, in light and dark, for raw markup, sideways scrolling and poor link contrast.
Needs playwright with Chromium, pytest, git and LaTeX.
"""
import functools
import http.server
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import urllib.parse

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]
COURSES = ("hpc", "latex", "git-ci")
MEASURE = r"""() => {
  const lum = c => { const f = c.map(v => { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4) }); return .2126 * f[0] + .7152 * f[1] + .0722 * f[2] };
  const rgb = s => { const m = s.match(/[\d.]+/g).map(Number); return { c: m.slice(0, 3), a: m.length > 3 ? m[3] : 1 } };
  const bg = el => { for (let e = el; e; e = e.parentElement) { const b = rgb(getComputedStyle(e).backgroundColor); if (b.a > .5) return b.c } return [255, 255, 255] };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05) };
  const art = document.querySelector('.hpc-body');
  const clone = art.cloneNode(true); clone.querySelectorAll('pre, code').forEach(e => e.remove());
  const low = [...document.querySelectorAll('.hpc-body a, .toc a')].filter(a => a.getBoundingClientRect().width > 0 && ratio(rgb(getComputedStyle(a).color).c, bg(a)) < 4.5).map(a => a.innerText.slice(0, 30));
  return { text: clone.innerText, low, wide: document.documentElement.scrollWidth > innerWidth + 1, h1: document.querySelectorAll('h1').length };
}"""
RAW = [("include", r"!include"), ("Markdown table", r"\|\s*:?-{3,}"), ("heading marks", r"(?m)^#{2,} "), ("fence", r"```")]


def examples():
    bad = []
    with tempfile.TemporaryDirectory() as t:
        work = pathlib.Path(t)
        shutil.copytree(ROOT / "teaching/latex/examples", work / "tex", ignore=shutil.ignore_patterns("*.zip"))
        run = lambda c, cwd: subprocess.run(c, cwd=cwd, capture_output=True, text=True, errors="replace")
        for folder, name, bib in ((work / "tex", "minimal", False), (work / "tex", "slides", False), (work / "tex", "chapters", False), (work / "tex", "maths", False), (work / "tex/report", "main", True)):
            for c in [["pdflatex", "-interaction=nonstopmode", name]] + ([["bibtex", name]] if bib else []) + [["pdflatex", "-interaction=nonstopmode", name]] * 2:
                run(c, folder)
            log = (folder / f"{name}.log").read_text(encoding="latin1", errors="replace")
            errors = re.findall(r"(?m)^! .*", log) + re.findall(r"(?:Citation|Reference) `[^']+' [^\n]*undefined", log)
            if errors or not (folder / f"{name}.pdf").exists():
                bad.append(f"LaTeX example {name}: {errors[:3]}")
        p = work / "git"
        p.mkdir()
        shutil.copy2(ROOT / "teaching/git-ci/examples/practice.sh", p)
        git_bash = pathlib.Path(r"C:\Program Files\Git\bin\bash.exe")  # on Windows, plain "bash" can mean an empty WSL
        r = run([str(git_bash) if git_bash.exists() else "bash", "practice.sh"], p)
        if r.returncode or r.stdout.strip().splitlines()[-1] != "The mean is 12.":
            bad.append(f"Git practice script: {r.stdout[-200:]} {r.stderr[-200:]}")
        q = work / "py"
        q.mkdir()
        for f in ("calc.py", "test_calc.py"):
            shutil.copy2(ROOT / "teaching/git-ci/examples" / f, q)
        if run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"], q).returncode:
            bad.append("pytest example failed")
    return bad


def links():
    bad, n = [], 0
    pages = [p for c in COURSES for p in (ROOT / "teaching" / c).rglob("index.html")]
    ids = {}
    for p in pages:
        t = p.read_text(encoding="utf8")
        ids[p.resolve()] = set(re.findall(r'\bid="([^"]+)"', t))
        for href in re.findall(r'\bhref="([^"]+)"', t):
            if re.match(r"[a-z]+:|//", href):
                continue
            n += 1
            path, _, frag = urllib.parse.unquote(href).partition("#")
            target = p.resolve() if not path else (p.parent / path).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                bad.append(f"{p.relative_to(ROOT)}: missing {href}")
            elif frag and target in ids and frag not in ids[target]:
                bad.append(f"{p.relative_to(ROOT)}: missing anchor {href}")
    return bad, n, pages


def browser(pages):
    bad = []
    handler = functools.partial(type("Q", (http.server.SimpleHTTPRequestHandler,), {"log_message": lambda *a: None}), directory=str(ROOT))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for scheme, w in (("light", 1440), ("dark", 1440), ("light", 390), ("dark", 390)):
            pg = b.new_context(viewport={"width": w, "height": 850}, color_scheme=scheme).new_page()
            for p in pages:
                rel = p.parent.relative_to(ROOT).as_posix()
                pg.goto(f"http://127.0.0.1:{srv.server_address[1]}/{rel}/")
                m = pg.evaluate(MEASURE)
                for name, pat in RAW:
                    if re.search(pat, m["text"]):
                        bad.append(f"{scheme} {w} {rel}: raw {name}")
                if m["wide"]:
                    bad.append(f"{scheme} {w} {rel}: page scrolls sideways")
                if m["h1"] != 1:
                    bad.append(f"{scheme} {w} {rel}: {m['h1']} main headings")
                bad += [f"{scheme} {w} {rel}: low contrast {x}" for x in m["low"][:3]]
        b.close()
    srv.shutdown()
    return bad


if __name__ == "__main__":
    bad = examples()
    print("examples:", "OK" if not bad else "FAILED")
    lb, n, pages = links()
    print(f"{n} local links checked")
    bad += lb + browser(pages)
    print("\n".join("FAIL " + b for b in bad[:50]) or f"OK: {len(pages)} course pages in 4 views")
    sys.exit(bool(bad))
