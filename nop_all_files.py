#!/usr/bin/python

import sys
import os
import argparse
import alterSource as alter

def main():
    parser = argparse.ArgumentParser(description="Inserts nops in all source files (.c) in a directory")
    parser.add_argument('directory', type=str, help="directory containing source files to alter")
    parser.add_argument("-n", "--numNops", type=int, default=1, 
                help="number of nops to insert with each block (number of \
                        blocks/opportunities to insert nops varies for each file)")

    args = parser.parse_args()

    if not os.path.exists(args.directory):
        print("Error: directory does not exist")
        sys.exit(-1)
    
    for filename in os.listdir(args.directory):
        if filename.endswith(".c"):
            fullPath = os.path.join(args.directory, filename)
            alter.nops(fullPath, args.numNops)
    
if __name__ == "__main__":
    main()
