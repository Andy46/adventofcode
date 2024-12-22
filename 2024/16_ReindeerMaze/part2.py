#!/bin/python3

import copy
import click

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])

filename = f"{filepath}/00_example1.data"
filename = f"{filepath}/00_example2.data"
filename = f"{filepath}/00_example3.data"

filename = f"{filepath}/00_example3_moveleft.data"
filename = f"{filepath}/00_example3_moveright.data"
filename = f"{filepath}/00_example3_moveup.data"
filename = f"{filepath}/00_example3_movedown.data"

filename = f"{filepath}/00_test.data"

# Read data
INITIAL_WAREHOUSE = []
INITIAL_ROBOT_MOVES = []
with open(filename, "r") as file:
    lines = [line.strip() for line in file.readlines()]

    fileSplit = lines.index('')
    warehouseLines = lines[:fileSplit]
    movesLines = lines[(fileSplit+1):]
    
    INITIAL_WAREHOUSE = [list(row.strip()) for row in warehouseLines]

    for line in movesLines:
        INITIAL_ROBOT_MOVES.extend(list(line))

# Helper functions
def printWarehouse(warehouse):
    for row in warehouse:
        for item in row:
            print (item, end='')
        print("")

def convertWarehouse(warehouse):
    newWarehouse = []
    for y in range(len(warehouse)):
        row = []
        for x in range(len(warehouse[0])):
            if isBox(warehouse, [x,y]):
                row.extend(['[', ']'])
            elif isWall(warehouse, [x,y]):
                row.extend(['#', '#'])
            elif isEmpty(warehouse, [x,y]):
                row.extend(['.', '.'])
            elif isRobot(warehouse, [x,y]):
                row.extend(['@', '.'])
        newWarehouse.append(row)
    return newWarehouse

# Find and detection functions
TOKEN_WALL  = '#'
def isWall(warehouse, pos):
    return warehouse[pos[1]][pos[0]] == TOKEN_WALL

TOKEN_BOX_LEFT  = '['
TOKEN_BOX_RIGHT = ']'
TOKEN_BOX       = 'O'
def isBox(warehouse, pos):
    return warehouse[pos[1]][pos[0]] in [TOKEN_BOX, TOKEN_BOX_LEFT, TOKEN_BOX_RIGHT]

TOKEN_EMPTY = '.'
def isEmpty(warehouse, pos):
    return warehouse[pos[1]][pos[0]] == TOKEN_EMPTY

TOKEN_ROBOT = '@'
def isRobot(warehouse, pos):
    return warehouse[pos[1]][pos[0]] == TOKEN_ROBOT

def findRobot(warehouse):
    for y in range(len(warehouse)):
        for x in range(len(warehouse[0])):
            if warehouse[y][x] == TOKEN_ROBOT:
                return [x,y]
    print("ERROR: No robot found")
    return None

def getNextPosition(robot, dir): # Test performance if/else vs calculateAll/getToken
    positions = {'^' : [robot[0]  , robot[1]-1],
                 '>' : [robot[0]+1, robot[1]  ],
                 'v' : [robot[0]  , robot[1]+1],
                 '<' : [robot[0]-1, robot[1]  ]}
    return positions[dir] 

def findEmptyOrWall(warehouse, currentPos, dir):
    nextPos = getNextPosition(currentPos, dir)
    while True:
        if isEmpty(warehouse, nextPos):
            return nextPos
        elif isWall(warehouse, nextPos):
            return nextPos
        nextPos = getNextPosition(nextPos, dir)

def getBoxSides(warehouse, boxPos):
    posLeft = []
    posRight = []
    if warehouse[boxPos[1]][boxPos[0]] == TOKEN_BOX_LEFT:
        posLeft = [boxPos[0], boxPos[1]]
        posRight = [boxPos[0]+1, boxPos[1]]
    elif warehouse[boxPos[1]][boxPos[0]] == TOKEN_BOX_RIGHT:
        posLeft = [boxPos[0]-1, boxPos[1]]
        posRight = [boxPos[0], boxPos[1]]
    return [posLeft, posRight]

# Moving functions
def getDistance(robot, position):
    return abs(sum([pair[0] - pair[1] for pair in zip(robot, position)]))

def shiftHorizontal(row, startPos, endPos, direction):
    newRow = copy.deepcopy(row)
    if direction == '>':
        newRow[(startPos[0]+1):(endPos[0]+1)] = row[startPos[0]:(endPos[0])]
        newRow[startPos[0]] = TOKEN_EMPTY
    elif direction == '<':
        newRow[(endPos[0]):startPos[0]] = row[(endPos[0]+1):(startPos[0]+1)]
        newRow[startPos[0]] = TOKEN_EMPTY
    return newRow

def canMoveVertical(warehouse, boxPos, direction):
    
    boxSides = getBoxSides(warehouse, boxPos)
    nextPositions = [getNextPosition(pos, direction) for pos in boxSides]

    if isWall(warehouse, nextPositions[0]) or isWall(warehouse, nextPositions[1]):
        return False
    else:
        canMoveLeft  = isEmpty(warehouse, nextPositions[0]) or canMoveVertical(warehouse, nextPositions[0], direction)
        canMoveRight = isEmpty(warehouse, nextPositions[1]) or canMoveVertical(warehouse, nextPositions[1], direction)
        
        return canMoveLeft and canMoveRight

def moveVertical(warehouse, boxPos, direction):
    newWarehouse = copy.deepcopy(warehouse)

    boxSides = getBoxSides(warehouse, boxPos)
    nextPositions = [getNextPosition(pos, direction) for pos in boxSides]
    
    for newPosition in nextPositions:
        if isBox(newWarehouse,newPosition):
            newWarehouse = moveVertical(newWarehouse, newPosition, direction)
    
    newLeftSide, newRightSide = nextPositions
    newWarehouse[newLeftSide[1]][newLeftSide[0]] = TOKEN_BOX_LEFT
    newWarehouse[newRightSide[1]][newRightSide[0]] = TOKEN_BOX_RIGHT

    leftSide, rightSide = boxSides
    newWarehouse[leftSide[1]][leftSide[0]] = TOKEN_EMPTY
    newWarehouse[rightSide[1]][rightSide[0]] = TOKEN_EMPTY

    return newWarehouse

def moveBox(warehouse, boxPos, direction):
    newWarehouse = copy.deepcopy(warehouse)

    if direction == '^' or direction == 'v':
        if canMoveVertical(newWarehouse, boxPos, direction):
            newWarehouse = moveVertical(newWarehouse, boxPos, direction)
            return True, newWarehouse
    elif direction == '>' or direction == '<':
        pos = findEmptyOrWall(newWarehouse, boxPos, direction)
        if isEmpty(warehouse, pos):
            newWarehouse[boxPos[1]] = shiftHorizontal(newWarehouse[boxPos[1]], boxPos, pos, direction)
            return True, newWarehouse
    
    return False, newWarehouse

def move(warehouse, robot, direction):
    newWarehouse = copy.deepcopy(warehouse)
    newRobot     = copy.deepcopy(robot)

    def moveRobot(warehouse, robot, position):
        warehouse[robot[1]][robot[0]] = TOKEN_EMPTY
        warehouse[position[1]][position[0]] = TOKEN_ROBOT
        return warehouse, position

    nextPosition = getNextPosition(robot, direction)

    if isEmpty(newWarehouse, nextPosition):
        newWarehouse, newRobot = moveRobot(newWarehouse, robot, nextPosition)

    elif isBox(newWarehouse, nextPosition):
        moved, newWarehouse = moveBox(newWarehouse, nextPosition, direction)
        if moved:
            newWarehouse, newRobot = moveRobot(newWarehouse, robot, nextPosition)

    return newWarehouse, newRobot

#################################################
# Part 2 - Goods Positioning System (Big boxes) #
#################################################

# Helper functions for part 2
def calculateGPS(warehouse, TOKEN):
    total = 0
    for y in range(len(warehouse)):
        for x in range(len(warehouse[0])):
            if warehouse[y][x] == TOKEN:
                total += y*100 + x
    return total

if __name__ == "__main__":
    SECOND_WAREHOUSE = convertWarehouse(INITIAL_WAREHOUSE)

    # Print initial state of the problem
    print("Second warehouse:")
    warehouse = SECOND_WAREHOUSE
    printWarehouse(warehouse)
    # print(f"Robot moves: {INITIAL_ROBOT_MOVES}")

    # Init second part
    robot = findRobot(SECOND_WAREHOUSE)
    print("Robot position:", robot)

    # Run part 2
    with click.progressbar(INITIAL_ROBOT_MOVES) as bar: # Progress bar
        for direction in bar:
            warehouse, robot = move(warehouse, robot, direction) 
            # print(f"\nMove {direction}:")
            # printWarehouse(warehouse)

    print(f"\nFinal warehouse:")
    printWarehouse(warehouse)

    # Run part 2: Calculate GPS
    gpsTotal = calculateGPS(warehouse, TOKEN_BOX_LEFT)

    # Output result
    print(f"Sum of all boxes' GPS coordinates (big boxes): {gpsTotal}")