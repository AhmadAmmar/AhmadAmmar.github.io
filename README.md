# ahmadammar.github.io

Personal academic website of Ahmad Ammar, served by GitHub Pages at <https://ahmadammar.github.io/>.

## Layout

| Path | Contents |
|---|---|
| `src/pages/*.html` | Page bodies, each with a short header (`title`, `description`, `nav`, `out`) |
| `build.py` | Wraps every page body in the shared header and footer and writes `sitemap.xml` |
| `assets/` | Stylesheet and script shared by all pages |
| `teaching/egm305/` | EGM305 study guides, slides and the Atmosphere Atlas (`atlas/index.html`) |
| `files/` | Downloadable CV (PDF) |

The pamphlet at `/marxist-economics/` is published from its own repository, [AhmadAmmar/marxist-economics](https://github.com/AhmadAmmar/marxist-economics).

## Editing

Edit a file in `src/pages/`, then run

```
python build.py
```

and commit both the source and the generated page. The generated `.html` files in the root and in `teaching/egm305/` should not be edited by hand.

To refresh the CV PDF after editing `src/pages/cv.html`, print `cv.html` to PDF from a browser (the page has a print layout) and save it as `files/Ahmad_Ammar_CV.pdf`.

## Licence

Text and teaching materials © Ahmad Ammar. Data shown in the Atmosphere Atlas remain under the licences of their providers, credited inside the atlas.
