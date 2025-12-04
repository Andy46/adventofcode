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
        currentPos = (currentPos + delta) if op == 'R' else (currentPos - delta)
        print(f"Current position: {currentPos}")
        if currentPos % 100 == 0:
            password = (password + 1)

print(f"The password is: {password}")

    