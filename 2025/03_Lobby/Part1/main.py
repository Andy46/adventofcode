# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/example.data"
filename = f"{filepath}/test.data"

# DATA PARSING
def readData(filename : str) -> str:
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines()]


# AUX FUNCTIONS
def getBatteries(bank : str) -> list[int]:
    return [int(battery) for battery in bank]

def findMaxJoltage(bank : str) -> int:
    batteries = getBatteries(bank)
    joltage = 0
    for i, first in enumerate(batteries):
        for second in batteries[(i+1):]:
            tmp = first*10 + second
            joltage = max(joltage, tmp)
    return joltage 

# PUZZLE SOLVING
if __name__=="__main__":
    banks = readData(filename)
    joltages = [findMaxJoltage(bank) for bank in banks]
    total = sum(joltages)
    # print(f"Bank joltages: {joltages}")
    print(f"Total joltage: {total}")
