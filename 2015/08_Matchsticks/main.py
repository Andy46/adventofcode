import re

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/00_example.data"
filename = f"{filepath}/00_test.data"

# Output title
print ("Day 8: Matchsticks")

# Read data
data = []

with open(filename, mode="r") as file:
    data = [line.strip() for line in file.readlines()]

# Helper functions
def countChars(string):
    return len(string)

##################################
# Part 1 - Decoding and counting #
##################################

# Helper functions
def countMemVals(string):
    chars= []

    # Remove initial and final quotes
    string = string[1:-1]

    # Count and remove escaped characters
    ESCAPED_CHARS = [r"\\x[0-9A-Fa-f]{2}", r"\\\"", r"\\\\"]
    items = ESCAPED_CHARS
    for item in items:
        chars.extend(re.findall(item, string))
        string = re.sub(item, "", string)
    chars.extend(string)

    return len(chars)

# Calculate
sum = 0
for line in data:
    sum = sum + (countChars(line) - countMemVals(line))

# Output result
print(f"Decoding difference of part 1: {sum}")

##################################
# Part 2 - Encoding and counting #
##################################

# Helper functions
def countExtraEncoded(string):
    chars= []

    # Remove initial and final quotes
    string = string[1:-1]

    # Count and remove escaped characters
    ESCAPED_CHARS = [r"\\x[0-9A-Fa-f]{2}", r"\\\"", r"\\\\"]
    items = ESCAPED_CHARS
    for item in items:
        chars.extend(re.findall(item, string))
        string = re.sub(item, "", string)
    chars.extend(string)
    # return len(chars)
    
    count = 0
    for item in chars:
        if "\\x" in item:
            count = count + 5 # "\\xXX"
        elif "\\\"" in item:
            count = count + 4 # "\\\\\\\""
        elif "\\\\" in item:
            count = count + 4 # "\\\\\\\\"
        else:   
            count = count + 1
    count = count + 6 # "\"...\""
    return count

# Calculate
sum = 0
for line in data:
    sum = sum + (countExtraEncoded(line) - countChars(line))

# Output result
print(f"Encoding difference of part 2: {sum}")


