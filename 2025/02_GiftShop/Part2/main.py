# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/example.data"
filename = f"{filepath}/test.data"

# DATA PARSING
def extractRanges(input : str)-> list[str]:
    SEPARATOR_STR=','
    RANGE_SEPARATOR='-'

    ranges = [range for range in input.split(SEPARATOR_STR)]
    ranges = [[range.split(RANGE_SEPARATOR)[0], range.split(RANGE_SEPARATOR)[1]] for range in ranges]

    return ranges

def readData(filename : str) -> str:
    with open(filename, "r") as file:
        return file.readline() 

# AUX FUNCTIONS
def getFactors(num : int) -> list[int]:
    factors = []
    for i in range(2, num+1):
        if num % i == 0:
            factors.append(i)
    return factors

MAX_SIZE = 20
factors = [getFactors(num) for num in range(MAX_SIZE)]

def printFactors():
    for i, f in enumerate(factors):
        print(f"Factors {i}: {f}")

def split(text : str, num : int) -> list[str]:
    textList = []
    textSize = len(text)
    splitSize = int(textSize / num)
    for pos in range(0, textSize, splitSize):
        textList.append(text[pos:pos+splitSize])
    return textList

def isValid(id : str) -> bool:
    for factor in factors[len(id)]:
        pieces = split(id, factor)
        firstPiece = pieces[0]
        if all(piece == firstPiece for piece in pieces):
            return False
    return True # If reaches here id is valid

def getInvalidIds(rng : list) -> list[str]:
    first = rng[0]
    last = rng[1]

    invalidIds = []
    for value in range(int(first), int(last)+1):
        if not isValid(str(value)):
            invalidIds.append(str(value))
    return invalidIds

# PUZZLE EXECUTION
if __name__=="__main__":
    data = readData(filename)
    ranges = extractRanges(data)
    invalidIds = []

    for rng in ranges:
        invalidIds.extend(getInvalidIds(rng))
    total = sum([int(id) for id in invalidIds])
    print(f"Sum of invalids: {total}")
