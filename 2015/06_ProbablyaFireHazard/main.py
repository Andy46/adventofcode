import hashlib
import re

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/00_example.data"
filename = f"{filepath}/00_test.data"

# Output title
print ("Day 6: Probably a Fire Hazard")

# Read data
data = []
with open(filename, "r") as file:
    lines = file.read()    
    data = re.findall(r"(.*) (\d+),(\d+) .* (\d+),(\d+).*\n", lines)

# Helper functions
def followInstructions(data):
    for instruction in data:
        cmd = instruction[0]
        ix = int(instruction[1])
        iy = int(instruction[2])
        fx = int(instruction[3])
        fy = int(instruction[4])
        if cmd == 'toggle':
            toggle(ix, iy, fx, fy)
        elif cmd == 'turn on':
            turnOn(ix, iy, fx, fy)
        elif cmd == 'turn off':
            turnOff(ix, iy, fx, fy)

############################
# Part 1 - Counting lights #
############################


# Helper functions for part 1
rows = 1000
cols = 1000
lights = [[False]*cols for _ in range(rows)]

def turnOn(ix, iy, fx, fy):
    for x in range(ix, fx+1):
        for y in range(iy, fy+1):
            lights[x][y] = True

def turnOff(ix, iy, fx, fy):
    for x in range(ix, fx+1):
        for y in range(iy, fy+1):
            lights[x][y] = False

def toggle(ix, iy, fx, fy):
    for x in range(ix, fx+1):
        for y in range(iy, fy+1):
            lights[x][y] = not lights[x][y]

# Calculate
followInstructions(data)
count = sum([sum(row) for row in lights])

# Output result
print (f"Count of ON lights: {count}")
    

# ####################################
# # Part 2 - Counting gradual lights #
# ####################################

# Helper functions for part 2
rows = 1000
cols = 1000
lights = [[0]*cols for _ in range(rows)]

def turnOn(ix, iy, fx, fy):
    for x in range(ix, fx+1):
        for y in range(iy, fy+1):
            lights[x][y] = lights[x][y] + 1

def turnOff(ix, iy, fx, fy):
    for x in range(ix, fx+1):
        for y in range(iy, fy+1):
            lights[x][y] = max(lights[x][y] - 1, 0)

def toggle(ix, iy, fx, fy):
    for x in range(ix, fx+1):
        for y in range(iy, fy+1):
            lights[x][y] = lights[x][y] + 2

# Calculate
followInstructions(data)
count = sum([sum(row) for row in lights])

# Output result
print (f"Count of ON gradual lights: {count}")
    
