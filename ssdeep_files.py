#!/usr/bin/python
import sys
import ssdeep

def ssdeep_files(file1, file2, quiet):
    with open(file1, 'rb') as f1:
        hash1 = ssdeep.hash(f1.read())
            
    with open(file2, 'rb') as f2:
        hash2 = ssdeep.hash(f2.read())

    if not quiet: print("%s hash: %s" %(file1, hash1))
    if not quiet: print("%s hash: %s" %(file2, hash2))

    similar = ssdeep.compare(hash1, hash2)
       
    if not quiet: print("Similarity: %d" %similar)

    return hash1, hash2, similar

def main():    
    if len(sys.argv) != 3:
        print("Must supply two files to compare")
        sys.exit(0)

    ssdeep_files(sys.argv[1], sys.argv[2])

    
if __name__ == "__main__":
    main()
