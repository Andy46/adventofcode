
# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/00_example.data"
filename = f"{filepath}/00_test.data"

# Read data
rules = []
updates = []
with open(filename, "r") as file:
    lines = [line.strip() for line in file.readlines()]
    MAIN_SEPARATOR = ""
    RULE_SEPARATOR = '|'
    UPDATE_SEPARATOR = ','
    rules = lines[:lines.index(MAIN_SEPARATOR)]
    rules = [rule.split(RULE_SEPARATOR) for rule in rules]
    updates = lines[(lines.index(MAIN_SEPARATOR)+1):]
    updates = [update.split(UPDATE_SEPARATOR) for update in updates]

# Helper functions
def isValid(rules, update):
    for rule in rules:
        pos0 = update.index(rule[0]) if rule[0] in update else None
        pos1 = update.index(rule[1]) if rule[1] in update else None
        if pos0 is None or pos1 is None:
            continue
        elif pos0 < pos1:
            continue
        else:
            return False
    return True        

###################################
# Part 1 - Find valid updates sum #
###################################

# Calculate
validSum = 0
for update in updates:
    valid = isValid(rules, update)
    middle = int(update[int(len(update)/2)])
    if isValid(rules, update):
        validSum = validSum + middle

# Output result
print(f"Valid updates sum: {validSum}")

#####################################
# Part 2 - Find invalid updates sum #
#####################################

# Helper functions for part 2
def findPosition(rules, update, elem):
    applicable = [rule for rule in rules if rule[0] == elem or rule[1] == elem]
    start_index = 0
    end_index = len(update)
    for rule in applicable:
        if rule[0] in update:
            start_index = max(start_index, update.index(rule[0])+1)
        elif rule[1] in update:
            end_index = min(end_index, update.index(rule[1]))
        if start_index == end_index:
            break
    return start_index

def insertElem(rules, update, elem):
    if update == []:
        update.append(elem)
    else:
        pos = findPosition(rules, update, elem)
        update.insert(pos, elem)
        if not isValid(rules, update):
            pass

def fixUpdate(rules, update):
    fixed = []
    for elem in update:
        insertElem(rules, fixed, elem)
    return fixed

# Calculate
invalidSum = 0
for update in updates: 
    if not isValid(rules, update):
        fixed = fixUpdate(rules, update)
        middle = int(fixed[int(len(update)/2)])
        if not isValid(rules, fixed):
            print("ERROR")
        invalidSum = invalidSum + middle


# Output result
print(f"Invalid updates sum: {invalidSum}")