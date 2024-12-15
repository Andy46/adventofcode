#!/bin/python3

import copy
import click

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])

filename = f"{filepath}/00_example1.data"
filename = f"{filepath}/00_example2.data"

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

# Find and detection functions
TOKEN_WALL  = '#'
def isWall(warehouse, pos):
    return warehouse[pos[1]][pos[0]] == TOKEN_WALL

TOKEN_BOX   = 'O'
def isBox(warehouse, pos):
    return warehouse[pos[1]][pos[0]] == TOKEN_BOX

TOKEN_EMPTY = '.'
def isEmpty(warehouse, pos):
    return warehouse[pos[1]][pos[0]] == TOKEN_EMPTY

TOKEN_ROBOT = '@'
def findRobot(warehouse):
    for y in range(len(warehouse)):
        for x in range(len(warehouse)):
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

def findEmptyOrWall(warehouse, robot, dir):
    nextPos = getNextPosition(robot, dir)
    while True:
        if isEmpty(warehouse, nextPos):
            return nextPos
        elif isWall(warehouse, nextPos):
            return nextPos
        nextPos = getNextPosition(nextPos, dir)

# Moving functions
def getDistance(robot, position):
    return abs(sum([pair[0] - pair[1] for pair in zip(robot, position)]))

def move(warehouse, robot, direction):
    newWareHouse = copy.deepcopy(warehouse)
    newRobot = copy.deepcopy(robot)

    nextPosition = findEmptyOrWall(newWareHouse, robot, direction)
    if isEmpty(newWareHouse, nextPosition):
        distance = getDistance(robot, nextPosition)
        if distance == 1:
            newRobot = getNextPosition(robot, direction)
            newWareHouse[robot[1]][robot[0]] = TOKEN_EMPTY
            newWareHouse[newRobot[1]][newRobot[0]] = TOKEN_ROBOT
        elif distance > 1:
            newWareHouse[nextPosition[1]][nextPosition[0]] = TOKEN_BOX
            newRobot = getNextPosition(robot, direction)
            newWareHouse[robot[1]][robot[0]] = TOKEN_EMPTY
            newWareHouse[newRobot[1]][newRobot[0]] = TOKEN_ROBOT

    return newWareHouse, newRobot

# #####################################
# # Part 1 - Goods Positioning System #
# #####################################

# Helper functions for part 1
def calculateGPS(warehouse):
    total = 0
    for y in range(len(warehouse)):
        for x in range(len(warehouse[0])):
            if isBox(warehouse, [x,y]):
                total += y*100 + x
    return total

if __name__ == "__main__":

    # Print initial state of the problem
    print("Initial warehouse:")
    warehouse = INITIAL_WAREHOUSE
    printWarehouse(INITIAL_WAREHOUSE)
    # print(f"Robot moves: {INITIAL_ROBOT_MOVES}")
    
    # Init first part
    robot = findRobot(warehouse)
    print("Robot position:", robot)

    # Run part 1
    with click.progressbar(INITIAL_ROBOT_MOVES) as bar: # Progress bar
        for direction in bar:
            warehouse, robot = move(warehouse, robot, direction) 
            # print(f"Move {direction}:")
            # printWarehouse(warehouse)

    print(f"\nFinal warehouse:")
    printWarehouse(warehouse)

    # Run part 1: Calculate GPS
    gpsTotal = calculateGPS(warehouse)

    # Output result
    print(f"Sum of all boxes' GPS coordinates: {gpsTotal}")
