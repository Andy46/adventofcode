#!/bin/python3
import copy
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

INITIAL_GARDEN = copy.deepcopy(initialData)

###########################################
# Part 2 - Find fence price with discount #
###########################################

# Functions to find regions
def isInGarden(cell):
    return ((cell[0] >= 0) and (cell[0] < len(INITIAL_GARDEN))) and ((cell[1] >= 0) and (cell[1] < len(INITIAL_GARDEN[0])))

def getContiguousCells(x, y):
    return [[x-1,y],[x,y-1],[x+1,y],[x,y+1]]

def getContiguousPlants(x, y):
    return list(filter(isInGarden, getContiguousCells(x, y)))

def clearGardenCell(garden, cell):
    garden[cell[0]][cell[1]] = None

def getRegion(garden, x, y):
    plant = INITIAL_GARDEN[x][y]
    region = []
    newCells = [[x,y]]
    garden[x][y] = None
    while len(newCells) != 0:
        region.extend(newCells)

        nextCells = []
        for cell in newCells:
            contiguousPlants = getContiguousPlants(cell[0], cell[1])
            nextCells.extend([cell for cell in contiguousPlants if (INITIAL_GARDEN[cell[0]][cell[1]] == plant and garden[cell[0]][cell[1]] is not None)])
            # Remove duplicates
            [clearGardenCell(garden, cell) for cell in nextCells]
            
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

regions = findRegions(copy.deepcopy(initialData))

# Functions to find sides of a region
def rotate(dirToken, n):
    directions = ['n', 'e', 's', 'w']
    return directions[(directions.index(dirToken) + len(directions) + n) % len(directions)]

def getNextCell(x, y, dirToken):
    if dirToken == 'n':
        return x-1, y
    elif dirToken == 'e':
        return x, y+1
    elif dirToken == 's':
        return x+1, y
    elif dirToken == 'w':
        return x, y-1


def findRegionPerimeter(region):
    firstCell = tuple(region[0])
    firstDir  = 'e'
    
    region = list(map(tuple, region))
    
    currentCell = firstCell
    currentDir = firstDir
    
    perimeter = 0
    while True:
        leftDir = rotate(currentDir, -1)
        x, y = currentCell[0], currentCell[1]
        nextLeftCell  = getNextCell(x, y, leftDir)
        nextFrontCell = getNextCell(x, y, currentDir)
        
        if tuple(nextLeftCell) in region:
            currentCell = nextLeftCell
            currentDir  = rotate(currentDir, -1)
            perimeter   = perimeter
        elif tuple(nextFrontCell) in region:
            currentCell = nextFrontCell
            currentDir  = currentDir
            perimeter   = perimeter + 1
        else:
            currentCell = currentCell
            currentDir  = rotate(currentDir, 1)
            perimeter   = perimeter + 1
                    
        if tuple(currentCell) == firstCell and currentDir == firstDir:
            break
    return perimeter

totalPrice = 0
for key in regions.keys():
    for region in regions[key]:
        regionPerimeter = findRegionPerimeter(region)
        # print(f"Region: {region} - {regionPerimeter}")
        regionPrice = regionPerimeter * len(region)
        totalPrice += regionPrice

# Helper functions for part 2
def constructRegion(plant, region):
    minX = min([cell[1] for cell in region])
    maxX = max([cell[1] for cell in region])
    minY = min([cell[0] for cell in region])
    maxY = max([cell[0] for cell in region])
    
    deltaX = (maxX - minX)
    deltaY = (maxY - minY)
        
    regionMap = []
    for y in range(deltaY + 1):
        row = []
        for x in range(deltaX + 1):
            row.append(None)
        regionMap.append(row)

    for cell in region:
        x = ((cell[1] - minX))
        y = ((cell[0] - minY))
        regionMap[y][x] = plant
    return regionMap

def printRegionMap(key, region):
    for row in region:
        print(f"{key}: {row}")

def printRegion(key, region):
    for row in region:
        print(f"{key}: {row}")

# Functions to find internal regions within a region
def isInRegion(region, cell):
    return ((cell[0] >= 0) and (cell[0] < len(region))) and ((cell[1] >= 0) and (cell[1] < len(region[0])))

def isNone(region, cell):
    return region[cell[0]][cell[1]] is None

def getContiguousNoneCells(x, y):
    return [[x-1,y],[x-1,y-1],[x,y-1],[x+1,y-1],[x+1,y],[x+1,y+1],[x,y+1],[x-1,y+1]]

def getContiguousNone(region, x, y):
    nones = []
    for cell in getContiguousNoneCells(x, y):
        if isInRegion(region, cell):
            if isNone(region, cell):
                nones.append(cell)
    return nones
    
notNone = '.'
def clearNoneCell(mainRegion, cell):
    mainRegion[cell[0]][cell[1]] = notNone
    
def getNoneRegion(mainRegion, x, y):
    initialMainRegion = copy.deepcopy(mainRegion)
    region = []
    newCells = [[x,y]]
    mainRegion[x][y] = notNone
    while len(newCells) != 0:
        region.extend(newCells)

        nextCells = []
        for cell in newCells:
            # get contiguous cells to all cells
            contiguousNones = getContiguousNone(initialMainRegion, cell[0], cell[1])
            nextCells.extend([cell for cell in contiguousNones if (mainRegion[cell[0]][cell[1]] is None)])
            for cell in nextCells:
                if cell in region:
                    nextCells.remove(cell)
            # Remove duplicates
            [clearNoneCell(mainRegion, cell) for cell in nextCells]
            
        newCells = nextCells
    return region

def findNoneRegionsWithin(mainRegion):
    noneRegions = []
    for x in range(len(mainRegion)):
        for y in range(len(mainRegion[0])):
            if mainRegion[x][y] is None:
                region = getNoneRegion(mainRegion, x, y)
                noneRegions.append(region)
                # printRegionMap('.', mainRegion)

    return noneRegions

def isInnerNoneRegion(mainRegion, noneRegion):
    def isIn(cell):
        return (cell[0] > 0 and cell[0] < (len(mainRegion) - 1)) and ((cell[1] > 0 and cell[1] < (len(mainRegion[0])-1)))
    allIn = all([isIn(cell) for cell in noneRegion])
    # Is not connected to other region
    return allIn and True

# Functions to find sides of a region
def rotate(dirToken, n):
    directions = ['n', 'e', 's', 'w']
    return directions[(directions.index(dirToken) + len(directions) + n) % len(directions)]

def getNextCell(x, y, dirToken):
    if dirToken == 'n':
        return x-1, y
    elif dirToken == 'e':
        return x, y+1
    elif dirToken == 's':
        return x+1, y
    elif dirToken == 'w':
        return x, y-1

def findRegionSides(region):
    firstCell = tuple(region[0])
    firstDir  = 'e'
    
    region = list(map(tuple, region))
    
    currentCell = firstCell
    currentDir = firstDir
    
    sides = 0
    while True:
        leftDir = rotate(currentDir, -1)
        x, y = currentCell[0], currentCell[1]
        nextLeftCell  = getNextCell(x, y, leftDir)
        nextFrontCell = getNextCell(x, y, currentDir)
        
        if tuple(nextLeftCell) in region:
            currentCell = nextLeftCell
            currentDir  = rotate(currentDir, -1)
            sides       = sides + 1
        elif tuple(nextFrontCell) in region:
            currentCell = nextFrontCell
            currentDir  = currentDir
            sides       = sides
        else:
            currentCell = currentCell
            currentDir  = rotate(currentDir, 1)
            sides       = sides + 1
                    
        if tuple(currentCell) == firstCell and currentDir == firstDir:
            break
    return sides

# Calculate total price with discount
regions = findRegions(copy.deepcopy(initialData))
totalPrice = 0    
for key in regions.keys():
    for region in regions[key]:
        externalSidesPrice = 0

        # 1 - Construct region to find sub regions
        constructedRegion = constructRegion(key, region)
        # printRegionMap(key, constructedRegion)
        # print(f"Region size: {key}-{len(region)}")
        
        # 2 - Find external sides of the region
        externalSides = findRegionSides(region)
        externalSidesPrice = externalSides * len(region)
        # print(f"External sides: {key}-{externalSides}")
        # print(f"External sides price: {key}-{externalSidesPrice}")

        # 3 - Find internal sub-regions of the current region
        mainRegion = copy.deepcopy(constructedRegion)
        noneRegions = findNoneRegionsWithin(mainRegion)
        internalRegions = []
        for noneRegion in noneRegions:
            # print(f"is inner: {isInnerNoneRegion(mainRegion, noneRegion)}")
            if isInnerNoneRegion(mainRegion, noneRegion):
                internalRegions.append(noneRegion)
                
        # 4 - Find sides for each internal region
        internalSides = 0
        for internal in internalRegions:
            internalRegionSides = findRegionSides(internal)
            internalSides += internalRegionSides
        internalSidesPrice = internalSides * len(region)
        # print(f"Internal sides: {key}-{internalSides}")
        # print(f"Internal sides price: {key}-{internalSidesPrice}")

        # 5 - Summ up all sides
        allSides = externalSides + internalSides
        allSidesPrice = allSides * len(region)
        # print(f"All  sides: {key}-{allSides}")
        # print(f"All sides price: {key}-{allSidesPrice}")

        # 6 - Calculate price for the region
        totalRegionPrice = allSides * len(region)
        # print(f"Total region price: {key}-{totalRegionPrice}")

        # 7 - Accumulate the region price
        totalPrice += totalRegionPrice
        
# Output result
print(f"Total price with discount: {totalPrice}")