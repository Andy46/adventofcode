import copy
import click

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])
filename = f"{filepath}/00_example.data"
filename = f"{filepath}/00_test.data" 

# Read data
initialData = []
with open(filename, "r") as file:
    initialData = list(file.readline().strip())
diskMap = list(map(int,initialData))

# Helper functions
def resolveMap(diskMap):
    disk = []
    currentID = 0
    for index in range(len(diskMap)):
        if index % 2 == 0:
            newBlocks = [currentID] * diskMap[index]
            disk.extend(newBlocks)
            currentID = currentID + 1
        else:
            newBlocks = [None] * diskMap[index]
            disk.extend(newBlocks)
    return disk

def calculateChecksum(disk):
    disk = [0 if elem is None else elem for elem in disk]
    temp = list(zip(disk, range(len(disk))))
    checksum = sum([elem[0]*elem[1] for elem in temp])
    return checksum

#######################################
# Part 1 - Compress but fragment disk #
#######################################

# Helper functions for part 1
def compressDisk(disk):
    index = 0
    while index < len(disk):
        if disk[index] is None:
            disk[index] = disk[-1]
            disk = disk[:-1]
        while disk[-1] is None:
            disk = disk[:-1]
        index = index + 1
    return disk

originalDisk = resolveMap(diskMap)
compressedDisk = compressDisk(originalDisk.copy())
checksum = calculateChecksum(compressedDisk)
print(f"Fragmented disk checksum: {checksum}")

##################################################
# Part 2 - Compress disk with no defragmentation #
##################################################

# Helper functions for part 2
def findFiles(disk):
    files = []
    index = 0
    while index < len(disk):
        if disk[index] is None:
            index = index + 1
            continue
        startIndex = index
        index = index + 1
        while index < len(disk):
            if disk[index] == disk[index-1]:
                index = index + 1
            else:
                break
        endIndex = index
        fileSize = (endIndex - startIndex)
        files.append([startIndex, fileSize])
    return files

def findEmptySpaces(disk):
    spaces = []
    index = 0
    while index < len(disk):
        if None not in disk[index:]:
            break
        firstEmpty = index + disk[index:].index(None)
        index = firstEmpty
        while index < len(disk) and disk[index] is None:
            index = index + 1
        emptySpace = [firstEmpty, index - firstEmpty] # Position of empty space and size
        spaces.append(emptySpace)
    return spaces

def compressDisk(disk):
    files = findFiles(disk)
    files.reverse()
    spaces = findEmptySpaces(disk)
    
    with click.progressbar(files) as bar: # Progress bar
        for file in bar:
            # Find first empty space with enough space for file
            tempSpaces = copy.deepcopy(spaces)
            for space in tempSpaces:
                spaceIndex, spaceSize = space
                fileIndex, fileSize  = file
                if spaceIndex < fileIndex and spaceSize >= fileSize:
                    disk[spaceIndex:spaceIndex+fileSize] = disk[fileIndex:fileIndex+fileSize]
                    disk[fileIndex:fileIndex+fileSize] = [None] * fileSize
                    if spaceSize == fileSize:
                        spaces.remove(space)
                    else:
                        spaces[spaces.index(space)] = [spaceIndex+fileSize, spaceSize-fileSize]
                        spaces.append([fileIndex, fileSize])
                    break
    return disk

originalDisk = resolveMap(diskMap)
compressedDisk = compressDisk(originalDisk.copy())
checksum = calculateChecksum(compressedDisk)
print(f"Unfragmented disk {checksum}")
