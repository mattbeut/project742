#!/usr/bin/python

import sys
import os
import argparse


def nops(source, numNops):
        NOP_STR = ' asm("' + 'nop; '*numNops + '");'
	with open(source) as infile:
		lines = infile.readlines()

	foundParantheses = False
	count = 0
        # To catch file permission errors
        try:
            with open(source, 'w') as outfile:
                for line in lines:
                    newline = line
                    line = line.strip()
                    if (foundParantheses):
                        if(line == '{'):
                            newline = line + NOP_STR + '\n'
                            count += 1
                        foundParantheses = False
                    elif line.endswith(')'):
                        foundParantheses = True
                            
                    outfile.write(newline)

            filename = os.path.basename(source)
            print("Inserted %d nops at %d locations in: %s" %(numNops, count, filename))
        except:
            pass

def main():
    parser = argparse.ArgumentParser(description="Inserts 'nop' instructions \
    		throughout supplied source code. Warning: alters code in place")
    parser.add_argument("source", type=str, help="path to source code")
    parser.add_argument("-n", "--numNops", type=int, default=1, 
                help="number of nops to insert with each block (number of \
                        blocks/opportunities to insert nops varies for each file)")

    args = parser.parse_args()
    nops(args.source, args.numNops)

if __name__ == "__main__":
    main()
