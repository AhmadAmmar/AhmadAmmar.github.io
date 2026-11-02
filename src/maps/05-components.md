---
title: "5. Each component, with its parameters"
slug: components
description: 5. Each component, with its parameters: Making maps that can be repeated and published.
---

## 5.1 The frame: `map_axes()`

**From the code:** `research_helpers/carto.py, map_axes(), lines 56--71`

``` {startFrom="56"}
def map_axes(projection, extent=None, width="double", ratio=0.62, ax=None, grid=True, land=True, step=(10, 10)):
    """A map with quiet land, sea and graticule. Extent is lon0, lon1, lat0, lat1 in degrees."""
    fig = None
    if ax is None:
        fig, ax = plt.subplots(figsize=size(width, ratio), subplot_kw={"projection": projection})
    if extent:
        ax.set_extent(extent, ccrs.PlateCarree())
    if land:
        ax.add_feature(cfeature.LAND.with_scale("50m"), facecolor=MUTED_LAND, edgecolor="none", zorder=0)
        ax.add_feature(cfeature.OCEAN.with_scale("50m"), facecolor=MUTED_WATER, edgecolor="none", zorder=0)
    if grid:
        g = ax.gridlines(draw_labels=True, x_inline=False, y_inline=False, linewidth=0.3, color=GRID, xlocs=mpl.ticker.MultipleLocator(step[0]), ylocs=mpl.ticker.MultipleLocator(step[1]))
        g.top_labels = g.right_labels = False
        g.xlabel_style = g.ylabel_style = {"size": 6.5, "color": INK}
    ax.spines["geo"].set_linewidth(0.5)
    return (fig, ax) if fig else ax
```

| Parameter | Meaning |
|:---|:---|
| `projection` | The map’s projection |
| `extent` | `[lon0, lon1, lat0, lat1]` in degrees, or `None` to set it later |
| `width` | `"single"`, `"onehalf"` or `"double"` column, or inches |
| `ratio` | Height as a share of width |
| `ax` | Draw on an existing panel, for multi-panel figures. Nothing new is created |
| `grid`, `land` | Turn the graticule or base layer off, as you may want over imagery |
| `step` | Graticule spacing in degrees |

## 5.2 The scale bar: `scale_bar()`

**From the code:** `research_helpers/carto.py, scale_bar(), lines 74--78`

``` {startFrom="74"}
def scale_bar(ax, location="lower left"):
    """Scale bar in metres of the map's projection. It is true along the standard parallels only; say so in the caption."""
    bar = ScaleBar(1, "m", location=location, frameon=True, box_color="white", box_alpha=0.8, font_properties={"size": 6.5}, length_fraction=0.18, width_fraction=0.008, color=INK, scale_loc="top")
    ax.add_artist(bar)
    return bar
```

Pass `location` as `"lower left"`, `"upper right"` and so on, and place it where data is absent. The white box keeps it readable over imagery. It reads in metres of the map’s projection, so on a geographic axis, with units of degrees, it would be wrong: use a projected axes.

## 5.3 The inset: `locator()`

**From the code:** `research_helpers/carto.py, locator(), lines 115--124`

``` {startFrom="115"}
def locator(fig, position, extent, box, projection=None):
    """Small overview map. position is [left, bottom, width, height] in figure units; box is the lon0, lon1, lat0, lat1 of the main map."""
    a = fig.add_axes(position, projection=projection or ccrs.PlateCarree())
    a.set_extent(extent, ccrs.PlateCarree())
    a.add_feature(cfeature.LAND.with_scale("50m"), facecolor=MUTED_LAND, edgecolor="#666666", linewidth=0.3)
    a.add_feature(cfeature.OCEAN.with_scale("50m"), facecolor=MUTED_WATER)
    a.add_feature(cfeature.BORDERS.with_scale("50m"), edgecolor="#888888", linewidth=0.3)
    x0, x1, y0, y1 = box
    a.plot([x0, x1, x1, x0, x0], [y0, y0, y1, y1, y0], color="#D55E00", linewidth=0.9, transform=ccrs.PlateCarree())
    return a
```

| Parameter | Meaning |
|:---|:---|
| `position` | `[left, bottom, width, height]` as shares of the figure, from 0 to 1 |
| `extent` | The wider area the inset shows |
| `box` | The main map’s limits, drawn as an orange box |
| `projection` | Defaults to plain latitude and longitude |

Place it over empty or unimportant ground, and always look at the result. Our first flood map hid a marked town under its inset, and a later version hid the axis labels. Positions are in figure units, so moving an inset can take a few tries.

## 5.4 Other parts

**From the code:** `research_helpers/carto.py, credit(), lines 127--128`

``` {startFrom="127"}
def credit(fig, text, y=0.005):
    fig.text(0.995, y, text, ha="right", va="bottom", fontsize=5.5, color="#444444")
```

**From the code:** `research_helpers/carto.py, panel_labels(), lines 81--83`

``` {startFrom="81"}
def panel_labels(axes, x=-0.02, y=1.03):
    for i, ax in enumerate(axes):
        ax.text(x, y, f"({chr(97 + i)})", transform=ax.transAxes, fontweight="bold", fontsize=9, va="bottom", ha="right")
```

## 5.5 Legends

Cartopy polygons do not always appear in legends automatically, so make the handles yourself. For long legends, put them below the map, so that they do not cover data:

``` {.python language="Python"}
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in colours]
ax.legend(handles, names, loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=3)
```

## 5.6 Rasters

For a raster in another projection, warp it first, and then draw it. This gives you control over resampling, and avoids blurry or blocky results. Use nearest neighbour for classes, which must not be averaged, and bilinear for continuous data.

``` {.python language="Python"}
transform, w, h = calculate_default_transform(src.crs, target, src.width, src.height, *src.bounds, resolution=1000)
out = np.full((h, w), 255, dtype="uint8")
reproject(src.read(1), out, src_transform=src.transform, src_crs=src.crs,
          dst_transform=transform, dst_crs=target, resampling=Resampling.nearest)
ax.imshow(out, extent=box, origin="upper", transform=ax.projection, interpolation="nearest")
```

Mind **nodata**. Our snow map once lost a whole class, because 0 was both a class and the file’s nodata value. Reserve a value such as 255, and treat it explicitly.

