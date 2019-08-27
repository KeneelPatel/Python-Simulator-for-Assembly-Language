def disassemble(instructions, debugMode):
    PC = 0                          #keeps track of what line of of instrcution form the txt file is being run
    IC  = 0                            #kee[s track of instruction count and the program counter
    branch = 0                             # branch counter
    MI = 0                                 #memory instruction counter
    finished = False                        #is the program finished?https://www.onlinegdb.com/edit/r11FQ6ouN#debug_window_call_stack
    reg = [0]*24                            #declare register array all initialized to 0
    mem = [0]*55                    #memory from 0x2000 ot 0x2050
    fetch = instructions[PC]
    #for fetch in instructions:
    while(not finished):                #while condition to iterate the loop
        fetch = instructions[PC]
        #print(str(fetch[0:4]));
        if(str(fetch[0:4]) == "0100"):          #init
            if(str(fetch[4:8]) == "0000"):      #different input for init based on the user input from the file
                reg[0] = 251
                #print("init $0 {}".format(reg[0]))
            if(str(fetch[4:8]) == "0001"):
                reg[0] = 118
            if(str(fetch[4:8]) == "0010"):
                reg[0] = 79
            if(str(fetch[4:8]) == "0011"):
                reg[0] = 10
        elif(str(fetch[0:4]) == "0001"):        #store
            MI  = MI + 1
            Rx = int(fetch[4:8], 2)             #store instruction to store values into the memory
            mem[8 + Rx] = reg[0];
        elif((str(fetch[0:4]) == "1011")):    #storeword big number
            MI  = MI + 1
            if(str(fetch[4]) == "0"):           #storeword big number instruction to store number to specific memory
                                                #index such as 24 as well as 48
                mem[24] = reg[0]
            else:
                mem[48] = reg[0]
        elif(str(fetch[0:4]) == "0010"):        #drop and combine
            Rx = int(fetch[4:6],2)              #to drop middle 8 bits and to combine them together
            Ry = int(fetch[6:8],2)
            a = (int(reg[Rx], 2))
            b = (int(reg[Ry], 2))
            a = '{0:08b}'.format(a)
            b = '{0:08b}'.format(b)
            reg[0] = str(a[0:4]) + str(b[4:8])
            reg[0] = int(reg[0], 2)
            #print(reg[0])
            #finished  = True;
        elif(str(fetch[0:4]) == "0000"):        #square
            Rx = int(fetch[5:8], 2)             #to square the value stored at register
            square = reg[Rx] * reg[Rx]
            square = '{0:016b}'.format(square)
            # print("here - " + square)
            reg[1] = (square[0:8])
            reg[2] = (square[8:16])
        elif(str(fetch[0:4]) == "1010"):        #and
            Rx = int(fetch[4:6], 2)             #and operator to do the and operation
            Ry = int(fetch[6:8], 2)
            reg[Rx] = reg[Ry] & 1
        elif(str(fetch[0:4]) == "1100"):        #srl
            Rx = int(fetch[4:6], 2)             #srl to shift the number to the right by 1
            shift = 1
            reg[Rx] = reg[Rx] >> (shift)
        #elif(str(fetch[0:4] == "1111")):
        #    if(str(fetch[4:8] == "0000")):
        #        print("Hi")
        elif(str(fetch[0:4]) == "1110"):        #storehammingweight
            MI  = MI + 1
            Rx = int(fetch[4:8], 2)             #to store the hamming weight back to the memory
            mem[32 + Rx] = reg[3]
            reg[1] = 9 + Rx
        elif(str(fetch[0:4]) == "0011"):        #load
            MI  = MI + 1                        #to load value from the memory to the register
            Rx = int(fetch[4:6], 2)
            Ry = reg[int(fetch[6:8], 2)]
            reg[Rx] = mem[Ry]
        elif(str(fetch[0:4]) == "0101"):         #add
            Rx = int(fetch[4:6], 2)             #to add two registers
            Ry = int(fetch[6:8], 2)
            reg[Rx] = reg[Rx] + reg[Ry]
        elif(str(fetch[0:4]) == "1001"):        #add for the average 
            Rx = int(fetch[4:6], 2)             #special condition for the add to handle addition number greater than 255
            Ry = int(fetch[6:8], 2)
            if(reg[Rx] == 0):
                add = reg[Rx] + reg[Ry]
            else:
                add = int(reg[Rx],2) + (int(reg[3],2)) * 2**8 + reg[Ry]
            add = '{0:016b}'.format(add)
            reg[Rx] = add[8:16]
            reg[3] = add[0:8]
        elif(str(fetch[0:4]) == "0110"):         #addi
            Rx = int(fetch[4:6], 2)              #addi instruction to add immediate number to the register
            Ry = int(fetch[6:8], 2)
            reg[Rx] = reg[Rx] + Ry
        elif(str(fetch[0:4]) == "0111"):        #bne
            Rx = int(fetch[4:6], 2)             #branch not equal instruction to iterate the loop 
            branch = branch + 1
            IC = IC + 1
            if(str(fetch[6:8]) == "00"):
                if(reg[Rx] != 24):
                    PC = PC - 4
            if(str(fetch[6:8]) == "01"):
                if(reg[Rx] != 8):
                    PC = PC - 5
            if(str(fetch[6:8]) == "10"):
                if(reg[Rx] != 48):
                    PC = PC - 4
        elif(str(fetch[0:4]) == "1000"):        #average
            Rx = int(fetch[4:6], 2)             #average instruction to calculate the average number
            Ry = int(fetch[6:8], 2)
            if(str(fetch[0:8]) == "10000011"):
                reg[Rx] = int((int(reg[Rx],2) + int(reg[Ry], 2) * 2**8)/16)
            else:
                reg[Rx] = int(reg[Ry] / 16)
        elif(str(fetch[0:4]) == "1101"):        #set
            Rx = int(fetch[4:6], 2)             #set instruction to set values of the registers to particular value
            if(str(fetch[6:8]) == "00"):
                reg[Rx] = 0
            elif(str(fetch[6:8]) == "01"):
                reg[Rx] = 8
            elif(str(fetch[6:8]) == "10"):
                reg[Rx] = 32
            elif(str(fetch[6:8]) == "11"):
                reg[Rx] = 48
        elif(str(fetch[0:8] == "11111111")):    #to exit the program
            finished = True;
        PC =  PC + 1;
        IC = IC + 1
        #print("Done!!!!")
    x = 0
    print("==============Register Values=====================")     #printing out register values
    while(x < 8):
        print("reg[{}] = {}".format(x, reg[x]))
        x = x + 1
    y = 0
    print("==============Memory Values=======================")     #priting out memory output
    while(y < 49):
        print("mem[{}] = {}    mem[{}] = {}    mem[{}] = {}".format(y, mem[y], y + 1, mem[y+1], y+2, mem[y+2]))
        y = y + 3
    print("==============Genral Output=======================")     #printing out general output
    print("Instruction count(IC) : {}".format(IC))
    print("Program count(PC) : {}".format(PC))
    print("Branch instruction count : {}".format(branch))
    print("Memory instruction count : {}".format(MI))
    
        

def main():
    openFile = str(input("Enter the name of the file with the extention .txt : "))  #getting file name from the user
    inFile = open(openFile, "r")       #opens the file
    instructions = []                       #declares an array
    for line in inFile:
        if(line == "\n" or line[0] == '#'):
            continue
        line = line.replace('\n', '')
        # line = format(int(line, 16), "032b")    #formats tthe number as 32bits and uses 0 as filler
        instructions.append(line)
    inFile.close()
    debugMode = int(input("1: Debug Mode \n0: Normal Mode : "))
    disassemble(instructions, debugMode)        #function call 

main()