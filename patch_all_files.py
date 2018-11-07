#!/usr/bin/python

import sys
import os
import argparse
import patch_addForSub as patch

def main():
    parser = argparse.ArgumentParser(description="Patches all files in a directory")
    parser.add_argument('directory', type=str, help="directory of binaries to patch")
    args = parser.parse_args()

    if not os.path.exists(args.directory):
        print("Error: directory does not exist")
        sys.exit(-1)
    
    for filename in os.listdir(args.directory):
        fullPath = os.path.join(args.directory, filename)
        patch.patchBinary(fullPath)
    
if __name__ == "__main__":
    main()
