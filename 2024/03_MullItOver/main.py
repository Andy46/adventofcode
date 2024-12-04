import re

# Files
filename = "00_example.data"
filename = "00_test.data"

#####################################
# Part 1 - Find all multiplications #
#####################################

# Read data
muls=[]
with open(filename, "r") as file:
    data=file.read()
    muls=re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data)

# Calculate
total=0
for mul in muls:
    a = int(mul[0])
    b = int(mul[1])
    total = total + (a*b)

# Output result
print("Total 1: " + str(total))
    
#########################################
# Part 2 - Find enabled multiplications #
#########################################

# Read data
muls=[]
with open(filename, "r") as file:
    data=file.read()
    muls=re.findall(r"(do\(\))|(mul\(\d{1,3},\d{1,3}\))|(don\'t\(\))", data)

# Calculate
total=0
enable=True
for mul in muls:
    if r'do()' in mul:
        enable = True
    elif r"don't()" in mul:
        enable = False
    elif enable == True:
        elems = re.findall(r"(\d{1,3}),(\d{1,3})", mul[1])[0]
        a = int(elems[0])
        b = int(elems[1])
        total = total + (a*b)

# Output result
print("Total 2: " + str(total))
