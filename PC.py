import memory as mem

#this is the program counter, it controls the flow of the instruction(memory address) being executed
class PC():
    #creates a new 24 bit word/aka a memory address pointing to memory address 0
    def __init__(self):
        self.address = mem.WORD()
    #increments the memory address by 1
    def increment(self):
        self.address.update(mem.Bus_ADD(self.address.read(),mem.conv.to_bus(1)))
    #jumps from the current memory address to the one specificied
    def jump(self,bus):
        self.address.update(bus)
    #returns the current memory address it is holding
    def read(self):
        return self.address.read()
