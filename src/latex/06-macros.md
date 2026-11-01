---
title: Your own commands, packages and themes
slug: macros
description: Variables and functions in LaTeX, parameters, counters, custom environments and reusable style files.
---

## LaTeX as a language

LaTeX is a programming language, and its commands behave like functions and variables.

```latex
% A variable: one place to change a value
\newcommand{\studyarea}{Greater London}

% A function with one parameter, used as \term{surplus value}
\newcommand{\term}[1]{\textbf{#1}}

% A function with two parameters, where the first is optional
\newcommand{\money}[2][PKR]{#1~#2}   % \money{160} gives PKR 160
```

`#1` is the first parameter. `\renewcommand` changes an existing command.

## Environments and counters

```latex
\newtheorem{example}{Example}[section]      % numbered within each section

\begin{example}[A coffee-shop worker]
  ...
\end{example}

\newcounter{step}
\stepcounter{step}\thestep
```

## Numbers from your analysis

Don't type results by hand into a document. Have your analysis write a file of commands:

```latex
% Written by a script. Do not edit by hand.
\newcommand{\meanDemand}{369}
```

Then `\input{numbers}` and write `\meanDemand` in the text. When the data changes, the document follows. This prevents the most common errors in scientific writing, as described in the [Git and automation guide](../../git-ci/).

## Your own style file

Put a shared look in a `.sty` file, then load it in any document.

```latex
% mystyle.sty
\ProvidesPackage{mystyle}
\RequirePackage{xcolor}
\definecolor{brand}{HTML}{0D6A6E}
```

```latex
\usepackage{mystyle}
```

For a whole document type, such as a thesis, write a `.cls` class file instead. Most journals and universities supply one. Keep your text separate from the style, so that moving to a different template only needs one change.

## Useful packages

| Package | Purpose |
|---|---|
| `amsmath` | Mathematics |
| `geometry` | Page size and margins |
| `graphicx` | Images |
| `booktabs` | Clean tables |
| `longtable`, `tabularx` | Long and flexible tables |
| `xcolor` | Colour |
| `hyperref` | Links |
| `cleveref` | Automatic reference words |
| `natbib`, `biblatex` | Citations |
| `siunitx` | Numbers and units |
| `tikz`, `pgfplots` | Diagrams and plots |
| `glossaries` | Glossaries and acronyms |
| `tcolorbox` | Coloured boxes |
| `beamer` | Slides, as a class |

Load only what you use, and load `hyperref` late, as it changes many others.
