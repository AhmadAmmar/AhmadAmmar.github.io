---
title: "2. The tools, and how they fit together"
slug: tools
description: 2. The tools, and how they fit together: Making maps that can be repeated and published.
---

| Tool | Its job |
|:---|:---|
| Matplotlib | Draws everything. A *figure* is the page, and an *axes* is one plot on it |
| Cartopy | Adds map projections to Matplotlib; an axes with a projection is a *GeoAxes* |
| GeoPandas | Reads and reprojects vector data such as GeoJSON |
| rasterio | Reads and reprojects rasters such as GeoTIFF |
| NumPy | Holds raster values as arrays |
| matplotlib-scalebar | Draws the scale bar |
| cmcrameri | Scientific colour maps, from Crameri et al. (2020) |
| Earth Engine | Computes on satellite archives, in the cloud |
| research-helpers | Our layer: `carto` sets the house style and checks each map |
| LaTeX | Places the finished map in a paper or book |

## 2.1 Two ideas that prevent most mistakes

##### Figure size is set in inches, in journal widths.

Fonts are in points, so a figure drawn at its printed width keeps its text at the true size. If you draw a figure large and shrink it, its text shrinks as well. **From the code:** `research_helpers/carto.py, size(), lines 45--47`

``` {startFrom="45"}
def size(width="double", ratio=0.62):
    w = WIDTH.get(width, width)
    return w, w * ratio
```

##### `transform` says what your data is in, and `projection` what the map is in.

This is the most common source of confusion. The map’s projection is set once. Each thing you draw says which coordinates *it* uses:

``` {.python language="Python"}
ax = plt.axes(projection=carto.albers(85, 25, 45))         # the map
ax.plot(lon, lat, transform=ccrs.PlateCarree())            # data in degrees
ax.imshow(a, extent=box, transform=ccrs.UTM(42))           # data in UTM metres
```

`PlateCarree` here means “plain longitude and latitude”. If you leave out `transform`, Cartopy assumes that the numbers are already in the map’s projection, and your data lands in the wrong place or disappears.

## 2.2 The house style

`use_style()` runs once at the top of a script. It sets fonts, line widths and export settings, so all figures in a project match. **From the code:** `research_helpers/carto.py, use_style(), lines 33--42`

``` {startFrom="33"}
def use_style():
    """Set fonts, weights and export options once, so every figure in a project matches."""
    mpl.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": ["Source Sans 3", "Source Sans Pro", "Arial", "DejaVu Sans"], "font.size": 8,
        "axes.titlesize": 9, "axes.titleweight": "bold", "axes.titlelocation": "left", "axes.labelsize": 8,
        "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.6, "axes.edgecolor": INK, "axes.labelcolor": INK,
        "xtick.color": INK, "ytick.color": INK, "xtick.labelsize": 7, "ytick.labelsize": 7, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "legend.frameon": False, "legend.fontsize": 7, "lines.linewidth": 1.1, "figure.dpi": 150, "savefig.dpi": 400, "savefig.bbox": "tight",
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none", "axes.prop_cycle": mpl.cycler(color=QUALITATIVE),
    })
```

Three of its settings deserve a note. `pdf.fonttype=42` embeds real text, which journals ask for and which stays editable. `savefig.dpi=400` is above the common 300 dpi print requirement. `savefig.bbox="tight"` trims empty margins, so check the final size.

## 2.3 A minimal script

``` {.python language="Python"}
from research_helpers import carto
import cartopy.crs as ccrs, geopandas as gpd

carto.use_style()                                    # 1 style
g = gpd.read_file("regions.geojson")                 # 2 data
proj = carto.albers(85, 25, 45)                      # 3 projection
fig, ax = carto.map_axes(proj, [60, 108, 22, 47])    # 4 frame, land, grid
ax.add_geometries(g.geometry, ccrs.PlateCarree(),    # 5 subject
                  facecolor=carto.QUALITATIVE[0], edgecolor="white", linewidth=0.2)
carto.scale_bar(ax)                                  # 6 scale
carto.finish_map(fig, "figures/map_regions",         # 7 checks and saves
                 title="Regions", sources=["GMBA"], crs="Albers equal-area")
```

