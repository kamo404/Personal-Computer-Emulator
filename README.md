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
   Finally using the two later sequential circuits i was able to construct RAM. In this system ram will consist of 65
