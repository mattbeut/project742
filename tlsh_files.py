#!/usr/bin/python
import tlsh
import argparse

def tlsh_files(file1, file2, quiet):
    with open(file1, 'rb') as f1:
        hash1 = tlsh.forcehash(f1.read())
    with open(file2, 'rb') as f2:
        hash2 = tlsh.forcehash(f2.read())
        
    if hash1 and hash2:
        if not quiet: print("%s hash: %s" %(file1, hash1))
        if not quiet: print("%s hash: %s" %(file2, hash2))

        differences = tlsh.diff(hash1, hash2)
        if not quiet: print("Differences: %d" % differences)

        similarity = max(0, (( 300 - float(differences) ) / 3 ))
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

    tlsh_files(args.file1, args.file2, False)


if __name__ == "__main__":
    main()
