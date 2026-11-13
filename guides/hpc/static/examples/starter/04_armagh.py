"""Warmest, coldest and wettest complete years at Armagh Observatory, from real Met Office records."""
from armagh import read_months, yearly

rows = read_months("data/armaghdata.txt")
years = yearly(rows)
print(f"{len(rows)} monthly records, {len(years)} complete years, {min(years)} to {max(years)}")
warm = max(years, key=lambda y: years[y]["tmean"])
cold = min(years, key=lambda y: years[y]["tmean"])
wet = max(years, key=lambda y: years[y]["rain"])
print(f"Warmest: {warm}, mean {years[warm]['tmean']:.2f} C")
print(f"Coldest: {cold}, mean {years[cold]['tmean']:.2f} C")
print(f"Wettest: {wet}, {years[wet]['rain']:.0f} mm")
