# ahmadammar.github.io

Personal academic website of Ahmad Ammar: <https://ahmadammar.github.io/>.

[![Build and publish site](https://github.com/AhmadAmmar/AhmadAmmar.github.io/actions/workflows/site.yml/badge.svg)](https://github.com/AhmadAmmar/AhmadAmmar.github.io/actions/workflows/site.yml)

This repository holds **sources only**. GitHub builds the site from them on every push to `main`
(`.github/workflows/site.yml`, about three minutes) and publishes the result to GitHub Pages. Built pages and
guide PDFs are not kept here.

## Layout

| Path | Contents |
|---|---|
| `src/pages/*.html` | Page bodies (home, research, teaching, writing, CV, projects), each with a short header |
| `build.py` | Wraps every page body in the shared header and footer; writes `sitemap.xml` and `robots.txt` |
| `guides/<guide>/` | Each guide or essay: `document.toml`, chapters in `tex/`, figures, notebooks (`notebooks/*.py`), the last notebook run (`frozen/`), and files served beside the pages (`static/`) |
| `build_guides.py` | Builds every guide with [research-helpers](https://github.com/GeospatialGeeks/research-helpers)' stack (PDF and web pages), then `build.py` |
| `assets/`, `favicon.svg` | Stylesheet, script and icon shared by all pages |
| `files/` | Downloads that are not built here (CV, EGM305 lab cards and guides) |
| `teaching/atmosphere/` | The Atmosphere handbook, built from a private source and committed as built |
| `redirects/` | Forwarding pages for renamed addresses (`tools/rename_page.py`) |
| `.stack-hold` | Paths never published |

Two guides live in other public repositories and are fetched by the build:
[sar-reading-manual](https://github.com/AhmadAmmar/sar-reading-manual) and the map manual in
[research-helpers](https://github.com/GeospatialGeeks/research-helpers/tree/main/docs/map_manual).
The pamphlet at `/marxist-economics/` is published from [its own repository](https://github.com/AhmadAmmar/marxist-economics).

## Editing

* **Any page, anywhere:** edit the source (a chapter's `.tex`, a `src/pages/*.html`) in GitHub's editor or
  locally, commit and push. The site rebuilds and goes live in a few minutes.
* **With previews:** `python -m research_helpers.stack studio` opens every document with its chapters beside
  their rendering; *Save and publish* commits the changed sources and pushes. In VS Code, Ctrl+Shift+B builds
  the exact PDF of the open chapter.
* **A full local build** (to see everything before pushing): `python build_guides.py`. It writes the pages
  into this folder for viewing; git ignores them.
* **Notebooks** run only on a machine with their data. Each run is copied to the guide's `frozen/` folder:
  commit it, and GitHub builds from it without rerunning (as Quarto does with `_freeze`).

## Checks on every build

Internal links, missing alternative text, oversized images and pages without a heading (the stack's audit),
and, in the run summary, every outside link (lychee). Pull requests are built and checked but not published.
A weekly scheduled build shows a broken toolchain or link before an edit needs it, and Dependabot proposes
updates to the workflow's actions once a month.

## Toolchain

`python -m research_helpers.stack doctor` lists what a build needs and what this machine has.
On GitHub: Ubuntu, Python 3.12 (`requirements-site.txt`), pandoc 3.13, TeX Live, Poppler. PDFs use the
open-licence fonts shipped with the stack (Caladea, Inconsolata), so they come out the same everywhere.

## Licence

Text and teaching materials © Ahmad Ammar. To cite, see `CITATION.cff`.
