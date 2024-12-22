#!/bin/python3

import copy
import click

# Files
import sys, os
filepath = os.path.dirname(sys.argv[0])

filename = f"{filepath}/00_test.data"
filename = f"{filepath}/00_example1.data"
filename = f"{filepath}/00_example2.data"

def getComboOperand(combo):
    if combo <= 3:
        return combo
    elif combo == 4:
        return Register_A
    elif combo == 5:
        return Register_B
    elif combo == 6:
        return Register_C
    else:
        return None

def adv(combo):
    global Register_A, Register_B, Register_C, ProgramCounter
    operand = getComboOperand(combo)
    Register_A = int(Register_A / pow(2, operand))
    ProgramCounter += 2
    
def bxl(operand):
    global Register_A, Register_B, Register_C, ProgramCounter
    Register_B = Register_B ^ operand
    ProgramCounter += 2

def bst(combo):
    global Register_A, Register_B, Register_C, ProgramCounter
    operand = getComboOperand(combo)
    Register_B = operand % 8
    ProgramCounter += 2

def jnz(literal):
    global Register_A, Register_B, Register_C, ProgramCounter
    operand = literal
    if Register_A == 0:
        ProgramCounter += 2
    else:
        ProgramCounter = operand   

def bxc(_):
    global Register_A, Register_B, Register_C, ProgramCounter
    Register_B = Register_B ^ Register_C
    ProgramCounter += 2

FIRST_OUT = True
def out(combo):
    global Register_A, Register_B, Register_C, ProgramCounter, FIRST_OUT
    operand = getComboOperand(combo)%8
    if not FIRST_OUT:
        print(',', end='')
    print(operand, end='')
    FIRST_OUT = False
    ProgramCounter += 2

def bdv(combo):
    global Register_A, Register_B, Register_C, ProgramCounter
    operand = getComboOperand(combo)
    Register_B = int(Register_A / pow(2, operand))
    ProgramCounter += 2

def cdv(combo):
    global Register_A, Register_B, Register_C, ProgramCounter
    operand = getComboOperand(combo)
    Register_C = int(Register_A / pow(2, operand))
    ProgramCounter += 2


commands = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]


ProgramCounter = 0
Register_A = 47006051
Register_B = 0
Register_C = 0
Program    = "2,4,1,3,7,5,1,5,0,3,4,3,5,5,3,0"
Program    = [int(item) for item in Program.split(',') if item is not None] 

print("Output: ", end='')
while ProgramCounter < len(Program):
    operation = commands[Program[ProgramCounter]]
    cmbop  = Program[ProgramCounter+1]
    operation(cmbop)
print("")
print(f"Register_A: {Register_A}")
print(f"Register_B: {Register_B}")
print(f"Register_C: {Register_C}")