# %% [markdown]
# # 03 · Making maps and graphics that tell the truth, and making them interactive
#
# A map is an argument. This notebook shows the choices that change what a reader sees (classes, colours,
# normalisation), then several kinds of map and chart, then interactivity inside the notebook:
#
# | Tool | Use | Works when shared |
# |---|---|---|
# | matplotlib / geopandas `.plot()` | print-quality static maps and figures | always (image) |
# | geopandas `.explore()` / **folium** | zoomable web maps with hover, layers, heat maps, side-by-side | yes (HTML saved in the notebook) |
# | **plotly** | interactive charts: hover, zoom, filter by legend | yes |
# | **ipywidgets** | sliders and menus that re-run code | only in a live notebook (Jupyter, Colab, VS Code) |

# %% [markdown]
# *Running this in Google Colab?* The next cell installs the few libraries Colab lacks (about a minute). Notebooks
# 04-07 read files made by 01 and 02: run those first in the same session, or keep the `data` folder on Google Drive.

# %%
import sys, subprocess
if "google.colab" in sys.modules:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "osmnx", "overturemaps", "mapclassify", "esda", "libpysal", "folium", "plotly"], check=True)

# %%
import warnings; warnings.filterwarnings("ignore")
from pathlib import Path
import numpy as np, pandas as pd, geopandas as gpd, matplotlib.pyplot as plt, mapclassify as mc
DATA, CRS = Path("data"), 32642
grid = gpd.read_file(DATA / "grid_500m.gpkg")
area = gpd.read_file(DATA / "boundary.gpkg").to_crs(CRS)
poi = gpd.read_file(DATA / "places.gpkg").to_crs(CRS)
lived = grid[grid.people > 50].copy()
lived["people_per_ha"] = lived.people / 25

# %% [markdown]
# ## 1. Same data, four maps: class schemes change the story

# %%
fig, ax = plt.subplots(1, 4, figsize=(20, 5.5))
for a, s in zip(ax, ["EqualInterval", "Quantiles", "NaturalBreaks", "HeadTailBreaks"]):
    lived.plot("people_per_ha", scheme=s, k=5, cmap="YlOrRd", ax=a, legend=True, legend_kwds={"loc": "lower left", "fontsize": 7, "fmt": "{:.0f}"})
    area.boundary.plot(ax=a, color="k", lw=.5); a.set_title(s); a.set_axis_off()
plt.suptitle("People per hectare in 500 m cells"); plt.tight_layout()

# %% [markdown]
# Equal intervals hide variation among most cells; quantiles exaggerate small differences; natural breaks follow
# gaps; head/tail breaks suit very skewed data (a few very dense cells). Say which you used, and why.
#
# ## 2. Counts or rates? Normalise
# A map of *number of clinics* shows where cells are big or busy; *clinics per 10,000 people* shows provision.

# %%
lived["clinics"] = gpd.sjoin(poi[poi.category == "health"][["geometry"]], lived, predicate="within").groupby("cell").size().reindex(lived.cell).fillna(0).values
lived["clinics_per_10k"] = lived.clinics / lived.people * 1e4
fig, ax = plt.subplots(1, 2, figsize=(13, 6))
lived.plot("clinics", ax=ax[0], cmap="Blues", legend=True, legend_kwds={"shrink": .6}); ax[0].set_title("clinics and pharmacies (count)")
lived.plot("clinics_per_10k", ax=ax[1], cmap="Blues", scheme="Quantiles", k=5, legend=True, legend_kwds={"loc": "lower left", "fmt": "{:.1f}"}); ax[1].set_title("per 10,000 people")
for a in ax: area.boundary.plot(ax=a, color="k", lw=.5); a.set_axis_off()

# %% [markdown]
# ## 3. Two variables on one map: a bivariate choropleth
# Population density against walking time to a clinic: dense *and* far is where need meets distance.

# %%
q = lambda s: pd.qcut(s.rank(method="first"), 3, labels=False)
lived["bv"] = q(lived.people_per_ha).astype(int) * 3 + q(lived.min_to_clinic.fillna(lived.min_to_clinic.max())).astype(int)
pal = ["#e8e8e8", "#e4acac", "#c85a5a", "#b0d5df", "#ad9ea5", "#985356", "#64acbe", "#627f8c", "#574249"]
fig, ax = plt.subplots(figsize=(9, 9))
lived.plot(color=[pal[i] for i in lived.bv], ax=ax); area.boundary.plot(ax=ax, color="k", lw=.5); ax.set_axis_off()
ins = ax.inset_axes([.02, .02, .2, .2])
ins.imshow(np.array([[int(pal[r * 3 + c][1:], 16) for c in range(3)] for r in range(3)])[::-1].astype(np.uint32).view(np.uint8).reshape(3, 3, 4)[:, :, 2::-1], origin="upper")
ins.set_xticks([0, 2], ["near", "far"]); ins.set_yticks([0, 2], ["dense", "sparse"]); ins.set_xlabel("walk to clinic", fontsize=8); ins.set_ylabel("people/ha", fontsize=8)
ax.set_title("Population density × walking time to a clinic");

# %% [markdown]
# ## 4. Small multiples: one map per category

# %%
cats = ["education", "health", "worship", "shops and markets", "public transport", "work"]
fig, ax = plt.subplots(2, 3, figsize=(15, 10))
for a, c in zip(ax.ravel(), cats):
    area.plot(ax=a, color="#f2f2f2"); sub = poi[poi.category == c]
    sub.plot(ax=a, markersize=3, color="C3"); a.set_title(f"{c} ({len(sub)})"); a.set_axis_off()
plt.tight_layout()

# %% [markdown]
# ## 5. Charts that go with maps

# %%
fig, ax = plt.subplots(1, 2, figsize=(13, 4.5))
poi.category.value_counts().plot.barh(ax=ax[0], color="C0"); ax[0].set_title("Places by category (OSM)"); ax[0].invert_yaxis()
w = lived.dropna(subset=["min_to_clinic"]).sort_values("min_to_clinic")
ax[1].plot(w.min_to_clinic, w.people.cumsum() / w.people.sum(), lw=2)
ax[1].set(xlabel="walking minutes to nearest clinic", ylabel="share of people", title="Cumulative access curve", xlim=(0, 60)); ax[1].grid(alpha=.3)
plt.tight_layout()

# %% [markdown]
# ## 6. Interactive maps in the notebook
# ### One line: `explore()`

# %%
lived.to_crs(4326).explore(column="min_to_clinic", cmap="RdYlGn_r", scheme="Quantiles", k=5,
                           tooltip=["people", "buildings", "min_to_clinic", "shops"], tiles="CartoDB positron",
                           style_kwds={"weight": 0, "fillOpacity": .6}, legend_kwds={"caption": "walk to clinic (min)"})

# %% [markdown]
# ### Several layers, a heat map and a minimap with folium

# %%
import folium
from folium.plugins import HeatMap, MiniMap, Fullscreen, MeasureControl
m = folium.Map(location=[30.19, 67.01], zoom_start=12, tiles="CartoDB positron")
folium.TileLayer("OpenStreetMap", name="OpenStreetMap").add_to(m)
folium.TileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", attr="Esri World Imagery", name="satellite").add_to(m)
lived.to_crs(4326).explore(m=m, column="people_per_ha", cmap="YlOrRd", scheme="Quantiles", k=5, name="people per hectare", style_kwds={"weight": 0, "fillOpacity": .5})
p4 = poi.to_crs(4326)
HeatMap(list(zip(p4[p4.category == "shops and markets"].geometry.y, p4[p4.category == "shops and markets"].geometry.x)), name="shops (heat map)", radius=10, show=False).add_to(m)
p4[p4.category == "worship"].explore(m=m, color="green", name="places of worship", marker_kwds={"radius": 3}, tooltip=["name"] if "name" in p4 else None)
MiniMap().add_to(m); Fullscreen().add_to(m); MeasureControl().add_to(m)
folium.LayerControl(collapsed=False).add_to(m); m

# %% [markdown]
# ### Side by side: two maps that pan and zoom together

# %%
from folium.plugins import DualMap
dm = DualMap(location=[30.19, 67.01], zoom_start=13, tiles=None)
folium.TileLayer("CartoDB positron").add_to(dm.m1)
folium.TileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", attr="Esri World Imagery").add_to(dm.m2)
lived.to_crs(4326).explore(m=dm.m1, column="buildings", cmap="viridis", style_kwds={"weight": 0, "fillOpacity": .6}, legend=False)
dm

# %% [markdown]
# Left: buildings per cell from the data. Right: satellite imagery. Pan either: does the data match what you see?
#
# ### Interactive charts with plotly

# %%
import plotly.express as px
px.scatter(lived, x="people_per_ha", y="min_to_clinic", size="buildings", color="shops", hover_data=["cell"],
           labels={"people_per_ha": "people per hectare", "min_to_clinic": "walk to clinic (min)"},
           title="Each 500 m cell: density, access, shops (hover a bubble)", height=480)

# %% [markdown]
# ### Sliders and menus (live notebooks only)
# `ipywidgets` re-runs a function when a control moves. In a published page the slider does nothing, because no
# Python is running behind it; open the notebook in Colab or Jupyter to use it.
#
# ```python
# import ipywidgets as w
# @w.interact(minutes=w.IntSlider(5, 5, 60, 5))
# def show(minutes=15):
#     ax = lived.plot(color="#eee", figsize=(6, 6))
#     lived[lived.min_to_clinic <= minutes].plot(ax=ax, color="C2")
#     ax.set_title(f"{lived.people[lived.min_to_clinic <= minutes].sum() / lived.people.sum():.0%} of people within {minutes} min"); ax.set_axis_off()
# ```
#
# ## Saving and sharing
# - Static: `plt.savefig("map.png", dpi=300)`; for print use PDF or SVG.
# - Interactive: `m.save("map.html")` gives one file anyone can open in a browser; plotly: `fig.write_html(...)`.
# - Always add the data credit: "© OpenStreetMap contributors (ODbL); Overture Maps; WorldPop (CC BY 4.0)".
