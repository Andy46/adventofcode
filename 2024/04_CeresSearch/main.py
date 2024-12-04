
# Files
filename = "00_example.data"
filename = "00_test.data"

# Read data
data = []
with open(filename, "r") as file:
    for line in file.readlines():
        line = line.strip()
        data.append(list(line))

# Helper functions
def findWordDir(data, word, x, y, dx, dy):
    x = int(x)
    y = int(y)
    dx = int(dx)
    dy = int(dy)

    for letter in word:
        if x < 0 or x >= len(data):
            return False
        if y < 0 or y >= len(data[0]):
            return False
        if not data[x][y] == letter:
            return False
        x = x + dx
        y = y + dy
    return True

######################
# Part 1 - Find XMAS #
######################

# Helper functions for part 1
def findWord(data, word, x, y):
    count = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if findWordDir(data, word, x, y, dx, dy):
                count = count + 1
    return count

# Calculate
word="XMAS"
totalCount = 0
for x in range(0, len(data)):
    for y in range(0, len(data[0])):
        totalCount = totalCount + findWord(data, word, x, y)

# Output result
print("Total count for '" + word + "': " + str(totalCount))

########################
# Part 2 - Find (X)MAS #
########################

# Helper functions for part 2
def findWordX(data, word, x, y):
    count = 0
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            if findWordDir(data, word, x-dx, y-dy, dx, dy):
                count = count + 1
    return count == 2

# Calculate
word="MAS"
totalCount = 0
for x in range(1, len(data)-1):
    for y in range(1, len(data[0])-1):
        totalCount = totalCount + findWordX(data, word, x, y)
        
# Output result
print("Total count for (X)'" + word + "': " + str(totalCount))
