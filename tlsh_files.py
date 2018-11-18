#!/usr/bin/python
import tlsh
import argparse
import ssdeep

HASH_LEN = 35 # Number of bytes in the hashes produced by TLSH. Differences
              # are counted by TLSH in accordance with the number of bytes
              # that differ between hashes. This is used to obtain a
              # percentage like other metrics.

def tlsh_files(file1, file2, quiet):
    with open(file1, 'rb') as f1:
        hash1 = tlsh.hash(f1.read())
    with open(file2, 'rb') as f2:
        hash2 = tlsh.hash(f2.read())

    if hash1 and hash2:
        if not quiet: print("%s hash: %s" %(file1, hash1))
        if not quiet: print("%s hash: %s" %(file2, hash2))

        differences = tlsh.diff(hash1, hash2)
        if not quiet: print("Differences: %d" % differences)

        similarity = (( HASH_LEN - float(differences) ) / HASH_LEN )* 100
        if not quiet: print("similarity: %d" % similarity)
        
        return hash1, hash2, int(similarity)

    else:
        if not quiet: print("[ ERROR ] unable to perform hash")
        return hash1, hash2, None

def main():
    parser = argparse.ArgumentParser(description="perform tlsh hash on two files and compare")
    parser.add_argument('file1', type=str)
    parser.add_argument('file2', type=str)

    args = parser.parse_args()

    tlsh_files(args.file1, args.file2)


if __name__ == "__main__":
    main()
