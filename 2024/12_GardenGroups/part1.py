#!/bin/python3
import copy
import click
import multiprocessing
from multiprocessing import Pool

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])

filename = f"{filepath}/00_example1.data"
filename = f"{filepath}/00_example2.data"
filename = f"{filepath}/00_example3.data"
filename = f"{filepath}/00_example4.data"
filename = f"{filepath}/00_example5.data"

filename = f"{filepath}/00_test.data"

# Read data
initialData = []
with open(filename, "r") as file:
    initialData = list(list(line.strip()) for line in file.readlines())

initialGarden = copy.deepcopy(initialData)

#############################
# Part 1 - Find fence price #
#############################

def printGarden(garden):
    for row in garden:
        print(row)

def isInGarden(cell):
    return ((cell[0] >= 0) and (cell[0] < len(initialData))) and ((cell[1] >= 0) and (cell[1] < len(initialData[0])))

def getContiguousCells (x, y):
    return [[x-1,y],[x,y-1],[x+1,y],[x,y+1]]

def getContiguousPlant(x, y):
    return list(filter(isInGarden, getContiguousCells(x, y)))

def clearCell(garden, x, y):
    garden[x][y] = None
    
def getRegion(garden, x, y):
    plant = garden[x][y]
    region = []
    newCells = [[x,y]]
    while len(newCells) != 0:
        # Add new cells to region and remove them from the garden
        region.extend(newCells)
        [clearCell(garden, c[0], c[1]) for c in newCells]

        # Find more cells for region
        nextCells = []
        for cell in newCells:
            contiguousCells = getContiguousPlant(cell[0], cell[1])
            nextCells.extend([c for c in contiguousCells if (garden[c[0]][c[1]] == plant)])
            [clearCell(garden, c[0], c[1]) for c in nextCells]
        newCells = nextCells

    return plant, region

def findRegions(garden):
    regions = {}
    for x in range(len(garden)):
        for y in range(len(garden[0])):
            if garden[x][y] is not None:
                plant, region = getRegion(garden, x, y)
                if plant in regions:
                    regions[plant].append(region)
                else:
                    regions[plant] = [region]
    return regions

def calculateFence(garden, plant, region):
    fences = 0
    for cell in region:
        contiguous = getContiguousCells(cell[0], cell[1])
        for other in contiguous:
            if not isInGarden(other):
                fences += 1 
            elif garden[other[0]][other[1]] != plant:
                fences += 1
    return fences

def calculateFencePrice(garden, regions):
    totalPrice = 0
    for plant in regions.keys():
        for region in regions[plant]:
            regionFences = calculateFence(garden, plant, region)
            totalPrice += (regionFences * len(region))
    return totalPrice

# Find regions
gardenCopy = copy.deepcopy(initialData)
regions = findRegions(gardenCopy)

# Calculate total fence price
gardenCopy = copy.deepcopy(initialData)
fencePrice = calculateFencePrice(gardenCopy, regions)

# Output results
print(f"Fences price: {fencePrice}")

