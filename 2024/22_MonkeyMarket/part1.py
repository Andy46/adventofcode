#!/bin/python3
from itertools import permutations
import copy
import click

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])

filename, DEBUG = f"{filepath}/00_example1.data", True
filename, DEBUG = f"{filepath}/00_example2.data", True
filename, DEBUG = f"{filepath}/00_test.data", False

# Read data
SECRET_LIST = []
with open(filename, "r") as file:
    SECRET_LIST = [int(line.strip()) for line in file.readlines()]

PRUNE_VAL = 16777216
def calculateNext(secret):
    # Step 1
    mixer = int(secret * 64)
    secret = secret ^ mixer
    secret = secret % PRUNE_VAL
    # Step 2
    mixer = int(secret / 32)
    secret = secret ^ mixer
    secret = secret % PRUNE_VAL
    # Step 3
    mixer = int(secret * 2048)
    secret = secret ^ mixer
    secret = secret % PRUNE_VAL
    return secret

def calculateShiftedNext(secret):
    # Step 1
    mixer = secret << 6
    secret = secret ^ mixer
    secret = secret % PRUNE_VAL
    # Step 2
    mixer = secret >> 5
    secret = secret ^ mixer
    secret = secret % PRUNE_VAL
    # Step 3
    mixer = secret << 11
    secret = secret ^ mixer
    secret = secret % PRUNE_VAL
    return secret

def calculateLastSecret(first):
    ITERATIONS = 2000
    secret = first
    for it in range(ITERATIONS):
        # secret = calculateNext(secret)
        secret = calculateShiftedNext(secret) # Shift operations save ~200ms
        pass
    return secret

#############################
# Part 1 - Find the secrets #
#############################

# Calculate
newSecrets = []
with click.progressbar(SECRET_LIST) as bar:
    for secret in bar:
        last = calculateLastSecret(secret)
        newSecrets.append(last)
totalSum = sum(newSecrets)

# Output result
print(f"Total sum: {totalSum}")