import hashlib
import re

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/00_example.data"
filename = f"{filepath}/00_test.data"
filename = f"{filepath}/00_test2.data"

# Output title
print ("Day 7: Some Assembly Required")

# Read data
data = []
with open(filename, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    for line in lines:
        ASSIGN_OPERATOR = " -> "
        instruction, var = line.split(ASSIGN_OPERATOR)
        data.append([instruction, var])

# Helper functions
def NOT(x):
    return (~x) & 0xFFFF

def OR(x, y):
    return (x | y) & 0xFFFF

def AND(x, y):
    return (x & y) & 0xFFFF

def LSHIFT(x, n):
    return (x << n) & 0xFFFF

def RSHIFT(x, n):
    return (x >> n) & 0xFFFF

operations = {
    "NOT"   : NOT,
    "OR"    : OR,
    "AND"   : AND,
    "LSHIFT": LSHIFT,
    "RSHIFT": RSHIFT
}

###################################
# Part 1&2 - Logic gate emulation #
###################################
vars = {}

# Calculate
while data:
    tempData = data.copy()
    for instruction in tempData:
        var = instruction[1]

        elems = instruction[0].split(" ")
        if len(elems) == 1:
            x = elems[0]
            if x in vars or x.isnumeric():
                vars[var] = int(x) if x.isnumeric() else vars[x]
                data.remove(instruction)
        elif len(elems) == 2:
            op = elems[0]
            x = elems[1]
            if x in vars or x.isnumeric():
                x = int(x) if x.isnumeric() else vars[x]
                vars[var] = operations[op](x)
                data.remove(instruction)
        elif len(elems) == 3:
            op = elems[1]
            x = elems[0]
            y = elems[2]
            if (x in vars or x.isnumeric()) and (y in vars or y.isnumeric()):
                x = int(x) if x.isnumeric() else vars[x]
                y = int(y) if y.isnumeric() else vars[y]
                vars[var] = operations[op](x, y)
                data.remove(instruction)
    
# Output result
print(vars["a"])
