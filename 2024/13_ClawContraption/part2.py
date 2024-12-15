#!/bin/python3

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/00_example1.data"
filename = f"{filepath}/00_test.data"

# Read data
import re
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
            OFFSET = 0
            OFFSET = 10000000000000
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

#######################################
# Part 2 - Find the prize (optimized) #
#######################################

def det(matrix):
    return (matrix[0][0] * matrix[1][1]) - (matrix[1][0] * matrix[0][1])

def determineMinimumTokens(buttonA, buttonB, prize):

    D = det([buttonA,buttonB])
    Dx = det([prize,buttonB])
    Dy = det([buttonA,prize])

    A = Dx/D
    B = Dy/D 

    calculatedA = [A*axisA for axisA in buttonA]
    calculatedB = [B*axisB for axisB in buttonB]
    calculated = [a+b for a,b in zip(calculatedA, calculatedB)]

    if A%1==0 and B%1==0 and all([a==b for a,b in zip(calculated, prize)]):
        return [A,B]
    else:
        return [0,0]

def calculateMachine(machine):
    buttons = machine['buttons']
    prize   = machine['prize']
    machineTokens = determineMinimumTokens(buttons[0]["moves"], buttons[1]["moves"], prize) 
    machineTokens = machineTokens[0]*buttons[0]['tokens'] + machineTokens[1]*buttons[1]['tokens']
    return int(machineTokens)

machines = initialData

machineTokens = [calculateMachine(machine) for machine in machines]
totalTokens = sum(machineTokens)

# Output results
print(f"Total tokens: {totalTokens}")