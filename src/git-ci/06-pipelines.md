---
title: Reproducible pipelines
slug: pipelines
description: One source and many outputs, shared data, generated numbers and rebuilding everything with one command.
---

## The idea

If you copy a number from your analysis into a paper by hand, sooner or later they will differ. So store each thing once, and generate the rest.

```text
data/figures.json  --->  analysis code  --->  numbers.tex  --->  paper.pdf
                                         \-->  tables and figures
                                          \->  web pages and slides
```

## Rules that prevent most errors

1. **Raw data is read-only.** Scripts read it and write elsewhere.
2. **Numbers in text are generated.** A script writes them as LaTeX commands, for example.
3. **Equations live in one tested function.** Everything calls it.
4. **One command rebuilds everything.** It might be `python build_all.py` or `make`.
5. **Each output records its source**, such as a commit or a checksum.
6. **Generated files say so**, in a comment at the top, so that nobody edits them by hand.
7. **Paths are relative.** `C:\Users\me\data` works only for you.
8. **Random steps have a fixed seed**, so that results repeat exactly.
9. **The environment is recorded**, in a `requirements.txt`, `environment.yml` or container.

## A worked example

My [pamphlet project](https://ahmadammar.github.io/marxist-economics/how-it-works/) has one LaTeX source and one data file. One command builds the website, the PDF, a report, slides and a calculator from them, then checks that they all agree.

When I switched the pamphlet to shared numbers, a check confirmed that the PDF's text hadn't changed at all. That kind of proof is what makes a large change safe.

## Tools for larger projects

| Tool | Good for |
|---|---|
| `make`, Snakemake, Nextflow | Rebuilding only what changed |
| Conda, `venv`, `uv` | Python environments |
| Docker, Apptainer | Whole environments, including on HPC |
| DVC, DataLad, Git LFS | Versioning large data |

Start simple. A short script that runs each step in order goes a long way.
