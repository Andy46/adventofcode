# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/example.data"
filename = f"{filepath}/test.data"

INITIAL_POS = 50

password = 0
currentPos = INITIAL_POS
print(f"Initial position: {currentPos}")
with open(filename, "r") as file:
    for line in [line.strip() for line in file.readlines()]:
        op = line[0]
        delta = int(line[1:])

        for i in range(0, delta):
            currentPos = (currentPos + 1) if op == 'R' else (currentPos - 1)
            if currentPos < 0:
                currentPos = currentPos + 100
            elif currentPos >= 100:
                currentPos = currentPos - 100
            #print(f"Current position: {currentPos}")
            if currentPos == 0:
                password = password + 1
                #print(f"Password: {password}")

print(f"The password is: {password}")

    