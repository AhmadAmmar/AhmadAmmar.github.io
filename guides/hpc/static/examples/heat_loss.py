#!/usr/bin/env python3
"""Toy simulation for the HPC tutorial: the yearly heating need of one simple building.

    python heat_loss.py case_007.json

It reads one case, does a small calculation, and writes the answer next to the input.
The physics is deliberately basic (see "heat loss" in the tutorial). The numbers are
illustrative: the point is to have something small that you can run thousands of times.
"""
import json   # reads and writes JSON, a plain-text format of names and values
import sys    # gives access to the words typed after the script name (sys.argv)
from pathlib import Path   # handles file paths in a tidy way on any operating system


def yearly_heat(u_wall, wall_area, air_changes, volume, degree_days):
    """Return heat need in kWh per year.

    u_wall       how leaky the wall is, in W per square metre per kelvin
    wall_area    wall area, in square metres
    air_changes  how many times per hour the indoor air is replaced
    volume       indoor volume, in cubic metres
    degree_days  how cold the year is, in kelvin-days
    """
    fabric = u_wall * wall_area                # heat lost through the walls, W per kelvin
    air = 0.33 * air_changes * volume          # heat lost with the air; 0.33 Wh warms 1 m3 of air by 1 K
    return (fabric + air) * degree_days * 24 / 1000   # W/K x K-days x 24 h/day = Wh; /1000 gives kWh


def main():
    path = Path(sys.argv[1])                   # sys.argv[1] is the first word after the script name
    case = json.loads(path.read_text())        # read the file, and turn its text into a Python dictionary
    answer = yearly_heat(**case)               # ** passes the dictionary's entries as named arguments
    # with_suffix swaps .json for .out, so case_007.json gives case_007.out
    path.with_suffix(".out").write_text(f"{answer:.1f}\n")   # :.1f means one decimal place


if __name__ == "__main__":                     # true only when run directly, not when imported
    main()
