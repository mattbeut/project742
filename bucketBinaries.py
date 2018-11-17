#!/usr/bin/python

import sys
import os
import argparse
import shutil

def bucket(args):
    buckets =   {
                # Identical, new build 
                'coreutils_newBuild':   ['coreutils_8.30_O2', 'coreutils_8.30_newBuild'],
                # Identical, new build with debug/symbols
                'coreutils_debug':      ['coreutils_8.30_O2_debug', 'coreutils_8.30_O2_newBuild_debug'],
                # Different major version
                'coreutils_major':      ['coreutils_6.12_O2', 'coreutils_7.6_O2', 'coreutils_8.30_O2'],
                # Different minor version
                'coreutils_minor':
                ['coreutils_8.28_O2', 'coreutils_8.29_O2', 'coreutils_8.30_O2'],
                # Different gcc optimization flags
                'coreutils_optimization':
                ['coreutils_8.30_O0', 'coreutils_8.30_O1', 'coreutils_8.30_O2',
                 'coreutils_8.30_O3', 'coreutils_8.30_Os', 'coreutils_8.30_Ofast'],
                # Functionally identical instruction patches
                'coreutils_patched':
                ['coreutils_8.30_O2', 'coreutils_8.30_O2_addForSub', 'coreutils_8.30_O2_addSubSwap'],
                # Insertion of 'nop' instructions
                'coreutils_nops':
                ['coreutils_8.30_O2', 'coreutils_8.30_O2_nops1', 'coreutils_8.30_O2_nops10']
                }

    for dir_name in os.listdir(args.directory):
        dir_path = os.path.join(args.directory, dir_name)
        if os.path.isfile(dir_path): continue

        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)

            matching_buckets = []
            for bucket_name in buckets.keys():
                if dir_name in buckets[bucket_name]:
                    bucket_path = os.path.join(args.out, bucket_name) 
                    matching_buckets.append(bucket_path)

            for bucket_path in matching_buckets:
                if not os.path.exists(bucket_path):
                    os.makedirs(bucket_path)
               
                new_file_dir = os.path.join(bucket_path, file_name)
                if not os.path.exists(new_file_dir):
                    os.makedirs(new_file_dir)

                new_file_name = file_name + '-' + dir_name
                new_file_path = os.path.join(new_file_dir, new_file_name)
                shutil.copyfile(file_path, new_file_path)

def main():
    parser = argparse.ArgumentParser(description="Creates buckets for all unique builds of each binary")
    parser.add_argument('directory', type=str, help="Directory which contains directories of unique \
            builds to bucket")
    parser.add_argument('-o', dest='out', help="output directory", default='buckets')

    args = parser.parse_args()

    if not os.path.exists(args.out):
        os.makedirs(args.out)

    bucket(args)

if __name__ == "__main__":
    main()
 
