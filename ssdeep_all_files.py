#!/usr/bin/python

#
# Iterates through all of the files in a directory, creates
# the hash for the file and compares it to every other file
# in the directory
#
# usage: python ssdeep_all_files.py directory
#

import sys
import os
import argparse
import ssdeep_files as sf

def process_files(args):
    dir = args.directory

    done = []
    
    for file1 in os.listdir(dir):
        filename1 = dir + "/" + file1
        done.append(file1)
        
        for file2 in os.listdir(dir):
            if args.dedup and file2 in done:
                continue
            filename2 = dir + "/" + file2
            sf.ssdeep_files(filename1, filename2)

def main():
    parser = argparse.ArgumentParser(description="compare all the files in a directroy with ssdeep")
    parser.add_argument('directory', type=str, help="directory to process")
    parser.add_argument('--dedup', dest='dedup', action='store_true')

    args = parser.parse_args()

    process_files(args)

if __name__ == "__main__":
    main()
