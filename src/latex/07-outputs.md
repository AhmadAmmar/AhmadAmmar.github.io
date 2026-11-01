---
title: Slides, Word, web pages and images
slug: outputs
description: Beamer slides, posters, converting LaTeX to Word, PowerPoint, HTML and images with Pandoc and other tools.
---

## Slides with Beamer

!include examples/slides.tex latex

`<1->` and `<2->` reveal items one click at a time. `\usetheme` changes the look.

## Posters

The `beamerposter`, `tikzposter` and `baposter` packages make large single pages. Set the paper size, then build it like any other document.

## Word

Journals and co-authors often want `.docx`. Pandoc converts LaTeX, including citations:

```bash
pandoc main.tex -o main.docx --citeproc --bibliography=refs.bib
```

Complex layouts and custom commands may not survive, so always check the result. To keep equations as editable Word equations, use a citation style file with `--csl` and check each table. My [research-helpers](https://github.com/GeospatialGeeks/research-helpers) package has a `latex2docx` tool built for this.

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
