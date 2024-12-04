
# Files
filename = "00_example.data"
filename = "00_test.data"

# Output title
print ("Day 1: Not Quite Lisp")

# Read data
data = []
with open(filename, "r") as file:
    data = file.read()

#################################
# Part 1 - Find the final floor #
#################################

# Calculate
finalFloor = data.count('(') - data.count(')')

# Output result
print("Final floor: " + str(finalFloor))

##########################
# Part 2 - Find floor -1 #
##########################

# Calculate
currentFloor = 0
position = 0
for char in data:
    position = position + 1
    if char == '(':
        currentFloor = currentFloor + 1
    elif char == ')':
        currentFloor = currentFloor - 1
    if currentFloor == -1:
        break

# Output result
print("Floor -1 found in position: " + str(position))
