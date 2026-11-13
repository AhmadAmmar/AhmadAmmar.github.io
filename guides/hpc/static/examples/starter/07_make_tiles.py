"""Make 8 small SYNTHETIC satellite tiles: invented red and near-infrared reflectance, not real imagery.

Greener tiles have higher near-infrared and lower red, as vegetation does. The seed makes every run identical.
"""
import csv
import os
import random

random.seed(42)
os.makedirs("tiles", exist_ok=True)
for t in range(8):
    green = t / 7  # tile 0 is built-up, tile 7 is parkland
    with open(f"tiles/tile_{t}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["red", "nir"])
        for _ in range(10_000):
            w.writerow([round(random.gauss(0.20 - 0.14 * green, 0.02), 4), round(random.gauss(0.22 + 0.28 * green, 0.03), 4)])
print("wrote 8 tiles to tiles/")
