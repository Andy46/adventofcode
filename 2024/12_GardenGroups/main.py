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

#######################################
# Part 1 -  #
#######################################
def printGarden(garden):
    for row in garden:
        print(row)

# TODO: Change is in garden to use local variable
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

# Output results

print(f"=== Part 1 ===")

# Find regions
gardenCopy = copy.deepcopy(initialData)
regions = findRegions(gardenCopy)

# Calculate total fence price
gardenCopy = copy.deepcopy(initialData)
fencePrice = calculateFencePrice(gardenCopy, regions)

print(f"Fences price: {fencePrice}")
print(f"==============")


print(f"=== Part 2 ===")

def calculateExternalSides(region):
    def rotate(token, rotation):
        # CW  -> dir = 1
        # CCW -> dir = -1
        dirs = ['n', 'e', 's', 'w']

        return dirs[((dirs.index(token) + rotation) + len(dirs)) % len(dirs)]
    
    def getNextCell(x, y, dirToken):
        if dirToken == 'n':
            return x-1, y
        elif dirToken == 'e':
            return x, y+1
        elif dirToken == 's':
            return x+1, y
        elif dirToken == 'w':
            return x, y-1

    firstCell = region[0]
    firstDir  = 'e'
    
    currentCell = firstCell
    currentDir = firstDir

    sides = 0
    
    region = list(map(tuple, region))
    while True:
        nextLeftCell  = getNextCell(currentCell[0], currentCell[1], rotate(currentDir, -1))
        nextFrontCell = getNextCell(currentCell[0], currentCell[1], currentDir)

        if tuple(nextLeftCell) in region:
            currentDir = rotate(currentDir, -1)
            currentCell = nextLeftCell
            sides = sides + 1

        elif tuple(nextFrontCell) in region:
            currentDir = currentDir
            currentCell = nextFrontCell

        else:
            currentDir = rotate(currentDir, 1)
            currentCell = currentCell
            sides = sides + 1

        if (tuple(currentCell) == tuple(firstCell)) and (currentDir == firstDir):
            break
    return sides

def calculateSidesPrice(regions):
    totalPrice = 0
    for plant in regions.keys():
        for region in regions[plant]:
            regionSides = calculateExternalSides(region)
            # print(f"{plant}({regionSides}): {region}")
            totalPrice += (regionSides * len(region))
    return totalPrice

sidePrice = calculateSidesPrice(regions)
print(f"Sides price: {sidePrice}")

print(f"==============")

