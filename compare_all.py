#!/usr/bin/python

#
# calls extractHeaders on all of the files in the passed directory, then
# performs chosen algorithm on all files between each binary
#

import sys
import os
import csv
import argparse
from shutil import copyfile
import fileinput

import extractHeaders as eh
import ssdeep_files as sf
import tlsh_files as tf
import mvhash_files as mf

supported_algs = ["ssdeep", "tlsh", "mvhash"]

def preprocess_dir(args):
    filedir = args.directory

    for f in os.listdir(filedir):
        rel_path = filedir + "/" + f
        args.binary = rel_path
        
        eh.extract(args)

        # copy original file over too for full comparison
        # XXX: not ideal, dependant on extractHeaders' format
        copyfile(rel_path, args.out + "/" + f +"/" + f)
#
# performs extractHeaders on all files in the passed directory
# and copies the original files to the out directory for comparison
#
def preprocess_all(args):
    filedir = args.directory
    
    if args.allDirs:
        for d in os.listdir(filedir):
            if os.path.isfile(d): continue
            args.directory = os.path.join(filedir, d)
            preprocess_dir(args)
    else:
        preprocess_dir(args)

#
# Pretty much the same code as in ssdeep_headers.py but with writes to csv file
# compares each file in one directory with files of the same extension in
# the second passed directory
# writes output with passed writer
#
def compare_all_files(d1, d2, writer, alg, quiet):
    
    for file1 in os.listdir(d1):
        ext1 = os.path.splitext(file1)
        
        for file2 in os.listdir(d2):
            ext2 = os.path.splitext(file2)

            if ext1[-1] == ext2[-1]:
                if ext1[-1]:
                    category = ext1[-1][1:]
                else:
                    category = "full"

                full_f1 = os.path.join(d1, file1)
                full_f2 = os.path.join(d2, file2)
               
                if alg == 'all':
                    _,_,ssdeep = sf.ssdeep_files(full_f1, full_f2, quiet)
                    _,_,tlsh = tf.tlsh_files(full_f1, full_f2, quiet)
                    _,_,mvhash = mf.mvhash_files(full_f1, full_f2, quiet)
                elif alg == "ssdeep":
                    hash1, hash2, metric = sf.ssdeep_files(full_f1, full_f2, quiet)
                elif alg == "tlsh":
                    hash1, hash2, metric = tf.tlsh_files(full_f1, full_f2, quiet)
                elif alg == "mvhash":
                    hash1, hash2, metric = mf.mvhash_files(full_f1, full_f2, quiet)
                else:
                    print("[ ERROR ] algorithm not supported")
                    sys.exit(0)
                
                bin1 = file1.split('-')[0]
                bin2 = file2.split('-')[0]
                if bin1 == bin2:
                    truth = 'yes'
                else:
                    truth = 'no'

                file1_size = os.path.getsize(full_f1)
                file2_size = os.path.getsize(full_f2)

                file_info = [file1, file2, file1_size, file2_size, category]
                if alg == 'all':
                    writer.writerow(file_info + [ssdeep, tlsh, mvhash] + [truth])
                else:
                    writer.writerow(file_info + [metric, hash1, hash2, truth])
                
            
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

    csvfilename = args.algorithm + "-comparisons.csv"
    csvfile = open(args.out + "/" + csvfilename, 'w')
    writer = csv.writer(csvfile, delimiter=',')

    file_info_header = ['file1', 'file2', 'file1_size', 'file2_size', 'section']
    if args.algorithm == 'all':
        writer.writerow(file_info_header + supported_algs + ['truth'])
    else: 
        writer.writerow(file_info_header + ['metric', 'hash1', 'hash2', 'truth'])

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

            compare_all_files(fulld1, fulld2, writer, args.algorithm, args.quiet)
            
    csvfile.close()

    return csvfilename


def create_html_from_template(out, csvfilename):
    template_file = "template.html"

    # same name as csv file but with .html ext
    html_file = os.path.join(out, os.path.splitext(csvfilename)[0] + ".html")
    copyfile(template_file, html_file)
    
    for line in fileinput.input(html_file, inplace=True):
        print line.replace("%CSV_FILENAME%", csvfilename),

        
def main():
    parser = argparse.ArgumentParser(description="extractHeaders from all files in a directory")
    parser.add_argument('directory', type=str, help="directory to process")
    parser.add_argument('algorithm', type=str, help='algorithm to use')
    parser.add_argument('--extra', dest='extra', action='store_true',
                        help='set to perform repetitive comparisons (self to self, file1 to file2 and vice versa)')
    parser.add_argument('-o', dest='out', help='output directory', default="out-compare_all")
    parser.add_argument('--viz', dest='viz', action='store_true', help='set to create html visualization')
    parser.add_argument('-a', '--allDirs', action='store_true',
                        help='process all directories within supplied directory')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='silence print statements from hashing results')
    
    args = parser.parse_args()

    if not os.path.exists(args.out): os.makedirs(args.out)

    # this just to add another level to the out directory structure to make
    # it easier to process multiple directories without changing -out
    filedir_reformat = args.directory.replace('/','_')
    if filedir_reformat.endswith('_'): filedir_reformat = filedir_reformat[0:-1]
    args.out = args.out + "/" + filedir_reformat

    # double check that algorithm is supported before going forward
    if not args.algorithm in (supported_algs + ['all']):
        print("[ ERROR ] algorithm not supported: "+ args.algorithm)
        sys.exit(-1)
    
    preprocess_all(args)

    csvfile = compare_all_dirs(args)

    if args.viz :
        create_html_from_template(args.out, csvfile)

    
    
if __name__ == "__main__":
    main()
