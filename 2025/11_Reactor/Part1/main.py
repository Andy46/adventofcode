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
def findNode(nodes : dict[Node], nodeTag):
    return nodes[nodeTag]

def findPathsDFS(nodes):
    initialNode = findNode(nodes, "you")
    finalNode = findNode(nodes, "out")
    initialPath = [initialNode]

    completePaths = []
    # print(initialNode)
    stack = [(initialNode, initialPath)]
    while stack:
        currentNode, currentPath = stack.pop()

        for nextNodeTag in currentNode.links:
            nextNode = nodes[nextNodeTag]
            if nextNode == finalNode: # Found a path from initial node to final node
                completedPath = currentPath.copy()
                completedPath.append(nextNode)
                completePaths.append(completedPath)

            if nextNode not in currentPath: # Avoid loops
                newPath = currentPath.copy()
                newPath.append(nextNode)
                stack.append((nextNode, newPath))
    return completePaths

# PUZZLE SOLVING
if __name__=="__main__":
    nodes = readData(filename)
    # printData(nodes)
    completePaths = findPathsDFS(nodes)
    printData(completePaths)
    print(f"Complete path count: {len(completePaths)}")
