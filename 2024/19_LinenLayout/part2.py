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

# print (INITIAL_TOWELS)
#for pattern in INITIAL_PATTERNS:
#    print(pattern)

def orderTowels(towels):
    towels = copy.deepcopy(towels)
    towels.sort()
    towels.reverse()
    # print(towels)
    sets = {}
    for towel in towels:
        if towel[0] not in sets:
            sets[towel[0]] = []
        sets[towel[0]].append(towel)
    return sets
# print(orderTowels(INITIAL_TOWELS))


ORDERED_TOWELS = orderTowels(INITIAL_TOWELS)

patternList = {}

def isPatternAvailable(towels, pattern):
    if pattern == "":
        return 1
    
    matchingTowels = []
    if pattern[0] in towels:
        matchingTowels = [towel for towel in towels[pattern[0]] if towel == pattern[:len(towel)]]

    available = 0
    for towel in matchingTowels:
        count = 0
        if pattern[len(towel):] in patternList:
            available += patternList[pattern[len(towel):]]
        else:
            subCount = isPatternAvailable(towels, pattern[len(towel):])
            patternList[pattern[len(towel):]] = subCount
            available += subCount
        
    return available

def isAvailable(pattern):
    return isPatternAvailable(ORDERED_TOWELS, pattern)

from multiprocessing import Pool

availablePatterns = []
with click.progressbar(INITIAL_PATTERNS) as bar:
    with Pool(20) as processes:
        availablePatterns = processes.map(isAvailable, bar)

#availablePatterns = [pattern for pattern in availablePatterns if pattern[0]]
count = sum(availablePatterns)


# print(f"Available patterns: {availablePatterns}")
print(f"Available patterns count: {count}")
