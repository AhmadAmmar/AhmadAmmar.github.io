---
title: How LaTeX works
slug: basics
description: The structure of a document, how compiling works, commands, environments and reading errors.
---

## The idea

You write a text file ending in `.tex`, and a program called an *engine* turns it into a PDF. That step is called *compiling*. It's closer to running code than to saving a Word file: errors stop it, and the source and result are separate.

!include examples/minimal.tex latex

Compile it with:

```bash
pdflatex minimal
```

::: {.output}
**What you should see at the end of the run**

```text
Output written on minimal.pdf (1 page, 15054 bytes).
Transcript written on minimal.log.
```
:::

::: {.shown}
![The top of minimal.pdf.](img/minimal.png){alt="A line of text reading: Hello, world. One plus one is 1 + 1 = 2, with the sum set in maths."}
:::

This makes `minimal.pdf`, plus helper files such as `minimal.log`, which records what happened, and `minimal.aux`, which remembers numbers between runs.

## The parts of a document

- **The preamble** is everything before `\begin{document}`. It sets the document type and loads packages. Nothing here is printed.
- **The body** is everything between `\begin{document}` and `\end{document}`.

## Syntax

- **A command** starts with a backslash: `\section{Method}`. Required inputs, or *arguments*, go in braces, and optional ones in square brackets: `\documentclass[11pt]{article}`.
- **An environment** has a start and an end, and changes what's between them: `\begin{center}` and `\end{center}`.
- **A comment** starts with `%` and runs to the end of the line.
- **A blank line** starts a new paragraph. Single line breaks and extra spaces are ignored.
- **Special characters** need a backslash to print: `\%`, `\$`, `\&`, `\#`, `\_`, `\{`, `\}`.

## Why you sometimes compile more than once

Numbers for sections, equations and citations are only known after a full pass. LaTeX writes them to the `.aux` file on one run, and reads them on the next. So a contents page or a reference can need two or three runs. A warning saying `Rerun to get cross-references right` means exactly that.

The full sequence with a bibliography is:

```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

On the first run of the [complete report](../references/), LaTeX doesn't yet know the numbers, so it says so. These warnings are normal at this stage, and they went away after the full sequence:

::: {.output}
**What you should see (only the warning and result lines)**

```text
$ pdflatex main
Package natbib Warning: Citation `clarke2001' on page 1 undefined on input line
LaTeX Warning: Reference `sec:method' on page 1 undefined on input line 30.
LaTeX Warning: Reference `tab:walls' on page 1 undefined on input line 31.
LaTeX Warning: Reference `fig:loss' on page 1 undefined on input line 31.
LaTeX Warning: Reference `eq:loss' on page 1 undefined on input line 39.
Package natbib Warning: There were undefined citations.
LaTeX Warning: There were undefined references.
LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right.

$ pdflatex main     (the last run of the sequence)
Output written on main.pdf (2 pages, 107972 bytes).
```
:::

The tool `latexmk -pdf main` works out how many runs are needed and does them for you, though it needs Perl on Windows.

## Choosing an engine

| Engine | Use it when |
|---|---|
| `pdflatex` | The default for most documents, with the widest compatibility |
| `xelatex` | You want system fonts, or scripts such as Urdu and Arabic |
| `lualatex` | You want system fonts plus scripting with Lua |

## Reading errors

An error line starts with `!`. Press Enter past it in a terminal, or use `-interaction=nonstopmode` so that it doesn't stop. Fix the **first** error, because one fault can cause many later ones.

```text
! Undefined control sequence.
l.12 \sectoin
             {Method}
```

This says line 12 uses a command that doesn't exist, here a misspelling. The [troubleshooting chapter](../troubleshooting/) lists common errors.
