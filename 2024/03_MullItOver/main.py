import re

filename="test.data"
muls=[]
with open(filename, "r") as file:
    data=file.read()
    muls=re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data)

# Part 1
total=0
for mul in muls:
    print (mul)
    a = int(mul[0])
    b = int(mul[1])
    total = total + (a*b)

print("Total: " + str(total))
    

