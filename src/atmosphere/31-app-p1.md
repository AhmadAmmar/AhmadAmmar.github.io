---
title: "A. Part I: formulas, derivations and symbols"
slug: app-p1
description: A. Part I: formulas, derivations and symbols: The Atmosphere, a book worked step by step.
---

## A.1 Formulas {#p1-sec:formulas}

Every formula used in Part I, with the equation number where it is introduced and explained.

<div class="center">

| **Quantity** | **Formula** | **Where, and what for** |
|:---|:---|:---|
| Ideal gas law | $p=\rho R_dT$ | Eq. ([3.1](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:gaslaw)); density from pressure and temperature (Q13) |
| Hydrostatic balance | $\Delta p/\Delta z=-\rho g$ | Eq. ([3.2](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:hydro)); why pressure falls with height |
| Exponential pressure | $p=p_0e^{-z/H}$, $H=R_dT/g$ | Eq. ([3.3](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:expo)); scale height (Q1, Q12) |
| Fraction of the atmosphere above | $f=2^{-z/5.6}$ ($z$ in km) | Eq. ([3.4](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:fraction)); Q1, Q3 |
| After $n$ halvings | $f_n=1/2^{n}$ | Eq. ([3.5](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:halving)); Table [3.1](/teaching/atmosphere/p1-ch02_pressure/#p1-tab:table1) |
| Pressure from the fraction | $p=1000\,f$ hPa | Eq. ([3.6](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:pressure)); Q2, Q3 |
| Partial pressure of oxygen | $p_{\mathrm{O_2}}=0.21\,p$ | Eq. ([4.1](/teaching/atmosphere/p1-ch03_oxygen/#p1-eq:dalton)); Q4 |
| Lapse rate | $\Gamma=-\Delta T/\Delta z$ | Eq. ([5.1](/teaching/atmosphere/p1-ch04_temperature/#p1-eq:lapse)); Q5, Q7–Q10 |
| Standard atmosphere | $T=15-6.5\,z$ to 11 km, then $-56.5$ $^{\circ}\mathrm{C}$ | Eq. ([5.2](/teaching/atmosphere/p1-ch04_temperature/#p1-eq:stdT)); Q5 |
| Scale height from data | $H=(z_2-z_1)/\ln(p_1/p_2)$ | Eq. ([8.1](/teaching/atmosphere/p1-ch07_stability/#p1-eq:Hdata)); Q12 |
| Dry adiabatic lapse rate | $\Gamma_d=g/c_p=9.8$ $^{\circ}\mathrm{C\,km^{-1}}$ | Eq. ([8.2](/teaching/atmosphere/p1-ch07_stability/#p1-eq:dalr)); Q13 |
| Potential temperature | $\theta=T(1000/p)^{0.286}$ | Eq. ([8.3](/teaching/atmosphere/p1-ch07_stability/#p1-eq:theta)); Q13 |
| Kelvin and Celsius | $T_{\mathrm{K}}=T_{\ensuremath{^{\circ}\mathrm{C}}}+273.15$ | § [1.3](/teaching/atmosphere/how-to-use/#sec:conventions) |

</div>

## A.2 Derivations for the curious {#p1-sec:derivations}

### A.2.1 Pressure falls exponentially with height {#p1-sec:der-expo}

Start from hydrostatic balance, Eq. ([3.2](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:hydro)), written for a very thin layer, $dp/dz=-\rho g$, and replace the density using the gas law, Eq. ([3.1](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:gaslaw)), $\rho=p/(R_dT)$: $$\frac{dp}{dz}=-\frac{g}{R_dT}\,p\qquad\Longrightarrow\qquad\frac{dp}{p}=-\frac{dz}{H},\qquad H=\frac{R_dT}{g}.$$ The rate of fall of $p$ is proportional to $p$ itself. If $T$ (and so $H$) is taken as constant, integrating from sea level ($z=0$, $p=p_0$) to height $z$ gives $\ln(p/p_0)=-z/H$, that is $$p=p_0\,e^{-z/H},$$ which is Eq. ([3.3](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:expo)). The pressure halves when $e^{-z/H}=\tfrac12$, at $z_{1/2}=H\ln2=0.693\,H$; the 5.6 km corresponds to $H=8.08$ km. Writing the same law for two levels and dividing, $p_1/p_2=e^{(z_2-z_1)/H}$, so $\ln(p_1/p_2)=(z_2-z_1)/H$: rearranged, this is Eq. ([8.1](/teaching/atmosphere/p1-ch07_stability/#p1-eq:Hdata)), which gives the scale height of a layer from two lines of a sounding.

**Without calculus.** Divide the atmosphere into thin slabs, each $\Delta z$ thick. By Eqs. ([3.2](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:hydro)) and ([3.1](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:gaslaw)), crossing one slab lowers the pressure by $\Delta p=\rho g\,\Delta z=p\,\Delta z/H$: the same *fraction* $\Delta z/H$ of whatever pressure there is. Removing the same fraction again and again is exactly what an exponential does.

### A.2.2 The dry adiabatic lapse rate and potential temperature {#p1-sec:der-dalr}

The first law of thermodynamics for one kilogram of air says that heat added goes into warming the air and into the work it does as it expands: $dq=c_p\,dT-dp/\rho$. In an adiabatic process no heat is added, $dq=0$, so $$c_p\,dT=\frac{dp}{\rho}.$$ For air moving vertically through an atmosphere in hydrostatic balance, $dp=-\rho g\,dz$, Eq. ([3.2](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:hydro)). Substituting, $$c_p\,dT=-g\,dz\qquad\Longrightarrow\qquad\frac{dT}{dz}=-\frac{g}{c_p}=-\frac{9.81}{1004}=-0.0098\ \mathrm{K\,m^{-1}},$$ which is Eq. ([8.2](/teaching/atmosphere/p1-ch07_stability/#p1-eq:dalr)): dry air cools by 9.8 $^{\circ}\mathrm{C}$ per km as it rises and warms by the same amount as it sinks. Alternatively, dividing $c_p\,dT=dp/\rho$ by $T$ and using $1/\rho=R_dT/p$ gives $c_p\,dT/T=R_d\,dp/p$; integrating from $(T,p)$ to $(\theta,1000\ \ensuremath{\mathrm{hPa}})$, $$c_p\ln\frac{\theta}{T}=R_d\ln\frac{1000}{p}\qquad\Longrightarrow\qquad\theta=T\left(\frac{1000}{p}\right)^{R_d/c_p},$$ which is Eq. ([8.3](/teaching/atmosphere/p1-ch07_stability/#p1-eq:theta)), with $R_d/c_p=287/1004=0.286$ (Wallace and Hobbs 2006, ch. 3).

## A.3 Symbols {#p1-sec:symbols}

| $\textbf{Symbol}$ | **Meaning** | **Unit** | **First used** |
|:---|:---|:---|:---|
| $\textbf{Symbol}$ | **Meaning** | **Unit** | **First used** |
| $c_p$ | specific heat of dry air at constant pressure | J kg$^{-1}$ K$^{-1}$ | Eq. ([8.2](/teaching/atmosphere/p1-ch07_stability/#p1-eq:dalr)) |
| $f$ | fraction of the atmosphere above a height | – | Eq. ([3.4](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:fraction)) |
| $g$ | acceleration due to gravity | m s$^{-2}$ | Eq. ([3.2](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:hydro)) |
| $\Gamma$ | lapse rate | $^{\circ}\mathrm{C\,km^{-1}}$ | Eq. ([5.1](/teaching/atmosphere/p1-ch04_temperature/#p1-eq:lapse)) |
| $\Gamma_d$ | dry adiabatic lapse rate | $^{\circ}\mathrm{C\,km^{-1}}$ | Eq. ([8.2](/teaching/atmosphere/p1-ch07_stability/#p1-eq:dalr)) |
| $H$ | scale height | km | Eq. ([3.3](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:expo)) |
| $p$ | pressure | hPa or Pa | Eq. ([3.1](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:gaslaw)) |
| $p_0$ | pressure at sea level | hPa | Eq. ([3.3](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:expo)) |
| $p_{\mathrm{O_2}}$ | partial pressure of oxygen | hPa | Eq. ([4.1](/teaching/atmosphere/p1-ch03_oxygen/#p1-eq:dalton)) |
| $R_d$ | gas constant for dry air | J kg$^{-1}$ K$^{-1}$ | Eq. ([3.1](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:gaslaw)) |
| $\rho$ | density of the air | kg m$^{-3}$ | Eq. ([3.1](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:gaslaw)) |
| $T$ | temperature | K or $^{\circ}\mathrm{C}$ | Eq. ([3.1](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:gaslaw)) |
| $\theta$ | potential temperature | K | Eq. ([8.3](/teaching/atmosphere/p1-ch07_stability/#p1-eq:theta)) |
| $x_{\mathrm{O_2}}$ | fraction of the molecules that are oxygen | – | Eq. ([4.1](/teaching/atmosphere/p1-ch03_oxygen/#p1-eq:dalton)) |
| $z$ | height above sea level | m or km | Eq. ([3.2](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:hydro)) |

: Table A.1. The symbols used in Part I. Each equation’s own *where* list repeats the symbols it uses.

## A.4 About the figures and the data {#p1-sec:about}

Every figure in Part I was drawn for it in the document itself with TikZ and pgfplots, from the data and the equations in the text.

- The **halving-rule curves** (Figures [3.2](/teaching/atmosphere/p1-ch02_pressure/#p1-fig:q1graph) and [4.1](/teaching/atmosphere/p1-ch03_oxygen/#p1-fig:q3)) are Eq. ([3.4](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:fraction)); the dashed comparison curve and the layered profile of Figure [5.1](/teaching/atmosphere/p1-ch04_temperature/#p1-fig:layers) are the U.S. Standard Atmosphere (NOAA et al. 1976).

- The **soundings** (Figures [6.1](/teaching/atmosphere/p1-ch05_soundings/#p1-fig:soundings), [7.1](/teaching/atmosphere/p1-ch06_lapse/#p1-fig:florida) and [8.1](/teaching/atmosphere/p1-ch07_stability/#p1-fig:q12)) plot the values of Tables [6.1](/teaching/atmosphere/p1-ch05_soundings/#p1-tab:soundings) and [7.1](/teaching/atmosphere/p1-ch06_lapse/#p1-tab:florida), joined by straight lines.

- The **potential temperatures** (Figure [8.2](/teaching/atmosphere/p1-ch07_stability/#p1-fig:theta)) are computed from the soundings with Eq. ([8.3](/teaching/atmosphere/p1-ch07_stability/#p1-eq:theta)), and the **oxygen partial pressures** (Figure [4.2](/teaching/atmosphere/p1-ch03_oxygen/#p1-fig:q4)) with Eq. ([4.1](/teaching/atmosphere/p1-ch03_oxygen/#p1-eq:dalton)).

- The **hydrostatic slab** (Figure [3.1](/teaching/atmosphere/p1-ch02_pressure/#p1-fig:slab)) is a diagram of the forces in Eq. ([3.2](/teaching/atmosphere/p1-ch02_pressure/#p1-eq:hydro)).

- The **tropopause band** of Figure [7.2](/teaching/atmosphere/p1-ch06_lapse/#p1-fig:troplat) and the **ocean-current sketch** of Figure [9.1](/teaching/atmosphere/p1-ch08_climates/#p1-fig:atlantic) are schematic: they show the pattern, not measurements.

The soundings are single ascents on a single day; they illustrate the structure of the atmosphere and should not be read as climatological averages (§ [9.4](/teaching/atmosphere/p1-ch08_climates/#p1-sec:q14)).

<div id="refs" class="references csl-bib-body hanging-indent" data-entry-spacing="0">

<div id="ref-noaa1976" class="csl-entry">

NOAA, NASA and US Air Force (1976) U.S. Standard atmosphere, 1976. U.S. Government Printing Office, Washington, DC.

</div>

<div id="ref-wallace2006" class="csl-entry">

Wallace, J.M. and Hobbs, P.V. (2006) Atmospheric science: An introductory survey, 2nd ed. Elsevier Academic Press, Amsterdam.

</div>

</div>

