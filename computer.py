from CPU import CPU
from memory import RAM
from conversion import to_bus,to_int

#this loads ram and a cpu, parsing in the ram into the cpu
main_ram = RAM()
main_cpu = CPU(main_ram)



#this takes in an opcode and operand and makes combines them into a single word
def Encode(opcode,operand):
    opcode = to_bus(opcode)
    operand = to_bus(operand)
    return opcode[0:5] + operand[0:19]

#this loads a program into ram
def loader(program):
    for address, instruction in enumerate(program):
        main_ram.write(to_bus(address),instruction)

#this takes an entire program and firsts encodes it into a word then loading it into memory starting from location 0
def assemble_load(program):
    pr = list()
    for instruction in program:
        pr.append(Encode(instruction[0],instruction[1]))
    loader(pr)

#This is my isa, it basically shows what instruction corresponds to and how to write a program
"""
0 HALT -> Stops the program
1 ADD -> it adds whatever is in register 1 and register 2 and puts them into the acc
2 SUB -> it subtracts whatever is in register 2 from register 1 (basically its reg1 - reg2) and then stores the result into the acc
3 PUSH -> (remember the stack pointer) this adds whatever contents is inside the acc (numerical value) into the current location where the stack pointer is
          and then moves the stackpointer down to the next memory address e.g(if 10 is in acc and the stackptr is on memory address 6000 then it adds the value 10 into memory address 6000 and then moves the stackptr to point at memory address 5999)
4 POP -> oposite of PUSH, it moves the stackptr up a memory address e.g(from memory location 5999 to 6000) and then returns the value at the location it moved to
5 CALL -> this stores the current memory address in the PC into the stackptr (essentially calling PUSH) and then jumps to the memory address specifiec by the operand by making the PC that memory address
6 RETURN -> opposite of CALL and it just calls the POP instruction to receive whatever memory address was put into the stack and then jumps back to it by setting the PC to that address
7 LOAD_R1 -> this loads whatever value from a memory address specified in the oparend into register 1
8 LOAD_R2 -> this loads whatever value from a memory address specified in the operand into register 2
9 LOAD_ACC -> this loads whatever value from a memory address specified in the operand into the acc
10 STORE_R1 -> this stores whatever value that is in register 1 into the memory address specified in the operand
11 STORE_R2 -> this stores whatever value that is in register 2 into the memory address specified in the operand
12 STORE_ACC -> this stores whatever value that is in the acc into the memory address specified in the operand
13 MOV_R1_ACC -> instruction that copies the contents of register 1 and loads them into the acc
14 MOV_R2_ACC -> instruction that copies the contents of register 2 and loads them into the acc
15 MOV_R1_R2 -> instruction that copies the contents of register 1 and loads them into register 2
16 AND -> this performs the bitwise AND operation by using the data in register 1 and register 2 and storing the resulting into the acc
17 OR -> this performs the bitwise OR operation by using the data in register 1 and register 2 and storing the resulting into the acc
18 NOT -> this performs the bitwise NOT operation by using the data in register 1 and storing the resulting into the acc
19 XOR -> this performs the bitwise XOR operation by using the data in register 1 and register 2 and storing the resulting into the acc
20 JMP -> this updates the PC to the operand, essentially jumping to a new memory address/instruction to be executed (essentially a loop)
21 JMP_IZ -> instruction that updates the PC to the operand if the contents in the acc is zero 
22 JMP_IN -> instruction that updates the PC to the operand if the contents in the acc is negative
23 EQ -> This instruction takes the content in register 1 and register 2 and determines if their equal it updates the acc as 1(true) or 0(false)
24 GT -> This instruction takes the content in register 1 and register 2 and determines if register 1 is greater than register 2 it updates the acc as 1(true) or 0(false)
25 GRS -> This instruction takes the content in register 1 and register 2 and determines if register 1 is strictly greater than register 2 it updates the acc as 1(true) or 0(false)
26 LS -> This instruction performs bitwise left shift on whatever value is inside the acc, it essentially multiplies a number by 2
31 NOP -> This instruction does nothing (good as a placeholder for pausing without stopping the program)
"""
#Now to create a program you must always specifiy and opcode and operend
#in the case in which an instruction does not require an operand just set it to 0 or any other placeholder BUT it is still compuslory
# e.g ADD requires no operand therefore it is just (1,0)
# But LOAD_R1 rquires the memory address like (7,1000) [which says load the contents in address 1000 into register 1]
#to create a program you just need to make a sequence of intstructions inside a list
# e.g [(7,1000),(8,1001),(1,0),(12,1002)] -> this says 1] load address 1000 into reg 1, 2] load address 1001 into reg 2, 3]ADD reg1 & reg2 4]store contents of acc(which is reg1+reg2) into address 1002
#finally after creating a program parse it into the assemble_load function and run the cpu

#this is just me manually initiallizing some values. memory location 1000 = 5, memory location 1001 = 1
main_ram.write(to_bus(1000),to_bus(12))
main_ram.write(to_bus(1001),to_bus(10))



#this program is a list of tuples, each tuple indicating an opcode and operand. making use of the isa table in cpu i can get the opcode
#then the operand just corresponds to what address in memory to fetch data ifff the instruction requires data
#instructions are read from left to right, and then the (0,0) is important to actually stop the cpu and not run forever
#finally i parse the program into the assemble load function so that it can load it into memory
program = [(7,1000),(8,1001),(1,0),(31,0),(0,0)]
assemble_load(program)


#this runs the cpu by calling the run() function and it starts executing instructions from memort address 0
main_cpu.run()

#This is the debug area
#since my current cpu/computer cant take in input or show output i have to use print statements on indidual registers or memory address
#this is to verify that the program ran as expected
print(to_int(main_cpu.reg1.read()))
print(to_int(main_cpu.reg2.read()))
print(to_int(main_cpu.acc.read()))
print(to_int(main_cpu.PC.read()))
