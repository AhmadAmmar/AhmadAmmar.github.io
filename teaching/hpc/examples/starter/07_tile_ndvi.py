"""One array task computes mean NDVI for one tile. NDVI = (NIR - red) / (NIR + red), a measure of greenness."""
import csv
import os

task = int(os.environ.get("SLURM_ARRAY_TASK_ID", 0))
with open(f"tiles/tile_{task}.csv") as f:
    rows = [(float(r["red"]), float(r["nir"])) for r in csv.DictReader(f)]
ndvi = [(n - r) / (n + r) for r, n in rows]
mean = sum(ndvi) / len(ndvi)
os.makedirs("results", exist_ok=True)
with open(f"results/ndvi_{task}.csv", "w") as f:
    f.write(f"{task},{len(ndvi)},{mean:.3f}\n")
print(f"tile {task}: {len(ndvi)} pixels, mean NDVI {mean:.3f}")
