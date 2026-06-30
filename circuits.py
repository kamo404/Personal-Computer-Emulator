from logic import AND, OR, NOT, NAND, NOR, XOR, XNOR
from conversion import to_bus

#we begin with a half adder the output is a sum and carry out given by the following truth table
"""
A B SUM carry
0 0  0   0
0 1  1   0
1 0  1   0
1 1  0   1

SUM is simple XOR and carry is simple AND

"""
#returns : (sum,carry)
def Half_Add(a,b):
    return XOR(a,b), AND(a,b)

#this makes use of two full adders because it is important to note that both carrys never overlap
#important to note: since the variables i made do not persist outside the function and die immediately after use, they are wires and not memory 
#returns: (sum, carry)

def Full_ADD(a,b,cin):
    sum1, carry1 = Half_Add(a,b)
    sum2,carry2 = Half_Add(sum1,cin)
    return sum2, OR(carry1,carry2)

#This is the key distinction since we are adding entire busses
#remembering that a bus is 24 bits or 3 bytes.

def Bus_ADD(a,b):
    output_bus = list() #our 24 wires for the output of the result
    carry = 0 #initially there is no carry in the first arithmetic step
    for wire_a,wire_b in zip(a,b): #we iterate through each wire simulteously and add them 
        sum, carry = Full_ADD(wire_a,wire_b,carry)
        output_bus.append(sum)
    return output_bus

#this does subtraction (a-b) by making b a twos complement number
def BUS_SUBT(a,b):
    return Bus_ADD(a,two_com(b))

#turns every bit in the bus into the opposite value
def Bitwise_NOT(a):
    output_bus = list()
    for wire in a:
        output_bus.append(NOT(wire))
    return output_bus

#does an AND operation on each bit and returns the result as a bus
def Bitwise_AND(a,b):
    output_bus = list()
    for wire_a, wire_b in zip(a,b):
        output_bus.append(AND(wire_a,wire_b))
    return output_bus

#does an OR operation on each bit and returns the result as a bus
def Bitwise_OR(a,b):
    output_bus = list()
    for wire_a, wire_b in zip(a,b):
        output_bus.append(OR(wire_a,wire_b))
    return output_bus

#does an XOR operation on each bit and returns the result as a bus
def Bitwise_XOR(a,b):
    output_bus = list()
    for wire_a, wire_b in zip(a,b):
        output_bus.append(XOR(wire_a,wire_b))
    return output_bus


#This circuit checks if two numbers are the same
#we accomplish this by first determining whether each bit is the same, using XNOR. outputs 1 if both bits are either 0 or 1
#then we use an AND gate using the property 1^A=A to simplify the logic
#this returns a single bit either 1 (True) or 0 (False)
def Equality(a,b):
    inter_bus = list()
    logic = 1
    for wire_a,wire_b in zip(a,b):
        inter_bus.append(XNOR(wire_a,wire_b))
    for wire in inter_bus:
        logic = AND(logic,wire)
    return logic

#This is the oppisite of the equality circuit
def NotEquality(a,b):
    inter_bus = list()
    logic = 1
    for wire_a,wire_b in zip(a,b):
        inter_bus.append(XNOR(wire_a,wire_b))
    for wire in inter_bus:
        logic = AND(logic,wire)
    return NOT(logic)


#uses (bit_wise_not) to creating a two complementary of a number (it is a form of representing negative numbers in binary)
def two_com(a):
    num1 = to_bus(1)
    res_wire = Bitwise_NOT(a)
    return Bus_ADD(res_wire,num1)

#checks if the left number is  greater than or equal the right value e.g 5>4 is true because 5-4 = 1 --> 0001 --> 1000 therefore 0 = positive
def Check_GRTO(a,b):
    sum_wire = Bus_ADD(a,two_com(b))
    return NOT(sum_wire[23])

#checks if the left number is  less than or equal the right value, using the inverse logic of Check_GRTO
def Check_LSTO(a,b):
    return NOT(Check_GRTS(a,b))

#checks if the left number is strictly greater than the right value
def Check_GRTS(a,b):
    num0 =to_bus(0)
    sum_wire = Bus_ADD(a,two_com(b))
    return AND(NOT(sum_wire[23]),NotEquality(sum_wire,num0))

#opposite of CHECK_GRTS
def Check_LSTS(a,b):
    return Check_GRTS(b,a)


#This circuits displays the value of either wire a or b given the control (c=1 means check wire a. c=0 means check wire b)
def single_Multi(a,b,c):
    wire_ac = AND(a,c)
    wire_bc = AND(b,NOT(c))
    return OR (wire_ac,wire_bc)

#Takes in two buses as input and depending on the control displays either one
def Bus_Multi(a,b,c):
    output_wire = list()
    for wire_a,wire_b in zip(a,b):
        output_wire.append(single_Multi(wire_a,wire_b,c))
    return output_wire

#performs left shifting on the word level, which means every bit shifts to the right by one place (essentially multiplcation by 2 in binary)
def LS(a):
    return Bus_ADD(a,a)