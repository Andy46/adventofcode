#!/bin/python3

import copy
import click

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])

filename, EXAMPLE = f"{filepath}/00_example1.data", True
filename, EXAMPLE = f"{filepath}/00_test.data", False

# Read data
INITIAL_MAZE = []
with open(filename, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    INITIAL_MAZE = [list(row.strip()) for row in lines]

# Helper functions
def printMaze(maze):
    for row in maze:
        for item in row:
            if str(item) in "E#.S":
                if EXAMPLE:
                    print (item*2, end='')
                else:
                    print (item*6, end='')
            else:
                if EXAMPLE:
                    print("{0:2d}".format(item), end='')
                else:
                    print("{0:6d}".format(item), end='')
        print("")

# Find and detection functions
def findToken(maze, token):
    for y in range(len(maze)):
        for x in range(len(maze)):
            if maze[y][x] == token:
                return [x,y]
    print(f"ERROR: No {token} found")
    return None

def findEnd(maze):
    TOKEN_END   = 'E'
    return findToken(maze, TOKEN_END)

def isEnd(maze, pos):
    TOKEN_END   = 'E'
    return maze[pos[1]][pos[0]] == TOKEN_END

def findStart(maze):
    TOKEN_START   = 'S'
    return findToken(maze, TOKEN_START)

def isStart(maze, pos):
    TOKEN_START   = 'S'
    return maze[pos[1]][pos[0]] == TOKEN_START

def isWall(maze, pos):
    TOKEN_WALL  = '#'
    return maze[pos[1]][pos[0]] == TOKEN_WALL

def isEmpty(maze, pos):
    TOKEN_EMPTY = '.'
    return maze[pos[1]][pos[0]] == TOKEN_EMPTY

# Transformation functions

def getAllDirPositions(position):
    return [[[position[0]  , position[1]-1], 'n'],
            [[position[0]+1, position[1]  ], 'e'],
            [[position[0]  , position[1]+1], 's'],
            [[position[0]-1, position[1]  ], 'w']]

def getAllDirPositionsN(position, N):
    return [[[position[0]  , position[1]-N], 'n'],
            [[position[0]+N, position[1]  ], 'e'],
            [[position[0]  , position[1]+N], 's'],
            [[position[0]-N, position[1]  ], 'w']]

# Maze related functions
def isValidPosition(maze, position):
    return (position[0] >= 0 and position[0] < len(maze[0]) and 
                position[1] >= 0 and position[1] < len(maze))

def setMazeCell(maze, cell, cost):
    maze[cell[1]][cell[0]] = cost

def getMazeCell(maze, cell):
    return maze[cell[1]][cell[0]]

def getNextPositionsInMaze(maze, current, LAST):
    if all([a==b for a,b in zip(current[0], LAST)]):
        return []
    
    currentPosition  = current[0]
    currentDirection = current[1]
    currentCost      = current[2]

    directions = ['n','e','s','w']
    allNextPositions = [[position,dir] for position, dir in getAllDirPositions(currentPosition) if isValidPosition(maze, position)]

    nextPositions = []
    for newPosition, newDirection in allNextPositions:
        ROTATION_COST = 0
        FORWARD_COST  = 1

        rotationCW = abs(directions.index(newDirection) - directions.index(currentDirection))
        rotationCCW = 4 - rotationCW
        rotations = min([rotationCW,rotationCCW])

        newCost = currentCost + ((rotations * ROTATION_COST) + FORWARD_COST)
        
        # Write cost to cell
        if not isWall(maze, newPosition):
            if isEnd(maze, newPosition) or isEmpty(maze, newPosition):
                setMazeCell(maze, newPosition, newCost)
                nextPositions.append([newPosition, newDirection, newCost])
            elif isStart(maze, newPosition):
                continue
            else:
                cellCost = getMazeCell(maze, newPosition)
                if newCost < cellCost:
                    setMazeCell(maze, newPosition, newCost)
                    nextPositions.append([newPosition, newDirection, newCost])

    return nextPositions

def floodFill(MAZE, FIRST, LAST):
    maze = copy.deepcopy(MAZE)
    newPositions = [[FIRST, 'e', 0]]
    cost = 0
    setMazeCell(maze, FIRST, cost)
    while len(newPositions):
        nextPositions = [] 
        for cell in newPositions:
            nextPositions.extend(getNextPositionsInMaze(maze, cell, LAST))
        cost += 1
        # printMaze(maze)
        newPositions = nextPositions
    setMazeCell(maze, LAST, cost)
    return maze

##################################
# Part 1 - Find fastest with 2ns #
##################################

def countShortcuts(maze, shortlen):

    totalSaved = []
    for x in range(len(maze[0])):
        for y in range(len(maze)):
            currentPosition = [x,y]
            if not isWall(maze, currentPosition):
                allNextPositions = [position for position, dir in getAllDirPositionsN(currentPosition, shortlen) if isValidPosition(maze, position) and not isWall(maze,position)]
                for nextPosition in allNextPositions:
                    if not isWall(maze, nextPosition):
                        currentValue = int(getMazeCell(maze, currentPosition))
                        nextValue     = int(getMazeCell(maze, nextPosition))
                        if nextValue < currentValue:
                            totalSaved.append(currentValue - nextValue - shortlen)
    return totalSaved

if __name__ == "__main__":

    # Print initial state of the problem
    # print("Initial Maze:")
    maze = INITIAL_MAZE
    # printMaze(maze)
    
    # Init first part
    START = findStart(maze)
    END   = findEnd(maze)
    # print(f"Start: {START} - End: {END}")

    # Run part 1
    # filledMaze = floodFill(maze, END, START)
    # print(f"\nFinal maze:")
    # printMaze(filledMaze)

    filledMaze = floodFill(maze, END, START)
    # print(f"\nFinal maze:")
    # printMaze(filledMaze)

    shortlen = 2
    totalSaved = countShortcuts(filledMaze, shortlen)
    greaterThan100 = [saved for saved in totalSaved if saved >= 100]
    print(f"Total saved with shortcuts: {len(greaterThan100)}")