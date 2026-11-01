---
title: "20. Part III at a glance"
slug: p3-ch01_orientation
description: 20. Part III at a glance: The Atmosphere, a book worked step by step.
---

## 20.1 What this part covers

This part has three sections, each building a skill that the next one needs, so it pays to work through them in order. It brings together the two parts before it: the vertical structure of Part I gives the pressure surfaces whose slopes drive the wind, and the uneven solar heating of Part II is what makes them slope.

Moisture.

: How do we say how much water vapour the air holds? You meet four different measures (vapour pressure, mixing ratio, relative humidity and dew point) and learn to move between them with a table and a graph.

Motion.

: Why does the air move at all, and why does it move the way it does? You study the three forces that matter for large-scale winds (the pressure gradient force, the Coriolis force and friction) and see how their balance gives the geostrophic wind high up and a wind that crosses the isobars near the ground.

Weather maps.

: You decode the station model that every weather map uses, draw streamlines from wind barbs, and analyse a whole map: isobars, the low, the fronts, the cloud and the rain.

The moisture questions are numbered 1 to 6. The numbering starts again at 1 for the motion questions, which run to 11, and the weather map questions carry on from 12 to 14. A question of this part is always named with its section, for example *Moisture Q3*, *Motion Q7* or *Map Q12*.

| **Question** | **What it asks** | **Chapter** | **Equations** |
|:---|:---|:---|:---|
| Moisture Q1 | relative humidity of five samples | [21](/teaching/atmosphere/p3-ch02_moisture/#p3-ch:moisture) | ([21.3](/teaching/atmosphere/p3-ch02_moisture/#p3-eq:rh)) |
| Moisture Q2 | heating cold air indoors in winter | [21](/teaching/atmosphere/p3-ch02_moisture/#p3-ch:moisture) | ([21.3](/teaching/atmosphere/p3-ch02_moisture/#p3-eq:rh)) |
| Moisture Q3 | ranking five samples by actual vapour | [21](/teaching/atmosphere/p3-ch02_moisture/#p3-ch:moisture) | ([21.4](/teaching/atmosphere/p3-ch02_moisture/#p3-eq:wrh)) |
| Moisture Q4 | the weakness of relative humidity | [21](/teaching/atmosphere/p3-ch02_moisture/#p3-ch:moisture) |  |
| Moisture Q5 | dew point of 20 $^{\circ}\mathrm{C}$, 10 $\mathrm{g\,kg^{-1}}$ | [22](/teaching/atmosphere/p3-ch03_dewpoint/#p3-ch:dew) | ([21.2](/teaching/atmosphere/p3-ch02_moisture/#p3-eq:we)) |
| Moisture Q6 | dew point of 34 $^{\circ}\mathrm{C}$ at 62 % | [22](/teaching/atmosphere/p3-ch03_dewpoint/#p3-ch:dew) | ([21.4](/teaching/atmosphere/p3-ch02_moisture/#p3-eq:wrh)), ([22.1](/teaching/atmosphere/p3-ch03_dewpoint/#p3-eq:thumb)) |
| Motion Q1–Q6 | pressure surfaces, Saskatoon and Monterrey | [24](/teaching/atmosphere/p3-ch05_surfaces/#p3-ch:surfaces) | ([24.1](/teaching/atmosphere/p3-ch05_surfaces/#p3-eq:hyps)), ([23.1](/teaching/atmosphere/p3-ch04_forces/#p3-eq:pgf)) |
| Motion Q7 | geostrophic wind, north and south | [25](/teaching/atmosphere/p3-ch06_geostrophic/#p3-ch:geo) | ([25.1](/teaching/atmosphere/p3-ch06_geostrophic/#p3-eq:geo)) |
| Motion Q8–Q9 | friction and the forces on a box | [26](/teaching/atmosphere/p3-ch07_friction/#p3-ch:fric) | ([26.1](/teaching/atmosphere/p3-ch07_friction/#p3-eq:friction)) |
| Motion Q10–Q11 | four circulation systems | [26](/teaching/atmosphere/p3-ch07_friction/#p3-ch:fric) | ([26.1](/teaching/atmosphere/p3-ch07_friction/#p3-eq:friction)) |
| Map Q12 | decode four station models | [27](/teaching/atmosphere/p3-ch08_station/#p3-ch:station) | ([27.1](/teaching/atmosphere/p3-ch08_station/#p3-eq:ftoc)) |
| Map Q13 | streamlines | [28](/teaching/atmosphere/p3-ch09_streamlines/#p3-ch:stream) |  |
| Map Q14 | fronts and the full analysis | [29](/teaching/atmosphere/p3-ch10_fronts/#p3-ch:fronts) | ([25.1](/teaching/atmosphere/p3-ch06_geostrophic/#p3-eq:geo)) |

: Table 20.1. Where each question is answered, and the equations it needs.

Chapter [23](/teaching/atmosphere/p3-ch04_forces/#p3-ch:forces) builds the physics of the motion section before its questions; Chapter [30](/teaching/atmosphere/p3-ch11_revision/#p3-ch:revision) gathers every answer in one table. The formulas, the 34 stations of the weather map, derivations and weather symbols are in Appendix [C](/teaching/atmosphere/app-p3/#p3-app).

## 20.2 What to have beside you

- A calculator that has `ln` and `exp` keys, though most questions need only multiplication and division.

- Four coloured pencils for the force diagrams: <span style="color: fred">red</span> for the pressure gradient force, <span style="color: fblue">blue</span> for the Coriolis force, <span style="color: fgreen!80!black">green</span> for friction, and black for the wind.

- A ruler and a soft pencil for the weather map.

## 20.3 Symbols and units

| **Symbol** | **Meaning** | **Unit** |
|:---|:---|:---|
| $T$, $T_d$ | air temperature, dew-point temperature | $^{\circ}\mathrm{C}$ ($^{\circ}\mathrm{F}$ on the station models) |
| $e$, $e_s$ | vapour pressure, saturation vapour pressure | hPa (= mb) |
| $w$, $w_s$ | mixing ratio, saturation mixing ratio | $\mathrm{g\,kg^{-1}}$ |
| RH | relative humidity | \% |
| $p$ | air pressure | hPa (= mb) |
| $z$ | height above the ground | m |
| $\rho$ | air density (about 1.2 kg m$^{-3}$ near the ground) | kg m$^{-3}$ |
| $f$ | Coriolis parameter, $f=2\Omega\sin\varphi$ | s$^{-1}$ |
| $V$, $V_g$ | wind speed, geostrophic wind speed | $\mathrm{m\,s^{-1}}$ (or knots) |
| $\Delta n$ | distance across the isobars (or height lines) | km |

: Table 20.2. The symbols used in Part III.

**Millibar and hectopascal.** Older charts say *mb*; modern texts say *hPa*. They are the same: $1\ \mathrm{mb}=1\ \mathrm{hPa}=100$ Pa. This part uses both.

**Knots.** Wind barbs use knots: $1\ \mathrm{kt}=0.514\ \ensuremath{\mathrm{m\,s^{-1}}}\approx 1.85\ \mathrm{km\,h^{-1}}$.

## 20.4 About the weather map

The weather map shows 34 stations in the central United States on one day. Wind speeds were obtained by counting barbs and are approximate. The fronts were placed by hand from the temperature, dew-point and wind changes, as an analyst would. § [C.2](/teaching/atmosphere/app-p3/#p3-app:stations) lists every station.

