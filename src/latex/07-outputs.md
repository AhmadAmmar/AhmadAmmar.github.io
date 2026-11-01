---
title: Slides, Word, web pages and images
slug: outputs
description: Beamer slides, posters, converting LaTeX to Word, PowerPoint, HTML and images with Pandoc and other tools.
---

## Slides with Beamer

!include examples/slides.tex latex

It compiles to three PDF pages, because each reveal is its own page:

::: {.shown .page-row}
![Title slide](img/slides-title.png){alt="A slide with the title Heat Loss Through a Wall and the author A Student."}

![First reveal](img/slides-step-1.png){alt="A slide headed The equation, with one bullet point: Heat loss depends on the wall, its area and the temperature."}

![Second reveal](img/slides-step-2.png){alt="The same slide with a second bullet added, the equation Q = U A delta T."}
:::

`<1->` and `<2->` reveal items one click at a time. `\usetheme` changes the look.

## Posters

The `beamerposter`, `tikzposter` and `baposter` packages make large single pages. Set the paper size, then build it like any other document.

## Word

Journals and co-authors often want `.docx`. Pandoc converts LaTeX, including citations:

```bash
pandoc main.tex -o main.docx --citeproc --bibliography=refs.bib
```

Pandoc writes equations as editable Word equations, and `--csl` with a style file sets the citation style. Complex layouts and custom commands may not survive, so always check the result, especially tables. My [research-helpers](https://github.com/GeospatialGeeks/research-helpers) package has a `latex2docx` tool built for this.

## Web pages

Pandoc also makes HTML. `pandoc main.tex -o main.html --mathjax` gives one page, with equations drawn by MathJax in the browser. For a whole site, split the document by section, and let a site generator such as MkDocs handle the navigation.

Things need care in conversion, so test the result in a browser. In my own [pamphlet project](https://github.com/AhmadAmmar/marxist-economics), these all caused real faults:

- Dollar signs for money turned text into maths.
- Print-only commands such as `\toprule` showed in red inside equations.
- Commands the browser doesn't know, such as `\pounds`, needed defining.
- Labels needed converting into links and numbers.

## PowerPoint and images

PowerPoint has no good route from LaTeX, so the reliable method is to compile to PDF, turn each page into an image, then build a deck with those images and speaker notes:

```python
from research_helpers.carousel import pdf_to_images, images_to_pptx

images = pdf_to_images("slides.pdf", "images", pixels=1440)
images_to_pptx(images, "slides.pptx", notes=["Read this aloud."] * len(images))
```

The slides look exact, though you edit them in LaTeX and not in PowerPoint.

## One source, many outputs

The principle across all of these is to edit one source and generate everything else. The [Git and automation guide](../../git-ci/) shows how to make this happen by itself.
