"""One array task handles one decade of the Armagh record, and writes one small result file."""
import os
from armagh import read_months, yearly

FIRST = 1870
task = int(os.environ.get("SLURM_ARRAY_TASK_ID", 0))
decade = FIRST + 10 * task
years = yearly(read_months("data/armaghdata.txt"))
values = [v["tmean"] for y, v in years.items() if decade <= y < decade + 10]
os.makedirs("results", exist_ok=True)
with open(f"results/decade_{decade}.csv", "w") as f:
    f.write(f"{decade},{len(values)},{sum(values) / len(values):.2f}\n")
print(f"task {task}: {decade}s, {len(values)} years")
