#!/usr/bin/env python3

import csv
from pathlib import Path
import sys
import time

if len(sys.argv) != 3:
    print("bga.py [csv] [footprint]")
    exit(1)

input = sys.argv[1]
output = sys.argv[2]

module = Path(output).stem

header = None
rows = []
with open(input, newline="") as i:
    for row in csv.reader(i):
        if header is None:
            header = row
        else:
            rows.append(row)

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

for row in rows:
    if len(row) >= 4 and len(row[0]) >= 1:
        pin = row[0]
        x = float(row[3])/1000.0
        y = -float(row[4])/1000.0
        o.write("  (pad " + pin + " smd circle (at " + str(x) + " " + str(y) + ") (size 0.25 0.25) (layers F.Cu F.Paste F.Mask))\n")

o.write(")\n")
