ardenGroups/main.py
import copy
import click
import multiprocessing
from multiprocessing import Pool

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/00_example2.data"
filename = f"{filepath}/00_example3.data"
filename = f"{filepath}/00_test.data"

filename = f"{filepath}/00_example1.data"

# Read data
initialData = []
with open(filename, "r") as file:
    initialData = list(list(line.strip()) for line in file.readlines())
print (initialData)

initialGarden = copy.deepCopy(initialData)

#######################################
# Part 1 - 
#######################################

def isInGarden(cell):
    return ((cell[0] >= 0) and (cell[0] < len(iniditalGarden))) and ((cell[1] >= 0) and (cell[1] < len(initialGarden[0])))

def getContiguousCells(x, y):
    return [[x-1,y],[x,y-1],[x+1,y],[x,y+1]]

def getContiguousCells(garden, x, y):
    cells = filter(isInGarden, getContiguousCells())
    return cells

def clearGardenCell(garden, cell):
    garden[cell[0]][cell[1]] = None

def getRegion(garden, x, y):
    plant = initialGarden[x][y]
    region = []
    found = True
    newCells = [[x,y]]
    garden[x][y] = None
    while len(newCells) != 0:
        nextCells = []
        for cell in newCells:
            nextCells = list(

            # Remove cell from search list
            nextCells.append(cell)

        newCells = nextCells



def findRegions(garden):
    regions = {}
    for x in range(len(garden)):
        for y in range(len(garden[0])):
            if garden[x][y] is not None:
                plant, region = getRegion(garden, x, y)
                #[garden[cell[0]][cell[1] = None for cell in region]
                if plant in regions:
                    regions[plant].append(region)
                else:
                    regions[plant] = [region]
    return regions




regions = findRegions(copy.deepcopy(initialData))

# Output results
