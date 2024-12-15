#!/bin/python3

import copy
import click
import re

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
            prize = [int(value) for axis, value in [l.split('=') for l in loc]] 
            
            machine["buttons"] = buttons
            machine["prize"]   = prize
            initialData.append(machine)
    
            # Next machine
            machine = {}        
            buttons = []
        
        else: # Ignore empty lines
            continue

def printMachine(machine):
    print(f"{machine['buttons']} | {machine['prize']}")

def printMachines(machines):
    for machine in machines:
        print(f"{machine['buttons']} | {machine['prize']}")

###########################
# Part 1 - Find the prize #
###########################

def findTokens(button, prize):
    tokens = 0
    while all(prize, lambda x: x > 0):
        # Push button
        prize - button['moves']
        tokens += button['tokens']
    if all(prize, lambda x: x == 0):
        return True, tokens
    else:
        return False, 0

def achievedPrize(prize):
    return all([x == 0 for x in prize])

def overflowPrize(prize):
    return any([x < 0 for x in prize])

def findTokenChain(buttons, prize):
    # Push button
    currentButton = buttons[0]
    nextPrize = [x - y for x, y in zip(prize, currentButton['moves'])] 

    chains = []

    if achievedPrize(nextPrize):
        return True, [[currentButton]]
    elif overflowPrize(nextPrize):
        return False, []
    else:
        # Keep using button until fail/achieve
        achieved, subchains = findTokenChain(buttons, nextPrize)
        if achieved:
            for subchain in subchains:
                subchain.append(currentButton)
                chains.append(subchain)
        
        if len(buttons) > 1:
            achieved, subchains = findTokenChain(buttons[1:], nextPrize)
            if achieved:
                for subchain in subchains:
                    subchain.append(currentButton)
                    chains.append(subchain)

        # Use next button until fail/achive
        return (len(chains) > 0), chains


def calculateChainTokens(chain):
    totalTokens = sum([button['tokens'] for button in chain])
    return totalTokens

# Calculate
machines = copy.deepcopy(initialData)
totalTokens = 0
with click.progressbar(machines) as bar: # Progress bar
    for machine in bar:
        buttons = machine['buttons']
        prize   = machine['prize']
        for i in range(len(buttons)):
            possible, chains = findTokenChain(buttons[i:], prize)
            
            if possible:
                for chain in chains:
                    countA = len([button for button in chain if button == buttons[0]])
                    countB = len([button for button in chain if button == buttons[1]])

                chainTokens = [calculateChainTokens(chain) for chain in chains]
                minChainTokens = min(chainTokens)
                totalTokens += minChainTokens

# Output results
print(f"Total tokens: {totalTokens}")