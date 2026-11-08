"""Build every guide and book from LaTeX with research_helpers.stack and place it on this site.

    python build_guides.py            all guides, then python build.py
    python build_guides.py sar maps   only these
    python build_guides.py check      look for broken links across the built site

Which guides exist, and where their LaTeX lives, is listed in GUIDES.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

from research_helpers import stack

HERE = Path(__file__).resolve().parent
HOME = Path.home()
GUIDES = {
    "hpc": (HERE / "guides/hpc", "HPC_tutorial_Ahmad_Ammar.pdf"),
    "latex": (HERE / "guides/latex", "LaTeX_guide_Ahmad_Ammar.pdf"),
    "git-ci": (HERE / "guides/git-ci", "Git_CI_guide_Ahmad_Ammar.pdf"),
    "sar": (HOME / "dev/sar-reading-manual", "Reading_radar_images_Ahmad_Ammar.pdf"),
    "maps": (HOME / "dev/research-helpers/docs/map_manual", "Reproducible_maps_Ahmad_Ammar.pdf"),
    "site-setup": (HERE / "guides/site-setup", "Website_guide_Ahmad_Ammar.pdf"),
    "contribute": (HERE / "guides/contribute", "Contributing_guide_Ahmad_Ammar.pdf"),
    "atmosphere": (Path(r"D:\OneDrive - Ulster University\Demonstrating\EGM305\companion"), "The_Atmosphere_Ahmad_Ammar.pdf"),
    "climate-data": (HERE / "guides/climate-data", "Climate_data_Ahmad_Ammar.pdf", "writing"),
    "climate-data-python": (HERE / "guides/climate-data-python", "Climate_data_in_Python_Ahmad_Ammar.pdf"),
    "hypothesis-testing": (HERE / "guides/hypothesis-testing", "Hypothesis_testing_Ahmad_Ammar.pdf"),
    "radar-python": (HERE / "guides/radar-python", "Radar_images_in_Python_Ahmad_Ammar.pdf"),
    "satellite-python": (HERE / "guides/satellite-python", "Satellite_images_in_Python_Ahmad_Ammar.pdf"),
    "pixel-animation": (HERE / "guides/pixel-animation", "Pixel_animation_Ahmad_Ammar.pdf"),
}


def activate_shots(root):
    """A step written %SHOT{file}{caption} gains its picture as soon as the file exists; until then the text stands alone."""
    img = root / "../shots/img"
    for f in [*(root / "tex").glob("*.tex"), *(root / "../shared").glob("*.tex")] if (root / "tex").exists() else []:
        s = f.read_text(encoding="utf8")
        new = re.sub(r"%SHOT\{([^}]+)\}\{([^}]*)\}", lambda m: f"\\begin{{figure}}[H]\\centering\\includegraphics[width=\\linewidth]{{{m[1]}}}\\caption{{{m[2]}}}\\end{{figure}}" if (img / m[1]).exists() else m[0], s)
        if new != s:
            f.write_text(new, encoding="utf8", newline="\n")


def build(course):
    root, pdf_name, *section = GUIDES[course]
    dest = HERE / (section[0] if section else "teaching") / course       # guides under teaching/, essays under writing/
    activate_shots(root)
    d = stack.load(root)
    results = stack.pdf(root)
    bad = {k: v["errors"] for k, v in results.items() if v["errors"]}
    if bad:
        print("LaTeX problems in", course, bad)
    made = root / "build" / f"{d['name']}_{d['layouts'][0]}.pdf"
    shutil.copy2(made, HERE / "files" / pdf_name)
    stack.web(root)
    stack.deploy(root, dest)
    (dest / "404.html").unlink(missing_ok=True)    # the site has one error page, at its root


def check():
    """Every internal link and picture in the built site must point at a file that exists."""
    missing = {}
    pages = [p for p in HERE.rglob("*.html") if not {"guides", "src", ".git"} & set(p.relative_to(HERE).parts)]
    for page in pages:
        for link in re.findall(r'(?:href|src|data-src)="([^"#?]+)', page.read_text(encoding="utf8", errors="replace")):
            if re.match(r"[a-z]+:|//", link):
                continue
            target = (HERE / link.lstrip("/")) if link.startswith("/") else (page.parent / link)
            if link.startswith(("/GBEM", "/marxist-economics", "marxist-economics", "GBEM")) or "/GBEM" in link or "marxist-economics" in link:
                continue
            if not (target.exists() or (target / "index.html").exists()):
                missing.setdefault(link, str(page.relative_to(HERE)))
    print(len(pages), "pages,", len(missing), "broken links")
    for k, v in list(missing.items())[:40]:
        print(" ", k, "<-", v)
    return missing


if __name__ == "__main__":
    wanted = sys.argv[1:]
    if wanted == ["check"]:
        sys.exit(1 if check() else 0)
    for course in wanted or GUIDES:
        build(course)
    subprocess.run([sys.executable, str(HERE / "build.py")], check=True, cwd=HERE)
    check()
