#!/bin/python3

import copy
import click

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])

filename = f"{filepath}/00_example1.data"
filename = f"{filepath}/00_test3.data"
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

def isPatternAvailable(towels, pattern):
    if pattern == "":
        # return [True, []]
        return True
    
    matchingTowels = []
    if pattern[0] in towels:
        matchingTowels = [towel for towel in towels[pattern[0]] if towel == pattern[:len(towel)]]

    available = False
    for towel in matchingTowels:
        available = isPatternAvailable(towels, pattern[len(towel):])
        if available:
            return True

    return False

def isAvailable(pattern):
    temp = isPatternAvailable(ORDERED_TOWELS, pattern)
    temp.append(pattern)
    return temp

###################################
# Part 1 - All towel combinations #
###################################

# Calculate
availablePatterns = []
for pattern in INITIAL_PATTERNS:
    temp = isPatternAvailable(ORDERED_TOWELS, pattern)
    availablePatterns.append(temp)
count = len([pattern for pattern in availablePatterns if pattern])

# Output result
print(f"Available patterns count: {count}")
