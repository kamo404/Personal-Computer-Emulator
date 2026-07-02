from PC import PC
from memory import WORD,RAM
import circuits as circ
from conversion import to_bus,to_int


#This is where i put everything together to make a functioning CPU using the fetch execute cycle
class CPU():

    def __init__(self,ram: RAM):
        self.running = True #This is a very important boolean, it determines whether a program is running or not
        self.CIR = WORD() #Current instruction register: stores the memory address of the current instruction being executed 
        self.PC = PC() #program counter
        self.acc = WORD() #This is the accumulator: it stores arithmetic results at each step
        self.reg1 = WORD() #this is register 1, just holds a word amount of data 24 bits
        self.reg2 = WORD() #this is register 2, another holder
        self.ram = ram #this takes in the RAM from the memory we made as an argument
        self.stackptr = WORD() #this is a stackpointer, it holds the memory address of where the stack pointer currently is
        self.stackptr.update(to_bus(65535)) # this just updates the stack pointer to initailize at the last memory address
        #This is my isa, it holds a dictionary of all the operations that my cpu can execute, different combinations of operations can create entire systens
        self.isa = {0: self.halt,
                    1: self.add,
                    2: self.sub,
                    3: self.push,
                    4: self.pop,
                    5: self.call,
                    6: self.retr,
                    7: self.load_r1,
                    8: self.load_r2,
                    9: self.load_acc,
                    10: self.store_r1,
                    11: self.store_r2,
                    12: self.store_acc,
                    13: self.move_r1_acc,
                    14: self.move_r2_acc,
                    15: self.move_r1_r2,
                    16: self.AND,
                    17: self.OR,
                    18: self.NOT,
                    19: self.XOR,
                    20: self.jmp,
                    21: self.jmp_iz,
                    22: self.jmp_in,
                    23: self.eq,
                    24: self.gt,
                    25: self.gts,
                    26: self.lshift,
                    27: self.Out,
                    28: self.In,
                    31: self.nop}
    
    #breaks up a word into its opcode and its operand
    def Decode(self,bus):
        return bus[0:5], bus[5:24]
    
    #sets running to false so that the program will stop
    def halt(self,op):
        self.running = False

    #function that adds contents of register 1 and 2 into the accumulator
    def add(self,op):
        self.acc.update(circ.Bus_ADD(self.reg1.read(),self.reg2.read()))

    #function that subtracts contents of register 1 and 2 into the accumulator (position matters)
    def sub(self,op):
        self.acc.update(circ.BUS_SUBT(self.reg1.read(),self.reg2.read()))

    #this function takes in a bus/WORD and puts it into where the stackpointer is currently pointing to and then moves down to another memory address
    def push(self,op):
        self.ram.write(self.stackptr.read(),op)
        self.stackptr.update(circ.BUS_SUBT(self.stackptr.read(),to_bus(1)))

    #this function moves the pointer up by one memory address and displays the value at that address
    def pop(self,op):
        self.stackptr.update(circ.Bus_ADD(self.stackptr.read(),to_bus(1)))
        self.acc.update(self.ram.read(self.stackptr.read()))
    
    #sets the pc to whatever the operand was/essentially "goes" to a specific memory address
    def jmp(self,op):
        self.PC.jump(op)

    def jmp_iz(self,op):
        if circ.Equality(self.acc.read(), to_bus(0)):
            self.jmp(op)

    def jmp_in(self,op):
        if circ.Check_LSTS(self.acc.read(),to_bus(0)):
            self.jmp(op)

    #this adds the current PC into the stack and then jumps to the operand memory adress
    def call(self,op):
        self.push(self.PC.read())
        self.jmp(op)
    
    #this jumps to the memory address that was in the stack
    def retr(self,op):
        self.pop(op)
        self.jmp(self.acc.read())

    def load_r1(self, op):
        self.reg1.update(self.ram.read(op))
    
    def load_r2(self, op):
        self.reg2.update(self.ram.read(op))

    def load_acc(self, op):
        self.acc.update(self.ram.read(op))

    def store_r1(self,op):
        self.ram.write(op,self.reg1.read())

    def store_r2(self,op):
        self.ram.write(op,self.reg2.read())       

    def store_acc(self,op):
        self.ram.write(op,self.acc.read()) 

    def move_r1_acc(self,op):
        self.acc.update(self.reg1.read())

    def move_r2_acc(self,op):
        self.acc.update(self.reg2.read())

    def move_r1_r2(self,op):
        self.reg2.update(self.reg1.read())

    def AND(self,op):
        self.acc.update(circ.Bitwise_AND(self.reg1.read(),self.reg2.read()))

    def OR(self,op):
        self.acc.update(circ.Bitwise_OR(self.reg1.read(),self.reg2.read()))

    def XOR(self,op):
        self.acc.update(circ.Bitwise_XOR(self.reg1.read(),self.reg2.read()))

    def NOT(self,op):
        self.acc.update(circ.Bitwise_NOT(self.reg1.read()))

    def eq(self,op):
        self.acc.update(to_bus(circ.Equality(self.reg1.read(),self.reg2.read())))

    def gt(self,op):
        self.acc.update(to_bus(circ.Check_GRTO(self.reg1.read(),self.reg2.read())))
    
    def gts(self,op):
        self.acc.update(to_bus(circ.Check_GRTS(self.reg1.read(),self.reg2.read())))

    def lshift(self,op):
        self.acc.update(circ.LS(self.reg1.read()))

    def nop(self,op):
        pass

    def In(self,op):
        self.acc.update(to_bus(int(input())))
        
    def Out(self,op):
        print(to_int(self.acc.read()))


    #this executes the fetch ececute cycle once
    def step(self):
        #Fetch cycle. read from ram (according to pc) and load it into CIR, increment pc
        self.CIR.update(self.ram.read(self.PC.read()))
        self.PC.increment()

        #decode cycle, splits instruction inside cir into opcode and operand
        opcode, operand = self.Decode(self.CIR.read())
        operand = to_bus(to_int(operand))

        #execute stage. look up opcode in isa and input corresponding operand
        self.isa[to_int(opcode)](operand)

    #this will run indefinetely unless running is set to false,which can only happen when a program comes upon a HALT
    def run(self):
        while self.running:
            self.step()