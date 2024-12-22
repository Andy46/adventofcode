#!/bin/python3
from itertools import permutations
import copy
import click

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])

filename, DEBUG = f"{filepath}/00_example1.data", True
filename, DEBUG = f"{filepath}/00_example2.data", True
filename, DEBUG = f"{filepath}/00_example3.data", True

filename, DEBUG = f"{filepath}/00_test.data", False

# Read data
SECRET_LIST = []
with open(filename, "r") as file:
    SECRET_LIST = [int(line.strip()) for line in file.readlines()]

SECRET_SEQS = {} # "secret:" {"seq": (), "bananas" : int}


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

SECRET_SEQS = {}
def calculateSequences(secret):
    secret_tups = {}
    ITERATIONS = 2000
    seq = []
    for it in range(ITERATIONS):
        prev = secret
        # secret = calculateNext(secret)
        secret = calculateShiftedNext(secret) # Shift operations save ~200ms

        prev_val = (prev % 10)
        val = (secret % 10)
        diff = val - prev_val
        seq.append(diff)

        if len(seq) == 4:
            tup = tuple(seq)
            if tup not in SECRET_SEQS:
                SECRET_SEQS[tup] = []
            if tup not in secret_tups:
                if val > 0: # Note: This optimizes the program by ~50 ms
                    SECRET_SEQS[tup].append(val)
                secret_tups[tup] = val
            seq.pop(0)

    return secret

#####################################
# Part 2 - Sell secret hidden spots #
#####################################

# Calculate
with click.progressbar(SECRET_LIST) as bar:
    for secret in bar:
        calculateSequences(secret)
SECRET_SEQS.update({seq: sum(SECRET_SEQS[seq]) for seq in SECRET_SEQS.keys()})
MAX = max(SECRET_SEQS.values())

# Output result
print(f"Max profit: {MAX}")