---
title: Structure, text and appearance
slug: text
description: Document classes, sections, contents pages, fonts, colours, lists and page layout.
---

## Document classes

The class sets the overall type of document.

| Class | For |
|---|---|
| `article` | Papers and short reports |
| `report` | Long reports with chapters |
| `book` | Books |
| `beamer` | Slides |

## Headings and contents

```latex
\section{Method}
\subsection{Data}
\subsubsection{Cleaning}
\tableofcontents
```

Numbers come automatically, and adding a star, as in `\section*{Thanks}`, leaves a heading unnumbered and out of the contents. Split long documents into files with `\input{chapter1}`.

## Text and fonts

```latex
\emph{emphasis}  \textbf{bold}  \texttt{code}  \underline{underlined}
{\small smaller text}  {\large larger text}
```

Prefer `\emph` over forcing italics, because it describes meaning, and it adapts when nested. For dashes, `-` joins words, `--` makes ranges such as 10--20, and `---` is a long dash. Quotes are written as two backticks and two apostrophes.

## Fonts

With `pdflatex`, fonts come from packages, for example `\usepackage{helvet}` with `\renewcommand{\familydefault}{\sfdefault}` for a sans-serif body. With `xelatex`, you can name any installed font:

```latex
\usepackage{fontspec}
\setmainfont{Source Serif 4}
```

## Colour

```latex
\usepackage{xcolor}
\definecolor{brand}{HTML}{0D6A6E}
\textcolor{brand}{Coloured text}
```

Define each colour once, by name, so that you can change the whole document from one line. Don't rely on colour alone to carry meaning, because some readers can't see the difference and pages may be printed in black and white.

## Lists

```latex
\begin{itemize}
  \item A point
\end{itemize}
\begin{enumerate}
  \item A first step
\end{enumerate}
```

## Page layout

```latex
\usepackage[a4paper,margin=2.5cm]{geometry}
\usepackage{setspace}
\onehalfspacing
\usepackage{fancyhdr}
\pagestyle{fancy}
```

## Links

```latex
\usepackage{hyperref}            % load this near the end of the preamble
\href{https://example.org}{a link}
\url{https://example.org}
```

`hyperref` also makes every cross-reference and contents entry clickable.
