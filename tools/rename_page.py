"""Give a page or a document a new address, update every link to it, and leave a forwarding page at the old one.

    python tools/rename_page.py writing/thermometer-and-ledger writing/climate-data
    python tools/rename_page.py --dry-run teaching/sar teaching/radar

What it does, in order:
 1. Built pages: moves the folder (or file) at the old address to the new one.
 2. Sources: a page in src/pages whose 'out:' is the old address gets the new one; a guide whose folder is the old
    address is renamed in build_guides.py and in guides/, so the next build writes to the new place.
 3. Links: every text file in the repository (pages, sources, settings, LaTeX) that names the old address, as
    /old/, old/ or ../old/, names the new one instead.
 4. Forwarding: a small page at the old address sends visitors and search engines to the new one, so links from
    elsewhere keep working. It is left out of the sitemap.
Nothing outside this repository is changed. Run it from the GitHub Actions form "Rename a page", or locally.
"""
import argparse
import re
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
TEXT = {".html", ".md", ".tex", ".toml", ".py", ".xml", ".txt", ".js", ".css", ".json", ".yml", ".bib"}
SKIP = {".git", "build", "__pycache__", "node_modules"}

FORWARD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Moved</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0; url={rel}">
<script>location.replace("{rel}" + location.hash)</script>
</head><body><p>This page has moved to <a href="{rel}">{url}</a>.</p></body></html>
"""


def clean(p):
    p = p.strip().strip("/")
    if not re.fullmatch(r"[a-z0-9][a-z0-9/_-]*", p):
        raise SystemExit(f"not a page address: {p!r} (use lower-case letters, digits, - and /)")
    return p


def git_mv(a, b, dry):
    print("move", a.relative_to(HERE), "->", b.relative_to(HERE))
    if dry:
        return
    b.parent.mkdir(parents=True, exist_ok=True)
    tracked = subprocess.run(["git", "ls-files", "--error-unmatch", str(a)], cwd=HERE, capture_output=True).returncode == 0
    if tracked:
        subprocess.run(["git", "mv", str(a), str(b)], cwd=HERE, check=True)
    else:
        shutil.move(str(a), str(b))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("old"); ap.add_argument("new"); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    old, new, dry = clean(a.old), clean(a.new), a.dry_run
    if old == new:
        raise SystemExit("old and new are the same")
    site = re.search(r'^url = "([^"]+)"', (HERE / "site.toml").read_text(encoding="utf8"), re.M)[1].rstrip("/")

    # 1. built pages
    src_dir, dst_dir = HERE / old, HERE / new
    if src_dir.exists():
        if dst_dir.exists():
            raise SystemExit(f"{new} already exists")
        git_mv(src_dir, dst_dir, dry)

    # 2. sources: a site page, or a guide folder
    for page in (HERE / "src/pages").glob("*.html"):
        s = page.read_text(encoding="utf8")
        t = re.sub(rf"(?m)^out: {re.escape(old)}/index\.html$", f"out: {new}/index.html", s)
        if t != s:
            print("source", page.relative_to(HERE))
            if not dry:
                page.write_text(t, encoding="utf8", newline="\n")
    old_key, new_key = old.rsplit("/", 1)[-1], new.rsplit("/", 1)[-1]
    if old.rsplit("/", 1)[0] == new.rsplit("/", 1)[0] and old_key != new_key:
        bg = HERE / "build_guides.py"
        s = bg.read_text(encoding="utf8")
        if f'"{old_key}": (' in s:                 # a guide: its build key is its address, wherever its source lives
            if (HERE / "guides" / old_key).exists():
                git_mv(HERE / "guides" / old_key, HERE / "guides" / new_key, dry)
                s = s.replace(f'HERE / "guides/{old_key}"', f'HERE / "guides/{new_key}"')
            s = s.replace(f'"{old_key}": (', f'"{new_key}": (')
            if not dry:
                bg.write_text(s, encoding="utf8", newline="\n")
            print("guide", old_key, "->", new_key, "in build_guides.py")

    # 3. links everywhere
    pat = re.compile(rf"(?<![\w-]){re.escape(old)}(?=/|\.html|[\"'#)\s]|$)")
    changed = 0
    for f in HERE.rglob("*"):
        if f.suffix not in TEXT or not f.is_file() or SKIP & set(f.relative_to(HERE).parts):
            continue
        if f.resolve() == Path(__file__).resolve():
            continue
        s = f.read_text(encoding="utf8", errors="surrogateescape")
        t = pat.sub(new, s)
        if t != s:
            changed += 1
            if not dry:
                f.write_text(t, encoding="utf8", errors="surrogateescape", newline="\n")
    print("files with links updated:", changed)

    # 4. forwarding page at the old address
    depth = old.count("/") + 1
    rel = "../" * depth + new + "/"
    stub = HERE / "redirects" / old / "index.html"   # tracked forwarding pages, copied into the published site
    print("forward", old, "->", new)
    if not dry:
        stub.parent.mkdir(parents=True, exist_ok=True)
        stub.write_text(FORWARD.format(url=f"{site}/{new}/", rel=rel), encoding="utf8", newline="\n")
        hidden = HERE / "site.toml"
        s = hidden.read_text(encoding="utf8")
        if f'"{old}/"' not in s:
            s = re.sub(r'^not_in_sitemap = \[', f'not_in_sitemap = ["{old}/", ', s, count=1, flags=re.M)
            hidden.write_text(s, encoding="utf8", newline="\n")


if __name__ == "__main__":
    main()
