import copy
import click

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/00_example.data"
filename = f"{filepath}/00_example2.data"
filename = f"{filepath}/00_example3.data"
filename = f"{filepath}/00_example4.data"

filename = f"{filepath}/00_test.data"

# Read data
initialData = []
with open(filename, "r") as file:
    initialData = [list(line.strip()) for line in file.readlines()]

# Helper functions
def findAntennas(data):
    EMPTY_TOKEN = '.'
    antennas = {}
    for row in range(len(data)):
        for col in range(len(data[0])):
            if data[row][col] != EMPTY_TOKEN:
                antenna = data[row][col]
                if data[row][col] not in antennas:
                    antennas[antenna] = []
                antennas[antenna].append(list([row,col]))
    return antennas
antennas = findAntennas (initialData)

def isInMap(pos):
    x = pos[0]
    y = pos[1]
    return (x >= 0 and x < len(initialData)) and (y >= 0 and y < len(initialData[0]))

###########################
# Part 1 - Find antinodes #
###########################

# Helper functions for part 1
def findAntinodes(antenna):
    antinodes = []
    for x in range(len(antenna)):
        posA = list(antenna[x])
        for y in range(x+1, len(antenna)):
            posB = list(antenna[y])
            diff = list([posA[0] - posB[0], posA[1] - posB[1]])
            antiA = list([posA[0] + diff[0], posA[1] + diff[1]])
            antiB = list([posA[0] - diff[0], posA[1] - diff[1]])
            antiC = list([posB[0] + diff[0], posB[1] + diff[1]])
            antiD = list([posB[0] - diff[0], posB[1] - diff[1]])
            antis = [antiA, antiB, antiC, antiD]
            for a in antis.copy():
                if list(a) == posA or list(a) == posB:
                    antis.remove(a)       
            antis = list(filter(isInMap, antis))
            antinodes.extend(antis)

    return antinodes

# Calculate
antinodes = {}
for antenna, positions in antennas.items():
    positions = list(map(tuple, positions))
    antinodes[antenna] = findAntinodes(positions) 

allAntinodes = []
for antenna, positions in antinodes.items():
    allAntinodes.extend(positions)

allAntinodes = list(map(tuple, allAntinodes))
allAntinodes = set(allAntinodes)
antinodeCount = len(allAntinodes)

# Output result
print(f"Count of antinodes in map: {antinodeCount}")

###############################
# Part 2 - Find all antinodes #
###############################

# Helper functions for part 2 
def findAntinodes(antenna):
    #####################################################################
    ## NOTE: This function does not cover antinodes between 2 antennas ##
    ##       In my case it was not necessary                           ##
    #####################################################################
    antinodes = []
    for x in range(len(antenna)):
        posA = list(antenna[x])
        for y in range(x+1, len(antenna)):
            posB = list(antenna[y])
            if posA == posB:
                continue
            else:
                diff = list([posA[0] - posB[0], posA[1] - posB[1]])
                for i in range(0, 1000): # Brute force...
                    antiA = list([posA[0] + (i*diff[0]), posA[1] + (i*diff[1])])
                    antiB = list([posA[0] - (i*diff[0]), posA[1] - (i*diff[1])])
                    antiC = list([posB[0] + (i*diff[0]), posB[1] + (i*diff[1])])
                    antiD = list([posB[0] - (i*diff[0]), posB[1] - (i*diff[1])])
                    antis = [antiA, antiB, antiC, antiD]
                    antis = list(filter(isInMap, antis))
                    antinodes.extend(antis)
                    if len(antis) == 0:
                        break            
    return antinodes

# Calculate
antinodes = {}
for antenna, positions in antennas.items():
    positions = list(map(tuple, positions))
    antinodes[antenna] = findAntinodes(positions) 

allAntinodes = []
for antenna, positions in antinodes.items():
    allAntinodes.extend(positions)

allAntinodes = list(map(tuple, allAntinodes))
allAntinodes = set(allAntinodes)
antinodeCount = len(allAntinodes)

# Output result
print(f"Count of all antinodes in map: {antinodeCount}")