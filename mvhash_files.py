#
# Download mvhash from here: https://dasec.h-da.de/staff/breitinger-frank/
# (all the way at the bottom)
#
# Make executable with:
# gcc misc.c mv.c rle.c uint8.c Levenshtein.c file.c match.c main.c \
# -D NO_PYTHON -O3 -o mvHash
#
# and put in the directory of this script
#
# As far as I can tell, computing the hash for a single file just segfaults.
# I don't see another way to get the hash string, but this does parse out the
# similarity metric. 
#

#!/usr/bin/python
import argparse
import subprocess
from subprocess import Popen, PIPE

def mvhash_files(file1, file2, quiet):
    
    session = subprocess.Popen(['./mvHash', '-g', file1, file2],
                               stdout=PIPE, stderr=PIPE)
    stdout,stderr = session.communicate()

    similarity_str = stdout.split('|')[-1]
    if not quiet: print("%s | %s"%(file1, file2))

    try:
        similarity = int(similarity_str)
        if not quiet: print("Similarity: " + similarity_str + ">")
        return "", "", similarity        
    except Exception:
        # having trouble catching the output from mvHash here. Most likely
        # files too short. You can run with normal mvHash to see
        if not quiet: print("Similarity could not be calculated")
        return "", "", None

def main():
    parser = argparse.ArgumentParser(description="perform tlsh hash on two files and compare")
    parser.add_argument('file1', type=str)
    parser.add_argument('file2', type=str)

    args = parser.parse_args()

    mvhash_files(args.file1, args.file2)


if __name__ == "__main__":
    main()
