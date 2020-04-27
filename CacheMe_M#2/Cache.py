import random
import string
import math
import re


# Class for Cache: 
class Cache:
    def __init__(self, cacheSize, blockSize, associativity, r_policy, traceFile):
        self.cacheSize = cacheSize
        self.blockSize = blockSize
        self.associativity = associativity
        self.r_policy = r_policy
        self.traceFile = traceFile
        # Calculate Cache:
        self.numberOfBlocks = (((cacheSize * 1024) / blockSize) / 1024) # Blocks in Bits
        self.totalBlocks = ((cacheSize * 1024) / blockSize)
        self.indexSize = int(math.log((self.numberOfBlocks * 1024 // associativity), 2))
        self.offsetSize = math.log(blockSize, 2)
        self.tagSize = int(32 - self.indexSize - self.offsetSize)
        self.numberOfIndices = (2 ** self.indexSize)
        self.calculatedIndicesKB = self.numberOfIndices / 1024
        self.totalRows = (2 ** self.indexSize) / 1024
        self.rows = int(self.totalRows * 1024)
        self.overheadMemory = ((self.tagSize + 1) * associativity * self.numberOfIndices) / 8
        self.mem = (self.overheadMemory) + (cacheSize * 1024)
        self.memKB = self.mem / 1024
        self.cost = (float(self.mem)/1024) * 0.05
        self.hitRate = 0
        self.compMisses=0
        self.missRate = 0;
        self.total_cycles = 0
        self.total_instructions = 0
        self.cacheMisses = 0
        self.unusedKB = ( (self.totalBlocks-self.compMisses) * (self.blockSize+self.overheadMemory) / 1024 )
        self.waste = (self.cost/self.cacheSize) * self.unusedKB
        self.cachAccesses = 0
        self.cacheHits = 0
        self.cacheMisses = 0
        self.confMisses = 0
        self.sizeS = 0
    indexList = []
    

    # Calculate Space for Address:
    def calAdd(self, address, tagBits, indexBits, blockOffsetBits):
        binaryAdd = bin(int(address, 16))[2:].zfill(32)
        binaryBlockOffset = binaryAdd[(32 - blockOffsetBits):]
        binaryIndex = binaryAdd[(32 - blockOffsetBits - indexBits):(32 - blockOffsetBits)]
        binaryTag = binaryAdd[:(tagBits)]
        # Convert offset into an Int
        blockOffset= str(int(binaryBlockOffset, 2))
        index = int(binaryIndex, 2)
        tag = str(hex(int(binaryTag, 2)))
        result = {'tag': tag, 'index': index, 'blockOffset': blockOffset}
        return result
    

    # Add to Address Space:
    def inAdd(self, address_space, bytesRead):
        self.cachAccesses += 1
        indexList = self.indexList
        blockSize = self.blockSize
        cacheHit = False
        # Return Rows to Read
        offset = address_space['blockOffset']
        indexExtra = int((int(offset) + bytesRead) / blockSize)
        if((int(offset) + bytesRead % blockSize) != 0):
            indexExtra += 1

        # Check Rows:
        for extra in range(0, indexExtra):
            indexSelected = extra + address_space['index']
            if (indexSelected + 1) >= self.rows:
                indexSelected = indexSelected - self.rows
            
            # Check Block on this Row:
            for blockCache in indexList[indexSelected]:
                if blockCache.tag == address_space['tag']:
                    cacheHit = True
                    self.total_cycles += 1
            
            # Check if Tags Match:
            if (cacheHit == False):
                emptyBlock = False
                self.cacheMisses += 1
                self.total_cycles += (3 * int(blockSize / 4))
                # Check for usable block, replace:
                for blockCache in indexList[address_space['index']]:
                    if(blockCache.valid == 0):
                        self.compMisses += 1
                        blockCache.valid = 1
                        emptyBlock = True
                        break

                # Check Replacement Policy:
                if emptyBlock == False:
                    if(self.r_policy == "RR"):
                        starting = True
                        count = 0
                        for blockCache in indexList[indexSelected]:
                            if blockCache.next == True:
                                blockCache.tag = address_space['tag']
                                blockCache.next = False
                                starting = False
                                # Check Next Block:
                                if (count + 1) < self.associativity:
                                    indexList[indexSelected][(count + 1)].next = True
                                else:
                                    indexList[indexSelected][0].next = True
                            count += 1
                        if(starting == True):
                            indexList[indexSelected][0].next = True
                    elif(self.r_policy == "RND"):
                        randomize = random.randrange(0,self.associativity)
                        indexList[indexSelected][randomize].tag = address_space['tag']

    
    def setRates(self):
        self.missRate = float(self.cache_miss_count/self.total_cycles)
        self.hitRate = (1 - self.missRate) * 100
        self.cacheHits = self.cachAccesses - self.cache_miss_count

    # Cache Simulation to be called with in Sim.py:
    def cacheMe(self):
        tagSize = self.tagSize
        indexSize = self.indexSize
        traceFile = self.traceFile 
        cacheList = []  

        # Represents tables of cache considering Cache Assiciativity: 
        for index in range(int(self.rows)):
            blockList = []
            for block in range(self.associativity):
                blockList.append(Block(0, "0", 0))
            self.indexList.append(blockList)

        # Validate Existance and Open Trace File for Reading:
        file = open(traceFile, 'r')
        if not file:
            print("ERROR: '%s' FAILED TO READ FILE", file)
            exit(1)

        # Start
        new_block = True
        empty = '0x00000000'
        for line in file:
            # [*NOTE] - These expressions seem to santize lines one and two but hard to work with as is:
            # info = re.match(r'^.+\((\d{2})\).\s(.{8}).+$', line)
            # read_write = re.match(r'^.+:\s(\w{8}).*:\s(\w{8}).*$', line)
            if line == '\n':
                new_block = True
                continue
            # [*NOTE] - These tokens split up the lines in to groups but fails to santize the data:
            tokens = line.split() 
   
            # Get Length and Address from first line:
            if new_block:
                bytes_read = int(tokens[1][1:3])
                address = str(tokens[2])
                new_block = False

		# Calculate Address:
                address_space = self.calAdd(address, int(tagSize), int(indexSize), int(self.offsetSize))
                self.inAdd(address_space, bytes_read)
                self.total_cycles += 2
                self.total_instructions += 1
            
            else:
                writeAdd = hex(int(tokens[1], 16))
                readAdd = hex(int(tokens[4], 16))
		# if info:
                # address = '0x' + info.group(2)
                # length = int(info.group(1))
                # cache_list.append(address + ',' + str(length))
            	# if read_write:
                # write_address = '0x' + str(read_write.group(1))
                # read_address = '0x' + str(read_write.group(2))
            	# writeAdd = '0x' + str(read_write.group(1))
		# [*NOTE] - Orignially these are checking with 
                if (int(writeAdd,16) != 0):
                    address_space = self.calAdd(str(tokens[1]), int(tagSize), int(indexSize), int(self.offsetSize))
			        self.inAdd(address_space, 4)
			        self.total_cycles += 2
                if (int(readAdd, 16) != 0):
                    address_space = self.calAdd(str(tokens[4]), int(tagSize), int(indexSize), int(self.offsetSize))
			        self.inAdd(address_space, 4)
			        # Add to CPI
			        self.total_cycles += 2
                        
        self.unusedKB = ((self.totalBlocks-self.compMisses) * (self.blockSize+self.overheadMemory) / 1024 )
        self.setRates()

# Class Block:
class Block:
    def __init__(self, valid, tag, next):
        self.tag = tag
        self.valid = valid
        self.next = next
