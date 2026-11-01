---
title: References, links and bibliographies
slug: references
description: Labels and cross-references, citations with BibTeX, and a complete worked report.
---

## Cross-references

Give anything numbered a label, then refer to it. The number updates itself if things move.

```latex
\section{Method}\label{sec:method}
See Section~\ref{sec:method} and Equation~\eqref{eq:energy}.
```

The `~` is a non-breaking space, which keeps "Section" and its number on one line. A prefix such as `sec:`, `eq:`, `tab:` or `fig:` is a helpful habit. The `cleveref` package can add the word for you: `\cref{sec:method}`.

## Citations

Keep references in a separate `.bib` file, and cite them by key:

!include examples/report/refs.bib bibtex

```latex
\usepackage[round]{natbib}
...
As \citet{clarke2001} shows, this holds \citep{clarke2001}.
...
\bibliographystyle{plainnat}
\bibliography{refs}
```

The bibliography tool picks up only the items you cite. Zotero can export a `.bib` file, and its Better BibTeX add-on keeps that file updated. `biblatex` with the `biber` tool is a more flexible alternative, while journals often supply their own `.bst` style for BibTeX.

## A complete small report

This pulls together everything so far: sections, equations, a table, a chart, cross-references, a bibliography and links.

!include examples/report/main.tex latex
