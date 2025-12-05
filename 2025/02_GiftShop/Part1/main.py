# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/example.data"
filename = f"{filepath}/test.data"

def halfLength(length : str) -> int:
    return int(len(length)/2)
    
def splitHalf(text : str) -> list[str]:
    return text[:halfLength(text)], text[halfLength(text):]

def extractRanges(input : str)-> list[str]:
    SEPARATOR_STR=','
    RANGE_SEPARATOR='-'

    ranges = [range for range in input.split(SEPARATOR_STR)]
    ranges = [[range.split(RANGE_SEPARATOR)[0], range.split(RANGE_SEPARATOR)[1]] for range in ranges]

    return ranges

def readData(filename : str) -> str:
    with open(filename, "r") as file:
        return file.readline() 

def isValid(id : str):
    idLen = len(id)
    if idLen % 2 == 1:
        return True
    else:
        first, second = splitHalf(id)
        return first != second

def getInvalidIds(rng : list) -> list[str]:
    first = rng[0]
    last = rng[1]

    invalidIds = []
    for value in range(int(first), int(last)+1):
        if not isValid(str(value)):
            invalidIds.append(str(value))
    return invalidIds

if __name__=="__main__":
    data = readData(filename)
    ranges = extractRanges(data)
    invalidIds = []

    for rng in ranges:
        invalidIds.extend(getInvalidIds(rng))
    total = sum([int(id) for id in invalidIds])
    print(f"Sum of invalids: {total}")
