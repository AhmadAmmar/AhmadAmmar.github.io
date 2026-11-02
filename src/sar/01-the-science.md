---
title: "1. The science behind the images"
slug: the-science
description: 1. The science behind the images: Reading radar images, a working manual.
---

## 1.1 Why radar sees what it sees

A radar sends a pulse and times its return. Distance comes from time, as $R = ct/2$, where $c$ is the speed of light and the 2 accounts for the trip out and back. Sentinel-1 uses C band: a frequency of 5.405 GHz, which is a wavelength of $\lambda = c/f \approx 5.5$ cm. Features much smaller than this look smooth to the radar, which is why calm water and tarmac act like mirrors.

The sensor looks sideways, not straight down. If it looked straight down, two points at equal distance either side would return together and could not be told apart. Looking sideways at about 29 to 46 degrees in this mode solves that, and also causes the distortions described below.

## 1.2 What backscatter is

The radar equation says how much power returns: $$
P_r = \frac{P_t\, G^2\, \lambda^2\, \sigma}{(4\pi)^3 R^4}
$$ Here $P_t$ is power sent, $G$ antenna gain, $R$ range and $\sigma$ the radar cross-section of the target. Everything but $\sigma$ is known about the instrument and geometry, so it can be removed by calibration. For a surface, $\sigma$ is divided by the ground area to give $\sigma^0$ (sigma nought), a dimensionless ratio that can be compared between places and dates.

## 1.3 What a decibel is

Backscatter spans many orders of magnitude, from about 0.001 for calm water to above 10 for a building’s corner. A logarithmic scale fits this on a readable range: $$
\sigma^0_{\mathrm{dB}} = 10\log_{10}\bigl(\sigma^0_{\mathrm{linear}}\bigr), \qquad \sigma^0_{\mathrm{linear}} = 10^{\sigma^0_{\mathrm{dB}}/10}
$$

<div class="center">

| Linear |    dB | Meaning                       |
|-------:|------:|:------------------------------|
|  0.001 | $-30$ | A thousandth of the reference |
|   0.01 | $-20$ | A hundredth                   |
|    0.1 | $-10$ | A tenth                       |
|      1 |     0 | Equal to the reference        |
|      2 |  $+3$ | About double                  |
|     10 | $+10$ | Ten times                     |

</div>

Decibels are ratios, so a difference in dB is a ratio in power. A change from $-10$ to $-13$ dB means half the power returned, wherever it happens on the scale. Negative values are normal and do not mean negative energy: they mean less than the reference.

##### Why averaging in dB is wrong.

Take two pixels at $-30$ and $0$ dB. Their mean in dB is $-15$ dB. In linear units, the mean of 0.001 and 1 is 0.5005, which is $-3$ dB. The dB mean is lower by 12 dB, a factor of about 16 in power, because a logarithm gives the dim pixel too much weight. So we average in linear power, as `mean_db()` does in Chapter [2](/teaching/sar/reading-radar-london/#sec:basics). Over a year of London scenes this matters most at strong targets, whose returns vary.

## 1.4 Polarisation: what VV and VH tell us

The radar’s wave oscillates in one plane. Sentinel-1 sends vertically (V) and receives both V and horizontal (H). Each surface changes this differently:

| Mechanism | What happens and where |
|:---|:---|
| Surface scattering | Rough ground reflects some energy back, mostly keeping polarisation, so VV is above VH |
| Volume scattering | Repeated scattering among leaves and branches scrambles polarisation, so VH rises |
| Double bounce | Ground and wall form a corner that returns energy strongly, so VV is very high, as in cities and flooded forest |
| Specular reflection | A smooth surface reflects energy away, so both are low, as on calm water |

The ratio VV minus VH (in dB, which is a ratio in linear terms) separates these partly, which is why it serves as the third band in our colour image.

## 1.5 Speckle

##### What it is.

A pixel holds many scatterers. Their returns add as waves with random phases, sometimes reinforcing and sometimes cancelling. So uniform ground looks grainy, even with a perfect instrument. Viewed the same way, the same ground gives the same grain, which makes it a form of interference and not random instrument noise.

##### The model.

Speckle is multiplicative: observed intensity $I$ is the true backscatter $\sigma^0$ times a random factor $n$ with mean 1: $$
I = \sigma^0 \cdot n, \qquad \mathrm{E}[n]=1, \qquad \mathrm{Var}[n] = 1/L
$$ Multiplicative means brighter areas have larger swings in linear units, and a logarithm turns these into a roughly constant spread. $L$ is the number of looks, or independent samples averaged. It can be estimated from a uniform area as the *equivalent number of looks*: $$
\mathrm{ENL} = \frac{\bar{I}^{\,2}}{\mathrm{Var}(I)}
$$

##### Measured here.

Over the most uniform 300 m patch near central London, ENL is 4.4 in one scene and 20.9 in the mean of 149 scenes. The increase is less than 149-fold, because the patch is not perfectly uniform and because real changes through the year remain. This also suggests a limit: averaging removes speckle at the cost of time detail, and filters such as Lee or Refined Lee remove it at the cost of spatial detail.

## 1.6 What has been done to the data

The Earth Engine collection `COPERNICUS/S1_GRD` holds Ground Range Detected scenes, already processed as follows:

1.  **Orbit file:** precise position of the satellite.

2.  **GRD border noise removal:** low-value strips at scene edges.

3.  **Thermal noise removal:** the instrument’s own noise.

4.  **Radiometric calibration:** digital numbers to $\sigma^0$.

5.  **Terrain correction:** moved to map position with a digital elevation model.

6.  **Conversion to dB.**

It has not had speckle filtering or radiometric terrain flattening, so slopes facing the satellite stay bright. “Detected” also means phase has been discarded, so these scenes cannot be used for interferometry, and subsidence needs a different product.

## 1.7 Three distortions of mountains

Because radar measures distance, tall things shift towards the sensor:

- **Foreshortening:** slopes facing the radar look compressed and bright.

- **Layover:** the top of a steep slope or tower returns before its base, and appears displaced towards the sensor.

- **Shadow:** slopes facing away receive no signal and look black.

You can see the first of these in the hills in the lower left of the Sindh map, and the second in London’s towers. In both cases brightness reflects geometry, not material.

## 1.8 Reading rules

1.  Dark usually means smooth, or facing away. It does not always mean water.

2.  Bright usually means rough, wet, or a corner. It does not always mean buildings.

3.  Compare like with like: the same pass direction and season.

4.  Average in linear power, and report in dB.

5.  Trust change between dates more than a single absolute value.

