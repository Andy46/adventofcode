
# Files
filename = "00_example.data"
filename = "00_test.data"

# Read data
col1 = []
col2 = []

with open(filename, "r") as file:
    for line in file.readlines():
        line = line.strip()
        nums = line.split(" ")
        num1 = nums[0]
        num2 = nums[-1]
        col1.append(int(num1))
        col2.append(int(num2))

#####################################
# Part 1 - Calculate total distance #
#####################################
col1.sort()
col2.sort()

totalDistance = 0
for i in range(0, len(col1)):
    totalDistance = totalDistance + abs((col1[i] - col2[i]))
print("Total Distance: " + str(totalDistance))

#######################################
# Part 2 - Calculate similarity score #
#######################################
def getSetFromList(data):
    setData = {}
    for elem in data:
        if elem in setData:
            setData[elem] = setData[elem] + 1
        else:
            setData[elem] = 1
    return setData

set1 = getSetFromList(col1)
set2 = getSetFromList(col2)

similarityScore = 0
for elem in set1:
    if elem in set2:
        similarityScore = similarityScore + (elem * set1[elem] * set2[elem])
print("Similarity Score: " + str(similarityScore))
