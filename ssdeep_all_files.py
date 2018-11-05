#!/usr/bin/python

#
# Iterates through all of the files in a directory, creates
# the hash for the file and compares it to every other file
# in the directory
#
# usage: python ssdeep_all_files.py directory [--dedup] [--csv]
# --dedup refrains from comparing files to themselves and other
# files they've already been compared to.
# --csv outputs results to a csv file placed in the current
# directory
#

import sys
import os
import argparse
import csv
import ssdeep_files as sf

def process_files(args):
    filedir = args.directory

    done = []
    if args.csv:
        # Results in a filename that is the path to the directory with / replaced by _
        # then -ssdeep_all_files-out.csv In the current directory
        filedir_reformat = filedir.replace('/','_')
        if filedir_reformat.endswith('_') : filedir_reformat = filedir_reformat[0:-1]
        
        csvfilename = filedir_reformat + '-' + sys.argv[0].split('.')[0] + '-out.csv'
        
        csvfile= open(csvfilename, 'w')
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['file1', 'file2', 'similarity', 'hash1', 'hash2'])
    
    for file1 in os.listdir(filedir):
        filename1 = filedir + "/" + file1
        done.append(file1)
        
        for file2 in os.listdir(filedir):
            if args.dedup and file2 in done:
                continue
            filename2 = filedir + "/" + file2
            hash1,hash2,sim = sf.ssdeep_files(filename1, filename2)

            if args.csv:
                writer.writerow([file1, file2, sim, hash1, hash2])

    if args.csv:
        csvfile.close()

def main():
    parser = argparse.ArgumentParser(description="compare all the files in a directroy with ssdeep")
    parser.add_argument('directory', type=str, help="directory to process")
    parser.add_argument('--dedup', dest='dedup', action='store_true', help='set to avoid repetitive comparisons')
    parser.add_argument('--csv', dest='csv', action='store_true', help='set to output to csv')
    
    args = parser.parse_args()

    process_files(args)

if __name__ == "__main__":
    main()
