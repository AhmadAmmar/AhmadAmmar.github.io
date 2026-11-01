---
title: Troubleshooting and cheat sheet
slug: troubleshooting
description: Common LaTeX errors with their causes and a one-page reference of commands.
---

## Common errors

| Message | Usual cause | Fix |
|---|---|---|
| `Undefined control sequence` | A misspelt command, or a missing package | Check the spelling, or load the package |
| `Missing $ inserted` | Maths outside maths mode, or an unescaped `_` or `^` | Add `$ $`, or write `\_` |
| `Missing } inserted` | Unbalanced braces | Find the unmatched `{` |
| `File 'x.sty' not found` | A package isn't installed | Install it, or let MiKTeX do so |
| `File 'x' not found` | A wrong image or input path | Check the relative path |
| `Citation 'x' undefined` | The key is wrong, or BibTeX hasn't run | Check the key, then run the full sequence |
| `Reference 'x' undefined` | A missing label, or too few runs | Add the label, or compile again |
| `Overfull \hbox` | A line is too wide | A warning, so rewrite if it's visible |
| `Command \x already defined` | A name clash | Rename your command, as with `\day` |

If a document breaks after a strange failure, delete the helper files and compile again.

## Cheat sheet

```latex
\documentclass[11pt]{article}          % document type
\usepackage{amsmath}                   % load a package
\newcommand{\name}[1]{...#1...}        % your own command
\section{Title}\label{sec:x}           % heading with a label
\ref{sec:x}   \eqref{eq:y}             % refer to a number
\citep{key}                            % citation
\emph{a} \textbf{b} \texttt{c}         % emphasis, bold, code
$a^2$   \[ x \]   \frac{a}{b}          % maths
\includegraphics[width=\linewidth]{f}  % image
\input{file}                           % another file
```

```bash
pdflatex main      # compile
bibtex main        # build the bibliography
latexmk -pdf main  # do all the runs
latexmk -c         # remove helper files
```
