# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/example.data"
filename = f"{filepath}/test.data"

START_CHAR='S'
EMPTY_CHAR='.'
SPLIT_CHAR='^'
TACHYON_CHAR='|'

# DATA PARSING
def readData(filename : str) -> tuple[list[list[int]], list[str]]:
    with open(filename, "r") as file:
        text = [list(line.strip()) for line in file.readlines()]
        return text
def printData(data : any) -> None:
    print()
    for item in data:
        print(''.join([str(i) for i in item]))

# AUX FUNCTIONS
def iterateRow(picture : list[list[str]], row : int):
    if row == 0:
        return
    else:
        prevRow = picture[row - 1]
        currRow = picture[row]
        for col in range(len(picture[row])):
            if currRow[col] == EMPTY_CHAR:
                # Current column value
                currentColVal = 0
                if prevRow[col] == START_CHAR:
                    currentColVal = 1
                elif isinstance (prevRow[col], int):
                    currentColVal = prevRow[col]

                # Previous column value
                prevColVal = 0
                prevCol = col - 1
                if prevCol >= 0 and currRow[prevCol] == SPLIT_CHAR:
                    prevColVal = prevRow[prevCol] if isinstance(prevRow[prevCol], int) else 0

                # Next column value
                nextColVal = 0
                nextCol = col + 1
                if nextCol < len(currRow) and currRow[nextCol] == SPLIT_CHAR:
                    nextColVal = prevRow[nextCol] if isinstance(prevRow[nextCol], int) else 0

                newColVal = currentColVal + prevColVal + nextColVal
                if newColVal != 0:
                    currRow[col] = newColVal
                
def processPicture(picture : list[list[str]]):
    for row in range (len(picture)):
        iterateRow(picture, row)

def countSplits(picture : list[list[str]]):
    splits = 0
    for row in range (1,len(picture)):
        prevRow = picture[row - 1]
        currRow = picture[row]
        for col in range(len(picture[row])):
            if isinstance(prevRow[col], int) and currRow[col] == SPLIT_CHAR:
                splits = splits + 1
    return splits

def countPaths(picture : list[list[str]]):
    lastRow = picture[-1]
    return sum([i for i in lastRow if isinstance(i, int)])

# PUZZLE SOLVING
if __name__=="__main__":
    picture = readData(filename)
    # printData(picture)
    processPicture(picture)
    # printData(picture)
    splitCount = countSplits(picture)
    print(f"Total splits: {splitCount}")
    pathsCount = countPaths(picture)
    print(f"Total paths: {pathsCount}")
