#!/usr/bin/python

#
# calls extractHeaders on all of the files in the passed directory, then
# performs ssdeep on all files between each binary
#

import sys
import os
import argparse
from shutil import copyfile
import extractHeaders as eh
import ssdeep_files as sf
import csv

#
# performs extractHeaders on all files in the passed directory
# and copies the original files to the out directory for comparison
#
def preprocess_all(args):
    filedir = args.directory
    
    for f in os.listdir(filedir):
        rel_path = filedir + "/" + f
        args.binary = rel_path
        
        eh.extract(args)

        # copy original file over too for full comparison
        # XXX: not ideal, dependant on extractHeaders' format
        copyfile(rel_path, args.out + "/" + f +"/" + f)

#
# Pretty much the same code as in ssdeep_headers.py but with writes to csv file
# compares each file in one directory with files of the same extension in
# the second passed directory
# writes output with passed writer
#
def compare_all_files(d1, d2, writer):
    
    for file1 in os.listdir(d1):
        ext1 = os.path.splitext(file1)
        
        for file2 in os.listdir(d2):
            ext2 = os.path.splitext(file2)

            if ext1[-1] == ext2[-1]:
                if ext1[-1]:
                    category = ext1[-1][1:]
                else:
                    category = "full"
                    
                hash1, hash2, sim = sf.ssdeep_files(os.path.join(d1,file1), os.path.join(d2,file2))
                writer.writerow([file1, file2, category, sim, hash1, hash2])
                
            
#
# calls compare_all_files helper function on all combinations
# of directories found in dir
#
# skips files, and unless extra is set, skips comparing to self
# and combinations that have been compared before (doesn't compare
# both dir1 to dir2 and dir2 to dir1)
#
def compare_all_dirs(args):
    done = []

    csvfilename = "ssdeep-comparisons.csv"
    csvfile = open(args.out + "/" + csvfilename, 'w')
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['file1', 'file2', 'section', 'similarity', 'hash1', 'hash2'])

    # for every directory
    for d1 in os.listdir(args.out):
        fulld1 = os.path.join(args.out, d1)
        if os.path.isfile(fulld1): continue
        done.append(d1)

        # compare it every other directory
        for d2 in os.listdir(args.out):
            fulld2 = os.path.join(args.out, d2)
            if os.path.isfile(fulld2): continue
            
            # omit self and ones you've already been compared to unless extra is set
            if not args.extra and d2 in done: continue

            compare_all_files(fulld1, fulld2, writer)
            
    csvfile.close()
        

        
def main():
    parser = argparse.ArgumentParser(description="extractHeaders from all files in a directory")
    parser.add_argument('directory', type=str, help="directory to process")
    parser.add_argument('--extra', dest='extra', action='store_true',
                        help='set to perform repetitive comparisons (self to self, file1 to file2 and vice versa)')
    parser.add_argument('-o', dest='out', help='output directory', default="out-ssdeep_all")
    args = parser.parse_args()

    if not os.path.exists(args.out): os.makedirs(args.out)

    # this just to add another level to the out directory structure to make
    # it easier to process multiple directories without changing -out
    filedir_reformat = args.directory.replace('/','_')
    if filedir_reformat.endswith('_'): filedir_reformat = filedir_reformat[0:-1]
    args.out = args.out + "/" + filedir_reformat

    preprocess_all(args)

    compare_all_dirs(args)

    
    
if __name__ == "__main__":
    main()
