"""Great-circle distance from one city to about 240 others, with real Natural Earth data."""
import csv
import math
import sys

R = 6371.0  # mean radius of the Earth, km


def distance_km(lat1, lon1, lat2, lon2):
    """The haversine formula: shortest distance over a sphere."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


origin = sys.argv[1] if len(sys.argv) > 1 else "London"
with open("data/cities_natural_earth.csv", encoding="utf-8") as f:
    cities = list(csv.DictReader(f))
home = next(c for c in cities if c["name"] == origin)
rows = sorted(((distance_km(float(home["lat"]), float(home["lon"]), float(c["lat"]), float(c["lon"])), c["name"]) for c in cities if c is not home))
print(f"{len(cities)} cities. Nearest to {origin}:")
for d, name in rows[:3]:
    print(f"  {name}: {d:.0f} km")
print(f"Farthest: {rows[-1][1]}, {rows[-1][0]:.0f} km")
