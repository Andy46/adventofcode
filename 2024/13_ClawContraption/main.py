import copy
import click
import re

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/00_test.data"
filename = f"{filepath}/00_example1.data"

# Read data
initialData = []
with open(filename, "r") as file:
    machine = {}
    buttons = {}
    prize   = {}

    # Find machines
    for line in file.readlines():
        line = line.strip()
        if "Button" in line:
            name = re.findall(r"Button (.*):", line)
            moves = re.findall(r"(.\+\d+)", line)
            print(f"{name}: {moves}")
            for move in moves:
                axis, value = move.split('+')
                value = int(value)
                buttons[axis] = value
                
            print(buttons)
        elif "Prize" in line:
            loc = re.findall(r"(.=\d+)", line)
            for coord in loc:
                axis, value = coord.split('=')
                value = int(value)
                prize[axis] = value

        else:
            machine["buttons"] = buttons
            machine["prize"]   = prize
            initialData.append(machine)
            machine = {}
            buttons = {}
            prize   = {}
            continue

# List machines
for machine in initialData:
    print (machine)

#######################################
# Part 1 - #
#######################################
