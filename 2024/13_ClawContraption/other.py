#!/bin/python3

import copy
import click
import re
import multiprocessing
from multiprocessing import Pool

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/00_example1.data"
filename = f"{filepath}/00_test.data"

# Read data
initialData = []
with open(filename, "r") as file:
    machine = {}
    buttons = []
    prize   = {}

    # Find machines
    for line in file.readlines():
        line = line.strip()
        if "Button" in line:
            name = re.findall(r"Button (.*):", line)[0]
            moves = re.findall(r"(.\+\d+)", line)
            newButton = {}
            newButton['moves'] = [int(value) for axis, value in [m.split('+') for m in moves]] 
            if name == 'A':
                newButton['tokens'] = 3
            if name == 'B':
                newButton['tokens'] = 1
            buttons.append(newButton)

        elif "Prize" in line:
            loc = re.findall(r"(.=\d+)", line)
            OFFSET = 10000000000000
            OFFSET = 0
            prize = [int(value)+OFFSET for axis, value in [l.split('=') for l in loc]] 
            
            machine["buttons"] = buttons
            machine["prize"]   = prize
            initialData.append(machine)
    
            # Next machine
            machine = {}        
            buttons = []
        
        else: # Ignore empty lines
            continue

def printMachines(machines):
    for machine in machines:
        print(f"{machine['buttons']} | {machine['prize']}")

# printMachines(initialData)

#######################################
# Part 1 - #
#######################################

# def findTokens(button, prize):
#     tokens = 0
#     while all(prize, lambda x: x > 0):
#         # Push button
#         prize - button['moves']
#         tokens += button['tokens']
#     if all(prize, lambda x: x == 0):
#         return True, tokens
#     else:
#         return False, 0

def achievedPrize(pos, prize):
    return all([x == y for x, y in zip(pos, prize)])

def overflowPrize(pos, prize):
    return any([x > y for x, y in zip(pos, prize)])

def determineMinimumTokens(buttonA, buttonB, prize):
    combinations = []
    posA = [0, 0]
    countA = 0

    # Calculate every possible combination
    while not overflowPrize(posA, prize) and not achievedPrize(posA, prize):
        leftForB = [x - y for x, y in zip(prize, posA)]
        dividedB = [x / y for x, y in zip(leftForB, buttonB['moves'])]
        modedB   = [x % 1 for x in dividedB]
        if all([x == 0 for x in modedB]) and dividedB[0] == dividedB[1]:
            testedPair = [countA, dividedB[0]]
            combinations.append(testedPair) 

        posA = [x + y for x, y in zip(posA, buttonA['moves'])]
        countA += 1

    # Add final combination
    if achievedPrize(posA, prize):
        combinations.append([countA, 0])

    # Calculate tokens for each combination
    # print(machine)
    # print(combinations)
    combinationsTokens = [buttonA['tokens'] * countA + buttonB['tokens'] * countB for countA, countB in combinations]
    
    # Get minimum combination

    return min(combinationsTokens) if len(combinationsTokens) > 0 else 0


def calculateMachine(machine):
    print(f"Machine {machines.index(machine)}")
    buttons = machine['buttons']
    prize   = machine['prize']
    machineTokens = determineMinimumTokens(buttons[0], buttons[1], prize) 
    return machineTokens


MAX_THREADS = multiprocessing.cpu_count()
print(f"Multicore processing, {MAX_THREADS} threads will be used.")
machineTokens = []
machines = copy.deepcopy(initialData)
with Pool(processes=MAX_THREADS) as pool:
    machineTokens = pool.map(calculateMachine, machines)
totalTokens = sum(machineTokens)

# Output results
print(f"Total tokens: {totalTokens}")