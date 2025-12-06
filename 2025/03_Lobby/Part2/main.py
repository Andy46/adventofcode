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

class Joltage:
    MAX_BATTERIES = 12
    batteries = []

    def __init__(self):
        self.batteries = []

    def push(self, battery : int):
        self.batteries.append(battery)
        self.__fix()

    def __fix(self):
        if len(self.batteries) > self.MAX_BATTERIES:

            # Remove the first item that is less than the next
            for i in range(self.MAX_BATTERIES - 1):
                if self.batteries[i] < self.batteries[i+1]:
                    self.batteries.pop(i)
                    return
                
            # If reaches here, all batteries are in order
            # choose between the last 2 items inserted
            if self.batteries[-1] > self.batteries[-2]:
                self.batteries.pop(-2)
            else:
                self.batteries.pop(-1)


    def getJoltageValue(self):
        joltage = 0
        for battery in self.batteries:
            joltage = (joltage*10) + battery
        return joltage

def findBankJoltage(bank : str) -> int:
    batteries = getBatteries(bank)
    joltage = Joltage()
    for battery in batteries:
        joltage.push(int(battery))
    return joltage.getJoltageValue()

# PUZZLE SOLVING
if __name__=="__main__":
    banks = readData(filename)
    joltages = [findBankJoltage(bank) for bank in banks]
    total = sum(joltages)
    # print(f"Bank joltages: {joltages}")
    print(f"Total joltage: {total}")
