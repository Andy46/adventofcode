
# Files
filename = "00_example.data"
filename = "00_test.data"

# Output title
print ("Day 2: I Was Told There Would Be No Math")

# Read data
data = []
with open(filename, "r") as file:
    lines = file.readlines()
    data = [line.strip().split("x") for line in lines]
    
###########################
# Part 1 - Wrapping paper #
###########################

# Helper functions for part 1
def calculatePaper(present):
    sides = list(map(int, present))
    length = int(sides[0])
    width  = int(sides[1])
    height = int(sides[2])
    sideAreas = [length*width, width*height, height*length]
    totalArea = min(sideAreas) + 2*sum(sideAreas)
    return totalArea

# Calculate
presentAreas = [calculatePaper(present) for present in data]
totalArea = sum(presentAreas)

# Output result
print(f"Total paper for presents: {totalArea}")

# ####################
# # Part 2 - Ribbons #
# ####################

# Helper functions for part 2
def calculateBow(present):
    sides = list(map(int, present))
    length = int(sides[0])
    width  = int(sides[1])
    height = int(sides[2])
    return length * width * height

def calculateRibbon(present):
    sides = list(map(int, present))
    sides.remove(max(sides))
    return 2*(sides[0]+sides[1]) + calculateBow(present)

# Calculate
ribbons = [calculateRibbon(present) for present in data]
totalLength = sum(ribbons)

# Output result
print(f"Total ribbons for presents: {totalLength}")
