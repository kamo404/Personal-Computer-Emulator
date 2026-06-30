import memory as mem
import conversion as conv
import PC as pc
import circuits as circ
import CPU as cpu

#welcome to the testing file. from here you can make use of anything you want. there is a couple of bits of data to use and have fun
#P.S up above is a few shortcut for file names that you can use
#here is the hierachy of the files so you know which one to use first conversion -> logic -> circuits -> -> memory -> PC -> CPU
#if you dont know what to do. give it to claude and let it have fun =


#testing data
A = [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #this is 5
B = [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #this is 3
C = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] #this is 16 777 215

D = 0
E = 1

ram = mem.RAM()
cpu = cpu.CPU(ram)
opcode = [1,0,1,0,0]
operand = [1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
print(cpu.Decode(A))