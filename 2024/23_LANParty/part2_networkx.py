#!/bin/python3
import re
import click
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

##########################################
# Part 2 - Find largest network password #
##########################################

# Calculate
pcConnections = getGraphConnections(CONNECTION_LIST)

graph = nx.Graph()
graph.add_edges_from(pcConnections)
cliques = list(nx.find_cliques(graph))

maxlen = max([len(network) for network in cliques])
maxCliques = [network for network in cliques if len(network) == maxlen]

# Output result
password = ""
for pc in sorted(maxCliques[0]):
    password = password+pc+","
password = password[:-1]
print(f"Password is: {password}")