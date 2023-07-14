#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only

import csv
import os
from pathlib import Path
import sys
import time

if len(sys.argv) != 3:
    print("bga.py [csv] [footprint]")
    exit(1)

input = sys.argv[1]
output = sys.argv[2]

module = Path(output).stem

units = {}
for filename in sorted(os.listdir(input)):
    with open(os.path.join(input, filename), newline="") as i:
        rows = []
        for row in csv.reader(i):
            rows.append(row)
        units[Path(filename).stem] = rows;

o = open(output, "w")

timestamp = format(int(time.time()), 'X')
o.write("(module " + module + " (layer F.Cu) (tedit " + timestamp + ")\n")
o.write("  (attr smd)\n")
o.write("  (fp_text reference REF** (at 0 -1.27) (layer F.SilkS)\n")
o.write("    (effects (font (size 1 1) (thickness 0.15)))\n")
o.write("  )\n")
o.write("  (fp_text value " + module + " (at 0 1.27) (layer F.Fab)\n")
o.write("    (effects (font (size 1 1) (thickness 0.15)))\n")
o.write("  )\n")


for name, rows in units.items():
    for row in rows:
        if len(row) >= 4 and len(row[0]) >= 1:
            pin = row[0]
            x = float(row[3])/1000.0
            y = -float(row[4])/1000.0
            o.write("  (pad " + pin + " smd circle (at " + str(x) + " " + str(y) + ") (size 0.25 0.25) (layers F.Cu F.Paste F.Mask))\n")

o.write(")\n")
