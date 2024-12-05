import hashlib

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/00_example.data"
filename = f"{filepath}/00_example2.data"
filename = f"{filepath}/00_test.data"

# Output title
print ("Day 5: Doesn't He Have Intern-Elves For This?")

# Read data
data = []
with open(filename, "r") as file:
    lines = file.readlines()
    data = [line.strip() for line in lines]

# Helper functions

###############################
# Part 1 - Count nice strings #
###############################

# Helper functions for part 1
def contains3Vowels(token):
    ## Extended version ##
    # count = 0
    # for vowel in "aeiou":
    #     if vowel in token:
    #         count = count + token.count(vowel)
    ## On line ##
    count = sum(token.count(vowel) for vowel in "aeiou")
    return count >= 3

def containsDoubleLetter(token):
    prev = ' '
    for letter in token:
        if letter == prev:
            return True
        prev = letter
    return False

def containsForbiddenStrings(token):
    forbidden = ["ab", "cd", "pq", "xy"]
    ## Extended version ##
    # for string in forbidden:
    #     if string in token:
    #         return True
    # return False
    ## On line ##
    matches = [string in token for string in forbidden]
    return any(matches)

def isNice(token):
    return contains3Vowels(token) and containsDoubleLetter(token) and not containsForbiddenStrings(token)

# Calculate
niceStrings = [isNice(elem) for elem in data]
count = sum(niceStrings)

# Output result
print (f"Count of nice strings: {count}")
    

################################
# Part 2 - Count nicer strings #
################################

# Helper functions for part 2
def containsPairTwice(token):
    for i in range(0, len(token)-2):
        pair = token[i:i+2]
        if pair in token [i+2:]:
            return True
    return False

def containsSandwich(token):
    for i in range(0, len(token)-2):
        if token [i] == token[i+2]:
            return True
    return False

def isNicer(token):
    return containsPairTwice(token) and containsSandwich(token)

# Calculate
nicerStrings = [isNicer(elem) for elem in data]
count = sum(nicerStrings)

# Output result
print (f"Count of nicer strings: {count}")
    