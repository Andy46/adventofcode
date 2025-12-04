# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/example.data"
filename = f"{filepath}/test.data"

INITIAL_POS = 100050

password = 0
currentPos = INITIAL_POS
print(f"Initial position: {currentPos}")
with open(filename, "r") as file:
    for line in [line.strip() for line in file.readlines()]:
        op = line[0]
        delta = int(line[1:])

        completeLoops = int(abs(delta)/100)
        password = password + completeLoops

        delta = delta % 100
        newPos = 0
        if op == 'R':
            newPos = (currentPos + delta) 
        else:
            newPos = (currentPos - delta)
            if abs(newPos) % 100 == 0:
                password = (password + 1)

        newPosInt = int(newPos/100)
        currentPosInt = int(currentPos/100)
        if  currentPos % 100 != 0 and newPosInt != currentPosInt:
            password = password + 1

        currentPos = newPos


print(f"The password is: {password}")

    