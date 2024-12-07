import copy
import click

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/00_example.data"
filename = f"{filepath}/00_test.data"

# Read data
data = []
with open(filename, "r") as file:
    for line in file.readlines():
        line = line.strip()
        result = line.split(':')[0]
        operands = line.split(':')[1].strip().split(' ')
        data.append([int(result), list(map(int,operands))])

# Helper functions
def calculatePossibleResults(operands):
    results = []
    current = operands[0]
    others = operands[1:]
    if len(operands) == 1:
        return [current]
    else:
        for op in operations:
            results.extend([op(result, current) for result in calculatePossibleResults(others)])
    return results

def canBeTrue(result, operands):
    operands = operands.copy()
    operands.reverse()
    results = calculatePossibleResults(operands)
    # return result in results
    if result in results:
        # print(f"{result} can be true with {operands}")
        return True
    else:
        return False

#######################
# Part 1 - Guard path #
#######################
print ("Part 1 - Calibration with sum and mul")

# Helper functions for part 1
def add(a,b):
    return a+b

def multiply(a,b):
    return a*b

operations = [add, multiply]

# Calculate
totalCalibrationResult = 0
with click.progressbar(data) as bar: # Progress bar
    for equation in bar:
        result = equation[0]
        operands = equation[1]
        if canBeTrue(result, operands):
            totalCalibrationResult = totalCalibrationResult + result

# Calculate count and output result
print(f"Total calibration result: {totalCalibrationResult}")

# ###########################
# # Part 2 - Find loop path #
# ###########################
print ("Part 2 - Calibration with sum, mul and concat")

# Helper functions for part 2
def concat(a,b):
    return int(str(a) + str(b))

operations = [add, multiply, concat]

# Calculate
totalCalibrationResult = 0
with click.progressbar(data) as bar: # Progress bar
    for equation in bar:
        result = equation[0]
        operands = equation[1]
        if canBeTrue(result, operands):
            totalCalibrationResult = totalCalibrationResult + result

# Calculate count and output result
print(f"Real total calibration result: {totalCalibrationResult}")
