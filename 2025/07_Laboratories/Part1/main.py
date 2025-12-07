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
    for item in data:
        print(''.join(item))

# AUX FUNCTIONS
def iterateRow(picture : list[list[str]], row : int):
    if row == 0:
        return
    else:
        prevRow = picture[row - 1]
        currRow = picture[row]
        for col in range(len(picture[row])):
            if currRow[col] == EMPTY_CHAR:
                if prevRow[col] in [START_CHAR, TACHYON_CHAR]:
                    currRow[col] = TACHYON_CHAR
            elif currRow[col] == SPLIT_CHAR:
                prevCol = col - 1
                if prevCol >= 0 and currRow[prevCol] == EMPTY_CHAR:
                    currRow[prevCol] = TACHYON_CHAR
                nextCol = col + 1
                if nextCol < len(currRow) and currRow[nextCol] == EMPTY_CHAR:
                    currRow[nextCol] = TACHYON_CHAR
            elif currRow[col] in [START_CHAR, TACHYON_CHAR]:
                pass            
                
def processPicture(picture : list[list[str]]):
    for row in range (len(picture)):
        iterateRow(picture, row)

def countSplits(picture : list[list[str]]):
    splits = 0
    for row in range (1,len(picture)):
        prevRow = picture[row - 1]
        currRow = picture[row]
        for col in range(len(picture[row])):
            if prevRow[col] == TACHYON_CHAR and currRow[col] == SPLIT_CHAR:
                splits = splits + 1
    return splits


# PUZZLE SOLVING
if __name__=="__main__":
    picture = readData(filename)
    # printData(picture)
    processPicture(picture)
    # printData(picture)
    splitCount = countSplits(picture)
    print(f"Total splits: {splitCount}")
