# %% [markdown]
# # How to use this notebook
#
# Every test in this guide can be done with a pencil when the data are small. This notebook does exactly that: for each
# test it takes a handful of numbers, writes out **every line of the arithmetic**, one step under the other, and then
# checks the final answer against `scipy.stats`, the library used on the real data. Nothing is typed in by hand: each
# line is computed, so if you change the data and run the cell again, every line of working changes with it.
#
# Each section follows the same order of thinking, the order to follow with your own questions:
#
# 1. **What do we want to measure?** Say the question in words.
# 2. **What kind of data is it?** Counts, measurements, ranks, categories; one group, two groups, pairs, a series in time.
# 3. **How do such data behave?** What spread do they have, and what would they look like if nothing were going on?
# 4. **Which test, and why?** The test whose assumptions match the data.
# 5. **The arithmetic**, line by line, then **the check** in code.
#
# The working is also written to LaTeX files that the printed guide includes, so the PDF and this notebook always agree.

# %%
from math import comb, sqrt, erf
from pathlib import Path

import numpy as np
from scipy import stats

TEX = Path("../tex/by_hand")
TEX.mkdir(parents=True, exist_ok=True) if Path("../tex").exists() else None


def f(x, d=4):
    """A number as it would be written by hand: up to d decimals, no trailing zeros."""
    s = f"{x:.{d}f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class Working:
    """Collects lines of working, prints them, and writes them as a LaTeX align* block."""

    def __init__(self, name):
        self.name, self.lines = name, []

    def step(self, left, right, note=""):
        self.lines.append((left, right, note))

    def show(self):
        for left, right, note in self.lines:
            line = (left + " = " + right) if left else ("    = " + right)
            print(f"{plain(line):72s} {('  <- ' + note) if note else ''}")

    def save(self):
        if not Path("../tex").exists():
            return
        rows = []
        for left, right, note in self.lines:
            rows.append(f"{left} &= {right}" + (f" \\qquad \\text{{\\small ({note})}}" if note else ""))
        (TEX / f"{self.name}.tex").write_text("\\begin{align*}\n" + " \\\\\n".join(rows) + "\n\\end{align*}\n", encoding="utf8")


SYMBOLS = {r"\\times": "×", r"\\sum": "Σ", r"\\le": "≤", r"\\ge": "≥", r"\\chi": "χ", r"\\tau": "τ", r"\\rho": "ρ",
           r"\\mu": "μ", r"\\sigma": "σ", r"\\quad": "   ", r"\\left": "", r"\\right": "", r"\\,": " ", r"\\ ": " ",
           r"\\min": "min", r"\\max": "max"}


def plain(tex):
    """Turn the LaTeX working into readable plain text for the notebook: fractions as (a)/(b), roots as √(x)."""
    import re
    s = tex
    inner = r"\{([^{}]*)\}"
    for _ in range(6):
        s = re.sub(r"([\^_])" + inner, r"\1\2", s)                       # x^{n} -> x^n, S_{xy} -> S_xy
        s = re.sub(r"\\frac" + inner + inner, r"(\1)/(\2)", s)
        s = re.sub(r"\\binom" + inner + inner, r"C(\1, \2)", s)
        s = re.sub(r"\\sqrt" + inner, r"√(\1)", s)
        s = re.sub(r"\\(?:mathrm|text)" + inner, r"\1", s)
        s = re.sub(r"\\bar" + inner, r"\1̄", s)
        s = re.sub(r"\\hat" + inner, r"\1̂", s)
    for k, v in SYMBOLS.items():
        s = re.sub(k + (r"(?![a-zA-Z])" if k[-1].isalpha() else ""), v, s)   # \le must not eat \left
    s = s.replace("{", "").replace("}", "")
    s = re.sub(r"\(([\w.\-]+)\)/\(([\w.\-]+)\)", r"\1/\2", s)          # (a)/(b) -> a/b when both are simple
    return s


def norm_sf(z):
    return 0.5 * (1 - erf(z / sqrt(2)))

# %% [markdown]
# # A coin: the binomial test
#
# **What we want to measure.** Is a coin fair? We toss it 10 times and get 8 heads.
#
# **What kind of data.** A **count of successes** in a fixed number of independent tries, each with the same chance.
#
# **How such data behave.** If the coin is fair, the number of heads follows the **binomial distribution**: the chance
# of exactly k heads in n tosses is C(n, k) / 2ⁿ, where C(n, k) = n! / (k!(n−k)!) counts the orders in which k heads can
# come. Most results land near n/2 = 5; results far from 5 are rare.
#
# **Which test, and why.** With a count this small we do not need any approximation: add up the exact chances of every
# result at least as far from 5 as 8 is (8, 9, 10, and on the other side 2, 1, 0). That sum is the p-value.

# %%
n, k = 10, 8
w = Working("binomial")
w.step(r"P(X = k)", r"\binom{n}{k}\,\frac{1}{2^{n}}", "chance of exactly k heads")
w.step(r"2^{10}", f"{2 ** n}", "number of possible sequences")
for j in (8, 9, 10):
    w.step(fr"\binom{{10}}{{{j}}}", fr"\frac{{10!}}{{{j}!\,{10 - j}!}} = {comb(10, j)}")
upper = sum(comb(n, j) for j in range(k, n + 1))
w.step(r"P(X \ge 8)", r"\frac{" + " + ".join(str(comb(n, j)) for j in range(k, n + 1)) + "}{1024}")
w.step(r"", fr"\frac{{{upper}}}{{1024}}")
w.step(r"", f(upper / 2 ** n), "one tail")
w.step(r"p", fr"2 \times {f(upper / 2 ** n)}", "the other tail, 0 to 2 heads, is the same size")
w.step(r"", f(2 * upper / 2 ** n))
w.show(); w.save()
print("check, scipy.stats.binomtest:", f(stats.binomtest(k, n, 0.5).pvalue))

# %% [markdown]
# **Reading it.** p ≈ 0.11: a fair coin gives a result this lopsided about one time in nine. That is not rare enough to
# call the coin biased at α = 0.05. Ten tosses are simply too few to tell a fair coin from one that lands heads, say,
# 65 % of the time.

# %% [markdown]
# # The z-test for a mean
#
# **What we want to measure.** A thermometer is meant to read 20.0 °C in a bath held at exactly 20.0 °C. Four readings
# give 20.3, 20.1, 20.4 and 20.2 °C. Is it reading high?
#
# **What kind of data.** A few **measurements** of one quantity, with a known measurement spread: the maker says σ =
# 0.2 °C for single readings.
#
# **How such data behave.** Averaging cancels some random error: the mean of n readings scatters less than one reading,
# with **standard error** σ/√n. If nothing is wrong, the mean sits within about ±2 standard errors of 20.0 nineteen times
# in twenty.
#
# **Which test, and why.** σ is known (from the maker, not from these four readings), so we use **z** = (x̄ − μ₀) /
# (σ/√n) and the normal distribution. If σ had to be estimated from the readings themselves, we would use t instead.

# %%
x = np.array([20.3, 20.1, 20.4, 20.2]); mu0, sigma = 20.0, 0.2
w = Working("z_mean")
w.step(r"\bar{x}", r"\frac{" + " + ".join(f(v) for v in x) + "}{4}")
w.step(r"", fr"\frac{{{f(x.sum())}}}{{4}}")
w.step(r"", f(x.mean()))
w.step(r"\mathrm{SE}", r"\frac{\sigma}{\sqrt{n}}")
w.step(r"", fr"\frac{{{f(sigma)}}}{{\sqrt{{4}}}}")
w.step(r"", fr"\frac{{{f(sigma)}}}{{2}}")
w.step(r"", f(sigma / 2))
z = (x.mean() - mu0) / (sigma / 2)
w.step(r"z", r"\frac{\bar{x} - \mu_0}{\mathrm{SE}}")
w.step(r"", fr"\frac{{{f(x.mean())} - {f(mu0)}}}{{{f(sigma / 2)}}}")
w.step(r"", fr"\frac{{{f(x.mean() - mu0)}}}{{{f(sigma / 2)}}}")
w.step(r"", f(z, 2))
w.step(r"p", fr"2 \times P(Z > {f(z, 2)})", "two-sided: too high or too low")
w.step(r"", fr"2 \times {f(norm_sf(z), 4)}")
w.step(r"", f(2 * norm_sf(z), 4))
w.show(); w.save()
print("check, scipy.stats.norm:", f(2 * stats.norm.sf(z), 4))

# %% [markdown]
# **Reading it.** The mean is 20.25 °C, 2.5 standard errors above 20.0, and p ≈ 0.012: a correct thermometer would
# rarely give four readings this high, so it probably reads about 0.25 °C high. Note how n works: a single reading of
# 20.25 would give z = 1.25 and p ≈ 0.21, unremarkable. Averaging four readings halved the standard error and made the
# same offset convincing.

# %% [markdown]
# # The t-test for a trend
#
# **What we want to measure.** Is a station warming? Five years of annual mean temperature anomaly: 0.10, 0.25, 0.20,
# 0.40, 0.45 °C for years 1 to 5.
#
# **What kind of data.** **Pairs** (year, value): a measurement that may change steadily with time.
#
# **How such data behave.** Each year = a straight-line trend + random weather. A fitted slope b is itself uncertain:
# with other weather, the same trend would give a different b. Its spread is the **standard error** SE(b), estimated
# from how far the points scatter around the line.
#
# **Which test, and why.** **t = b / SE(b)** with n − 2 degrees of freedom: we use t, not z, because the scatter is
# estimated from the same five points, which adds uncertainty, and two numbers (slope and intercept) were fitted.

# %%
xs = np.arange(1, 6, dtype=float); ys = np.array([0.10, 0.25, 0.20, 0.40, 0.45])
n = len(xs); xb, yb = xs.mean(), ys.mean()
dx, dy = xs - xb, ys - yb
Sxx, Sxy = (dx ** 2).sum(), (dx * dy).sum()
b = Sxy / Sxx; a = yb - b * xb
fit = a + b * xs; e = ys - fit; SSE = (e ** 2).sum()
s2 = SSE / (n - 2); se_b = sqrt(s2 / Sxx); t = b / se_b
w = Working("t_trend")
w.step(r"\bar{x}", r"\frac{1 + 2 + 3 + 4 + 5}{5}")
w.step(r"", f(xb))
w.step(r"\bar{y}", r"\frac{" + " + ".join(f(v) for v in ys) + "}{5}")
w.step(r"", fr"\frac{{{f(ys.sum())}}}{{5}}")
w.step(r"", f(yb))
w.step(r"S_{xx}", r"\sum (x_i - \bar{x})^2")
w.step(r"", " + ".join(f"({f(d)})^2" for d in dx))
w.step(r"", " + ".join(f(d ** 2) for d in dx))
w.step(r"", f(Sxx))
w.step(r"S_{xy}", r"\sum (x_i - \bar{x})(y_i - \bar{y})")
w.step(r"", " + ".join(f"({f(p)})({f(q)})" for p, q in zip(dx, dy)))
w.step(r"", " + ".join(f"({f(p * q)})" for p, q in zip(dx, dy)))
w.step(r"", f(Sxy))
w.step(r"b", fr"\frac{{S_{{xy}}}}{{S_{{xx}}}} = \frac{{{f(Sxy)}}}{{{f(Sxx)}}}")
w.step(r"", f(b), "degrees C per year")
w.step(r"a", fr"\bar{{y}} - b\,\bar{{x}} = {f(yb)} - {f(b)} \times {f(xb)}")
w.step(r"", f(a))
w.step(r"\hat{y}_i", fr"a + b\,x_i = " + ",\\ ".join(f(v) for v in fit))
w.step(r"e_i", r"y_i - \hat{y}_i = " + ",\\ ".join(f(v) for v in e))
w.step(r"\mathrm{SSE}", r"\sum e_i^2 = " + " + ".join(f"({f(v)})^2" for v in e))
w.step(r"", f(SSE, 5))
w.step(r"s^2", fr"\frac{{\mathrm{{SSE}}}}{{n - 2}} = \frac{{{f(SSE, 5)}}}{{3}}")
w.step(r"", f(s2, 6))
w.step(r"\mathrm{SE}(b)", fr"\sqrt{{\frac{{s^2}}{{S_{{xx}}}}}} = \sqrt{{\frac{{{f(s2, 6)}}}{{{f(Sxx)}}}}}")
w.step(r"", fr"\sqrt{{{f(s2 / Sxx, 7)}}}")
w.step(r"", f(se_b, 5))
w.step(r"t", fr"\frac{{b}}{{\mathrm{{SE}}(b)}} = \frac{{{f(b)}}}{{{f(se_b, 5)}}}")
w.step(r"", f(t, 2))
w.step(r"\mathrm{df}", r"n - 2 = 3")
p_t = 2 * stats.t.sf(t, n - 2)
w.step(r"p", fr"2 \times P(T_3 > {f(t, 2)}) = {f(p_t, 4)}", "from a t table or software")
w.show(); w.save()
lr = stats.linregress(xs, ys)
print("check, scipy.stats.linregress: slope", f(lr.slope), " SE", f(lr.stderr, 5), " p", f(lr.pvalue, 4))

# %% [markdown]
# **Reading it.** The slope is 0.085 °C per year and it is 4.5 standard errors from zero; with only 3 degrees of
# freedom that still gives p ≈ 0.02. Look at how much depends on n: the t distribution with 3 df has heavy tails, so the
# same t with 30 years would give a p-value thousands of times smaller.

# %% [markdown]
# # Welch's t-test: two groups
#
# **What we want to measure.** Is monsoon rain lower in El Niño years? Four El Niño years: 82, 90, 78, 94 (% of
# normal). Five La Niña years: 105, 112, 98, 120, 110.
#
# **What kind of data.** **Two independent groups** of measurements.
#
# **How such data behave.** Each group mean is uncertain by its own standard error, s/√n. The difference of two means
# is uncertain by the two errors combined: variances add, so SE = √(s₁²/n₁ + s₂²/n₂).
#
# **Which test, and why.** **Welch's t** = difference / SE. Welch's version does not assume the groups have the same
# spread, which is safer than the classic equal-variance t-test, and its degrees of freedom come from the
# Welch–Satterthwaite formula, which uses both spreads.

# %%
g1 = np.array([82, 90, 78, 94.0]); g2 = np.array([105, 112, 98, 120, 110.0])
w = Working("welch")
stats_ = []
for name, g in (("1", g1), ("2", g2)):
    m_ = g.mean(); d_ = g - m_; ss = (d_ ** 2).sum(); v_ = ss / (len(g) - 1)
    stats_.append((m_, v_, len(g)))
    w.step(fr"\bar{{x}}_{name}", r"\frac{" + " + ".join(f(v) for v in g) + fr"}}{{{len(g)}}} = \frac{{{f(g.sum())}}}{{{len(g)}}}")
    w.step(r"", f(m_))
    w.step(fr"s_{name}^2", fr"\frac{{\sum (x - \bar{{x}}_{name})^2}}{{n_{name} - 1}}")
    w.step(r"", r"\frac{" + " + ".join(f"({f(v)})^2" for v in d_) + fr"}}{{{len(g) - 1}}}")
    w.step(r"", r"\frac{" + " + ".join(f(v ** 2) for v in d_) + fr"}}{{{len(g) - 1}}}")
    w.step(r"", fr"\frac{{{f(ss)}}}{{{len(g) - 1}}} = {f(v_)}")
(m1, v1, n1), (m2, v2, n2) = stats_
a1, a2 = v1 / n1, v2 / n2
se = sqrt(a1 + a2); tw = (m1 - m2) / se
dfw = (a1 + a2) ** 2 / (a1 ** 2 / (n1 - 1) + a2 ** 2 / (n2 - 1))
w.step(r"\mathrm{SE}", r"\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}")
w.step(r"", fr"\sqrt{{\frac{{{f(v1)}}}{{{n1}}} + \frac{{{f(v2)}}}{{{n2}}}}}")
w.step(r"", fr"\sqrt{{{f(a1)} + {f(a2)}}}")
w.step(r"", fr"\sqrt{{{f(a1 + a2)}}} = {f(se)}")
w.step(r"t", fr"\frac{{\bar{{x}}_1 - \bar{{x}}_2}}{{\mathrm{{SE}}}} = \frac{{{f(m1)} - {f(m2)}}}{{{f(se)}}}")
w.step(r"", fr"\frac{{{f(m1 - m2)}}}{{{f(se)}}} = {f(tw, 3)}")
w.step(r"\mathrm{df}", r"\frac{\left(\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}\right)^2}{\frac{(s_1^2/n_1)^2}{n_1 - 1} + \frac{(s_2^2/n_2)^2}{n_2 - 1}}")
w.step(r"", fr"\frac{{({f(a1 + a2)})^2}}{{\frac{{{f(a1)}^2}}{{{n1 - 1}}} + \frac{{{f(a2)}^2}}{{{n2 - 1}}}}}")
w.step(r"", fr"\frac{{{f((a1 + a2) ** 2)}}}{{{f(a1 ** 2 / (n1 - 1))} + {f(a2 ** 2 / (n2 - 1))}}}")
w.step(r"", f(dfw, 2))
pw = 2 * stats.t.sf(abs(tw), dfw)
w.step(r"p", fr"2 \times P(T_{{{f(dfw, 2)}}} > {f(abs(tw), 3)}) = {f(pw, 5)}")
w.show(); w.save()
r_ = stats.ttest_ind(g1, g2, equal_var=False)
print("check, scipy.stats.ttest_ind(equal_var=False): t", f(r_.statistic, 3), " df", f(r_.df, 2), " p", f(r_.pvalue, 5))

# %% [markdown]
# **Reading it.** The El Niño years average 86 % of normal and the La Niña years 109 %, a difference of 23 points,
# about 4.4 standard errors. With about 6.9 degrees of freedom that is p ≈ 0.003. Notice that df is not a whole number:
# the Welch–Satterthwaite formula estimates how much information the two variances carry together.

# %% [markdown]
# # Mann–Whitney U: two groups by ranks
#
# **What we want to measure.** The same question, without trusting the actual values: does one group **tend** to be
# larger? Useful when a single extreme year could pull a mean, or the data are not near normal.
#
# **What kind of data.** Two independent groups, used only through their **order**.
#
# **How such data behave.** Put all values in one queue from smallest to largest. If the groups do not differ, group 1's
# positions are a random pick from the queue, so their sum of ranks has a known spread.
#
# **Which test, and why.** **U** counts, over all pairs (one value from each group), how often group 1's value is the
# larger. Below, A marks the El Niño years and B the La Niña years. With 4 × 5 = 20 pairs, U runs from 0 to 20; under H₀ it is near 10. For groups this small the exact p-value
# comes from listing every way the ranks could fall.

# %%
allv = np.r_[g1, g2]; ranks = stats.rankdata(allv)
r1 = ranks[:n1].sum(); U1 = r1 - n1 * (n1 + 1) / 2; U2 = n1 * n2 - U1
w = Working("mann_whitney")
order = np.argsort(allv)
w.step(r"\text{sorted}", ",\\ ".join(f"{f(allv[i])}_{{{'A' if i < n1 else 'B'}}}" for i in order))
w.step(r"\text{ranks of A}", ",\\ ".join(f(v) for v in ranks[:n1]))
w.step(r"R_A", " + ".join(f(v) for v in ranks[:n1]) + f" = {f(r1)}")
w.step(r"U_A", r"R_A - \frac{n_A(n_A + 1)}{2}")
w.step(r"", fr"{f(r1)} - \frac{{{n1} \times {n1 + 1}}}{{2}}")
w.step(r"", fr"{f(r1)} - {f(n1 * (n1 + 1) / 2)} = {f(U1)}")
w.step(r"U_B", fr"n_A n_B - U_A = {n1} \times {n2} - {f(U1)} = {f(U2)}")
w.step(r"U", fr"\min(U_A, U_B) = {f(min(U1, U2))}")
ways = comb(n1 + n2, n1)
w.step(r"\text{ways to choose A's ranks}", fr"\binom{{{n1 + n2}}}{{{n1}}} = {ways}")
w.step(r"P(U \le 0)", fr"\frac{{1}}{{{ways}}}", "only one arrangement puts all of A at the bottom")
w.step(r"p", fr"2 \times \frac{{1}}{{{ways}}} = {f(2 / ways, 4)}", "two-sided")
w.show(); w.save()
print("check, scipy.stats.mannwhitneyu (exact):", f(stats.mannwhitneyu(g1, g2, alternative='two-sided', method='exact').pvalue, 4))

# %% [markdown]
# **Reading it.** Every El Niño year is drier than every La Niña year, so U = 0, the most extreme value possible. With
# only 126 ways to place four ranks among nine, the smallest possible two-sided p is 2/126 ≈ 0.016. That is a lesson in
# itself: with tiny samples a rank test **cannot** give a very small p-value, however clear the pattern.

# %% [markdown]
# # Correlation: Pearson and Spearman
#
# **What we want to measure.** Do two things move together? Five years of a Pacific temperature index (ONI, °C) and
# monsoon rain (% of normal).
#
# **What kind of data.** **Pairs** of measurements on the same years.
#
# **How such data behave.** If high ONI goes with low rain, the points fall along a downward line. **Pearson's r**
# measures how tightly they hug a straight line, from −1 to +1. It is the covariance scaled by both spreads, so it has
# no units.
#
# **Which test, and why.** For H₀: no linear relation, t = r √(n − 2) / √(1 − r²) with n − 2 df. **Spearman's ρ** does
# the same with ranks, for any steady (not necessarily straight) relation, and is less swayed by one odd year.

# %%
oni = np.array([-1.2, -0.4, 0.1, 0.8, 1.5]); rain = np.array([112, 104, 101, 92, 85.0])
dx, dy = oni - oni.mean(), rain - rain.mean()
Sxx, Syy, Sxy = (dx ** 2).sum(), (dy ** 2).sum(), (dx * dy).sum()
r = Sxy / sqrt(Sxx * Syy); n = len(oni)
tr = r * sqrt(n - 2) / sqrt(1 - r ** 2)
w = Working("pearson")
w.step(r"\bar{x}", fr"{f(oni.mean())}, \quad \bar{{y}} = {f(rain.mean())}")
w.step(r"x_i - \bar{x}", ",\\ ".join(f(v) for v in dx))
w.step(r"y_i - \bar{y}", ",\\ ".join(f(v) for v in dy))
w.step(r"S_{xx}", " + ".join(f(v ** 2) for v in dx) + f" = {f(Sxx)}")
w.step(r"S_{yy}", " + ".join(f(v ** 2) for v in dy) + f" = {f(Syy)}")
w.step(r"S_{xy}", " + ".join(f"({f(p * q)})" for p, q in zip(dx, dy)) + f" = {f(Sxy)}")
w.step(r"r", fr"\frac{{S_{{xy}}}}{{\sqrt{{S_{{xx}}\,S_{{yy}}}}}} = \frac{{{f(Sxy)}}}{{\sqrt{{{f(Sxx)} \times {f(Syy)}}}}}")
w.step(r"", fr"\frac{{{f(Sxy)}}}{{\sqrt{{{f(Sxx * Syy)}}}}} = \frac{{{f(Sxy)}}}{{{f(sqrt(Sxx * Syy))}}}")
w.step(r"", f(r))
w.step(r"t", fr"\frac{{r\sqrt{{n - 2}}}}{{\sqrt{{1 - r^2}}}} = \frac{{{f(r)} \times \sqrt{{3}}}}{{\sqrt{{1 - {f(r ** 2)}}}}}")
w.step(r"", fr"\frac{{{f(r * sqrt(3))}}}{{{f(sqrt(1 - r ** 2))}}} = {f(tr, 2)}")
pr = 2 * stats.t.sf(abs(tr), n - 2)
w.step(r"p", fr"2 \times P(T_3 > {f(abs(tr), 2)}) = {f(pr, 5)}")
rx, ry = stats.rankdata(oni), stats.rankdata(rain); dd = rx - ry
rho = 1 - 6 * (dd ** 2).sum() / (n * (n ** 2 - 1))
w.step(r"\text{ranks of } x", ",\\ ".join(f(v) for v in rx))
w.step(r"\text{ranks of } y", ",\\ ".join(f(v) for v in ry))
w.step(r"d_i", ",\\ ".join(f(v) for v in dd))
w.step(r"\rho", r"1 - \frac{6\sum d_i^2}{n(n^2 - 1)} = 1 - \frac{6 \times " + f((dd ** 2).sum()) + r"}{5 \times 24}")
w.step(r"", f(rho))
w.show(); w.save()
print("check, scipy.stats.pearsonr:", f(stats.pearsonr(oni, rain)[0]), f(stats.pearsonr(oni, rain)[1], 5),
      "  spearmanr:", f(stats.spearmanr(oni, rain)[0]))

# %% [markdown]
# **Reading it.** r ≈ −0.996: in these five made-up years the points lie almost exactly on a falling line, and even with
# n = 5 that is p ≈ 0.0003. Spearman's ρ is exactly −1 because the order is perfectly reversed. Real data are never this
# tidy (the guide's 50 real years give r ≈ −0.43); small examples are chosen so the arithmetic is easy to follow.

# %% [markdown]
# # Mann–Kendall: a trend by counting
#
# **What we want to measure.** Has June snow cover gone down? Six years (million km²): 9.1, 8.7, 8.9, 8.2, 7.9, 8.0.
#
# **What kind of data.** A **time series** where we only trust the order: is later lower?
#
# **How such data behave.** Compare every later year with every earlier one. With no trend, "later is higher" and
# "later is lower" are equally likely, so their difference S is near zero, with a variance that depends only on n.
#
# **Which test, and why.** **Mann–Kendall** uses S = Σ sign(xⱼ − xᵢ) over all pairs i < j. It needs no straight line
# and no normality, which is why it is common for snow, rivers and rainfall.

# %%
xs_ = np.array([9.1, 8.7, 8.9, 8.2, 7.9, 8.0]); n = len(xs_)
pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
signs = [int(np.sign(xs_[j] - xs_[i])) for i, j in pairs]
S = sum(signs); varS = n * (n - 1) * (2 * n + 5) / 18
Z = (S + 1) / sqrt(varS) if S < 0 else (S - 1) / sqrt(varS)
w = Working("mann_kendall")
w.step(r"\text{pairs}", fr"\frac{{n(n-1)}}{{2}} = \frac{{6 \times 5}}{{2}} = {len(pairs)}")
for i in range(n - 1):
    row = [s for (a_, b_), s in zip(pairs, signs) if a_ == i]
    w.step(fr"\text{{year {i + 1} vs later}}", ",\\ ".join(("+" if s > 0 else "-" if s < 0 else "0") + "1" for s in row) + f" \\quad (sum {sum(row)})")
w.step(r"S", f"{S}", "more falls than rises")
w.step(r"\tau", fr"\frac{{S}}{{n(n-1)/2}} = \frac{{{S}}}{{15}} = {f(S / 15)}")
w.step(r"\mathrm{Var}(S)", r"\frac{n(n-1)(2n+5)}{18} = \frac{6 \times 5 \times 17}{18}")
w.step(r"", f(varS))
w.step(r"Z", fr"\frac{{S + 1}}{{\sqrt{{\mathrm{{Var}}(S)}}}} = \frac{{{S + 1}}}{{\sqrt{{{f(varS)}}}}} = \frac{{{S + 1}}}{{{f(sqrt(varS))}}}", "+1: continuity correction")
w.step(r"", f(Z, 3))
w.step(r"p", fr"2 \times P(Z > {f(abs(Z), 3)}) = {f(2 * norm_sf(abs(Z)), 4)}")
w.show(); w.save()
tau_, p_ = stats.kendalltau(np.arange(n), xs_)
print("check, scipy.stats.kendalltau: tau", f(tau_), " p", f(p_, 4), "(exact; the normal approximation above is close)")

# %% [markdown]
# **Reading it.** Of 15 pairs, 13 fall and 2 rise, so S = −11 and τ = −0.73: later years are mostly lower. The normal
# approximation gives p ≈ 0.06 and scipy's exact calculation for n = 6 gives 0.056: just above 0.05. Six years are too
# few to be sure of a trend, however clear it looks. The working shows where the
# numbers come from: τ is just the balance of falls over rises, as a share of all pairs.

# %% [markdown]
# # Chi-square: counts in a table
#
# **What we want to measure.** Do flooded radar cells lie where water had been seen before? 100 cells, sorted two ways.
#
# **What kind of data.** **Counts in categories**: each cell is yes/no for "water seen before" and yes/no for "dark in 2022".
#
# **How such data behave.** If the two were unrelated, each row would split between the columns in the same proportions
# as the whole table. That gives an **expected** count for every cell: row total × column total / grand total.
#
# **Which test, and why.** **χ² = Σ (O − E)² / E** adds up how far observed counts are from expected, each relative to
# its expected size. With a 2 × 2 table, df = (2 − 1)(2 − 1) = 1. **Cramér's V** turns χ² into a strength from 0 to 1.

# %%
O = np.array([[42, 18], [10, 30.0]])          # rows: water before no / yes; columns: dark no / yes
rt, ct, N = O.sum(1), O.sum(0), O.sum()
E = np.outer(rt, ct) / N
cells = ((O - E) ** 2 / E)
chi2 = cells.sum(); V = sqrt(chi2 / N)
w = Working("chi_square")
w.step(r"\text{row totals}", f"{f(rt[0])},\\ {f(rt[1])}; \\quad \\text{{column totals}}\\ {f(ct[0])},\\ {f(ct[1])}; \\quad N = {f(N)}")
names = [["no, no", "no, yes"], ["yes, no", "yes, yes"]]
for i in range(2):
    for j in range(2):
        w.step(fr"E_{{{i + 1}{j + 1}}}", fr"\frac{{{f(rt[i])} \times {f(ct[j])}}}{{{f(N)}}} = {f(E[i, j])}", f"before {names[i][j].split(',')[0]}, dark{names[i][j].split(',')[1]}")
for i in range(2):
    for j in range(2):
        w.step(fr"\frac{{(O - E)^2}}{{E}}_{{{i + 1}{j + 1}}}", fr"\frac{{({f(O[i, j])} - {f(E[i, j])})^2}}{{{f(E[i, j])}}} = \frac{{{f((O[i, j] - E[i, j]) ** 2)}}}{{{f(E[i, j])}}} = {f(cells[i, j])}")
w.step(r"\chi^2", " + ".join(f(c) for c in cells.ravel()))
w.step(r"", f(chi2, 3))
w.step(r"\mathrm{df}", r"(2 - 1)(2 - 1) = 1")
pc = stats.chi2.sf(chi2, 1)
w.step(r"p", fr"P(\chi^2_1 > {f(chi2, 3)}) = {pc:.2e}".replace("e-0", r"\times 10^{-").replace("e-", r"\times 10^{-") + "}")
w.step(r"V", fr"\sqrt{{\frac{{\chi^2}}{{N}}}} = \sqrt{{\frac{{{f(chi2, 3)}}}{{{f(N)}}}}} = {f(V, 3)}")
w.show(); w.save()
c_ = stats.chi2_contingency(O, correction=False)
print("check, scipy.stats.chi2_contingency:", f(c_[0], 3), f"{c_[1]:.2e}")

# %% [markdown]
# **Reading it.** Of the 40 cells where water had been seen before, 30 were dark (75 %); of the 60 others, 18 were
# (30 %). Independence would have put 20.8 dark cells in the first row, not 30. χ² ≈ 19.5 on 1 df, p ≈ 10⁻⁵, and V ≈
# 0.44: a moderate to strong association. Each of the four terms shows which cells drive it.

# %% [markdown]
# # Benjamini–Hochberg: many p-values
#
# **What we want to measure.** Six map pixels were each tested for a trend. Which results should we believe?
#
# **What kind of data.** A **list of p-values**, one per test.
#
# **How such data behave.** Where nothing is happening, p-values are spread evenly between 0 and 1, so some fall below
# 0.05 by chance. The more tests, the more such false alarms.
#
# **Which test, and why.** **Benjamini–Hochberg** sorts the p-values and compares the k-th smallest with (k / m) q,
# where m is the number of tests and q the share of false discoveries we accept. The largest k that passes, and all
# smaller ones, are kept. It controls the share of false findings rather than the chance of any one, which suits maps.

# %%
pv = np.array([0.001, 0.008, 0.039, 0.041, 0.042, 0.60]); m, q = len(pv), 0.05
srt = np.sort(pv)
w = Working("bh")
w.step(r"m", fr"{m}, \quad q = {f(q)}")
passing = []
for k_, p_ in enumerate(srt, 1):
    th = k_ / m * q
    ok = p_ <= th
    passing.append(ok)
    w.step(fr"p_{{({k_})}} = {f(p_)}", fr"\frac{{{k_}}}{{{m}}} \times {f(q)} = {f(th)}", "pass" if ok else "fail")
kmax = max([i + 1 for i, ok in enumerate(passing) if ok], default=0)
w.step(r"k_{\max}", f"{kmax}", f"keep the {kmax} smallest p-values")
w.show(); w.save()
adj = stats.false_discovery_control(pv, method="bh")
print("check, scipy.stats.false_discovery_control:", [f(v, 3) for v in adj], "-> significant:", int((adj <= q).sum()))
print("plain p < 0.05 would keep:", int((pv < 0.05).sum()))

# %% [markdown]
# **Reading it.** Five of the six p-values are below 0.05, but under Benjamini–Hochberg only the two smallest survive:
# the next three, all near 0.04, are what a handful of pixels with no trend would produce among six tests. Two pixels
# with real change, not five, is the honest map.
