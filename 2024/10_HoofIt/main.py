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
    for line in file.readlines():
        initialData.append(list(map(int, list(line.strip()))))
print(initialData)

# Helper functions
HEADTRAILS=[0]
def findHeadTrails(topoMap):
    headTrails = []
    for x in range(len(topoMap)):
        for y in range(len(topoMap[0])):
            if topoMap[x][y] in HEADTRAILS:
                headTrails.append([x,y])
    return headTrails
    
def isStep(a, b):
    return b == (a + 1)
    
def isEnd(a):
    return a == 9
    
def isInMap(topoMap, pos):
    x = pos[0]
    y = pos[1]
    return (x >= 0 and x < len(topoMap)) and (y >= 0 and y < len(topoMap[0]))

def countTrailsEndPoints(topoMap, currentPos, endPoints):
    trails = 0
    x = currentPos[0]
    y = currentPos[1]
    DIRECTIONS = [[-1,0], [0,1], [1,0], [0,-1]]
    for dirPos in DIRECTIONS:
        nextPos = [pair[0]+pair[1] for pair in zip(currentPos, dirPos)]
        if isInMap(topoMap, nextPos):
            currentVal = topoMap[currentPos[0]][currentPos[1]]
            nextVal = topoMap[nextPos[0]][nextPos[1]]
            if isStep(currentVal, nextVal):
                if isEnd(nextVal):
                    trails = trails + 1
                    endPoints.append(nextPos)
                else:
                    trails = trails + countTrailsEndPoints(topoMap, nextPos, endPoints)
    return trails

def countTrailPaths(topoMap, currentPos):
    trails = 0
    x = currentPos[0]
    y = currentPos[1]
    DIRECTIONS = [[-1,0], [0,1], [1,0], [0,-1]]
    for dirPos in DIRECTIONS:
        nextPos = [pair[0]+pair[1] for pair in zip(currentPos, dirPos)]
        if isInMap(topoMap, nextPos):
            currentVal = topoMap[currentPos[0]][currentPos[1]]
            nextVal = topoMap[nextPos[0]][nextPos[1]]
            if isStep(currentVal, nextVal):
                if isEnd(nextVal):
                    trails = trails + 1
                    print(nextPos)
                else:
                    trails = trails + countTrailPaths(topoMap, nextPos)
    return trails

####################################
# Part 1&2 - Count trails and ends #
####################################

headTrails = findHeadTrails(initialData)
print(f"Head trails ({len(headTrails)}: {headTrails}")

trails = 0
endPointCount = 0

with click.progressbar(headTrails) as bar: # Progress bar
    for headTrail in bar:
        headTrailEndPoints = []
        count = countTrailsEndPoints(initialData, headTrail, headTrailEndPoints)
        print(f"Head trail: {headTrail} -> {count}: {headTrailEndPoints}")
        headTrailEndPoints = set([tuple(h) for h in headTrailEndPoints])
        endPointCount = endPointCount + len(headTrailEndPoints)
        trails = trails + count

print(f"Total endPoints: {endPointCount}")
print(f"Total trails: {trails}")
