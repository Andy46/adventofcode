#!/bin/python3
from itertools import permutations
import re
import click
import copy

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])

filename, DEBUG = f"{filepath}/00_example1.data", True
filename, DEBUG = f"{filepath}/00_test.data", False

# Read data
CONNECTION_LIST = []
with open(filename, "r") as file:
    CONNECTION_LIST = [line.strip() for line in file.readlines()]

def findPCConnections(connections):
    pcConnections = {}
    for connection in connections:
        pcs = re.findall(r"(.*)-(.*)", connection)[0]
        for pc in pcs:
            if pc not in pcConnections:
                pcConnections[pc] = []
            connected = list(copy.deepcopy(pcs))
            connected.remove(pc)
            pcConnections[pc].extend(connected)    
    return pcConnections

def findNetworks(pcConnections):
    pcNetworks = []
    pcList = list(pcConnections.keys())
    for A in range(len(pcList)-2):
        pcA = pcList[A]
        for B in range(A+1, len(pcList)-1):
            pcB = pcList[B]
            for pcC in pcConnections[pcA]:
                if pcA in pcConnections[pcB] and pcB in pcConnections[pcC] and pcC in pcConnections[pcA]:
                    pcNetworks.append(sorted([pcA, pcB, pcC]))
    return pcNetworks 

#######################################
# Part 1 - Find the networks with 't' #
#######################################

# Calculate
allNetworks3 = set()
pcConnections = findPCConnections(CONNECTION_LIST)

# print(f"Network {pc} - {connections}")
pcNetworks = findNetworks(pcConnections)
allNetworks3.update([tuple(network) for network in pcNetworks])
# print(f"All network ({len(allNetworks3)}): {allNetworks3}")
        
tPCs = [pc for pc in pcConnections.keys() if pc[0] == 't']
tNetworks = [network for network in allNetworks3 if any([pc in network for pc in tPCs])]

# Output result
print (f"Networks with 't*' ({len(tNetworks)})")