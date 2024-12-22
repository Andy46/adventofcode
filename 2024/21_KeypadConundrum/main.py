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



# DIR_PERMUTATIONS = {
#     "": [""],

#     "<": ["<"],
#     "^": ["^"],
#     ">": [">"],
#     "v": ["v"],

#     "<^": ["<v", "v<"],
#     "<v": ["<v", "v<"],

#     "^>": ["^>", ">^"],
#     "^<": ["^>", ">^"],

#     ">^": [">^", "^>"],
#     ">v": [">^", "^>"],

#     "v>": ["v>", ">v"],
#     "v<": ["v<", "<v"],

#     ">>^": [">>^"], # [">>^", ">^>", "^>>"], 
#     ">^>": [">>^"], # [">>^", ">^>", "^>>"], 
#     # "^>>": [">>^", ">^>", "^>>"],

#     # ">>v": [">>v", ">v>", "v>>"],
#     # ">v>": [">>v", ">v>", "v>>"],
#     # "v>>": [">>v", ">v>", "v>>"],

#     # "<<v": ["<<v", "<v<", "v<<"],
#     "<v<": ["<v<"], # ["<<v", "<v<", "v<<"],
#     "v<<": ["<v<"], # ["<<v", "<v<", "v<<"],

#     # "<<^": ["<<^", "<^<", "^<<"],
#     # "<^<": ["<<^", "<^<", "^<<"],
#     # "^<<": ["<<^", "<^<", "^<<"],

#     # "vv>": ["vv>", "v>v", ">vv"],
#     # "v>v": ["vv>", "v>v", ">vv"],
#     # ">vv": ["vv>", "v>v", ">vv"],

#     # "vv<": ["vv<", "v<v", "<vv"],
#     # "v<v": ["vv<", "v<v", "<vv"],
#     # "<vv": ["vv<", "v<v", "<vv"],

#     # "^^>": ["^^>", "^>^", ">^^"],
#     # "^>^": ["^^>", "^>^", ">^^"],
#     # ">^^": ["^^>", "^>^", ">^^"],

#     # "^^<": ["^^<", "^<^", "<^^"],
#     # "^<^": ["^^<", "^<^", "<^^"],
#     # "<^^": ["^^<", "^<^", "<^^"],
# }





# def findAllDistances(matrix):
#     def getDistance(A, B):
#         return sum([abs(pair[0] - pair[1]) for pair in zip(A, B)])

#     def getPositionValue(matrix, x, y):
#         return matrix[y][x]

#     def findDistancesXY(matrix, x, y):
#         distances = {}
#         for yd in range(len(matrix)):
#             for xd in range(len(matrix[0])):
#                 value = getPositionValue(matrix, xd, yd)
#                 distances[value] = getDistance([x,y], [xd,yd])
#         return distances
    
#     distances = {}
#     for y in range(len(matrix)):
#         for x in range(len(matrix[0])):
#             value = getPositionValue(matrix, x,y)
#             distances[value] = findDistancesXY(matrix, x, y)
#     return distances
    
# numDistances = findAllDistances(NUMKEYS)
# dirDistances = findAllDistances(DIRKEYS)

# print (f"Num distances: {numDistances}")
# print (f"Dir distances: {dirDistances}")

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
    Ax, Ay = A
    Bx, By = B
    if Ax < Bx: # First check left to right
        moves.extend('>'*(Bx-Ax))
    if Ay > By: # Then check bottom to up
        moves.extend('^'*(Ay-By))
    if Ax > Bx: # Then check right to left
        moves.extend('<'*(Ax-Bx))
    if Ay < By: # Then check up to bottom
        moves.extend('v'*(By-Ay))
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

def getDirPadMoves2(A, B):
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


# PERMUTATIONS = copy.deepcopy(DIR_PERMUTATIONS)

def calculatePermutations(move):
    return list(set(permutations(move)))

# def getNumCombinations(moves):
#     SPLITTER = 'A'
#     splitted = str(''.join(moves)).strip().split(SPLITTER)[:-1]
#     for move in splitted:
#         if move not in PERMUTATIONS:
#             PERMUTATIONS[move] = calculatePermutations(move)

#     def combine(chain, perms):
#         newChains = []
#         for perm in perms:
#             newChain = copy.deepcopy(chain)
#             newChain.append(perm)
#             newChains.append(newChain)
#         return newChains

        
#     combinations = [PERMUTATIONS[splitted[0]]]
#     for move in splitted[1:]:
#         nextCombinations = []
#         for currenCombination in combinations:
#             newCombinations = combine(currenCombination, PERMUTATIONS[move])
#             nextCombinations.extend(newCombinations)
#         combinations = nextCombinations

#     # Add A to all moves
#     def reconstruct(chain):
#         moves = ""
#         for move in [str(''.join(move)) for move in chain]:
#             moves = moves + move + "A"
#         return moves

#     combinations = set([reconstruct(combination) for combination in combinations])
#     return combinations

# def getDirCombinations(moves):
#     SPLITTER = 'A'
#     splitted = str(''.join(moves)).strip().split(SPLITTER)[:-1]
#     for move in splitted:
#         if move not in DIR_PERMUTATIONS:
#             DIR_PERMUTATIONS[move] = calculatePermutations(move)

#     def combine(chain, perms):
#         newChains = []
#         for perm in perms:
#             newChain = copy.deepcopy(chain)
#             newChain.append(perm)
#             newChains.append(newChain)
#         return newChains

        
#     combinations = [[perm] for perm in DIR_PERMUTATIONS[splitted[0]]]
#     for move in splitted[1:]:
#         nextCombinations = []
#         for currenCombination in combinations:
#             newCombinations = combine(currenCombination, DIR_PERMUTATIONS[move])
#             nextCombinations.extend(newCombinations)
#         combinations = nextCombinations

#     # Add A to all moves
#     def reconstruct(chain):
#         moves = ""
#         for move in [str(''.join(move)) for move in chain]:
#             moves = moves + move + "A"
#         return moves

#     combinations = set([reconstruct(combination) for combination in combinations])
#     return combinations




def getDirMoves1(dirMoves0):
    LATEST_CONVERSIONS = {
        "A": "A",

        "<A": "<v<A>>^A",
        "^A": "<A>A",
        ">A": "vA^A",
        "vA": "<vA>^A",

        "<^A": "v<<A>^A>A",
        "^<A": "<Av<A>>^A",
        
        "<vA": "v<<A>A>^A",
        "v<A": "<vA<A>>^A",

        ">^A": "vA<^A>A",
        "^>A": "<A>vA^A",

        ">vA": "vA<A>^A",
        "v>A": "<vA>A^A",

        ">>^A": "vAA<^A>A",
        ">^>A": "vAA<^A>A",
        "^>>A": "vAA<^A>A",
        
        ">^^A": "vA<^AA>A",
        "^>^A": "vA<^AA>A",
        "^^>A": "vA<^AA>A",

        "<<^A": "<Av<AA>>^A",
        "<^<A": "<Av<AA>>^A",
        "^<<A": "<Av<AA>>^A",
        
        "<^^A": "<AAv<A>>^A",
        "^<^A": "<AAv<A>>^A",
        "^^<A": "<AAv<A>>^A",
        
        "<v<A": "<vA<AA>>^A",
        "v<<A": "<vA<AA>>^A",
        "<<vA": "<vA<AA>>^A",

        "<vvA": "v<<A>AA^>A",
        "v<vA": "v<<A>AA^>A",
        "vv<A": "v<<A>AA^>A",

        ">vvA": "v<AA>A^A",
        "v>vA": "v<AA>A^A",
        "vv>A": "v<AA>A^A",

        "<<A": "v<<AA^A",
        "^^A": "<AA>A",
        ">>A": "vAA^A",
        "vvA": "<vAA>^A",

        "^^^A": "<AAA>A",
        "vvvA": "<vAAA>^A",

        ">>^^A": "vAA<^AA>A",
        "^^>>A": "vAA<^AA>A",
        
        ">>^^A": "vAA<^AA>A",
        "^^>>A": "vAA<^AA>A",

        "<<^^A": "<AAv<AA>>^A",
        "^^<<A": "<AAv<AA>>^A",
        
        "<<^^A": "<AAv<AA>>^A",
        "^^<<A": "<AAv<AA>>^A",
        
        "vv<<A": "<vAA<AA>>^A",
        "<<vvA": "<vAA<AA>>^A",

        "<<vvA": "v<<AA>AA^>A",
        "vv<<A": "v<<AA>AA^>A",

        ">>vvA": "v<AA>AA^A",
        "vv>>A": "v<AA>AA^A",

    }

    SPLITTER = 'A'
    splitted = str(''.join(dirMoves0)).strip().split(SPLITTER)[:-1]
    splitted = [move+'A' for move in splitted]

    subMoves = []
    for move in splitted:
        if move not in LATEST_CONVERSIONS:
            pass
        subMoves.append(LATEST_CONVERSIONS[move])

    temp = str(''.join(subMoves))

    return temp

def getDirMoves2(dirMoves1):
    LATEST_CONVERSIONS = {
        "A": "A",

        "<A": "<v<A>>^A",
        "^A": "<A>A",
        ">A": "vA^A",
        "vA": "<vA>^A",

        "<^A": "<v<A>^A>A",
        "^<A": "<Av<A>>^A",
        
        "<vA": "<v<A>A>^A",
        "v<A": "<vA<A>>^A",

        ">^A": "vA<^A>A",
        "^>A": "<A>vA^A",

        ">vA": "vA<A>^A",
        "v>A": "<vA>A^A",

        ">>^A": "vAA<^A>A",
        ">^>A": "vAA<^A>A", #"vA^<A>vA^A",
        
        "<v<A": "<vA<AA>>^A", #"<v<A>A<A>>^A",
        "v<<A": "<vA<AA>>^A",
    }

    SPLITTER = 'A'
    splitted = str(''.join(dirMoves1)).strip().split(SPLITTER)[:-1]
    splitted = [move+'A' for move in splitted]

    subMoves = []
    for move in splitted:
        if move not in LATEST_CONVERSIONS:
            pass
        subMoves.append(LATEST_CONVERSIONS[move])

    temp = str(''.join(subMoves))

    return temp






import re
def calculateComplexity(code):
    def printSequence(code, complexity, sequence):
        print(f"{code}({complexity}): {''.join(sequence)}")

    # Get moves to control the final robot
    codeMoves = findMovesPad(NUMKEYS, code, getNumPadMoves)
    printSequence(code, 0, codeMoves)
    # codeMovesSet = getNumCombinations(codeMoves)

    # dirMoves1Set = []
    # for codeMoves in codeMovesSet:
    dirMoves1 = getDirMoves1(codeMoves)
        # temp = getDirCombinations(dirMoves1)
        # dirMoves1Set.extend(temp)

    # dirMoves2Set = []
    # for dirMoves1 in dirMoves1Set:
    #     dirMoves2 = findMovesPad(DIRKEYS, dirMoves1, getDirPadMoves1)
    #     dirMoves2Set.extend(getDirCombinations(dirMoves2))
        # dirMoves2Set.append(dirMoves2)

    dirMoves2 = getDirMoves2(dirMoves1)

    

    # printSequence(code, 0, dirMoves1)

    # dirMoves2 = findMovesPad(DIRKEYS, dirMoves1, getDirPadMoves2)

    num, letter = re.findall("(\d+)([a-zA-Z])", code)[0]
    complexity = int(num) * len(dirMoves2)

    if DEBUG:
        printSequence(code, complexity, dirMoves2)

    return complexity


def calculateTotalComplexity(codes):
    totalComplexity = 0
    for code in CODE_LIST:
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