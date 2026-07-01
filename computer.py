from CPU import CPU
from memory import RAM
from conversion import to_bus,to_int
from assembler import assemble

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

#this calls the assembler which loads the program "number_adder.txt"
program = assemble(main_ram)
assemble_load(program)


#this runs the cpu by calling the run() function and it starts executing instructions from memort address 0
main_cpu.run()
