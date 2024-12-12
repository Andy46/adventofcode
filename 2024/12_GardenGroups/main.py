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

#######################################
# Part 1 -  #
#######################################
def printGarden(garden):
    for row in garden:
        print(row)

# TODO: Change is in garden to use local variable
# def isInGarden(x, y):
#     return ((x >= 0) and (x < len(initialData))) and ((y >= 0) and (y < len(initialData[0])))
def isInGarden(cell):
    return ((cell[0] >= 0) and (cell[0] < len(initialData))) and ((cell[1] >= 0) and (cell[1] < len(initialData[0])))

def getContiguousPlant(x, y):
    cells = [[x-1,y],[x,y-1],[x+1,y],[x,y+1]]
    cells = list(filter(isInGarden, cells))
    return cells

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
            nextCells = [c for c in contiguousCells if garden[c[0]][c[1]] == plant]
        newCells = nextCells

    return plant, region

def findRegions(garden):
    regions = {}
    for x in range(len(garden)):
        for y in range(len(garden[0])):
            if garden[x][y] is not None:
                plant, region = getRegion(garden, x, y)
                print(f"{plant}: {region}")
                if plant in regions:
                    regions[plant].append(region)
                else:
                    regions[plant] = [region]
    return regions


# print(f"=== Part 0 ===")
# gardenCopy = copy.deepcopy(initialData)
# printGarden(gardenCopy)
# print(f"Region for {[0,0]}: {getRegion(gardenCopy, 0, 0)}")
# printGarden(gardenCopy)
# print(f"==============")

# Calculate
gardenCopy = copy.deepcopy(initialData)
regions = findRegions(gardenCopy)

# Output results

print(f"=== Part 1 ===")
for key in regions.keys():
    print(f"{key}: {regions[key]}")

allRegions = []
for plantRegions in regions.values():
    print(plantRegions)
    allRegions.extend(plantRegions)
print(allRegions)
print(f"==============")

print(f"=== Part 2 ===")
print(f"==============")

