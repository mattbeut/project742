#!/usr/bin/python

import sys
import subprocess

if len(sys.argv) != 2:
    print("Must supply binary")
    sys.exit(0)

binary = sys.argv[1]
extractDir = binary + "_sections"
subprocess.call(['mkdir', extractDir])

sections = ['.text', '.data', '.rodata']

for s in sections:
	outfile = extractDir + '/' + binary + s
	subprocess.call(['objcopy', '-O', 'binary', 
			'-j', s, binary, outfile])

