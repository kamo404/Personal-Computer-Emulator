Welcome to My own Computer Emulator

In this project my goal is build a computer from the ground up, ultimatelty i dont want to make any use of if statements or conventional python ways to control the flow
of code but instead use basic building blocks (lets call them axioms) that i can derive any other thing from

To ensure consistencies i need to allow myself basic functions to be able to mimick real hardware, which will be the follow:
1. list: in order to store binary bits and manipulate them as a whole
2. for loops: in order to work with binary bits as a whole (list) instead of manually manipulating one element at a time
3. functions: in order to demonstrate a certain components purpose being "used"
4. variables inside of functions to demonstrate wires that only persist as long as the function is alive (as long as the component is being used)
5. classes: For two reasons ->  to allow me to make components whereby data need to persists beyond a function call e.g latches and RAM and secondly grouping together components of similar functions to allow for abstraction

6. Now let me tell you more about my system:
7. -> i am building a cpu whereby each bus(collection of wires) is 24 bits, that represents our WORD
8. -> Due to python limitations i will be making memory of similar 24 bits but with only a total of 2^16 address
9. -> i will have instructions that occupy the first 5 bits of a bus

Now lets go through each layer:

1. Logic.py
   to begin with i created 3 seperate logic gates: AND,OR,and NOT. i implemented this using pythonic code but does will be the only exceptions
   This is shown as i derive the other basic logic gates NAND,NOT,XOR,and XNOR using the 3 basic gates

2. circuits.py
   This file houses the myriad of seperation combinational circuits that will be used in the making of a full cpu and computer system
   this file ranges from half adders, to full adders, each one having sufficient documention to understand and again derived from the previous layer of abstraction

3. memory.py
   This file houses the first use of classes. Due to the need of wanting persistent states throughout computations, it was a necessity.
   To begin with i create a simple SR-Latch, which houses a single bit. by controlling whether that bit is 1, or 0 using the inputs S(set) and R(reset)
   second of all i was able to create a WORD, which is (hopefully you remember) a collection of 24 bits, but in terms of memory is a collection of 24 SR Latches
   thus a WORD is initialized with 24 latches and seperate functions on being able to update the contents of the word and reading the contents of the word
   Finally using the two later sequential circuits i was able to construct RAM. In this system ram will consist of 65536 seprate words numbers from 0->65535
   RAM is rather interesting as now we can write by taking in an entire bus as input or read by returning an entire bus as output

4. PC.py
 This file houses the program counter (though i will admit i should have just placed in inside memory file for obvious reasons
 The program counter is a special type of WORD which stores the address(memory address) of the next instruction to be executed
 It comprises of important functions such as increment which allows us to move one address up and jump which allows us to move to an entirely different  address although

5. CPU.py
   This is the power house of everything, whereby finally things start coming together to form a functioning computer
   Firstly let us address a couple of important states our cpu must have, these are mainly just registers, reg1,reg2,the accumulator, the CIR (current instruction register) and its own copy of the PC.
   The main difference comes from the isa, note in the previous mention that i said the first 5 bits of an bus houses the instruction (unless its a data bus) now the isa maps each number of those 2^5 bits into its own instruction set. This consists of executions that the cpu can do, each of them build using their own callable function
   The CPU houses these instructions, each taking is the op (or operand) as an argument (mainly for consistency sake) so that instructions that require the operand (or memory address) to write, or read data can do so
   Finally arguably the most important part is the step function, which even though at first glance is simple is literally the entire workings of how a cpu runs. step does one iteration of the follow: Read whatever address is  inside the PC and place it into the CIR then increment the PC, Look at the CIR and extract the necessary data from the corresponding memory address, Decode the data into its opcode and operand, lookup the instruction that the opcode represents from the isa, then finally run.
   The way this cycle continues indefinetely is by the run function which checks if a super special boolean called the runnnig bool is still true, and the only way this boolean can become false is through the insruction 00000 --> HALT

6. computer.py
   This file takes everything together by initiallizing ram and cpu and parsing the ram into the cpu and finally creating a program loader which takes YOUR custom programs and places them inside memory starting from address 0. This is the main file that you need to pay attention to and other ones can be used for purely inspection purposes

7. assembler.py
   Most of the documentation has been added inside programming.txt insie the programs folder which explains in detail the assembler and its structure

Other honourable mentions is the testing file which currentlty serves no purpose other than to test certain aspect to ensure proper functioning and the conversion file which convert normal human integer numbers into a 24 bit bus and vice versa.

In conclusion this is my first attempt at a something complete project and i hope you enjoy making your own programs and i look forward to the feedback
