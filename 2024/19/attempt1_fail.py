#!/bin/python3

import copy
import click

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])

filename = f"{filepath}/00_example1.data"
filename = f"{filepath}/00_test.data"

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
        
        nTowels = towels[pattern[0]] if pattern[0] in towels else []
        if len(nTowels) == 0:
            return False
        
        prev = pattern
        for towel in nTowels:
           if towel == pattern[:len(towel)]:
               pattern = pattern[len(towel):]
               break
        if pattern == prev:
            return False
    return True

print("")
availablePatterns = [pattern for pattern in INITIAL_PATTERNS if isPatternAvailable(ORDERED_TOWELS, pattern)]
notAvailablePatterns = [pattern for pattern in INITIAL_PATTERNS if not isPatternAvailable(ORDERED_TOWELS, pattern)]

print(f"Available patterns: {availablePatterns}")
print(f"Available patterns count: {len(availablePatterns)}")
print(f"Available patterns count: {len(notAvailablePatterns)}")