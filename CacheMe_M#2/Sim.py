import sys
import argparse
import math
import Cache
from Cache import Block
# Check Arguments:

if len(sys.argv)!=11:
    print("USAGE: " + sys.argv[0] + " -f <trace file> -s <cache size KB> -b <block size> -a <associativity> -r <replacement policy>")
    sys.exit(1)
 
# Start Parsing:
parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, action='store', dest="Trace_File")
parser.add_argument('-s', type=int, action='store', dest="Cache_Size")
parser.add_argument('-b', type=int, action='store', dest="Block_Size")
parser.add_argument('-a', type=int, action='store', dest="Associativity")
parser.add_argument('-r', type=str, action='store', dest="R_Policy")
 
# Save Arguments:
results = parser.parse_args()
# Define Tables
associativity = [1, 2, 4, 8, 16]
replace_policy = ["RR", "RND", "LRU"]

# Check Arguments:
if (results.Cache_Size < 1) or (results.Cache_Size > 8192):
    print("ERROR: Cache Size Less than 1KB or More Than 8MB")
    sys.exit(1)
if (results.Block_Size < 4) or (results.Block_Size > 64):
    print("ERROR: Block Size is Less Than 4 Bytes, or Greater Than 64 Bytes")
    sys.exit(1)
if not (results.Associativity in associativity):
    print("ERROR: Associativity Usage - 1, 2, 4, 8, 16")
    sys.exit(1)
if not (results.R_Policy in replace_policy):
    print("ERROR: Replacement Policy - RR, LRU, RND:")
    sys.exit(1)

#Cache Constructor filled with given parameters
myCache = Cache.Cache(results.Cache_Size,results.Block_Size,results.Associativity,results.R_Policy,results.Trace_File)
 
# Read Trace File: 
traceFile = open(results.Trace_File, "r")
if not traceFile:
    print("ERROR: Cannot open or find Trace File")
    sys.exit(1)
    

#calculating Cache
myCache.cacheMe()
# Display Header:
print("")
print("Cache Sumulator CS 3853 Spring 2020 - Group #18")
print("Trace File: " + str(myCache.traceFile))
print("")
print("***** Cache Input Parameters *****")
print("Cache Size: \t\t\t" + str(myCache.cacheSize) + " KB")
print("Block Size: \t\t\t" + str(myCache.blockSize) + " bytes")
print("Associativity: \t\t\t" + str(myCache.associativity))
print("Replacement Policy: \t\t" + myCache.r_policy)
 
# Display Calculations: 
print("")
print("***** Cache Calculated Values *****")
print("")
print("Total # Blocks: \t\t",int(myCache.totalBlocks))
print("Tag Size: \t\t\t{}".format(myCache.tagSize)+" bits")
print("Index Size: \t\t\t{}".format(myCache.indexSize)+" bits")
print("Total # Rows: \t\t\t{}".format(myCache.numberOfIndices))
print("Overhead Size: \t\t\t{0:.2f}".format(myCache.overheadMemory) + " bytes")
print("Implementation Memory Size: \t{0:.2f} KB {1}".format(myCache.memKB, "(" + str(myCache.mem) + " bytes)" ) )
print("Cost: \t\t\t\t${0:.2f}".format(myCache.cost))
print("")
print("")
print("")
print("***** Cache Simulation Result *****")
print("")
print("Total Cache Accesses: \t ", myCache.cachAccesses )
print("Cache Hits: \t\t ", myCache.cacheHits ) 
print("Cache Misses: \t\t ", myCache.cacheMisses )
print("--- Compulsory Misses: \t\t", myCache.compMisses)
print("--- Conflict Misses: \t\t ",myCache.cacheMisses -myCache.compMisses )
print("")
print("")
print("***** ***** CACHE HIT & MISS RATE: ***** *****")
print("")
print("Hit Rate:\t\t{0:.2f}".format(myCache.hitRate) + "%") #cache hit/cache access move two decimal right
print("Miss Rate: \t\t{0:.2f}".format(myCache.missRate) + "%")  #cache miss/cache access move two dec right
print("CPI: \t\t{0:.2f} Cycles/Instruction".format(myCache.total_cycles/myCache.total_instructions))
print("Unused Cache Space: \t\t{0:.2f} KB ".format(myCache.unusedKB) + "/ {0:.2f} KB".format(myCache.memKB) + " = {0:.2f}%".format(myCache.unusedKB/myCache.memKB) )
print("Waste: \t\t${0:.2f}".format(myCache.waste) )
block1 = 69
block2 = 9000
print("Unused Cache Blocks: \t\t" + str(block1) + " / " + str(block2) )
print("")

