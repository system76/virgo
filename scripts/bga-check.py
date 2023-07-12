#!/usr/bin/env python3

import csv
import os
from pathlib import Path
import sys
import time

if len(sys.argv) != 3:
    print("bga-check.py [original] [organized]")
    exit(1)

original = sys.argv[1]
organized = sys.argv[2]

original_pins = {}
with open(original, newline="") as i:
    header = None
    for row in csv.reader(i):
        if header is None:
            header = row
        elif len(row) >= 4 and len(row[0]) >= 1:
            original_pins[row[0]] = row

units = {}
for filename in sorted(os.listdir(organized)):
    with open(os.path.join(organized, filename), newline="") as i:
        rows = []
        for row in csv.reader(i):
            rows.append(row)
        units[Path(filename).stem] = rows;

organized_pins = {}
for name, rows in units.items():
    for row in rows:
        if len(row) >= 4 and len(row[0]) >= 1:
            if row[0] in organized_pins:
                raise Exception("Pin {} duplicated in unit {}".format(row[0], name))
            organized_pins[row[0]] = row

for pin in original_pins:
    if pin not in organized_pins:
        raise Exception("Pin {} not in organized pins".format(pin))
    if original_pins[pin] != organized_pins[pin]:
        raise Exception("Pin {} is {} in original pins but is {} in organized pins".format(pin, original_pins[pin], organized_pins[pin]))

for pin in organized_pins:
    if pin not in original_pins:
        raise Exception("Pin {} not in original pins".format(pin))
