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

::: {.output}
**What you should see**

```text
$ python -m pytest
============================= test session starts =============================
platform win32 -- Python 3.12.12, pytest-9.2.0, pluggy-1.7.0
rootdir: ...\py
plugins: platformdirs-4.14.2
collected 3 items

test_calc.py ...                                                         [100%]

============================== 3 passed in 0.09s ==============================
```
:::

Each dot is a passing test. To see a failure, I changed `u * area * delta_t` to `u * area + delta_t` in `calc.py`, as if by a slip of the finger. The code still runs without any error, but the tests catch it:

::: {.output}
**What you should see when a test fails (first lines trimmed)**

```text
test_calc.py FF.                                                         [100%]

================================== FAILURES ===================================
______________________________ test_known_answer ______________________________

    def test_known_answer():
>       assert heat_loss(2.1, 10, 15) == pytest.approx(315)
E       assert 36.0 == 315 ± 3.1e-04
E
E         comparison failed
E         Obtained: 36.0
E         Expected: 315 ± 3.1e-04

test_calc.py:8: AssertionError
________________ test_no_temperature_difference_means_no_loss _________________

    def test_no_temperature_difference_means_no_loss():
>       assert heat_loss(2.1, 10, 0) == 0
E       assert 21.0 == 0
E        +  where 21.0 = heat_loss(2.1, 10, 0)

test_calc.py:12: AssertionError
=========================== short test summary info ===========================
FAILED test_calc.py::test_known_answer - assert 36.0 == 315 ± 3.1e-04
FAILED test_calc.py::test_no_temperature_difference_means_no_loss - assert 21...
========================= 2 failed, 1 passed in 0.33s =========================
```
:::

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
