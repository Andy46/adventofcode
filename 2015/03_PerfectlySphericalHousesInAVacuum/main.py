
# Files
filename = "00_example.data"
filename = "00_test.data"

# Output title
print ("Day 3: Perfectly Spherical Houses in a Vacuum")

# Read data
data = []
with open(filename, "r") as file:
    lines = file.readlines()
    data = [line.strip() for line in lines]

# Helper functions
TOKEN_NORTH = '^'
TOKEN_EAST  = '<'
TOKEN_SOUTH = 'v'
TOKEN_WEST  = '>'

def move(x, y, token):
    if token == TOKEN_NORTH:
        return x+1, y
    if token == TOKEN_EAST:
        return x, y+1
    if token == TOKEN_SOUTH:
        return x-1, y
    if token == TOKEN_WEST:
        return x, y-1

########################
# Part 1 - House count #
########################

# Helper functions for part 1
def calculatePath(route):
    path = [[0,0]]
    for instruction in route:
        x, y = path[-1]
        x, y = move (x, y, instruction)
        path.append([x, y])
    return path

def countHouses(path):
    return set(tuple(elem) for elem in path)

for instructions in data:
    path = calculatePath(instructions)
    houses = countHouses(path)
    print(f"Number of houses: {len(houses)}")


###################################
# Part 2 - House count with robot #
###################################

# Helper functions for part 2
def calculatePathSantaRobot(route):
    pathSanta = [[0,0]]
    pathRobot = [[0,0]]
    count = 0
    for instruction in route:
        if count % 2 == 0:
            x, y = pathSanta[-1]
            x, y = move (x, y, instruction)
            pathSanta.append([x, y])
        else:
            x, y = pathRobot[-1]
            x, y = move (x, y, instruction)
            pathRobot.append([x, y])
        count = count + 1
    return pathSanta, pathRobot

def countHousesSantaRobot(pathSanta, pathRobot):
    pathCombined = pathSanta.copy()
    pathCombined.extend(pathRobot)
    return set(tuple(elem) for elem in pathCombined)

# Calculate
for instructions in data:
    pathSanta, pathRobot = calculatePathSantaRobot(instructions)
    houses = countHousesSantaRobot(pathSanta, pathRobot)
    print(f"Number of houses (with Robot): {len(houses)}")
