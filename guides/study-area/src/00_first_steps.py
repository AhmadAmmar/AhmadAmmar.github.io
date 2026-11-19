# %% [markdown]
# # 00 · First steps: maps for people who have never made one
#
# This guide is for researchers who know a place through people, archives, texts or fieldwork, and want maps to
# help them think and argue: ethnographers, historians, sociologists, political scientists, scholars of gender,
# labour, religion or literature. If you have never written code, start here. Nothing needs installing.
#
# ## Three ways to work, and when to use each
#
# | Route | Good for | Start |
# |---|---|---|
# | **uMap** or **Felt** in the browser | a quick shareable map of your own places, routes and notes; no code at all | umap.openstreetmap.fr, felt.com |
# | **QGIS** on your computer | careful maps for a thesis or book, tracing old maps, editing layers by hand | qgis.org (free) |
# | **These notebooks** (Python, in Google Colab) | anything repeated, counted, measured or combined: distances, overlaps, statistics, many districts at once | the "Open in Colab" link on each notebook |
#
# Most people use all three. Sketch in uMap, compute in a notebook, finish the figure in QGIS.
#
# ## How a notebook works
# A notebook is a page of text and small boxes of code (*cells*). Click a cell and press **Shift + Enter** to run it;
# the result appears underneath. Run cells from top to bottom. If something breaks, read the last line of the red
# message, fix the cell, and run it again: nothing is damaged.

# %% [markdown]
# *Running this in Google Colab?* The next cell installs the few libraries Colab lacks (about a minute). Notebooks
# 04-07 read files made by 01 and 02: run those first in the same session, or keep the `data` folder on Google Drive.

# %%
import sys, subprocess
if "google.colab" in sys.modules:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "osmnx", "overturemaps", "mapclassify", "esda", "libpysal", "folium", "plotly"], check=True)

# %%
print("Hello. This cell ran.")
2 + 3

# %% [markdown]
# ## The four ideas behind every map
#
# **1. A layer is a table with a shape in each row.** Each row is a thing (a district, a road, an interview place);
# columns describe it; one special column holds its shape: a **point**, a **line** or a **polygon**.

# %%
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
things = gpd.GeoDataFrame({
    "name": ["interview place", "route to market", "neighbourhood"],
    "kind": ["point", "line", "polygon"],
    "note": ["met two teachers here", "walked with A. in March", "where most families moved in the 1990s"]},
    geometry=[Point(67.00, 30.19), LineString([(67.00, 30.19), (67.01, 30.20), (67.02, 30.20)]),
              Polygon([(66.99, 30.18), (67.03, 30.18), (67.03, 30.21), (66.99, 30.21)])], crs=4326)
things

# %% [markdown]
# **2. Coordinates need a reference system (CRS).** Longitude and latitude in degrees (EPSG:4326) are what GPS and
# web maps use. To measure metres you *project* to a flat system, such as UTM zone 42N (EPSG:32642) for most of
# Balochistan.

# %%
print("length of the route in degrees:", round(things.geometry[1].length, 4), "(meaningless)")
print("length in metres:", round(things.to_crs(32642).geometry[1].length), "m")

# %% [markdown]
# **3. Layers combine by place.** "Which interviews fall in which district?" is a *spatial join*; "what is within 1
# km?" is a *buffer*. Notebooks 04 and 06 are full of these.
#
# **4. A map is an argument.** What you show, leave out, name and colour makes a claim. Notebook 07 is about doing
# that honestly and safely.
#
# ## Your first interactive map
# Zoom with the mouse wheel, drag to move, hover over a shape to read its note.

# %%
things.explore(column="kind", tooltip=["name", "note"], tiles="OpenStreetMap", marker_kwds={"radius": 8}, style_kwds={"weight": 3})

# %% [markdown]
# ## Words you will meet
#
# | Word | Meaning |
# |---|---|
# | vector | data made of points, lines, polygons (districts, roads, places) |
# | raster | data made of a grid of cells (satellite images, population per 100 m) |
# | attribute | a column describing each feature |
# | basemap | the background map (streets, satellite) under your layers |
# | choropleth | a map colouring areas by a value |
# | geocode | turn a place name into coordinates |
# | georeference | pin a scanned map or photo onto real coordinates |
# | OSM | OpenStreetMap, the free world map made by volunteers |
#
# Next: notebook 01 collects open data for a city (Quetta), notebook 02 for a whole province (Balochistan), and
# notebook 03 shows how to bring in your own field material.
