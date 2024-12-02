filename = "00_example.data"
filename = "00_test.data"

reports = []
with open(filename, "r") as file:
    for line in file.readlines():
        line = line.strip()
        levels = line.split(" ")
        levels = list(map(int, levels))
        reports.append(levels)

# Helper functions
def isAscendingDiffSafe(a, b, maxDelta):
    if (a > b) and ((a - b) <= maxDelta):
        return True
    else:
        return False

def isDescendingDiffSafe(a, b, maxDelta):
    if (a < b) and ((b - a) <= maxDelta):
        return True
    else:
        return False

UNSAFE_DIFF = 3
def isSafeAscending(report):
    for index in range(1, len(report)):
        if isAscendingDiffSafe(report[index], report[index-1], UNSAFE_DIFF):
            continue
        else:
            return False, index
    return True, 0
    
def isSafeDescending(report):
    for index in range(1, len(report)):
        if not (report[index] < report[index-1]):
            return False, index
        if abs(report[index] - report[index-1]) > UNSAFE_DIFF:
            return False, index
    return True, 0

#########################
# Part 1 - Safe reports #
#########################
safeCount = 0
for report in reports:
    if isSafeAscending(report)[0]:
        safeCount = safeCount + 1
    if isSafeDescending(report)[0]:
        safeCount = safeCount + 1
        
print("Safe reports: " + str(safeCount))

###############################
# Part 2 - Safe reports extra #
###############################
safeCount = 0
for report in reports:
    # Check ascending
    isSafe, index = isSafeAscending(report)
    if isSafe:
        safeCount = safeCount + 1
        continue
    else:
        for i in range (-1, 2):
            tempReport = report.copy()
            tempReport.pop(index + i)
            isSafe, index = isSafeAscending(tempReport)
            if isSafe:
                safeCount = safeCount + 1
                break

    # Check descending
    isSafe, index = isSafeDescending(report)
    if isSafe:
        safeCount = safeCount + 1
        continue
    else:
        for i in range (-1, 2):
            tempReport = report.copy()
            tempReport.pop(index + i)
            isSafe, index = isSafeDescending(tempReport)
            if isSafe:
                safeCount = safeCount + 1
                break

print("Safe reports extra: " + str(safeCount))



