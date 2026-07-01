from memory import RAM
from conversion import to_bus,to_int

def assemble(ram: RAM = None):
    lines = list()
    #this opens the file and extracts each line in a list (skipping blank lines)
    with open("programs/number_adder.txt","r") as file:
        for line in file:
            if line.strip():
                lines.append(line)

    #this goes through each line and strips any trailing or leading whitespaces
    for i in range(len(lines)):
        lines[i] = lines[i].strip()


    label_tbl = dict() #dictionary for labels and variables
    new_file = list() #this is to store remaining non variable label instructions
    curr_vars = list() #to store current variable labels for later storage

    #goes through each line and places variables in a custom list with their name and their value for later storage into proper memory
    for line in lines:
        word = list()
        if ".data" in line:
            curr_vars.append(line[6:].split())
        else:
            new_file.append(line)

    #creates the jump dictionary map, whereby each LABEL corresponds to the position at which they call
    counter = 0     
    for line in new_file:
        if ":" in line:
            label_tbl[line[0:]] = counter
        else:
            counter += 1

    #after proccesing the total number of lines in the programs it then loads the variable labels into ram at addresses after the literal program 
    temp_counter = counter
    for var in curr_vars:
        ram.write(to_bus(temp_counter),to_bus(int(var[1])))
        temp_counter += 1

    #this piece now loads the variable labels into the dictionary lookup
    for var in curr_vars:
        label_tbl[var[0]] = counter
        counter += 1

    #ISA instruction set that will be used to encode into binary 
    isa = { "HALT": 0,
            "ADD": 1,
            "SUB": 2,
            "PUSH": 3,
            "POP": 4,
            "CALL": 5,
            "RETR": 6,
            "LOAD_R1": 7,
            "LOAD_R2": 8,
            "LOAD_ACC": 9,
            "STORE_R1": 10,
            "STORE_R2": 11,
            "STORE_ACC": 12,
            "MOVE_R1_ACC": 13,
            "MOVE_R2_ACC": 14,
            "MOVE_R1_R2": 15,
            "AND": 16,
            "OR": 17,
            "NOT": 18,
            "XOR": 19,
            "JMP": 20,
            "JMP_IZ": 21,
            "JMP_IN": 22,
            "EQ": 23,
            "GT": 24,
            "GTS": 25,
            "LSHIFT": 26,
            "OUT": 27,
            "IN": 28,
            "NOP": 31}
    
    #breaks down code into its opcode and operand and formes a set of numeric instructions for it
    instruct = list()
    temp = list()
    for line in new_file:
        if ":" not in line:
            temp = line.split()
            opcode = isa[temp[0]]
            if len(temp) == 1:
                instruct.append([opcode,0])
            else:
                if temp[1] in label_tbl:
                    operand = label_tbl[temp[1]]
                    instruct.append([opcode,operand])
                else:
                    operand = int(temp[1])
                    instruct.append([opcode,operand])
            temp = list()
    return instruct
