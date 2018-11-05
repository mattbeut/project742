#!/usr/bin/python

import sys
import os
import subprocess
import argparse

def extract(args):
    binaryPath = args.binary
    binaryName = os.path.basename(binaryPath)
    extractDir = args.out + "/"+ binaryName + "_sections"

    if not os.path.exists(extractDir):
        os.makedirs(extractDir)

    sections = ['.text', '.data', '.rodata']

    for s in sections:
	outfile = extractDir + '/' + binaryName + s
	subprocess.call(['objcopy', '-O', 'binary', 
			 '-j', s, binaryPath, outfile])

def main():
    parser = argparse.ArgumentParser(description="Extract the headers of a binary")
    parser.add_argument('binary', type=str, help="binary to process")
    parser.add_argument('-o', dest='out', help="output directory", default="out-extractHeaders")

    args = parser.parse_args()

    if not os.path.exists(args.out):
        os.makedirs(args.out)

    extract(args)

if __name__ == "__main__":
    main()


    
