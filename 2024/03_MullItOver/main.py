import re

filename="example.data"
filename="test.data"

muls=[]
with open(filename, "r") as file:
    data=file.read()
    muls=re.findall(r"(do\(\))|(mul\(\d{1,3},\d{1,3}\))|(don\'t\(\))", data)

# Part 2
total=0
enable=True
for mul in muls:
    print (mul)
    if 'do()' in mul:
        enable = True
    elif r"don't()" in mul:
        enable = False
    elif enable == True:
        elems = re.findall(r"(\d{1,3}),(\d{1,3})", mul[1])[0]
        print (elems)
        a = int(elems[0])
        b = int(elems[1])
        print(a)
        print(b)
        total = total + (a*b)

print("Total 2: " + str(total))
