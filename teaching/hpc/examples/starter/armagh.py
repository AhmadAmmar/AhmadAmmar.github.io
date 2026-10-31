"""Read the Met Office historic station file for Armagh. Used by exercises 4 and 5."""


def number(text):
    """The file marks estimated values with * and provisional ones with #. Missing values are ---."""
    text = text.replace("*", "").replace("#", "")
    return None if "---" in text else float(text)


def read_months(path):
    rows = []
    with open(path, encoding="latin-1") as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 7 and parts[0].isdigit() and parts[1].isdigit():
                rows.append({"year": int(parts[0]), "month": int(parts[1]), "tmax": number(parts[2]), "tmin": number(parts[3]), "rain": number(parts[5])})
    return rows


def yearly(rows):
    """Yearly mean temperature and total rain, for years with all 12 months of both."""
    out = {}
    for y in sorted({r["year"] for r in rows}):
        m = [r for r in rows if r["year"] == y and None not in (r["tmax"], r["tmin"], r["rain"])]
        if len(m) == 12:
            out[y] = {"tmean": sum((r["tmax"] + r["tmin"]) / 2 for r in m) / 12, "rain": sum(r["rain"] for r in m)}
    return out
