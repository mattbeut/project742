#!/usr/bin/python

#
# calls extractHeaders on all of the files in the passed directory
#
# usage: python extract_all_headers.py directory [-o out]
#

import sys
import os
import argparse
import extractHeaders as eh

def extract_all(args):
    filedir = args.directory
    
    for f in os.listdir(filedir):
        rel_path = filedir + "/" + f
        args.binary = rel_path
        
        eh.extract(args)

def main():
    parser = argparse.ArgumentParser(description="extractHeaders from all files in a directory")
    parser.add_argument('directory', type=str, help="directory to process")
    parser.add_argument('-o', dest='out', help='output directory', default="out-extract_all_headers")
    
    args = parser.parse_args()

    extract_all(args)

if __name__ == "__main__":
    main()
