#!/usr/bin/python

import sys
import os
import subprocess

if len(sys.argv) != 2:
    print("Must supply binary")
    sys.exit(0)

binaryPath = sys.argv[1]
binaryName = os.path.basename(binaryPath)
extractDir = binaryName + "_sections"
subprocess.call(['mkdir', extractDir])

sections = ['.text', '.data', '.rodata']

for s in sections:
	outfile = extractDir + '/' + binaryName + s
	subprocess.call(['objcopy', '-O', 'binary', 
			'-j', s, binaryPath, outfile])

