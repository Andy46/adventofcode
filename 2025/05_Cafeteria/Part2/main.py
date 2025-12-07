# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/example.data"
filename = f"{filepath}/test.data"

# DATA PARSING
def readData(filename : str) -> list[list[str]]:
    with open(filename, "r") as file:
        text = [line.strip() for line in file.readlines()]
        split_index = text.index('')
        ranges = [text.split('-') for text in text[:split_index]]
        ranges = [[int(r[0]), int(r[1])] for r in ranges]
        ingredients = text[split_index+1:]
        ingredients = [int(i) for i in ingredients]
        return ranges, ingredients

def sortRanges(ranges):
    return sorted(ranges, key=lambda x: (x[0], x[1]))

# AUX FUNCTIONS
def joinRanges(range1, range2):
    min1, max1 = range1
    min2, max2 = range2

    if max1 < min2:
        return False, [range1, range2]
    elif max1 < max2:
        return True, [min1, max2]
    else: # max1 >= max2
        return True, [min1, max1]
    
def reduceRanges(ranges):
    newRanges = []
    rangeIndex = 1
    currentRange = ranges[0]
    while True:
        joined, rangeList = joinRanges(currentRange, ranges[rangeIndex])
        if joined:
            currentRange = rangeList
            rangeIndex = rangeIndex + 1
        else:
            newRanges.append(rangeList[0])
            currentRange = rangeList[1]
        if rangeIndex >= len(ranges):
            newRanges.append(currentRange)
            break
    return newRanges

def getRangeCount(r):
    return (r[1] - r[0] + 1)

def getFreshIdCount(ranges):
    rangesLengths = [getRangeCount(r) for r in ranges]
    return sum(rangesLengths)

# PUZZLE SOLVING
if __name__=="__main__":
    ranges, ingredients = readData(filename)
    ranges = sortRanges(ranges)
    # print(len(ranges))
    # print(ranges)
    ranges = reduceRanges(ranges)
    # print(len(ranges))
    # print(ranges)
    freshIds = getFreshIdCount(ranges)
    print(f"Fresh IDs count: {freshIds}")
