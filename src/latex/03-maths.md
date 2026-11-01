---
title: Mathematics
slug: maths
description: Inline and displayed equations, symbols, numbering and aligning multi-step derivations.
---

## Inline and displayed

Inline maths sits within a sentence, and displayed maths gets its own line. Load `amsmath` for anything beyond the basics.

```latex
The energy is $E = mc^2$ here.

\[ E = mc^2 \]          % displayed, no number

\begin{equation}        % displayed and numbered
  E = mc^2
  \label{eq:energy}
\end{equation}
```

## The building blocks

| You want | You write |
|---|---|
| Superscript and subscript | `x^2`, `x_i`, `x_{i,j}` |
| Fraction | `\frac{a}{b}` |
| Square root | `\sqrt{x}` |
| Greek letters | `\alpha`, `\mu`, `\Delta` |
| Sum and integral | `\sum_{i=1}^{n}`, `\int_0^1` |
| Operators and relations | `\times`, `\approx`, `\leq`, `\rightarrow` |
| Words in maths | `\text{hours}` |
| Spacing | `\,` small, `\quad` wide |
| Brackets that grow | `\left( \frac{a}{b} \right)` |

Braces group things, so `x^{10}` raises the whole 10, while `x^10` raises only the 1.

## Aligned derivations

Long derivations read best one step per line. Use `&` to mark where lines align, and `\\` to end a line.

```latex
\begin{align}
  r &= \frac{s}{c + v} \\
    &= \frac{e v}{c + v} \\
    &= \frac{e}{1 + c/v}.
\end{align}
```

Each line gets a number, and `align*` removes all of them. `\nonumber` removes one.

## Maths as your own commands

If a symbol means something in your project, name it once, and every use will follow.

```latex
\newcommand{\rate}{\ensuremath{r}}
```

## Tips

- Spell out what each symbol means in the text around the equation.
- Treat an equation as part of a sentence, with punctuation.
- Don't use `$` or `$$` for displayed equations in LaTeX. Use `\[ \]`, because `$$` skips LaTeX's spacing rules.
