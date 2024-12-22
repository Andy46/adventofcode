from itertools import permutations
import copy

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])

filename, DEBUG = f"{filepath}/00_test.data", False
filename, DEBUG = f"{filepath}/00_example1.data", True

# Read data
CODE_LIST = []
with open(filename, "r") as file:
    CODE_LIST = [line.strip() for line in file.readlines()]


def readMatrixFile(filename):
    matrix = []
    with open(filename, "r") as file:
        lines = [line.strip() for line in file.readlines()]
        matrix = [list(row.strip()) for row in lines]
    return matrix

numpadfile = f"{filepath}/01_numpad.data"
NUMKEYS = readMatrixFile(numpadfile)
dirpadfile = f"{filepath}/01_dirpad.data"
DIRKEYS = readMatrixFile(dirpadfile)

def getPositionValue(matrix, x, y):
    return matrix[y][x]

def getAllValuePositions(matrix):
    valuesPositions = {}
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            valuesPositions[getPositionValue(matrix, x,y)] = [x,y]
    return valuesPositions

def getNumPadMoves(A, B):
    moves = []

    LastX, LastY = len(NUMKEYS[0])-1, len(NUMKEYS)-1
    ProhibitedPos = [(0, LastY)]

    currentX, currentY = A
    Bx, By = B

    while currentX != Bx or currentY != By:
        if currentX > Bx and (currentX-1, currentY) not in ProhibitedPos: # Then check right to left
            moves.extend('<')
            currentX -= 1
        elif currentY > By and (currentX, currentY-1) not in ProhibitedPos: # Then check bottom to up
            moves.extend('^')
            currentY -= 1
        elif currentX < Bx: # First check left to right
            moves.extend('>')
            currentX += 1
        elif currentY < By: # Then check up to bottom
            moves.extend('v')
            currentY += 1

    moves.extend('A')
    return moves

def getDirPadMoves1(A, B):
    moves = []

    LastX, LastY = len(DIRKEYS[0])-1, len(DIRKEYS)-1
    ProhibitedPos = [(0, 0)]

    currentX, currentY = A
    Bx, By = B

    while currentX != Bx or currentY != By:
        if currentX > Bx and (currentX-1, currentY) not in ProhibitedPos: # Then check right to left
            moves.extend('<')
            currentX -= 1
        elif currentY < By and (currentX, currentY+1) not in ProhibitedPos: # Then check up to bottom
            moves.extend('v')
            currentY += 1
        elif currentX < Bx: # First check left to right
            moves.extend('>')
            currentX += 1
        elif currentY > By: # Then check bottom to up
            moves.extend('^')
            currentY -= 1

    moves.extend('A')
    return moves

print(getDirPadMoves1([2,0],[0,1]))

def getDirPadMoves2(A, B):
    return getDirPadMoves1(A, B)
    moves = []
    Ax, Ay = A
    Bx, By = B
    if Ax < Bx: # First check left to right
        moves.extend('>'*(Bx-Ax))
    if Ay < By: # Then check up to bottom
        moves.extend('v'*(By-Ay))
    if Ax > Bx: # Then check right to left
        moves.extend('<'*(Ax-Bx))
    if Ay > By: # Then check bottom to up
        moves.extend('^'*(Ay-By))
    moves.extend('A')
    return moves


def findMovesPad(matrix, code, padMoves):

    KEY_POSITIONS = getAllValuePositions(matrix)
    # if DEBUG:
    #     for item in KEY_POSITIONS.values():
    #         print (item)
    #     print(KEY_POSITIONS)
    
    currentKey = 'A'
    sequence = []
    for nextKey in code:
        currentPos = KEY_POSITIONS[currentKey]
        nextPos    = KEY_POSITIONS[nextKey]
        nextMoves  = padMoves(currentPos, nextPos)
        sequence.extend(nextMoves)
        currentKey = nextKey
    return sequence

# code = "029A"
# codeMoves = findMovesNumPad(NUMKEYS, code)
# print(f"Code {code} -> {codeMoves}")


PERMUTATIONS = {}

def calculatePermutations(move):
    return list(set(permutations(move)))

def getAllCombinations(moves):
    SPLITTER = 'A'
    splitted = str(''.join(moves)).strip().split(SPLITTER)[:-1]
    for move in splitted:
        if move not in PERMUTATIONS:
            PERMUTATIONS[move] = calculatePermutations(move)

    def combine(chain, perms):
        newChains = []
        for perm in perms:
            newChain = copy.deepcopy(chain)
            newChain.append(perm)
            newChains.append(newChain)
        return newChains

        
    combinations = [PERMUTATIONS[splitted[0]]]
    for move in splitted[1:]:
        nextCombinations = []
        for currenCombination in combinations:
            newCombinations = combine(currenCombination, PERMUTATIONS[move])
            nextCombinations.extend(newCombinations)
        combinations = nextCombinations

    # Add A to all moves
    def reconstruct(chain):
        moves = ""
        for move in [str(''.join(move)) for move in chain]:
            moves = moves + move + "A"
        return moves

    combinations = set([reconstruct(combination) for combination in combinations])



    return combinations






import re
def calculateComplexity(code):
    def printSequence(code, complexity, sequence):
        print(f"{code}({complexity}): {''.join(sequence)}")

    # Get moves to control the final robot
    codeMoves = findMovesPad(NUMKEYS, code, getNumPadMoves)
    printSequence(code, 0, codeMoves)
    codeMovesSet = getAllCombinations(codeMoves)

    dirMoves1Set = []
    for codeMoves in codeMovesSet:
        dirMoves1 = findMovesPad(DIRKEYS, codeMoves, getDirPadMoves1)
        printSequence(code, 0, dirMoves1)
        dirMoves1Set.extend(getAllCombinations(dirMoves1))

    dirMoves2Set = []
    for dirMoves1 in dirMoves1Set:
        dirMoves2 = findMovesPad(DIRKEYS, dirMoves1, getDirPadMoves2)
        printSequence(code, 0, dirMoves2)
        # dirMoves2Set.extend(getAllCombinations(dirMoves2))
        dirMoves2Set.append(dirMoves2)

    # printSequence(code, 0, dirMoves1)

    # dirMoves2 = findMovesPad(DIRKEYS, dirMoves1, getDirPadMoves2)

    num, letter = re.findall("(\d+)([a-zA-Z])", code)[0]
    complexity = int(num) * len(dirMoves2)
    printSequence(code, complexity, dirMoves2)

    return complexity


def calculateTotalComplexity(codes):
    totalComplexity = 0
    for code in codes:
        complexity = calculateComplexity(code)
        totalComplexity += complexity
    return totalComplexity

totalComplexity = calculateTotalComplexity(CODE_LIST)
print(f"Total complexity: {totalComplexity}")



# v<<A >>^A vA ^A v<<A >>^A A v<A <A >>^A A vA A ^< A> A v<A>^AA<A>Av<A<A>>^AAAvA^<A>A

# <v<A >>^A vA ^A <vA <A A >>^A A vA <^A >A A vA ^ A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
# v<<A>>^AvA^Av<<A>>^AAv<A<A>>^AAvAA^<A>Av<A>^AA<A>Av<A<A>>^AAAvA^<A>A




# <v<A
# >>^A
# vA 
# ^A
# <vA
# <A
# A
# >>^A
# A
# vA
# <^A
# >A
# A
# vA
# ^A
# <vA
# >^A
# A
# <A
# >A
# <v<A
# >A
# >^A
# A 
# A 
# vA 
# <^A 
# >A 