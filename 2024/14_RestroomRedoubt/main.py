#!/bin/python3

import copy
import multiprocessing
from multiprocessing import Pool

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])

filename = f"{filepath}/00_example2.data"
filename = f"{filepath}/00_example1.data"
MAP_WIDTH, MAP_HEIGHT = 11, 7

filename = f"{filepath}/00_test.data"
MAP_WIDTH,MAP_HEIGHT = 101, 103

# Read data
initialData = []
import re
with open(filename, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    for line in lines:
        numbers = [int(number) for number in re.findall(r"(-?\d+)", line)]
        position = numbers[:2]
        velocity = numbers[2:]
        initialData.append({"pos" : position, "vel" : velocity})

INITIAL_ROBOTS = copy.deepcopy(initialData)

# # Print robots
# print (f"Robots:")
# for robot in robots:
#     print (robot)

# Helper functions
def printMap(robots):
    def isEqualPos(posA, posB):
        return tuple(posA) == tuple(posB)
    def countRobots(x,y):
        xyRobots = [robot for robot in robots if isEqualPos(robot["pos"], [x, y])]
        return len(xyRobots)
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            count = countRobots(x,y)
            print(f"{count if count != 0 else '.'}", end='')
        print("")

def moveRobot(robot, N):
    posX, posY = robot["pos"]
    velX, velY = robot["vel"]

    newX = ((posX + MAP_WIDTH) + (velX * N)) % (MAP_WIDTH)
    newY = ((posY + MAP_HEIGHT) + (velY * N)) % (MAP_HEIGHT)

    return {"pos": [newX, newY], "vel": [velX, velY]}

#####################################
# Part 1 - Find the security factor #
#####################################

# Helper functions for part 1
def getRobotsInSection(robots, section):
    iniX, iniY = section["ini"]
    finX, finY = section["fin"]
    def isPosInSection(pos):
        x = pos[0]
        y = pos[1]
        return ((x >= iniX) and (x <= finX)) and ((y >= iniY) and (y <= finY))
    secRobots = [robot for robot in robots if isPosInSection(robot["pos"])]
    return secRobots

SECONDS = 100
finalRobots = [moveRobot(robot, SECONDS) for robot in INITIAL_ROBOTS]
# # Print final map
# print(f"After {SECONDS} seconds:")
# printMap(finalRobots)

# Calculate robots in sections
sectionLetters = ['A', 'B', 'C', 'D']
sectionA = {"ini": [0                   , 0],
            "fin": [int(MAP_WIDTH/2) - 1, int(MAP_HEIGHT/2) - 1]}
sectionB = {"ini": [int(MAP_WIDTH/2) + 1, 0],
            "fin": [MAP_WIDTH, int(MAP_HEIGHT/2) - 1]}
sectionC = {"ini": [0, int(MAP_HEIGHT/2 + 1)],
            "fin": [int(MAP_WIDTH/2) - 1, MAP_HEIGHT]}
sectionD = {"ini": [int(MAP_WIDTH/2) + 1, int(MAP_HEIGHT/2) + 1],
            "fin": [MAP_WIDTH      , MAP_HEIGHT      ]}
sections = [sectionA, sectionB, sectionC, sectionD]

sectionRobots = [getRobotsInSection(finalRobots, section) for section in sections]

# # Print robots in section
# for robots, letter in zip(sectionRobots, sectionLetters):
#    print (f"Section {letter}")
#    printMap(robots)

# Calculate final output
from functools import reduce
from operator import mul
safetyFactor = reduce(mul, [len(robots) for robots in sectionRobots])

# Output result
print(f"Safety factor:{safetyFactor}")

#################################################
# Part 2 - Find the easter egg (Christmas Tree) #
###################################££############

# Helper functions for part 2
def hasNeighbours(robots, robot):
    robotPos = copy.deepcopy(robot["pos"])
    posA = tuple([robotPos[0]+1,robotPos[1]])
    posB = tuple([robotPos[0],robotPos[1]+1])
    posC = tuple([robotPos[0]-1,robotPos[1]])
    posD = tuple([robotPos[0],robotPos[1]-1])
    positions = [posA,posB, posC, posD]
    count = [other for other in robots if (tuple(other["pos"]) in positions)]
    return len(count) >= 2

def findTree(step):
    procRobots = [moveRobot(robot, step) for robot in INITIAL_ROBOTS]

    # Dumm rule to find group of robots
    count = [robot for robot in procRobots if hasNeighbours(procRobots, robot)]
    if len(count) >= 100:
        printMap(procRobots)
        return True
    
    return False

# Calculate
MAX_THREADS = multiprocessing.cpu_count()
with Pool(processes=MAX_THREADS) as pool:
    START_SECOND  = 0
    FINISH_SECOND = 10000
    result = pool.map(findTree, range(START_SECOND, FINISH_SECOND))
    seconds = result.index(True)
    print(f"Tree is formed in second: {seconds}")
