#!/bin/python3

import copy
import click

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])

filename = f"{filepath}/00_example1.data"
MAZE_WIDTH, MAZE_HEIGHT = 7, 7
START_MS, END_MS = 12, 25

filename = f"{filepath}/00_test.data"
MAZE_WIDTH, MAZE_HEIGHT = 71, 71
START_MS, END_MS = 1024, 3045

TOKEN_EMPTY = '.'
TOKEN_WALL  = '#'
TOKEN_START = 'S'
TOKEN_END   = 'E'

# Read data
START_POS = [0,0]
END_POS   = [MAZE_WIDTH-1,MAZE_HEIGHT-1]

with open(filename, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    END_MS = len(lines)

def simulateMaze(SIM_MS):
    INITIAL_MAZE = []
    for y in range(MAZE_HEIGHT):
        row = []
        for x in range(MAZE_WIDTH):
            row.append(TOKEN_EMPTY)
        INITIAL_MAZE.append(row)
    ns = 0
    with open(filename, "r") as file:
        lines = [line.strip() for line in file.readlines()]
        END_MS = len(lines)
        for line in lines:
            x,y = [int(v) for v in line.split(',')]
            INITIAL_MAZE[y][x] = TOKEN_WALL
            ns += 1
            if ns >= SIM_MS:
                break
    INITIAL_MAZE[START_POS[0]][START_POS[1]] = TOKEN_START
    INITIAL_MAZE[END_POS[0]][END_POS[1]] = TOKEN_END
    
    return INITIAL_MAZE

# Helper functions
def printMaze(maze):
    for row in maze:
        for item in row:
            if str(item) in "E#.S":
                print (item*2, end='')
            else:
                print("{0:2d}".format(item), end='')
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
    if pos[0] < 0 or pos[0] >= MAZE_WIDTH:
        return True
    if pos[1] < 0 or pos[1] >= MAZE_HEIGHT:
        return True
    else:
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

# Maze related functions
def isValidPosition(maze, position):
    return isEmpty(maze, position)

def setMazeCell(maze, cell, cost):
    maze[cell[1]][cell[0]] = cost

def getMazeCell(maze, cell):
    return maze[cell[1]][cell[0]]

def getNextPositionsInMaze(maze, reindeer, LAST):
    if all([a==b for a,b in zip(reindeer[0], LAST)]):
        return []
    
    currentPosition  = reindeer[0]
    currentDirection = reindeer[1]
    currentCost      = reindeer[2]

    directions = ['n','e','s','w']
    allNextPositions = getAllDirPositions(currentPosition)

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
    while len(newPositions):
        nextPositions = [] 
        for cell in newPositions:
            nextPositions.extend(getNextPositionsInMaze(maze, cell, LAST))
        cost += 1
        # printMaze(maze)
        newPositions = nextPositions
    return maze

###############################################
# Part 2 - Find the blocking block's position #
###############################################

if __name__ == "__main__":

    print (f"MS: {START_MS} -> {END_MS}")
    for ms in range(START_MS, END_MS):
        # Print initial state of the problem
        # print("Initial Maze:")
        maze = simulateMaze(ms)
        # printMaze(maze)
        
        # Init first part
        START = findStart(maze)
        END   = findEnd(maze)
        # print(f"Start: {START} - End: {END}")

        # Run part 1
        # filledMaze = floodFill(maze, END, START)
        # print(f"\nFinal maze:")
        # printMaze(filledMaze)

        filledMaze = floodFill(maze, START, END)
        # print(f"\nFinal maze:")
        # printMaze(filledMaze)

        # Run part 1: Calculate GPS
        # gpsTotal = calculateGPS(warehouse)

        # Output result
        lowestScore = getMazeCell(filledMaze, END)
        # print(f"Lowest score: {lowestScore}")
        if lowestScore == TOKEN_END:
            print(f"MS -> {ms}")
            with open(filename, "r") as file:
                lines = [line.strip() for line in file.readlines()]
                print(f"Cell -> {lines[ms-1]}")
            break