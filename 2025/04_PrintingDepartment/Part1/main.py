# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/example.data"
filename = f"{filepath}/test.data"

ROLL_CHAR='@'
EMPTY_CHAR='.'

ACCESSIBLE_LIMIT = 4

# DATA PARSING
def readData(filename : str) -> list[list[str]]:
    with open(filename, "r") as file:
        return [list(line.strip()) for line in file.readlines()]

def printData(data : list[list[str]]) -> None:
    for line in data:
        print(line)

def calcAdjacentCount(rolls : list[list[str]], adjacents : list[list[int]], x : int, y : int):
    count = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            adjX = x+i
            adjY = y+j
            if adjX in range(len(rolls[0])) and adjY in range(len(rolls)):
                if (i!=0 or j!=0) and rolls[adjX][adjY] == ROLL_CHAR:
                    count = count + 1
    adjacents[x][y] = count
                
# PUZZLE SOLVING
if __name__=="__main__":
    rolls = readData(filename)
    adjacents = [[0] * len(rolls[0]) for _ in range(len(rolls))]

    for x in range(len(rolls[0])):
        for y in range(len(rolls)):
            calcAdjacentCount(rolls, adjacents, x, y)
    
    # printData(rolls)
    # printData(adjacents)

    accesible = 0
    for x in range(len(rolls[0])):
        for y in range(len(rolls)):
            if rolls[x][y] == ROLL_CHAR and adjacents[x][y] < ACCESSIBLE_LIMIT:
                accesible = accesible + 1
    print(f"Accesible rolls: {accesible}")
