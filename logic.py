#This is the lowest level logic of the computer
#It must be established that core axioms are required to establish a consistent logic flow
#The lowest level of abstraction I use is binary gates AND,OR,NOT. implemented with python, whilst everything going further is derived from these gates
#To Begin with a wire in this computer will be represented as binary bits. 1 indicating current flow and 0 indicating no current flow
#BUS: A collection of wires with 24 bits/24 wires and ordered using LSB(meaning we start ordering from the left not the right) indexing at 0
#WORD: This is a single bus and is the smallest unit of data storage and trasnport
#Memory will be arranged in groups of 3 bytes/24 bits and there will be a total of 2^16 memory addresses
#There is no accessing individual byte level or bit level data or sub dividing data inbetween smaller bytes


#Our axiom building blockscal
def AND(a,b):
    if a==1 and b==1:
        return 1
    else:
        return 0
    
def OR(a,b):
    if a==1 or b==1:
        return 1 
    else:
        return 0

def NOT(a):
    if a==1:
        return 0
    else:
        return 1
    
#additional gates (built using axiom gates)
def NAND(a,b):
    return NOT(AND(a,b))

def NOR(a,b):
    return NOT(OR(a,b))

def XOR(a,b):
    return(OR(AND(a,NOT(b)),AND(NOT(a),b) ))

def  XNOR(a,b):
    return(NOT(XOR(a,b)))