#!/bin/python3

import copy
import click

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])

filename = f"{filepath}/00_test.data"

filename = f"{filepath}/00_example1.data"
filename = f"{filepath}/00_example2.data"

# Read data
INITIAL_MAZE = []
with open(filename, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    INITIAL_MAZE = [list(row.strip()) for row in lines]

# Helper functions
def printMaze(maze):
    for row in maze:
        for item in row:
            if str(item) in "E#.S?":
                print (item*6, end='')
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

# def getDirPosition(reindeer, direction): 
#     return getAllDirPositions([direction])

# def rotate(direction, rotation): # CW=1, CCW=-1
#     directions = ['n', 'e', 's', 'w']
#     dir = (direction + len(directions) + rotation) % len(directions)
#     return dir

# Maze related functions
# def isValidPosition(maze, position):
#     return isEmpty(maze, position)

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
        ROTATION_COST = 1000
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

    cost = 0
    newPositions = [[FIRST, 'e', cost]]
    setMazeCell(maze, FIRST, cost)
    while len(newPositions):
        nextPositions = [] 
        for cell in newPositions:
            nextPositions.extend(getNextPositionsInMaze(maze, cell, LAST))
        cost += 1
        # printMaze(maze)
        newPositions = nextPositions
    return maze



def getNextTilesInMaze(maze, reindeerPos, FIRST, LAST):
    if all([a==b for a,b in zip(reindeerPos, LAST)]):
        return []
    
    currentPosition  = reindeerPos

    allNextPositions = [position for position, dir in getAllDirPositions(currentPosition)]

    # Remove not interesting tiles
    allNextPositions = [position for position in allNextPositions if not isWall(maze, position) and not isEmpty(maze, position)]

    if reindeerPos == FIRST:
        # Remove tiles not in the best paths
        allNextPositions = [position for position in allNextPositions if \
                            (getMazeCell(maze, reindeerPos) - getMazeCell(maze, position) == 1) or \
                            (getMazeCell(maze, reindeerPos) - getMazeCell(maze, position) == 1001)]
    else:
    # Remove tiles not in the best paths
        allNextPositions = [position for position in allNextPositions if \
                            (getMazeCell(maze, reindeerPos) - getMazeCell(maze, position) == 1)    or \
                            (getMazeCell(maze, reindeerPos) - getMazeCell(maze, position) == 1001) or \
                            (getMazeCell(maze, position) - getMazeCell(maze, reindeerPos) == 999)]

    return allNextPositions

def countTilesInBestPaths(MAZE, FIRST, LAST):
    maze = copy.deepcopy(MAZE)
    printingMaze = copy.deepcopy(MAZE)

    allTiles = []

    newPositions = [FIRST]
    while len(newPositions):
        allTiles.extend(newPositions)
        nextPositions = [] 
        for cell in newPositions:
            nextPositions.extend(getNextTilesInMaze(maze, cell, FIRST, LAST))
            setMazeCell(printingMaze, cell, '.')
        # printMaze(printingMaze)
        newPositions = nextPositions
    return allTiles


# ###################################
# # Part 1 - Find lowest score path #
# ###################################

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

    filledMaze = floodFill(maze, START, END)
    print(f"\nFinal maze:")
    # printMaze(filledMaze)

    # Output result
    lowestScore = getMazeCell(filledMaze, END)
    print(f"Lowest score: {lowestScore}")

    tiles = countTilesInBestPaths(filledMaze, END, START)
    tiles = list(set(map(tuple,tiles)))
    print(f"Number of tiles: {len(tiles)}")


