
#This takes a number and converts it into a 24 bit binary number
#e.g 7 is usually 000...0111 in binary but due to python lists it will be 1110...000
def to_bus(n):
    bus = list()
    while n > 1:
        bus.append(n%2)
        n = n//2
    bus.append(n)
    while len(bus) < 24:
        bus.append(0)
    if len(bus) >= 25:
        raise ValueError
    return bus
#this takes a 24 bit bus/aka a WORD and turns it into a number
def to_int(bus):
    total = 0
    for num,bit in enumerate(bus):
        total += bit*(2**num)
    return total