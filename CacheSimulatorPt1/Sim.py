#!/usr/bin/env python3
#
#
# Anthony Castro
#
import sys
import re
def power(x):
    i = 0
    while x != 1 and x >= 1:
        i += 1
        x /= 2
    return i
count = 0

if (len(sys.argv)-1)==10:
    for arg in sys.argv[1::2]:
        # Checks Arguments: -f -s -b -a -r
        if "f" in arg:
            fileName=sys.argv[2]
            try:
                with open(fileName,'r') as inputFile:
                    for line in inputFile:
                        if line=="\n":
                            line = re.sub(r'\n',"","");
                        else:
                            rLine=0
                            tok0 = line.split();
                            length = re.sub(r'\D',"",tok0[1])
                            address = tok0[2]
                            tok1 = inputFile.readline().split()
                            rLine = 1

                            dstM = tok1[1]
                            srcM = tok1[4]
                        
                            destPath = 1
                            srcPath = 1

                            if int(dstM, 16) == 0 and rLine == 1:
                                destPath = 0
                            if int(srcM, 16) == 0 and rLine == 1:
                                srcPath = 0
                       
                            if destPath == 0 and srcPath == 0:
                                print("Address: 0x"+address+": (00"+length+")")
                            else: 
                                print("Address: 0x"+address+": (00"+length+")")
                        count += 1
                        if count > 43:
                            break
            except IOError:
                print("Error opening file: " + sys.argv[2] + ".")
                sys.exit(1)
        # s - Cache Size
        elif 's' in arg:
            cacheSize = sys.argv[4]
        # b - Block Size
        elif 'b' in arg:
            blockSize = sys.argv[6]
        # a - Associativity
        elif 'a' in arg:
            associativity = sys.argv[8]
        # r - Replacement Policy
        elif 'r' in arg:
            if sys.argv[10] == "RR":
                replacementPolicy = "Round Robin"
            elif sys.argv[10] == "RND":
                replacementPolicy = "Random"
            elif sys.argv[10] == "LRU":
                replacementPolicy = "Least Recently Used"
            else:
                print("Error: " + sys.argv[10] + " is not a valid replacement type.\nUse either RR, RND, or LRU.")
                sys.exit(1)
            
    totalAddressSpace = 32
    k = power(int(cacheSize)) + 10
    j = power(int(blockSize))
    blocksIn2 = (k - j) 
    blocksIn2b = blocksIn2 - 10
    numBlocksKB = 2**blocksIn2b
    numRows = (int(cacheSize)/(int(blockSize)*int(associativity))) * 1024
    ajInBits = (j + power(int(associativity))) 
    index = (k - ajInBits)
    totalIndicies = 2**(index - 10)
    tagBits = totalAddressSpace - (j + index)
    overHead = ((tagBits + 1) * (2**blocksIn2))/8
    oHcS = overHead + (2**k)
    cost = (float(oHcS)/1024) * .05
       
    # Print Header
    print("\nCache Simulator - CS 3853 - Team #18")
    print("")
    print("Trace File: ", fileName)
    #print("Cmd Line:", " ".join(sys.argv))
    print("\n***** Cache Input Parameters *****")
    print("\nCache Size: ", cacheSize, "KB")
    print("Block Size: ", blockSize, "bytes")
    print("Associativity: ", associativity)
    print("R-Policy:", replacementPolicy)
    print("")
    print("***** Cache Calculated Values ***** ")
    print("\nTotal #Blocks: {} KB (2^{})".format(numBlocksKB, blocksIn2))
    print("Tag Size: {} bits".format(tagBits))
    #print("Index Size: {} bits, Total Indices: {} KB".format(index, totalIndicies))
    print("Index Size: {} bits".format(index))
    print("Total # Rows: {}".format(int(numRows)))
    print("Overhead Size: {:,} bytes".format(int(overHead)))
    print("Implementation Memory Size: {:,} bytes".format(int(oHcS)))
    print("Cost: $%.2f" % cost)
    #print("")
    #print("----- Results -----")
    #print("Cache Hit Rate: {}%".format(96.2))
    #print("CPI: ")
    #print("Cost: ")
    #print("Unused Cache Space: ")

else:
    print("Too many or too little arguements!")
    sys.exit(1)
