# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/example.data"
filename = f"{filepath}/test.data"

# DATA PARSING
def transpose(matrix : list[list[any]]) -> list[list[any]]:
    cols = len(matrix[0])
    rows = len(matrix)
    transposed = [[0 for _ in range(rows)] for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            transposed[j][i] = matrix[i][j]
    return transposed

def castMatrix(matrix, func):
    cols = len(matrix[0])
    rows = len(matrix)
    for i in range(rows):
        for j in range(cols):
            matrix[i][j] = func(matrix[i][j])

def printData(numbers, operations):
    print(numbers)
    print(operations)

def readData(filename : str) -> tuple[list[list[int]], list[str]]:
    with open(filename, "r") as file:
        text = [line.strip() for line in file.readlines()]
        data = [line.split() for line in text]
        numbers = transpose(data[:-1])
        castMatrix(numbers, int)
        operations = data[-1]
        return numbers, operations
    
# AUX FUNCTIONS
def calcOperation(numbers : list[int], operation : str):
    import math
    SUM_OP = '+'
    MULT_OP = '*'
    if operation == SUM_OP:
        return sum(numbers)
    elif operation == MULT_OP:
        return math.prod(numbers)
    else:
        print("WHAT")

def calcOperations(numbers : list[list[int]], operations : list[str]):
    results = [calcOperation(nums, op) for nums, op in zip(numbers, operations)]
    return sum(results)

# PUZZLE SOLVING
if __name__=="__main__":
    numbers, operations = readData(filename)
    # printData(numbers, operations)
    result = calcOperations(numbers, operations)
    print(f"Total value: {result}")
