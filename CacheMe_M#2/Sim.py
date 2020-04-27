import sys
import argparse
import math
from cache import Cache
from cache import Block

# Check Arguments:
if len(sys.argv)!=11:
    print("USAGE: " + sys.argv[0] + " -f <trace file> -s <cache size KB> -b <block size> -a <associativity> -r <replacement policy>")
    sys.exit(1)

# Start Parsing:
parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, action='store', help="Trace_File")
parser.add_argument('-s', type=int, action='store', help="Cache_Size")
parser.add_argument('-b', type=int, action='store', help="Block_Size")
parser.add_argument('-a', type=int, action='store', help="Associativity")
parser.add_argument('-r', type=str, action='store', help="R_Policy")

# Save Arguments:
results = parser.parse_args()

# Check Arguments:
if (results.s < 1) or (results.s > 8192):
    print("ERROR: Cache Size Less than 1KB or More Than 8MB")
    sys.exit(1)
if (results.b < 4) or (results.b > 64):
    print("ERROR: Block Size is Less Than 4 Bytes, or Greater Than 64 Bytes")
    sys.exit(1)
associativity = [1, 2, 4, 8, 16]
if not (results.a in associativity):
    print("ERROR: Associativity Usage - 1, 2, 4, 8, 16")
    sys.exit(1)
replace_policy = ["RR", "RND", "LRU"]
if not (results.r in replace_policy):
    print("ERROR: Replacement Policy - RR, LRU, RND:")
    sys.exit(1)

# Set Variables from Arguments:
cacheSize = results.s
blockSize = results.b
associativity = results.a
r_policy = results.r
traceFile = results.f
if (r_policy == "RND"):
    policyPrint = "Random"
if (r_policy == "RR"):
    policyPrint = "Round Robin"
if (r_policy == "LRU"):
    policyPrint = "Least Recently Used"

# Read Trace File:
traceFile = open(traceFile, "r")
if not traceFile:
    print("ERROR: Cannot open or find Trace File")
    sys.exit(1)

# Calculate Cache:
numberOfBlocks = (((cacheSize * 1024) / blockSize) / 1024) # Blocks in Bits
totalBlocks = ((cacheSize * 1024) / blockSize)
indexSize = int(math.log((numberOfBlocks * 1024 // associativity), 2))
offsetSize = math.log(blockSize, 2)
tagSize = int(32 - indexSize - offsetSize)
numberOfIndices = (2 ** indexSize)
calculatedIndicesKB = numberOfIndices / 1024
totalRows = (2 ** indexSize) / 1024
rows = int(totalRows * 1024)
overheadMemory = ((tagSize + 1) * associativity * numberOfIndices) / 8
mem = (overheadMemory) + (cacheSize * 1024)
memKB = mem / 1024
cost = (float(mem)/1024) * 0.05


# Display Header:
print("")
print("Cache Sumulator CS 3853 Spring 2020 - Group #18")
print("Trace File: " + results.f)
print("")
print("***** Cache Input Parameters *****")
print("Cache Size: \t\t\t" + str(results.s) + " KB")
print("Block Size: \t\t\t" + str(results.b) + " bytes")
print("Associativity: \t\t\t" + str(results.a))
print("Replacement Policy: \t\t" + str(policyPrint))

# Display Calculations:
print("")
print("***** Cache Calculated Values *****")
print("")
print("Total # Blocks: \t\t%.0f" % totalBlocks)
print("Tag Size: \t\t\t{}".format(tagSize)+" bits")
print("Index Size: \t\t\t{}".format(indexSize)+" bits")
print("Total # Rows: \t\t\t{}".format(numberOfIndices))
print("Overhead Size: \t\t\t%.0f" % overheadMemory + " bytes")
print("Implementation Memory Size: \t%.2f KB  " % memKB + "(%.0f bytes)" % mem)
print("Cost: \t\t\t\t$%.2f " % cost)
print("")
print("")

# Display Cache Results:
cache = Cache(cacheSize, blockSize, associativity, r_policy, traceFile.name)
cache.cacheMe()

