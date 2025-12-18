# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/example.data"
filename = f"{filepath}/test.data"

class Node:
    def __init__(self, tag, links):
        self.tag = tag
        self.links = links

    def __str__(self):
        return f"{self.tag} -> {self.links}"

# DATA PARSING
def readData(filename : str) -> list[list[int]]:
    with open(filename, "r") as file:
        text = [line.strip() for line in file.readlines()]
        nodeList = {}
        for line in text:
            tag = line.split(':')[0]
            links = (line.split(':')[1]).strip().split()
            nodeList[tag] = Node(tag, links)
        nodeList["out"] = Node("out", []) # Add final node
        return nodeList
    
def printData(data : any) -> None:
    if isinstance(data, dict):
        for key in data.keys():
            print(f"{key} - {data[key]}")        
    else:
        for item in data:
            print(item)

# AUX FUNCTIONS
def findNode(nodes : dict[Node], nodeTag : str) -> Node:
    return nodes[nodeTag]

memory = {}

def countPathsDFS(nodes : dict[Node], startNodeTag : str, finalNodeTag : str, fft : bool, dac : bool):
    currentNode = findNode(nodes, startNodeTag)
    # finalNode = findNode(nodes, finalNodeTag)

    paths = 0
    for link in currentNode.links:
        visitedFFT = fft or (startNodeTag == "fft")
        visitedDAC = dac or (startNodeTag == "dac")
        if link == finalNodeTag: # Reached final node
            if visitedFFT and visitedDAC:
                paths = paths + 1
        elif (link, visitedFFT, visitedDAC) in memory.keys(): # Check memory
            paths = paths + memory[(link, visitedFFT, visitedDAC)]
        else: # Continue running paths
            paths = paths + countPathsDFS(nodes, link, finalNodeTag, visitedFFT, visitedDAC)
    memory[(startNodeTag, visitedFFT, visitedDAC)] = paths
    return paths
            
# PUZZLE SOLVING
if __name__=="__main__":
    nodes = readData(filename)
    # printData(nodes)
    completePathCount = countPathsDFS(nodes, "svr", "out", False, False)
    # completePaths = findPathsDFS(nodes, "fft", "dac")
    # completePaths = findPathsDFS(nodes, "dac", "fft") # 0 routes
    print(f"Complete path count: {completePathCount}")
