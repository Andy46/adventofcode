import copy
import click

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/00_example1.data"
filename = f"{filepath}/00_example2.data"
filename = f"{filepath}/00_test.data"

# Read data
initialData = []
with open(filename, "r") as file:
    initialData = list(map(int, file.readline().strip().split(" ")))

#######################################
# Part 1 - Count pebbles (brute force)#
#######################################

# Helper functions
def blink(pebble):
    if pebble == 0:
        return [1]
    elif len(str(pebble)) % 2 == 0:
        string = str(pebble)
        half = int(len(string)/2)
        pebble_a = int(string[:half])
        pebble_b = int(string[half:])
        return [pebble_a, pebble_b]
    else:
        return [pebble*2024]
        
# Calculate
finalPebbles = initialData.copy()
with click.progressbar(range(25)) as bar: # Progress bar
    for i in bar:
        initialPebbles = finalPebbles
        finalPebbles = []
        for pebble in initialPebbles:
            finalPebbles.extend(blink(pebble))
            
print(f"=== Part 1 ===")
print(f"Pebble count = {len(finalPebbles)}")

#################################################
# Part 2 - Count more pebbles (less brute force)#
#################################################

# Helper functions
def blinkN(pebble):
    pebbleId     = pebble[0]
    pebbleAmount = pebble[1]
    if pebbleId == 0:
        return [[1, pebbleAmount]]
    elif len(str(pebbleId)) % 2 == 0:
        string = str(pebbleId)
        half = int(len(string)/2)
        pebbleId_a = int(string[:half])
        pebbleId_b = int(string[half:])
        return [[pebbleId_a, pebbleAmount], [pebbleId_b, pebbleAmount]]
    else:
        return [[pebbleId*2024, pebbleAmount]]

def groupPebbles(pebbles):
    newPebbles = copy.deepcopy(pebbles)
    newPebbles = sorted(newPebbles, key=lambda pebble : pebble[0])
    groupedPebbles = []
    for pebble in newPebbles:
        gPebble = next((gPebble for gPebble in groupedPebbles if gPebble[0] == pebble[0]), None)
        if gPebble:
            gPebble[1] = gPebble[1] + pebble[1]
        else:
            groupedPebbles.append(pebble)
    return groupedPebbles

# Calculate
finalPebblesN = [[pebble, 1] for pebble in initialData]
with click.progressbar(range(75)) as bar: # Progress bar
    for i in bar:
        initialPebblesN = finalPebblesN
        finalPebblesN = []
        for pebble in initialPebblesN:
            finalPebblesN.extend(blinkN(pebble))
        finalPebblesN = groupPebbles(finalPebblesN)

# Output results
totalPebbles = sum([pebble[1] for pebble in finalPebblesN])
print(f"=== Part 2 ===")
print(f"Different pebble count = {len(finalPebblesN)}")
print(f"Total pebble count = {totalPebbles}")
