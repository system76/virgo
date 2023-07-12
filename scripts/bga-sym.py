#!/usr/bin/env python3

import csv
from pathlib import Path
import sys
import time

if len(sys.argv) != 3:
    print("bga.py [csv] [symbol]")
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

units = 0
for row in rows:
    if len(row) == 1:
        units += 1

o = open(output, "w")

o.write("EESchema-LIBRARY Version 2.4\n")
o.write("#encoding utf-8\n")
o.write("#\n")
o.write("# " + module + "\n")
o.write("#\n")
o.write("DEF " + module + " U 0 40 Y Y " + str(units) + " L N\n")
o.write("F0 \"U\" 50 750 50 H V C CNN\n")
o.write("F1 \"" + module + "\" 50 650 50 H V C CNN\n")
o.write("F2 \"\" 50 150 50 H I C CNN\n")
o.write("F3 \"\" 50 150 50 H I C CNN\n")
o.write("DRAW\n")

def rect(unit, x1, x2, y1, y2):
    if count > 0:
        o.write("S " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + " " + str(unit) + " 1 0 f\n")

def text(unit, x, y, name):
    o.write("T 0 " + str(x) + " " + str(y) + " 60 0 " + str(unit) + " 1 \"" + name + "\" Normal 0 C C\n")

def pin(unit, x, y, dir, pin, name, type):
    o.write("X " + name + " " + pin + " " + str(x) + " " + str(y) + " 200 " + dir + " 50 50 " + str(unit) + " 1 " + type + "\n")

offset = 1000

unit = 0
switch = False
switch_count = 0
count = 0
for row in rows:
    if len(row) >= 3 and len(row[0]) >= 1:
        count += 1
        names = row[1].split("/")
        type = "U"
        if row[2] == "I":
            type = "I"
        elif row[2] == "O":
            type = "O"
        elif row[2] == "I/O":
            type = "B"
        elif row[2] == "GND":
            type = "W"
        elif row[2] == "PWR":
            type = "W"
        pin(unit, offset if switch else -offset, -count * 100, "L" if switch else "R", row[0], names[0], type)
    elif len(row) >= 1 and len(row[0]) >= 1:
        rect(unit, -offset + 200, offset - 200, 0, -max(count, switch_count) * 100 - 100)
        unit += 1
        switch = False
        switch_count = 0
        count = 0
        text(unit, 0, 100, row[0])
    elif len(row) == 0:
        switch = True
        switch_count = count
        count = 0
rect(unit, -offset + 200, offset - 200, 0, -max(count, switch_count) * 100 - 100)

o.write("ENDDRAW\n")
o.write("ENDDEF\n")
o.write("#\n")
o.write("#End Library\n")
