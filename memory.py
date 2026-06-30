from circuits import *
import conversion as conv


#Most Basic sequential circuit to be able to make memory, uses S for set and R for Reset to update state of the latch
class SRLATCH():
    #initiliazes a single SR latch to default to 0
    def __init__(self):
        self.Q = 0
    #this updates the value of the SR Latch(Q) depending on the configuration of S and R
    #S = 1 and R = 0 sets the bit to 1 whislt S = 0 and R = 1 sets the bit to 0
    def update(self,S,R):
        self.Q = OR(AND(self.Q,NOT(R)),AND(NOT(R),S))
    #this reads the value stored inside the latch
    def read(self):
        return self.Q
    

#This is a word(memory of 24 SR Latches) which enables updating entire word of memory and reading entire words of memory
class WORD():

    #this creates 24 latches at once and stores them in a list
    def __init__(self):
        self.latches = [SRLATCH() for _ in range(24)]

    #this takes in a bus and goes through each value and puts it inside the corresponding latches
    #if the value at that bit is 1 then it will make S=1 and R=0 else a bit value of 0 corresponds to S=0 and R=1
    def update(self,bus):
        for latch,bit in zip(self.latches,bus):
            latch.update(bit,NOT(bit))
    #this reads the entire value of the 24 bit SR latch
    def read(self):
        return [latch.read() for latch in self.latches]


#This creates a whole module of RAM which consists of 2^16 seperate word level addresses
class RAM():

    #initializes 2^16 words into a list
    def __init__(self):
        self.words = [WORD() for _ in range(65536)]

    #this converts a word address into an integer so that it can be used as an index then we update that word with the bus
    def write(self,address,bus):
        address = conv.to_int(address)
        self.words[address].update(bus)
    
    #outputs the result of a specific address
    def read(self,address):
        address = conv.to_int(address)
        return self.words[address].read()