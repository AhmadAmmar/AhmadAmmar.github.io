---
title: "6. From script to publication"
slug: workflow
description: 6. From script to publication: Making maps that can be repeated and published.
---

## 6.1 One way out: `finish_map()`

Every map leaves through this function, which refuses a map without its sources or projection, or without a scale bar or a reason for having none. It saves three formats and a record. **From the code:** `research_helpers/carto.py, finish_map(), lines 131--145`

``` {startFrom="131"}
def finish_map(fig, stem, *, title, sources, crs, scale_bar=True, boundary_note=False, status="final", note="", formats=("pdf", "png", "svg")):
    """The one exit for a map: it stops if basic elements are missing, and saves a record beside the map.

    A map must name its sources and projection and either carry a scale bar or say why not. The record makes it findable and repeatable.
    """
    if not sources:
        raise ValueError("a map must name its sources")
    if not crs:
        raise ValueError("a map must state its projection")
    if scale_bar is not True and not isinstance(scale_bar, str):
        raise ValueError("a map needs a scale bar, or a sentence saying why not")
    s = save(fig, stem, formats, {"Title": title})
    record = dict(title=title, sources=list(sources), crs=crs, scale_bar=scale_bar, boundary_note=BOUNDARY_NOTE if boundary_note else "", status=status, note=note, files=[s.with_suffix(f".{f}").name for f in formats])
    s.with_suffix(".map.json").write_text(json.dumps(record, indent=1), encoding="utf8")
    return s
```

**From the code:** `research_helpers/carto.py, save(), lines 86--99`

``` {startFrom="86"}
def save(fig, stem, formats=("pdf", "png", "svg"), meta=None):
    """Save vector and raster copies, without a timestamp so that a rebuild of the same figure is byte-stable where possible."""
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    for f in formats:
        md = {"Title": stem.name, **(meta or {})}
        if f == "pdf":
            md["CreationDate"] = None
        elif f == "svg":
            md["Date"] = None
        elif f == "png":
            md = {"Title": stem.name}
        fig.savefig(stem.with_suffix(f".{f}"), metadata=md)
    return stem
```

| Format      | Use                                                     |
|:------------|:--------------------------------------------------------|
| PDF         | LaTeX and print; a vector, except for rasters within it |
| PNG         | The web and slides, at 400 dpi                          |
| SVG         | Later editing, with text kept as text                   |
| `.map.json` | The record: title, sources, projection, status          |

## 6.2 Repeating a map

1.  One script draws one family of figures, and takes no manual steps.

2.  Data comes from named files or Earth Engine calls. Raw data is never edited.

3.  Downloads are cached, so a rerun does not depend on the network, and the file records what was used.

4.  Numbers in the text come from the same run, through `research_helpers.autotex`.

5.  Every Earth Engine job also has a `.js` script in `earth-engine-code`.

6.  Figures carry the name of what they show, such as `map_sindh_flood_2022`.

## 6.3 Loops for many maps

When maps differ only in their data, write one function and loop. Fixing the colour limits keeps them comparable.

``` {.python language="Python"}
def range_map(unit, values, limits):
    fig, ax = carto.map_axes(PROJ, EXTENT, width="single")
    g[g.unit == unit].plot(ax=ax, column=values, vmin=limits[0], vmax=limits[1],
                           cmap=carto.SEQUENTIAL, transform=ccrs.PlateCarree())
    carto.scale_bar(ax)
    carto.finish_map(fig, F / f"map_{unit.lower().replace(' ', '_')}", title=unit,
                     sources=["GMBA"], crs="Albers equal-area")
    plt.close(fig)              # free memory, or a long loop runs out

for unit in g.unit.unique():
    range_map(unit, "duration", (0, 250))
```

## 6.4 Checklist

- Is the projection right for the use, and is it stated?

- Is area measured in an equal-area projection?

- Are sources credited as their licences require?

- Does nothing cover the data: inset, legend or markers?

- Do the markers sit on what they claim? Check against the numbers.

- Are colours readable in greyscale and for colour-blind readers?

- Is text at least about 6 pt at printed size?

- Do disputed boundaries carry a note?

- Have you actually looked at the final file?

The last matters most. In making the maps in these projects, the code ran without error while markers missed their targets, polygons failed to draw, and a class vanished. Only looking caught them.

## 6.5 Different fields

Journals set their own limits: column width, formats, fonts, resolution. Set those through `size()` and the export options, and check the author guide. Journal requirements take priority over this manual. Elevation, geological and nautical maps also have their own conventions, such as standard symbols and colours, and these apply when you make such maps.

