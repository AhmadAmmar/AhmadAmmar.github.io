# %% [markdown]
# # Accounts, keys and web addresses for data
#
# Before any analysis you need three things: **an account** where the data provider asks for one, **a key** that your
# code can use without you typing a password, and **the right web address** for exactly the data you want. This
# notebook covers all three for the services used most in climate and Earth-observation work, and ends with the habits
# that keep downloads working when servers are busy.
#
# It builds on *Remote sensing basics in Python* (chapter "Getting the data"), which introduces the services; here we
# go further: which page to sign up on, which extra permissions a service needs, where each key lives on your computer,
# how to test it, and how data addresses (URLs) are built so you can write your own.
#
# Every cell runs without any account: cells that need one check first and say what to do. The outputs shown were made
# with real accounts.

# %%
import importlib.util, subprocess, sys
need = {"earthaccess": "earthaccess", "cdsapi": "cdsapi", "requests": "requests", "pystac_client": "pystac-client",
        "planetary_computer": "planetary-computer", "xarray": "xarray", "netCDF4": "netCDF4"}
missing = [pkg for mod, pkg in need.items() if importlib.util.find_spec(mod) is None]
if missing:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *missing], check=True)
import os, time, json
from pathlib import Path
import requests
import pandas as pd
DATA = Path("gd_data"); DATA.mkdir(exist_ok=True)
HOME = Path.home()

# %% [markdown]
# # Where to sign up, and for what
#
# | Service | Sign-up page | What it opens | Extra step after signing up |
# |---|---|---|---|
# | NASA Earthdata | https://urs.earthdata.nasa.gov/users/new | MODIS, VIIRS, GRACE, GEDI, MERRA-2, Sentinel-1 via ASF, GPW | **Authorise each data centre's app** (below) |
# | Copernicus Climate Data Store (CDS) | https://cds.climate.copernicus.eu (Login, then Register) | ERA5, ERA5-Land, satellite climate records | **Accept the licence on each dataset's page** (Download tab, bottom) |
# | Copernicus Early Warning Data Store | https://ewds.climate.copernicus.eu | GloFAS river discharge, fire danger | Same login as CDS; accept its own terms |
# | Copernicus Data Space | https://dataspace.copernicus.eu | All Sentinel missions | none |
# | Google Earth Engine | https://code.earthengine.google.com/register | Processing in Google's cloud | Create a Cloud project; choose the non-commercial tier |
# | OpenAQ | https://explore.openaq.org/register | Air-quality monitor data (API v3) | Copy the API key from your account page |
# | NASA FIRMS | https://firms.modaps.eosdis.nasa.gov/api/map_key/ | Active fires as CSV by area and day | none: the "MAP_KEY" arrives by e-mail |
# | ACLED | https://acleddata.com/register/ | Conflict and protest events | Access is reviewed; key on the account page |
# | Zenodo | https://zenodo.org (sign in with GitHub) | DOIs for your own data and code | Personal token for uploads from code |
#
# **Authorised apps (NASA).** One Earthdata login covers many archives, but each archive is an "application" you must
# approve once: profile page (https://urs.earthdata.nasa.gov/profile) > *Applications* > *Authorized Apps* >
# *Approve More Applications*. The ones this guide meets: **NASA GESDISC DATA ARCHIVE** (MERRA-2, GLDAS, Sentinel-5P
# copies), **LP DAAC Data Pool** (MODIS land products), **ASF Data Search** (Sentinel-1). Without it a download fails
# with *403 Forbidden* even though the password is right: that error is the clue.
#
# **Quotas.** Free services limit use. Earth Engine's non-commercial tier has a monthly computing budget; when it is used
# up the project goes into *Restricted Mode* and requests fail with "Too Many Requests" until it resets. The CDS queues
# large requests; OpenAQ and FIRMS limit requests per minute. Plan for this: small requests, caching, and a second
# route for the same data (last section).

# %% [markdown]
# # Where keys live, and how to keep them out of sight
#
# A key is a password for programs. It must never appear in a notebook, a script, a screenshot or a repository. Each
# library looks for its key in a fixed place, so the code itself never contains it:
#
# | Key | Where it lives | Format |
# |---|---|---|
# | NASA Earthdata | `~/.netrc` (Linux, Mac) or `~/_netrc` (Windows) | `machine urs.earthdata.nasa.gov login NAME password PASS` |
# | Copernicus CDS | `~/.cdsapirc` | `url: https://cds.climate.copernicus.eu/api` and `key: TOKEN` |
# | Earth Engine | made for you by `earthengine authenticate` (or `ee.Authenticate()`) | a credentials file in `~/.config/earthengine/` |
# | OpenAQ, FIRMS, ACLED, Zenodo | an **environment variable** | `OPENAQ_API_KEY`, `FIRMS_MAP_KEY`, ... |
#
# **Setting an environment variable once, permanently.** Windows (PowerShell): `setx OPENAQ_API_KEY "your-key"`, then
# open a new terminal. Mac and Linux: add `export OPENAQ_API_KEY="your-key"` to `~/.bashrc` or `~/.zshrc`. In Google
# Colab, use the key icon (*Secrets*) and `from google.colab import userdata; userdata.get("OPENAQ_API_KEY")`.
# A project-level alternative is a `.env` file read with *python-dotenv*: then add `.env` to `.gitignore`.
#
# **If a key leaks** (pushed to GitHub, shown in a talk): revoke it on the service's account page and make a new one.
# Changing it in your file is not enough; the old one still works until revoked.

# %%
def check_keys():
    """Which keys this computer has, without ever printing a key."""
    rows = []
    netrc = next((p for p in (HOME / ".netrc", HOME / "_netrc") if p.exists()), None)
    rows.append(("NASA Earthdata", "netrc file", bool(netrc and "urs.earthdata.nasa.gov" in netrc.read_text())))
    rows.append(("Copernicus CDS", "~/.cdsapirc", (HOME / ".cdsapirc").exists()))
    rows.append(("Earth Engine", "credentials file", (HOME / ".config/earthengine/credentials").exists()))
    for v in ("OPENAQ_API_KEY", "FIRMS_MAP_KEY", "ACLED_KEY"):
        rows.append((v.split("_")[0].title(), f"${v}", bool(os.environ.get(v))))
    return pd.DataFrame(rows, columns=["service", "where", "present"])
check_keys()

# %% [markdown]
# # Testing each key with the smallest possible request
#
# A key can be present and still not work (expired, licence not accepted, app not authorised). Test with a request so
# small it costs nothing.

# %%
def test(name, fn):
    t = time.time()
    try:
        return name, "works", fn(), round(time.time() - t, 1)
    except Exception as e:
        return name, "fails", f"{type(e).__name__}: {str(e)[:90]}", round(time.time() - t, 1)

def earthdata():
    import earthaccess
    a = earthaccess.login(strategy="netrc")
    return "logged in as an Earthdata user" if a.authenticated else "not logged in"

def openaq():
    k = os.environ.get("OPENAQ_API_KEY")
    if not k:
        return "no key set (skip)"
    r = requests.get("https://api.openaq.org/v3/locations", params={"coordinates": "31.52,74.35", "radius": 5000, "limit": 1},
                     headers={"X-API-Key": k}, timeout=60); r.raise_for_status()
    return f"{len(r.json()['results'])} monitor(s) returned (limit 1) near Lahore"

pd.DataFrame([test("NASA Earthdata", earthdata), test("OpenAQ", openaq)], columns=["service", "result", "detail", "seconds"])

# %% [markdown]
# # How data addresses are built
#
# Almost every download is a web address (URL). Once you can read its parts, you can write your own instead of
# clicking through a portal. Five patterns cover most of what you will meet.
#
# **1. A query (REST API).** `https://host/path?name=value&name=value`. The part after `?` holds *parameters*. Example,
# geoBoundaries (country boundaries, no account): `https://www.geoboundaries.org/api/current/gbOpen/PAK/ADM2/`; the
# path itself carries the country code and level. OpenAQ: `https://api.openaq.org/v3/locations?coordinates=31.52,74.35&radius=5000`.
#
# **2. A file-name template.** Archives name files by date, so you can build any address:
# `https://data.chc.ucsb.edu/products/CHIRPS/v2.0/global_monthly/tifs/chirps-v2.0.{YYYY}.{MM}.tif.gz`. Fill in the
# year and month with Python's f-strings. Archives do move: until 2026 this lived under `/products/CHIRPS-2.0/`, and old
# addresses now return *404 Not Found*. When a template stops working, open the archive's top folder in a browser and
# follow the folders down. (The new folder also holds CHIRPS version 3.0.)
#
# **3. A subsetting address.** Some servers cut the region and period for you, inside the URL. The IRI Data Library
# writes each step as a path segment: `.../.precipitation/X/70/80/RANGEEDGES/Y/26/34/RANGEEDGES/T/(Jan 2001)/(Dec 2024)/RANGEEDGES/data.nc`
# means: longitude 70-80 E, latitude 26-34 N, January 2001 to December 2024, as NetCDF. OPeNDAP servers do the same
# with a *constraint* after `?`: `file.nc4?TOTEXTTAU[0:23][236:236][412:412]` (time, latitude, longitude index ranges).
#
# **4. A catalogue search (STAC).** You do not build file addresses at all: you ask a catalogue for items in a box and
# a date range, and it returns their addresses (`pystac-client`, shown in *Remote sensing basics*).
#
# **Say who you are.** Some servers slow down or refuse requests that announce themselves only as `python-requests`
# (the default), answering *429 Too Many Requests* at once. A short `User-Agent` header naming your project usually
# fixes it (the CHIRPS server below has done this at busy times). Never put an e-mail address or name in it that you do not want logged.
#
# **5. Map tiles.** Basemaps are cut into tiles addressed by zoom and position: `https://server/{z}/{x}/{y}.png` for most
# servers, but Esri's is `.../tile/{z}/{y}/{x}`: the order differs, and getting it wrong gives a scrambled map. Some
# tile servers now require a key (CARTO's tiles show "API KEY REQUIRED" without one); Esri's reference layers do not.

# %%
def boundaries(iso="PAK", level="ADM2"):
    """Pattern 1: the API answers with JSON that contains the address of the GeoJSON file."""
    meta = requests.get(f"https://www.geoboundaries.org/api/current/gbOpen/{iso}/{level}/", timeout=60).json()
    return {k: meta[k] for k in ("boundaryName", "boundaryType", "boundaryYearRepresented", "admUnitCount", "gjDownloadURL")}
boundaries()

# %%
chirps_months = [f"https://data.chc.ucsb.edu/products/CHIRPS/v2.0/global_monthly/tifs/chirps-v2.0.{y}.{m:02d}.tif.gz"
                 for y in (2009, 2010) for m in (7, 8)]          # pattern 2: build addresses from a template
print(*chirps_months, sep="\n")
UA = {"User-Agent": "research-notebook/1.0 (learning; contact via your institution)"}   # say who you are
r = requests.head(chirps_months[0], timeout=60, allow_redirects=True, headers=UA)   # HEAD: "is it there, how big?"
print("exists:", r.status_code == 200, "| size:", int(r.headers.get("Content-Length", 0)) // 1_000_000, "MB")

# %%
# Pattern 3: CHIRPS monthly rainfall over Punjab (70-80 E, 26-34 N), 2001-2024, cut by the server: 37 MB instead of 7 GB.
IRI = ("https://iridl.ldeo.columbia.edu/SOURCES/.UCSB/.CHIRPS/.v2p0/.monthly/.global/.precipitation/"
       "X/70/80/RANGEEDGES/Y/26/34/RANGEEDGES/T/(Jan%202001)/(Dec%202024)/RANGEEDGES/data.nc")
f = DATA / "chirps_punjab_monthly.nc"
if not f.exists():
    with requests.get(IRI, stream=True, timeout=900) as r:
        r.raise_for_status()
        with open(f, "wb") as out:
            for chunk in r.iter_content(1 << 20):
                out.write(chunk)
print(f.name, round(f.stat().st_size / 1e6, 1), "MB")

# %% [markdown]
# # A request to the Climate Data Store
#
# The CDS does not use addresses you build: you send a *request*, a dictionary naming the dataset and what you want,
# and it queues, builds and returns a file. The easiest way to write one is the dataset's web page: choose options under
# *Download*, scroll to *API request*, and copy it. Here: ERA5-Land monthly rainfall and temperature over the same box.

# %%
e = DATA / "era5land_punjab_monthly.nc"
if not e.exists():
    if (HOME / ".cdsapirc").exists():
        import cdsapi
        cdsapi.Client(quiet=True).retrieve("reanalysis-era5-land-monthly-means", {
            "product_type": ["monthly_averaged_reanalysis"], "variable": ["total_precipitation", "2m_temperature"],
            "year": [str(y) for y in range(2001, 2025)], "month": [f"{m:02d}" for m in range(1, 13)], "time": ["00:00"],
            "area": [34, 70, 26, 80],                     # north, west, south, east: the CDS order
            "data_format": "netcdf", "download_format": "unarchived"}, str(e))
    else:                                                  # no key: a copy made for this guide (Copernicus licence, credited)
        url = "https://raw.githubusercontent.com/AhmadAmmar/AhmadAmmar.github.io/main/guides/gridded-data/notebooks/gd_data/era5land_punjab_monthly.nc"
        e.write_bytes(requests.get(url, timeout=300).content)
print(e.name, round(e.stat().st_size / 1e6, 1), "MB")

# %% [markdown]
# **Note the box order.** The CDS wants *north, west, south, east*; most other tools want *west, south, east, north*.
# Swapping them gives an empty or wrong area without an error.
#
# # Downloads that survive busy servers
#
# Public servers fail often: a queue is full, a quota is used up, a mirror is down. Four habits make code robust:
#
# 1. **Cache**: skip a file that is already there (every cell above does this).
# 2. **Wait and retry**: on *429 Too Many Requests* or *502/503/504*, wait, then try again, waiting longer each time.
# 3. **Mirrors**: some services run copies. OpenStreetMap's Overpass API, for example, is mirrored; when the main
#    server says it is "at capacity", another often answers.
# 4. **A second route**: the same data from another archive (MODIS from NASA instead of Earth Engine; ERA5-Land from the
#    CDS instead of Earth Engine). Check with a small overlap that both give the same numbers before mixing them.

# %%
def get_with_retry(url, params=None, tries=5, mirrors=(), timeout=120):
    """GET with exponential backoff on busy-server answers, trying mirrors in turn."""
    hosts = [url, *mirrors]
    for attempt in range(tries):
        for u in hosts:
            try:
                r = requests.get(u, params=params, timeout=timeout)
                if r.status_code in (429, 502, 503, 504):
                    print(f"  {u.split('/')[2]} busy ({r.status_code})"); continue
                r.raise_for_status(); return r
            except requests.RequestException as ex:
                print(f"  {u.split('/')[2]}: {type(ex).__name__}")
        time.sleep(min(60, 5 * 2 ** attempt))
    raise RuntimeError("no server answered")

q = '[out:json][timeout:60];node["amenity"="school"](31.50,74.33,31.53,74.37);out count;'
try:
    r = get_with_retry("https://overpass-api.de/api/interpreter", params={"data": q}, tries=3, timeout=90,
                       mirrors=("https://maps.mail.ru/osm/tools/overpass/api/interpreter", "https://overpass.private.coffee/api/interpreter"))
    print("schools mapped in a small part of Lahore:", r.json()["elements"][0]["tags"]["total"])
except RuntimeError:
    print("Every Overpass server was busy this time: exactly why the retries and mirrors exist. Run the cell again later.")
