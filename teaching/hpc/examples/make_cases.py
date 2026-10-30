#!/usr/bin/env python3
"""Write one input file per combination of settings: a small parameter sweep.

    python make_cases.py cases
"""
import itertools   # itertools.product gives every combination of several lists
import json
import sys
from pathlib import Path

U_WALL = [2.1, 1.5, 0.45]        # three wall types: W per square metre per kelvin
AIR_CHANGES = [1.0, 0.7, 0.5]    # three levels of draughtiness, per hour
DEGREE_DAYS = [1800, 2000, 2200] # three climates, kelvin-days

folder = Path(sys.argv[1])       # the folder name typed after the script name
folder.mkdir(parents=True, exist_ok=True)   # make it, with no error if it exists already

# enumerate numbers the combinations 0, 1, 2 ... so that each file gets a unique name
for number, (u, ach, hdd) in enumerate(itertools.product(U_WALL, AIR_CHANGES, DEGREE_DAYS)):
    case = {"u_wall": u, "wall_area": 90, "air_changes": ach, "volume": 200, "degree_days": hdd}
    # :03d pads the number to three digits, so that files sort in order: 000, 001 ... 026
    (folder / f"case_{number:03d}.json").write_text(json.dumps(case))

print(f"wrote {number + 1} cases to {folder}")
