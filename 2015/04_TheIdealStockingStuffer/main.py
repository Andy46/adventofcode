import hashlib

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/00_example.data"
filename = f"{filepath}/00_test.data"

# Output title
print ("Day 4: The Ideal Stocking Stuffer")

# Read data
data = []
with open(filename, "r") as file:
    lines = file.readlines()
    data = [line.strip() for line in lines]

# Helper functions

#########################
# Part 1 - Find MD5 (5) #
#########################

# Calculate
for elem in data:
    for i in range (0, 100000000000000):
        input = str(elem) + str(i)
        md5 = hashlib.md5(input.encode())
        digest = md5.hexdigest()
        if digest[:5] == "00000":
            # Output result
            print(f"Num {i} produces digest: {digest}")
            break

#########################
# Part 2 - Find MD5 (6) #
#########################

# Calculate
for elem in data:
    for i in range (0, 100000000000000):
        input = str(elem) + str(i)
        md5 = hashlib.md5(input.encode())
        digest = md5.hexdigest()
        if digest[:6] == "000000":
            # Output result
            print(f"Num {i} produces digest: {digest}")
            break