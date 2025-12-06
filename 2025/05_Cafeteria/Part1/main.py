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

def sortIngredients(ingredients):
    return sorted(ingredients)
    
# AUX FUNCTIONS
def countFresh(ranges, ingredients) -> int:
    freshCount = 0
    rangeIndex = 0
    for ingredient in ingredients:
        while ingredient > ranges[rangeIndex][1]:
            rangeIndex = rangeIndex + 1
            if rangeIndex >= len(ranges):
                return freshCount
        if ingredient >= ranges[rangeIndex][0] and ingredient <= ranges[rangeIndex][1]:
            freshCount = freshCount + 1
            # print(f"Ingredient {ingredient} is fresh")
    return freshCount

# PUZZLE SOLVING
if __name__=="__main__":
    ranges, ingredients = readData(filename)
    ranges = sortRanges(ranges)
    ingredients = sortIngredients(ingredients)
    # print(ranges)
    # print(ingredients)
    freshCount = countFresh(ranges, ingredients)
    print(f"Fresh ingredients count: {freshCount}")
