---
title: Testing research code
slug: testing
description: Known-answer tests, what makes a good test, data checks, and independent recalculation.
---

## Why test

A script that runs without errors can still be wrong. A test runs your code and checks the answer against something you know.

!include examples/calc.py python

!include examples/test_calc.py python

```bash
pip install pytest
python -m pytest
```

## Kinds of test for research

| Test | Question | Example |
|---|---|---|
| **Known answer** | Does it match a hand calculation? | 2.1 x 10 x 15 = 315 |
| **Limit case** | Does it behave at the extremes? | No temperature gap gives no heat loss |
| **Invariant** | Does a rule always hold? | Total price equals total value |
| **Simulated data** | Can it recover a truth you planted? | A model finds a jump you added |
| **Data check** | Is the data as expected? | No duplicates, values in range |
| **Independent recalculation** | Do two separate methods agree? | The same estimate from different code |
| **Rendered output** | Does the result look right to readers? | A browser opens each page |

## Lessons from real faults

These all happened in my own projects:

- **An independent recalculation** confirmed an estimate exactly, and adding a check for correlated data showed its confidence interval was too narrow.
- **A check of stated numbers against results** found a sample size typed wrongly into a paper.
- **A test for labels** found age groups named for the wrong years, though the numbers ran fine.
- **A browser test** found broken links, unreadable buttons and maths that displayed as raw code. Its first version missed some faults, because it looked for error messages and these made none.

So a passing test only shows that the things you tested held. When a fault gets through, add a test for that kind of fault.

## What tests cannot do

They can't show that a method is valid, or an argument sound. That takes reasoning and readers.
