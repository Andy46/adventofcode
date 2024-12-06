import copy
import click

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/00_example.data"
filename = f"{filepath}/00_test.data"

# Read data
initialData = []
with open(filename, "r") as file:
    for line in file.readlines():
        line = line.strip()
        initialData.append(list(line))

# Helper functions
PATH_TOKEN = 'X'
GUARD_TOKEN = '^' 
def findGuard(data):
    for x in range(0, len(data)):
        for y in range(0, len(data[0])):
            if data[x][y] == GUARD_TOKEN:
                return x,y

def getGuardToken(dirToken):
    if dirToken == 'n':
        return '^'
    elif dirToken == 'e':
        return '>'
    elif dirToken == 's':
        return 'v'
    elif dirToken == 'w':
        return '<'

OBSTACLE_TOKEN = '#'
def isObstacle(data, x, y):
    return data[x][y] == OBSTACLE_TOKEN
    
def rotate(dirToken):
    if dirToken == 'n':
        return 'e'
    elif dirToken == 'e':
        return 's'
    elif dirToken == 's':
        return 'w'
    elif dirToken == 'w':
        return 'n'

def getNextCell(x, y, dirToken):
    if dirToken == 'n':
        return x-1, y
    elif dirToken == 'e':
        return x, y+1
    elif dirToken == 's':
        return x+1, y
    elif dirToken == 'w':
        return x, y-1

def isCellInData(data, x, y):
    return x in range(len(data)) and y in range(len(data[0]))

def printMap(data):
    for line in data:
        print(line)

def move(data, guard):
    x = guard[0][0]
    y = guard[0][1]
    dir = guard [1]
    # Calculate move
    nextCell = getNextCell(x,y,dir)
    while isCellInData(data, nextCell[0], nextCell[1]) and isObstacle(data, nextCell[0], nextCell[1]):
        dir = rotate(dir)
        nextCell = getNextCell(x,y,dir)
    # Move guard
    guard = nextCell, dir
    # Rotate again if needed
    xt = guard[0][0]
    yt = guard[0][1]
    dir = guard [1]
    nextCell = getNextCell(xt, yt, dir)
    while isCellInData(data, nextCell[0], nextCell[1]) and isObstacle(data, nextCell[0], nextCell[1]):
        dir = rotate(dir)
        nextCell = getNextCell(xt,yt,dir)
    guard = guard[0], dir
    # Edit MAP
    data[x][y] = PATH_TOKEN
    if isCellInData(data, guard[0][0], guard[0][1]):
        data[guard[0][0]][guard[0][1]] = getGuardToken(dir)
    # Return changes
    return data, guard
    
#######################
# Part 1 - Guard path #
#######################
PRINT_MAP = False
data = copy.deepcopy(initialData)

# Calculate route
guard = findGuard(data), 'n'
print(f"Initial position: {guard}")
MainHistory=[guard] # Help for part 2
while isCellInData(data, guard[0][0], guard[0][1]):
    if PRINT_MAP:
        print("Current Map:")
        printMap(data)
    data, guard = move(data, guard)
    MainHistory.append(guard) # Help for part 2

if PRINT_MAP:
    print("Final Map:")
    printMap(data)

# Calculate positions
newData = []
for row in data:
    newRow = [cell==PATH_TOKEN for cell in row]
    newData.append(newRow)

# Calculate count and output result
posCount = sum([sum(row) for row in newData])
print(f"Guard travelled thourgh {posCount} positions")

# ###########################
# # Part 2 - Find loop path #
# ###########################

print("######################### WARNING #########################")
print("##### This is not optimized and takes a lot of time.  #####")
print("######################### WARNING #########################")

PRINT_MAP = False
data = copy.deepcopy(initialData)

# Helper functions for part 2
def addObstacle(data, pos):
    data[pos[0]][pos[1]] = OBSTACLE_TOKEN
    return data

def hasLoop(data, guard):
    history = [guard]
    while isCellInData(data, guard[0][0], guard[0][1]):
        if PRINT_MAP:
            print("Current Map:")
            printMap(data)
        data, guard = move(data, guard)
        if guard in history:
            return True
        else:        
            history.append(guard)
    return False
        
# Calculate
history = []
loopPositions = []
duplicatedPositions = []
initialGuard = findGuard(data), 'n'

maxPositions = len(MainHistory)
with click.progressbar(MainHistory) as bar: # Progress bar
    for guardPos in bar:
        # Generate new map with obstacle
        nextCell = getNextCell(guardPos[0][0], guardPos[0][1], guardPos[1])
        if nextCell in loopPositions:
            duplicatedPositions.append(nextCell)
            continue
        if isCellInData(data, nextCell[0], nextCell[1]) and nextCell not in loopPositions:
            newData = addObstacle(copy.deepcopy(initialData), nextCell)
            if PRINT_MAP:
                printMap(data)
                printMap(newData)
            # Test new map
            if hasLoop(newData, initialGuard):
                loopPositions.append(nextCell)

loopPositions = set(loopPositions)
print(f"Obstacle positions for loop: {len(loopPositions)}")