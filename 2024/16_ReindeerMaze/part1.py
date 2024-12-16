#!/bin/python3

import copy
import click

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])

filename = f"{filepath}/00_example2.data"
filename = f"{filepath}/00_test.data"

filename = f"{filepath}/00_example1.data"

# Read data
INITIAL_MAZE = []
with open(filename, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    INITIAL_MAZE = [list(row.strip()) for row in lines]

# Helper functions
def printMaze(maze):
    for row in maze:
        for item in row:
            print (item, end='')
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

def findStart(maze):
    TOKEN_START   = 'S'
    return findToken(maze, TOKEN_START)

def isWall(maze, pos):
    TOKEN_WALL  = '#'
    return maze[pos[1]][pos[0]] == TOKEN_WALL

def isEmpty(warehouse, pos):
    TOKEN_EMPTY = '.'
    return warehouse[pos[1]][pos[0]] == TOKEN_EMPTY

# Moving functions
def getNextPosition(reindeer, direction): # Test performance if/else vs calculateAll/getToken
    positions = {'n' : [reindeer[0]  , reindeer[1]-1],
                 'e' : [reindeer[0]+1, reindeer[1]  ],
                 's' : [reindeer[0]  , reindeer[1]+1],
                 'w' : [reindeer[0]-1, reindeer[1]  ]}
    return positions[direction] 

def rotate(direction, rotation): # CW=1, CCW=-1
    directions = ['n', 'e', 's', 'w']
    dir = (direction + len(directions) + rotation) % len(directions)
    return dir

def move():
    pass


# ###################################
# # Part 1 - Find lowest score path #
# ###################################

if __name__ == "__main__":

    # Print initial state of the problem
    print("Initial Maze:")
    maze = INITIAL_MAZE
    printMaze(maze)
    
    # Init first part
    START = findStart(maze)
    END   = findEnd(maze)
    print(f"Start: {START} - End: {END}")

    # Run part 1

    # print(f"\nFinal maze:")
    # printMaze(maze)

    # Run part 1: Calculate GPS
    # gpsTotal = calculateGPS(warehouse)

    # Output result
    lowestScore = 0
    print(f"Lowest score: {lowestScore}")
