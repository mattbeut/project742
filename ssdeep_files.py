#!/usr/bin/python
import sys
import ssdeep

if len(sys.argv) != 3:
    print("Must supply two files to compare")
    sys.exit(0)

with open(sys.argv[1], 'rb') as f1:
    hash1 = ssdeep.hash(f1.read())

with open(sys.argv[2], 'rb') as f2:
    hash2 = ssdeep.hash(f2.read())

print("%s hash: %s" %(sys.argv[1], hash1))
print("%s hash: %s" %(sys.argv[2], hash2))

similar = ssdeep.compare(hash1, hash2)

print("Similarity: %d" %similar)

