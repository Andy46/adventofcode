# Files
import sys, os
import math
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/example.data"
filename = f"{filepath}/test.data"

# Step 1 Calculate distances
# Step 2 Get smallest distances per box pair
# Step 3 Order pairs by smallest distances
# Step 4 Connect non connected boxes

def readData(filename : str) -> list[tuple]:
    with open(filename, "r") as file:
        text = [line.strip() for line in file.readlines()]
        boxes = [tuple(map(int, item.split(','))) for item in text]
        # items = [item.split(',') for item in text]
        # castMatrix(boxes, int)
        return boxes
    
def printData(data : list[any]) -> None:
    for item in data:
        print(item)

# AUX FUNCTIONS
def calcDistance3D(boxA, boxB):
    # distX=abs(boxB[0]-boxA[0])
    # distY=abs(boxB[1]-boxA[1])
    # distZ=abs(boxB[2]-boxA[2])
    # dist3D=math.sqrt((distX*distX)+(distY*distY)+(distZ*distZ))
    dist3D = math.sqrt(sum([abs((a-b)*(a-b)) for a,b in zip(boxA, boxB)]))
    return dist3D

class Distance:
    def __init__(self, boxA, boxB):
        self.boxA = min(boxA, boxB)
        self.boxB = max(boxA, boxB)
        self.dist = calcDistance3D(self.boxA, self.boxB)

    def __hash__(self):
        return (self.boxA, self.boxB, self.dist).__hash__()
    
    def __str__(self):
        return f"{self.boxA} - {self.boxB} : {self.dist}"

def calcAllDistances(boxes : list[tuple]) -> list[list[float]]:
    distances = set()
    for a, boxA in enumerate(boxes):
        for b, boxB in enumerate(boxes[a+1:]):
            distances.add(Distance(boxA, boxB))

    sortedDistances = sorted(distances, key=lambda x: x.dist)

    return sortedDistances

def sortDistances(distances):
    return sorted(distances, key=lambda x:x.getDistance())

def makeConnections(distances : list[Distance], count):
    circuits = []
    for i in range(count):
        dist = distances[i]
        circuitA = None
        circuitB = None
        # Find boxes in circuits
        for circuit in circuits:
            if dist.boxA in circuit:
                circuitA = circuit
            if dist.boxB in circuit:
                circuitB = circuit
            if circuitA is not None and circuitB is not None:
                break

        if circuitA is None and circuitB is None:
            newCircuit = set()
            newCircuit.add(dist.boxA)
            newCircuit.add(dist.boxB)
            circuits.append(newCircuit)
        elif circuitA is None:
            circuitB.add(dist.boxA)
        elif circuitB is None:
            circuitA.add(dist.boxB)
        elif circuitA != circuitB:
            circuitA.update(circuitB)
            circuits.remove(circuitB)

    return circuits

# PUZZLE SOLVING
if __name__=="__main__":
    boxes = readData(filename)
    # printData(boxes)
    distances = calcAllDistances(boxes)
    # printData(distances)
    circuits = makeConnections(distances, 1000)
    # printData(circuits)
    orderedCircuits = sorted(circuits, key=lambda x:len(x), reverse=True)
    # printData(orderedCircuits)

    import math
    total = math.prod([len(circuit) for circuit in orderedCircuits[:3]])

    print(f"Total circuit operations: {total}")  
    
