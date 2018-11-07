#!/usr/bin/python

import sys
import subprocess
from os import listdir
from os.path import join

COMPARE_SCRIPT = 'ssdeep_files.py'

if len(sys.argv) != 3:
    print("Must supply two directories")
    sys.exit(0)
    
dir1 = sys.argv[1]
dir2 = sys.argv[2]

for file1 in listdir(dir1):
    ext = file1.split('.')[1]

    for file2 in listdir(dir2):
        if ext == file2.split('.')[1]:
            subprocess.call(['python', COMPARE_SCRIPT,
                        join(dir1, file1), join(dir2, file2)])
