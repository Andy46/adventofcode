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
#for pattern in INITIAL_PATTERNS:
#    print(pattern)

def orderTowels(towels):
    towels = copy.deepcopy(towels)
    towels.sort()
    towels.reverse()
    print(towels)
    sets = {}
    for towel in towels:
        if towel[0] not in sets:
            sets[towel[0]] = []
        sets[towel[0]].append(towel)
    return sets
print(orderTowels(INITIAL_TOWELS))


ORDERED_TOWELS = orderTowels(INITIAL_TOWELS)

def isPatternAvailable(towels, pattern):
    pattern = copy.deepcopy(pattern)
    while len(pattern) > 0:
        print(pattern)
        nTowels = towels[pattern[0]] if pattern[0] in towels else []
        print(nTowels)
        prev = pattern
        pattern = [pattern[len(towel):] for towel in nTowels if len(towel) <= len(pattern) and towel == pattern[:len(towel)]]
        if not pattern or prev == pattern:
            return False

#
#        for towel in nTowels:
#            print(towel, pattern[:len(towel)])
#            if towel == pattern[:len(towel)]:
#                print(True)
#                pattern = pattern[len(towel):]
#                continue
#        return False
    return True

print("")
for pattern in INITIAL_PATTERNS:
    available = isPatternAvailable(ORDERED_TOWELS, pattern)
    print(f"Pattern {pattern} available: {available}")
