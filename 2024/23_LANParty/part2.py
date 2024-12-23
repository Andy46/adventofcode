#!/bin/python3
import re
import copy
import networkx as nx

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])

filename = f"{filepath}/00_example1.data"
filename = f"{filepath}/00_test.data"

# Read data
CONNECTION_LIST = []
with open(filename, "r") as file:
    CONNECTION_LIST = [line.strip() for line in file.readlines()]

def getGraphConnections(connections):
    pcConnections = []
    for connection in connections:
        pcs = re.findall(r"(.*)-(.*)", connection)[0]
        pcConnections.append((pcs[0], pcs[1]))
    return pcConnections


def BronKerbosch1(R, P, X, pcConnections, cliques):
    if not P and not X:
        cliques.append(R)
        return 
    for node in P.copy():
        RU = R | {node}              # Add node to R set
        PN = P & pcConnections[node] # Intersection of P and nodes connected to "node"
        XN = X & pcConnections[node] # Intersection of X and nodes connected to "node"
        BronKerbosch1(RU, PN, XN, pcConnections, cliques)
        P.remove(node)
        X.add(node)

def findNodeConnections(connections):
    pcConnections = {}
    for connection in connections:
        pcs = re.findall(r"(.*)-(.*)", connection)[0]
        for pc in pcs:
            if pc not in pcConnections:
                pcConnections[pc] = set()
            connected = set(copy.deepcopy(pcs))
            connected.remove(pc)
            pcConnections[pc].update(connected)
    return pcConnections

##########################################
# Part 2 - Find largest network password #
##########################################

# Calculate
pcConnections = findNodeConnections(CONNECTION_LIST)

cliques = []
BronKerbosch1(set(), set(pcConnections.keys()), set(), pcConnections, cliques)
maxlen = max([len(network) for network in cliques])
maxCliques = [network for network in cliques if len(network) == maxlen]

# Output result
password = ""
for pc in sorted(maxCliques[0]):
    password = password+pc+","
password = password[:-1]
print(f"Password is: {password}")
