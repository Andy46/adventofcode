# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/example.data"
filename = f"{filepath}/test.data"

RED_CHAR='#'
EMPTY_CHAR='.'

# DATA PARSING
def readData(filename : str) -> list[list[int]]:
    with open(filename, "r") as file:
        text = [line.strip() for line in file.readlines()]
        return [[int(val1), int(val2)] for val1, val2 in [line.split(',') for line in text]]
    
def printData(data : any) -> None:
    for item in data:
        print(item)

# AUX FUNCTIONS
def calcArea(posA : tuple[int, int], posB : tuple[int, int]) -> int:
    width  = abs(posA[0] - posB[0]) + 1
    height = abs(posA[1] - posB[1]) + 1
    return height*width

# PUZZLE SOLVING
if __name__=="__main__":
    tiles = readData(filename)
    # printData(tiles)
    areas = []
    for tileA in tiles:
        for tileB in tiles:
            areas.append(calcArea(tileA, tileB))
    print(f"Max area: {max(areas)}")
