#!/bin/python3

import copy
import click
import multiprocessing
from multiprocessing import Pool
import time

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])

filename = f"{filepath}/00_example2.data"
filename = f"{filepath}/00_example1.data"
filename = f"{filepath}/00_test.data"

# Node class
class MyNode:    
    def __init__(self, position, value):
        self.position = position
        self.value = value
        self.prevs = {'nodes' : [],
                      'directions' : []}
        self.nexts = {'nodes' : [],
                      'directions' : []}

    def addPrev(self, node, direction):
        self.prevs['nodes'].append(node)
        self.prevs['directions'].append(direction)

    def addNext(self, node, direction):
        self.nexts['nodes'].append(node)
        self.nexts['directions'].append(direction)

    def isPrev(self, node):
        if len(self.prevs) == 0:
            return False
        elif node in self.prevs['nodes']:
            return True
        else:
            return False
        
    def isNext(self, node):
        if len(self.prevs) == 0:
            return False
        elif node in self.nexts['nodes']:
            return True
        else:
            return False
        
    def hasPrev(self, node):
        if len(self.prevs) == 0:
            return False
        elif node in self.prevs['nodes']:
            return True
        else:
            return any([p.hasPrev(node) for p in self.prevs['nodes']])

    def hasNext(self, node):
        if len(self.prevs) == 0:
            return False
        elif node in self.nexts['nodes']:
            return True
        else:
            return any([p.hasNext(node) for p in self.nexts['nodes']])

# Read data
INITIAL_MAZE = []
with open(filename, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    INITIAL_MAZE = [list(row.strip()) for row in lines]

NODES = list()
for y in range(len(INITIAL_MAZE)):
    NODES_ROW = list()
    for x in range(len(INITIAL_MAZE[0])):
        NODES_ROW.append(MyNode([x,y], INITIAL_MAZE[y][x]))
    NODES.append(NODES_ROW)


# Helper functions
def printNodes(nodes):
    for y in range(len(INITIAL_MAZE)):
        for x in range(len(INITIAL_MAZE[0])):
            item = nodes[y][x]
            if str(item.value) in "E#.S?":
                print (item.value*6, end='')
            else:
                print("{0:6d}".format(item.value), end='')
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

def clearMazeCell(maze, pos):
    TOKEN_EMPTY = '.'
    maze[pos[1]][pos[0]] = TOKEN_EMPTY

# Transformation functions
def getMovements(position):
    return [[[position[0]  , position[1]-1], 'n'],
            [[position[0]+1, position[1]  ], 'e'],
            [[position[0]  , position[1]+1], 's'],
            [[position[0]-1, position[1]  ], 'w']]

def getNode (NODES, POS):
    return NODES[POS[1]][POS[0]]

def connectAllNodes(MAZE, nodes, FIRST, LAST, MAX_PATH):
    def connectNodes(currentNode):
        currentPosition = currentNode.position
        movements = getMovements(currentPosition)
        emptyPos = [[pos,dir] for pos,dir in movements if isEmpty(MAZE, pos)]
 
        if tuple(currentPosition) == tuple(LAST):
            return []

        for nextPos, dir in emptyPos:
            nextNode = getNode(nodes, nextPos)
            # if not currentNode.isPrev(nextNode):
            currentNode.addNext(nextNode, dir)
            nextNode.addPrev(currentNode, dir)
        
        return currentNode.nexts['nodes']

    FIRST_NODE = getNode(nodes, FIRST)
    newNodes = [FIRST_NODE]
    while len(newNodes) > 0:
        nextNodes = []
        for node in newNodes:
            if len(node.nexts['nodes']) == 0:
                tempNodes = connectNodes(node)
                if len(tempNodes) > 0:
                    nextNodes.extend(tempNodes)
        newNodes = nextNodes

def findPaths(nodes, FIRST, LAST, MAX_DEPTH):
    def findPathsToIterative(FIRST_NODE, LAST_NODE, MAX_DEPTH):
        
        finishedPaths = []
        initialPath = [[FIRST_NODE, 'e']]
        nextPaths = [initialPath]
        currentDepth = 0

        start = time.time()
        end = time.time()
        total_start = time.time()
        while len(nextPaths) > 0 and currentDepth < MAX_DEPTH:
            currentDepth += 1
            print(f"Current depth: {currentDepth} - {end-start}")
            start = time.time()
            newPaths = []
            for path in nextPaths:
                # Coger el ultimo nodo
                lastStep = path[-1]

                currentNode = lastStep[0]
                currentDir  = lastStep[1]

                # Si hay varios nodos, duplicar par y añadir un nodo a cada path
                nextNodes      = currentNode.nexts['nodes']
                nextDirections = currentNode.nexts['directions']

                for nextNode, nextDir in zip(nextNodes, nextDirections):
                    nexPos = nextNode.position

                    if nextNode not in [node for node, dir in path]:
                        newPath = [elem for elem in path]
                        newPath.append([nextNode, nextDir])

                        if nextNode == LAST_NODE:
                            finishedPaths.append(newPath)
                        else:
                            newPaths.append(newPath)
                    else:
                        pass

            nextPaths = newPaths
            end = time.time()
        total_end = time.time()

        print(f"Current depth: {currentDepth} - {total_end-total_start}")

        return finishedPaths

    FIRST_NODE = getNode(nodes, FIRST)
    LAST_NODE  = getNode(nodes, LAST)
    paths = findPathsToIterative(FIRST_NODE, LAST_NODE, MAX_DEPTH)
    return paths

    finalPaths = []
    for path in paths:
        newPath = [[FIRST_NODE,'e']]
        newPath.extend(path)
        finalPaths.append(newPath)
    return finalPaths

def calculatePathCost(path):
    print ("New path")
    cost = 0

    currentNode = path[0][0]
    currentDir  = path[0][1]
    # print(f"Node: {currentNode.position} - Cost: {cost}")

    for node, dir in path[1:]:
        prevNode, currentNode = currentNode, node
        prevDir, currentDir   = currentDir, dir
        cost += 1 if prevDir == currentDir else 1001
        # print(f"Node: {currentNode.position} - Cost: {cost}")

    return cost
        

# ###################################
# # Part 2 - Find lowest score path #
# ###################################

if __name__ == "__main__":
    MAX_PATH = 700    # Obtained from PART 1
    MAX_COST = 135512 # Obtained from PART 1

    # Print initial state of the problem
    # print("Initial Maze:")
    nodes = NODES
    printNodes(nodes)
    
    # Init first part
    START = findStart(INITIAL_MAZE)
    END   = findEnd(INITIAL_MAZE)
    print(f"Start: {START} - End: {END}")

    # Run part 1
    MAZE = copy.deepcopy(INITIAL_MAZE)
    clearMazeCell(MAZE, START)
    clearMazeCell(MAZE, END)

    # Calculate
    print ("Connecting nodes...")
    connectAllNodes (MAZE, nodes, START, END, MAX_PATH)
    print ("Finding paths...")
    paths = findPaths (nodes, START, END, MAX_PATH)

    print(f"Calculating paths' costs for {len(paths)} paths")
    # costs = [calculatePathCost(path) for path in paths]
    MAX_THREADS = multiprocessing.cpu_count()
    costs = []
    with Pool(processes=MAX_THREADS) as pool:
        print(f"{MAX_THREADS} threads will be used.")
        costs = pool.map(calculatePathCost, paths)
    print(f"Min cost was: {min(costs)}")

    bestPaths = [path for path, cost in zip(paths,costs) if cost == min(costs)]
    bestCosts = [cost for path, cost in zip(paths,costs) if cost == min(costs)]

    allNodes = []
    for path in bestPaths:
        pathNodes = [node for node, dir in path]
        allNodes.extend(pathNodes)
    allNodes = set(allNodes)
    print(len(allNodes))
    print(f"BestPaths: {len(bestPaths)} - BestCost: {bestCosts}")

