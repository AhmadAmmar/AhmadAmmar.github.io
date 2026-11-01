---
title: "B. Part II: formulas, derivations, data and symbols"
slug: app-p2
description: B. Part II: formulas, derivations, data and symbols: The Atmosphere, a book worked step by step.
---

## B.1 Formulas {#p2-app:formulas}

Every formula used in this part, with the equation number where it is introduced and explained. Temperatures are in kelvin; angles in degrees.

<div class="center">

| **Quantity** | **Formula** | **Where, and what for** |
|:---|:---|:---|
| Speed of a wave | $c=f\lambda$ | Eq. ([12.1](/teaching/atmosphere/p2-ch02_radiation/#p2-eq:cfl)); frequency from wavelength |
| Energy of a photon | $\varepsilon=hc/\lambda$ | Eq. ([12.2](/teaching/atmosphere/p2-ch02_radiation/#p2-eq:photon)); why short waves carry more energy |
| Planck curve | $B_\lambda=\dfrac{2hc^{2}}{\lambda^{5}}\,\dfrac{1}{e^{hc/\lambda k_BT}-1}$ | Eq. ([12.3](/teaching/atmosphere/p2-ch02_radiation/#p2-eq:planck)); the shape of every spectrum |
| Wien’s law | $\lambda_{\max}=C/T$ | Eq. ([13.1](/teaching/atmosphere/p2-ch03_wien/#p2-eq:wien)); peak from temperature (Q1, Q3) |
| Wien’s law, rearranged | $T=C/\lambda_{\max}$ | Eq. ([13.2](/teaching/atmosphere/p2-ch03_wien/#p2-eq:wienT)); temperature from peak (Q1, Q3b) |
| Stefan–Boltzmann law | $E=\sigma T^{4}$ | Eq. ([14.1](/teaching/atmosphere/p2-ch04_stefan/#p2-eq:sb)); total emission (Q2) |
| Ratio of emissions | $E_1/E_2=(T_1/T_2)^{4}$ | Eq. ([14.2](/teaching/atmosphere/p2-ch04_stefan/#p2-eq:ratio4)); Q2e |
| Stefan–Boltzmann, rearranged | $T=(E/\sigma)^{1/4}$ | Eq. ([17.3](/teaching/atmosphere/p2-ch07_balance/#p2-eq:Tinv)); temperature from emission (Q4d) |
| Inverse-square law | $S=S_E/d^{2}$ | Eq. ([16.1](/teaching/atmosphere/p2-ch06_planets/#p2-eq:invsq)); sunlight at each planet (Q3c) |
| Planetary temperature | $T=\left[\dfrac{S(1-a)}{4\sigma}\right]^{1/4}$ | Eq. ([16.2](/teaching/atmosphere/p2-ch06_planets/#p2-eq:Tp)); black-body temperature (Q3c) |
| Absorbed fraction | $1-a$ | Eq. ([17.1](/teaching/atmosphere/p2-ch07_balance/#p2-eq:absorbed)); Q4a–c |
| Global average sunlight | $\bar S=S/4$ | Eq. ([17.2](/teaching/atmosphere/p2-ch07_balance/#p2-eq:Sbar)); Q4b$'$ |
| Sun angle | $\beta=90^\circ-\theta_z$ | Eq. ([18.1](/teaching/atmosphere/p2-ch08_sunangle/#p2-eq:beta)); Q5a |
| Noon zenith angle | $\theta_z=|\varphi-\delta|$, $\delta=\pm23.5^\circ$ at the solstices | Eq. ([18.4](/teaching/atmosphere/p2-ch08_sunangle/#p2-eq:zenith)); Q5a |
| Beam spreading | $A=1/\sin\beta$ | Eq. ([18.2](/teaching/atmosphere/p2-ch08_sunangle/#p2-eq:spread)); Q5a |
| Solar intensity | $I=100\,\%/A=100\,\%\times\sin\beta$ | Eq. ([18.3](/teaching/atmosphere/p2-ch08_sunangle/#p2-eq:intensity)); Q5c |
| Kelvin to Celsius | $T_{\ensuremath{^{\circ}\mathrm{C}}}=T_{\mathrm{K}}-273.16$ | § [11.2](/teaching/atmosphere/p2-ch01_orientation/#p2-sec:conventions) |

</div>

## B.2 Derivations for the curious {#p2-app:derivations}

These derivations show where the formulas of this part come from. None is needed to answer the questions; each is referred to from the chapter where its result is used.

### B.2.1 Wien’s law from the Planck curve {#p2-sec:der-wien}

The peak of the Planck curve, Eq. ([12.3](/teaching/atmosphere/p2-ch02_radiation/#p2-eq:planck)), is where its slope is zero. Write $x=hc/(\lambda k_BT)$, so that a short wavelength is a large $x$. Up to constants that do not depend on $\lambda$, Eq. ([12.3](/teaching/atmosphere/p2-ch02_radiation/#p2-eq:planck)) becomes $$B_\lambda\propto\frac{x^{5}}{e^{x}-1}.$$ Setting the derivative with respect to $x$ to zero: $$\frac{d}{dx}\left(\frac{x^{5}}{e^{x}-1}\right)=\frac{5x^{4}(e^{x}-1)-x^{5}e^{x}}{(e^{x}-1)^{2}}=0
\quad\Longrightarrow\quad 5(e^{x}-1)=xe^{x}
\quad\Longrightarrow\quad x=5\,(1-e^{-x}).$$ This equation has no algebraic solution, but it is easy to solve by repeated substitution: start with $x=5$, then $x=5(1-e^{-5})=4.966$, then $5(1-e^{-4.966})=4.965$, and it settles at $x=4.965$. Turning back to the wavelength, $$\begin{align*}
\lambda_{\max}&=\frac{hc}{4.965\,k_B\,T}=\frac{C}{T},\quad\text{with}\\
C&=\frac{(6.626\times10^{-34})(2.998\times10^{8})}{4.965\times1.381\times10^{-23}}=2.8978\times10^{-3}\ \mathrm{m\,K}=2897.8\ \ensuremath{\mu\mathrm{m\,K}},
\end{align*}$$ which is Eq. ([13.1](/teaching/atmosphere/p2-ch03_wien/#p2-eq:wien)) with $C=2898$ $\mu\mathrm{m\,K}$. (Since $x$ falls steadily as $\lambda$ rises, the peak found in terms of $x$ is the same point as the peak in terms of $\lambda$; and $\lambda^{-5}$ in Eq. ([12.3](/teaching/atmosphere/p2-ch02_radiation/#p2-eq:planck)) is a constant times $x^{5}$, which is where the $x^{5}$ comes from.)

### B.2.2 The Stefan–Boltzmann law from the Planck curve {#p2-sec:der-sb}

The total power leaving one square metre of a black body is $\pi$ times the spectral radiance, Eq. ([12.3](/teaching/atmosphere/p2-ch02_radiation/#p2-eq:planck)), added up over all wavelengths (the factor $\pi$ collects the radiation leaving in every direction above the surface): $$E=\pi\int_{0}^{\infty}B_\lambda(T)\,d\lambda .$$ With the same substitution $x=hc/(\lambda k_BT)$ the integral becomes $$E=\frac{2\pi k_B^{4}T^{4}}{h^{3}c^{2}}\int_{0}^{\infty}\frac{x^{3}}{e^{x}-1}\,dx=\frac{2\pi k_B^{4}T^{4}}{h^{3}c^{2}}\times\frac{\pi^{4}}{15}.$$ All the temperature dependence has come out as $T^{4}$, and the rest is the Stefan–Boltzmann constant: $$\sigma=\frac{2\pi^{5}k_B^{4}}{15\,h^{3}c^{2}}=5.670\times10^{-8}\ \ensuremath{\mathrm{W\,m^{-2}}}\,\mathrm{K}^{-4},$$ which is Eq. ([14.1](/teaching/atmosphere/p2-ch04_stefan/#p2-eq:sb)). The value of the integral, $\pi^{4}/15=6.494$, is a standard result.

### B.2.3 The black-body temperature of a planet {#p2-sec:der-Tp}

This is worked through in full in § [16.4](/teaching/atmosphere/p2-ch06_planets/#p2-sec:Tp): absorbed sunlight on the disc, $S(1-a)\pi R^{2}$, equals emission from the sphere, $\sigma T^{4}4\pi R^{2}$, which gives Eq. ([16.2](/teaching/atmosphere/p2-ch06_planets/#p2-eq:Tp)). Dividing Eq. ([16.2](/teaching/atmosphere/p2-ch06_planets/#p2-eq:Tp)) for two planets shows how temperature scales: $$\frac{T_1}{T_2}=\left(\frac{S_1(1-a_1)}{S_2(1-a_2)}\right)^{1/4},$$ so with equal albedos, a planet at a quarter of the sunlight (twice the distance) is $4^{1/4}=\sqrt2=1.41$ times colder.

### B.2.4 Beam spreading {#p2-sec:der-spread}

In Figure [18.1](/teaching/atmosphere/p2-ch08_sunangle/#p2-fig:spreadgeom), draw a line across the beam at right angles to the rays: its length is the beam width, 1 unit. This line, the strip of ground covered by the beam (length $A$), and the edge ray make a right-angled triangle. The ground strip is the hypotenuse, and the beam width is the side opposite the angle $\beta$ at which the rays meet the ground. By the definition of the sine, $$\sin\beta=\frac{\text{opposite}}{\text{hypotenuse}}=\frac{1}{A}\qquad\Longrightarrow\qquad A=\frac{1}{\sin\beta},$$ which is Eq. ([18.2](/teaching/atmosphere/p2-ch08_sunangle/#p2-eq:spread)). The intensity per unit of ground is the beam’s energy divided by $A$, which is Eq. ([18.3](/teaching/atmosphere/p2-ch08_sunangle/#p2-eq:intensity)). In words: the energy per unit area is proportional to the sine of the sun angle, or equivalently to the cosine of the zenith angle, since $\sin\beta=\cos\theta_z$.

### B.2.5 The noon zenith angle {#p2-sec:der-zenith}

The local vertical at latitude $\varphi$ points along the Earth’s radius, at an angle $\varphi$ from the equatorial plane (Figure [18.2](/teaching/atmosphere/p2-ch08_sunangle/#p2-fig:solstice)). At noon the Sun lies in the same north–south plane, in the direction at angle $\delta$ from the equatorial plane, where $\delta$ is the latitude at which it is overhead. The Sun’s rays are parallel across the Earth, because the Sun is so far away, so the angle between the vertical and the direction of the Sun is the difference of the two angles: $$\theta_z=|\varphi-\delta| ,$$ which is Eq. ([18.4](/teaching/atmosphere/p2-ch08_sunangle/#p2-eq:zenith)). With $\delta=+23.5^\circ$ (June) and $-23.5^\circ$ (December), and a site north of the Tropic of Cancer, this gives $\theta_z=\varphi-23.5^\circ$ and $\theta_z=\varphi+23.5^\circ$. The value $23.5^\circ$ is the tilt of the Earth’s axis to the plane of its orbit (more precisely $23.44^\circ$).

## B.3 The spectra of Question 3, recomputed {#p2-app:data}

Each column of the Question 3 data (Table [15.1](/teaching/atmosphere/p2-ch05_spectra/#p2-tab:q3data)) was compared with the Planck curve, Eq. ([12.3](/teaching/atmosphere/p2-ch02_radiation/#p2-eq:planck)), by finding the temperature and the scale factor that minimise the relative differences between the two. All three columns fit one scale factor, about 316 times the spectral radiance in W m$^{-2}$ sr$^{-1}$ $\mu\mathrm{m}$$^{-1}$, and the best-fitting temperatures are $$T_A=254.1\ \mathrm{K},\qquad T_B=210.0\ \mathrm{K},\qquad T_C=184.1\ \mathrm{K},$$ the black-body temperatures of the Earth, Mars and Venus calculated in Question 3c (Table [16.1](/teaching/atmosphere/p2-ch06_planets/#p2-tab:planets)). Table [B.1](/teaching/atmosphere/app-p2/#p2-tab:fit) sets the given values beside the fitted curves: they agree to within about 0.3 % everywhere, which confirms that the data are Planck curves sampled every 2 $\mu\mathrm{m}$.

<div class="tabular">

@rrrrrrr@ & & &\
(lr)2-3(lr)4-5(lr)6-7 $\lambda$ & given & Planck, 254.1 K & given & Planck, 210.0 K & given & Planck, 184.1 K\
& 26.199 & 26.16 & 1.3338 & 1.338 & 0.11992 & 0.1202\
6 & 386.28 & 385.9 & 53.056 & 53.18 & 10.648 & 10.67\
8 & 970.65 & 969.8 & 218.86 & 219.2 & 65.619 & 65.7\
10 & 1313.3 & 1312 & 398.14 & 398.6 & 151.8 & 151.9\
12 & 1363.5 & 1363 & 502.49 & 503 & 224.7 & 224.9\
14 & 1248.6 & 1248 & 527.86 & 528.3 & 264.23 & 264.4\
16 & 1074.3 & 1074 & 502.41 & 502.8 & 273.39 & 273.5\
18 & 896.25 & 895.8 & 452.58 & 452.9 & 262.51 & 262.6\
20 & 737.1 & 736.7 & 395.22 & 395.4 & 241.03 & 241.1\
22 & 603.1 & 602.8 & 339.25 & 339.4 & 215.38 & 215.5\
24 & 493.45 & 493.2 & 288.62 & 288.8 & 189.36 & 189.4\
26 & 404.91 & 404.7 & 244.61 & 244.7 & 164.92 & 165\
28 & 333.76 & 333.6 & 207.16 & 207.2 & 142.9 & 142.9\
30 & 276.58 & 276.5 & 175.67 & 175.7 & 123.56 & 123.6\
\

</div>

Because the true peaks fall between the 2 $\mu\mathrm{m}$ sampling points, the highest data point in each column lies 0.3–0.6 $\mu\mathrm{m}$ to the right of the true peak. That is why Question 3b, which reads the peak from the data, gives temperatures a few kelvin below the true ones (§ [15.4](/teaching/atmosphere/p2-ch05_spectra/#p2-sec:q3b)).

## B.4 Symbols and constants {#p2-app:symbols}

| $\textbf{Symbol}$ | **Meaning** | **Unit** | **First used** |
|:---|:---|:---|:---|
| $\textbf{Symbol}$ | **Meaning** | **Unit** | **First used** |
| $a$ | albedo: fraction of sunlight reflected | – | Eq. ([16.2](/teaching/atmosphere/p2-ch06_planets/#p2-eq:Tp)) |
| $A$ | beam spreading (the “surface area”) | units | Eq. ([18.2](/teaching/atmosphere/p2-ch08_sunangle/#p2-eq:spread)) |
| $B_\lambda$ | spectral radiance | W m$^{-2}$ sr$^{-1}$ m$^{-1}$ | Eq. ([12.3](/teaching/atmosphere/p2-ch02_radiation/#p2-eq:planck)) |
| $\beta$ | sun angle (solar elevation) | degrees | Eq. ([18.1](/teaching/atmosphere/p2-ch08_sunangle/#p2-eq:beta)) |
| $c$ | speed of light | m s$^{-1}$ | Eq. ([12.1](/teaching/atmosphere/p2-ch02_radiation/#p2-eq:cfl)) |
| $C$ | Wien’s constant | $\mu\mathrm{m\,K}$ | Eq. ([13.1](/teaching/atmosphere/p2-ch03_wien/#p2-eq:wien)) |
| $d$ | distance from the Sun | AU | Eq. ([16.1](/teaching/atmosphere/p2-ch06_planets/#p2-eq:invsq)) |
| $\delta$ | solar declination | degrees | Eq. ([18.4](/teaching/atmosphere/p2-ch08_sunangle/#p2-eq:zenith)) |
| $E$ | emission per square metre (“intensity of radiation”) | $\mathrm{W\,m^{-2}}$ | Eq. ([14.1](/teaching/atmosphere/p2-ch04_stefan/#p2-eq:sb)) |
| $\epsilon$ | emissivity | – | § [12.6](/teaching/atmosphere/p2-ch02_radiation/#p2-sec:blackbody) |
| $\varepsilon$ | energy of one photon | J | Eq. ([12.2](/teaching/atmosphere/p2-ch02_radiation/#p2-eq:photon)) |
| $f$ | frequency | Hz | Eq. ([12.1](/teaching/atmosphere/p2-ch02_radiation/#p2-eq:cfl)) |
| $h$ | Planck’s constant | J s | Eq. ([12.2](/teaching/atmosphere/p2-ch02_radiation/#p2-eq:photon)) |
| $I$ | solar intensity per unit of ground | \% per unit | Eq. ([18.3](/teaching/atmosphere/p2-ch08_sunangle/#p2-eq:intensity)) |
| $k_B$ | Boltzmann’s constant | J K$^{-1}$ | Eq. ([12.3](/teaching/atmosphere/p2-ch02_radiation/#p2-eq:planck)) |
| $\lambda$ | wavelength | m or $\mu\mathrm{m}$ | Eq. ([12.1](/teaching/atmosphere/p2-ch02_radiation/#p2-eq:cfl)) |
| $\lambda_{\max}$ | wavelength of peak emission | $\mu\mathrm{m}$ | Eq. ([13.1](/teaching/atmosphere/p2-ch03_wien/#p2-eq:wien)) |
| $\varphi$ | latitude | degrees | Eq. ([18.4](/teaching/atmosphere/p2-ch08_sunangle/#p2-eq:zenith)) |
| $R$ | radius of a planet | m | § [16.4](/teaching/atmosphere/p2-ch06_planets/#p2-sec:Tp) |
| $S$ | solar constant at a planet | $\mathrm{W\,m^{-2}}$ | Eq. ([16.1](/teaching/atmosphere/p2-ch06_planets/#p2-eq:invsq)) |
| $\bar S$ | sunlight averaged over the globe, day and night | $\mathrm{W\,m^{-2}}$ | Eq. ([17.2](/teaching/atmosphere/p2-ch07_balance/#p2-eq:Sbar)) |
| $\sigma$ | Stefan–Boltzmann constant | $\mathrm{W\,m^{-2}}$ K$^{-4}$ | Eq. ([14.1](/teaching/atmosphere/p2-ch04_stefan/#p2-eq:sb)) |
| $T$ | absolute temperature | K | Eq. ([13.1](/teaching/atmosphere/p2-ch03_wien/#p2-eq:wien)) |
| $\theta_z$ | zenith angle | degrees | Eq. ([18.1](/teaching/atmosphere/p2-ch08_sunangle/#p2-eq:beta)) |

: Table B.2. Every symbol used in this part. Each equation’s own *where* list repeats the symbols it uses.

| **Quantity** | **Value used** | **Precise value** | **Source** |
|:---|:---|:---|:---|
| Wien’s constant $C$ |  $\mu\mathrm{m\,K}$ |  $\mu\mathrm{m\,K}$ | Tiesinga et al. (2021) |
| Stefan–Boltzmann $\sigma$ | $5.67\times10^{-8}$ $\mathrm{W\,m^{-2}}$ K$^{-4}$ | $5.670374\times10^{-8}$ | Tiesinga et al. (2021) |
| Planck’s constant $h$ | – | $6.62607015\times10^{-34}$ J s (exact) | Tiesinga et al. (2021) |
| Speed of light $c$ | – | $2.99792458\times10^{8}$ m s$^{-1}$ (exact) | Tiesinga et al. (2021) |
| Boltzmann’s constant $k_B$ | – | $1.380649\times10^{-23}$ J K$^{-1}$ (exact) | Tiesinga et al. (2021) |
| Solar constant $S$ |  $\mathrm{W\,m^{-2}}$ |  $\mathrm{W\,m^{-2}}$ | Kopp and Lean (2011; <span class="nocase">Prša et al.</span> 2016) |
| Earth’s albedo |  | about 0.29–0.30 | <span class="nocase">Forster et al.</span> (2021; Williams 2024) |
| Kelvin–Celsius offset |  | (exact) | Tiesinga et al. (2021) |
| Earth’s axial tilt | $23.5^\circ$ | $23.44^\circ$ | Stull (2017) |
| Sun’s effective temperature | – |  K | <span class="nocase">Prša et al.</span> (2016) |

: Table B.3. Constants. Answers in this part use the rounded values; the precise values are given for reference.

## B.5 About the figures and the data {#p2-app:about}

### B.5.1 How the figures were made

Every figure in this part was drawn for it as vector graphics, in the document itself with TikZ and pgfplots, so it stays sharp at any size and prints clearly in black and white (each curve has its own line style or marker as well as its own colour).

- The **Planck curves** (Figures [12.3](/teaching/atmosphere/p2-ch02_radiation/#p2-fig:planck-sun-earth), [13.1](/teaching/atmosphere/p2-ch03_wien/#p2-fig:wienfamily) and [15.1](/teaching/atmosphere/p2-ch05_spectra/#p2-fig:q3plot)) are computed from Eq. ([12.3](/teaching/atmosphere/p2-ch02_radiation/#p2-eq:planck)) with the constants of Table [B.3](/teaching/atmosphere/app-p2/#p2-tab:constants).

- The **Question 3 graph** (Figure [15.1](/teaching/atmosphere/p2-ch05_spectra/#p2-fig:q3plot)) plots the values of Table [15.1](/teaching/atmosphere/p2-ch05_spectra/#p2-tab:q3data); the curves through them are the fits described in Appendix [B.3](/teaching/atmosphere/app-p2/#p2-app:data).

- The **planetary temperatures** (Figure [16.2](/teaching/atmosphere/p2-ch06_planets/#p2-fig:planetbars)) are the values of Table [16.1](/teaching/atmosphere/p2-ch06_planets/#p2-tab:planets): calculated with Eq. ([16.2](/teaching/atmosphere/p2-ch06_planets/#p2-eq:Tp)), and the actual averages.

- The **sun-angle sketches** (Figure [18.3](/teaching/atmosphere/p2-ch08_sunangle/#p2-fig:q5sketches)) are drawn to the exact angles of Table [18.1](/teaching/atmosphere/p2-ch08_sunangle/#p2-tab:q5) and to one scale, each beam one unit (5 mm) wide, so the lengths of the red strips can be compared directly.

- The **energy flows** (Figure [17.1](/teaching/atmosphere/p2-ch07_balance/#p2-fig:flow)) are the values of Questions 4b$'$–4d, with arrow widths proportional to the flows.

### B.5.2 Limits to bear in mind

- The black-body model treats each planet as having one temperature, one albedo and no internal heat. It explains the main differences between the planets, not the details of any one of them.

- The sun-angle calculation gives the intensity at *noon* at the top of the atmosphere. Daily totals also depend on day length, and the energy reaching the ground on cloud and on the length of the path through the air (§ [18.5](/teaching/atmosphere/p2-ch08_sunangle/#p2-sec:q5b)).

- Values for the planets (albedos, average temperatures) are rounded here; current measured values are in Williams (2024).

## References

<div id="refs" class="references csl-bib-body hanging-indent" data-entry-spacing="0">

<div id="ref-forster2021" class="csl-entry">

<span class="nocase">Forster, P., Storelvmo, T., Armour, K. and others</span> (2021) The <span class="nocase">Earth’s</span> energy budget, climate feedbacks, and climate sensitivity, in: <span class="nocase">Masson-Delmotte, V. and others (Eds)</span>, Climate Change 2021: The Physical Science Basis. Contribution of Working Group i to the Sixth Assessment Report of the Intergovernmental Panel on Climate Change. Cambridge University Press, Cambridge, pp. 923–1054. <https://doi.org/10.1017/9781009157896.009>

</div>

<div id="ref-kopp2011" class="csl-entry">

Kopp, G. and Lean, J.L. (2011) A new, lower value of total solar irradiance: Evidence and climate significance. Geophysical Research Letters 38, L01706. <https://doi.org/10.1029/2010GL045777>

</div>

<div id="ref-prsa2016" class="csl-entry">

<span class="nocase">Prša, A., Harmanec, P., Torres, G., Mamajek, E. and others</span> (2016) Nominal values for selected solar and planetary quantities: IAU 2015 Resolution B3. The Astronomical Journal 152, 41. <https://doi.org/10.3847/0004-6256/152/2/41>

</div>

<div id="ref-stull2017" class="csl-entry">

Stull, R. (2017) [Practical meteorology: An algebra-based survey of atmospheric science](https://www.eoas.ubc.ca/books/Practical_Meteorology/). University of British Columbia, Vancouver.

</div>

<div id="ref-tiesinga2021" class="csl-entry">

Tiesinga, E., Mohr, P.J., Newell, D.B. and Taylor, B.N. (2021) CODATA recommended values of the fundamental physical constants: 2018. Reviews of Modern Physics 93, 025010. <https://doi.org/10.1103/RevModPhys.93.025010>

</div>

<div id="ref-williams2024" class="csl-entry">

Williams, D.R. (2024) [Planetary fact sheets: Mercury, Venus, Earth, Mars, Jupiter](https://nssdc.gsfc.nasa.gov/planetary/factsheet/).

</div>

</div>

