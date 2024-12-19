#!/bin/python3

import copy
import click

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])

filename = f"{filepath}/00_test.data"
filename = f"{filepath}/00_example1.data"

# Read data
INITIAL_TOWELS   = []
INITIAL_PATTERNS = []

with open(filename, "r") as file:
    lines = [line.strip() for line in file.readlines()]

    INITIAL_TOWELS = [towel for towel in lines[0].strip().split(", ") if towel is not None]

    for line in lines[2:]:
        INITIAL_PATTERNS.append(line.strip())

print (INITIAL_TOWELS)
for pattern in INITIAL_PATTERNS:
    print(pattern)

