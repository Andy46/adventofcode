# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/example.data"
filename = f"{filepath}/test.data"

# DATA PARSING
def transposeMatrix(matrix : list[list[any]]) -> list[list[any]]:
    cols = len(matrix[0])
    rows = len(matrix)
    transposed = [[0 for _ in range(rows)] for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            transposed[j][i] = matrix[i][j]
    return transposed

def printData(operations : any) -> None:
    print(operations)

def splitData(data, indexes):
    newData = []
    for indexPair in indexes:
        operation = [row[indexPair[0]:indexPair[1]] for row in data]
        newData.append(operation)
    return newData

def transposeNumbers(op):
    numbers = op[:-1]
    transposedNumbers = transposeMatrix(numbers)
    transposedNumbers = [int(''.join(item)) for item in transposedNumbers if any([c != ' ' for  c in item])]
    operator = op[-1].strip()
    return transposedNumbers, operator

def readData(filename : str) -> tuple[list[list[int]], list[str]]:
    with open(filename, "r") as file:
        text = [line.strip('\n') for line in file.readlines()]
        data = [line for line in text]
        
        # Calculate columns 
        operations = data[-1]
        opIndexesStarts = [i for i, x in enumerate(operations) if x != ' ']
        opIndexesEnds   = opIndexesStarts[1:] + [len(operations)]
        opIndexes = list(zip(opIndexesStarts, opIndexesEnds))

        # SplittedData
        splittedData = splitData(data, opIndexes)

        # Data numbers and operations
        parsedData = [transposeNumbers(item) for item in splittedData]
        return parsedData
    
# AUX FUNCTIONS
def calcOperation(numbers : list[int], operation : str) -> int:
    import math
    SUM_OP = '+'
    MULT_OP = '*'
    if operation == SUM_OP:
        return sum(numbers)
    elif operation == MULT_OP:
        return math.prod(numbers)
    else:
        print(f"Error: Operation not implemented: {operation}")
        print(f"Numbers: {numbers}")

def calcOperations(operations):
    results = [calcOperation(nums, op) for nums, op in operations]
    return sum(results)

# PUZZLE SOLVING
if __name__=="__main__":
    operations = readData(filename)
    # printData(operations)
    result = calcOperations(operations)
    print(f"Total value: {result}")
