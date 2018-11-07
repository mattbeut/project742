#!/usr/bin/python

# Note: requires radare2 to function
# Patches (in place, so make a backup if necessary) all 'add rsp, imm8'
# instructions in a binary with the equivalent 'sub rsp, imm8' instruction

import sys
import os
from tempfile import NamedTemporaryFile
import r2pipe
import argparse

def patchBinary(binary):
	patchBytes = NamedTemporaryFile()

	r = r2pipe.open(binary)

	# Disassemble binary
	r.cmd('aa')
	# Find all 4-byte 'add rsp, const8' instructions
	r.cmd('/c add rsp | grep " # 4:" > ' + patchBytes.name)

	count = 0
	with open(binary, 'r+b') as binfile:
		for line in patchBytes.readlines():
			# Address to patch
			patchAddr = int(line.split()[0], 16)

			# Seek to byte that must be inverted
			binfile.seek(patchAddr + 3)
			originalConst = ord(binfile.read(1))
			newConst = (~originalConst + 1) & 0xff

			# Seek back to byte to swap 'add' to 'sub'
			binfile.seek(patchAddr+2)
			binfile.write('\xec')

			# Write inverted byte
			binfile.write(chr(newConst))

			count += 1

	filename = os.path.basename(binary)

	print("Patched %d instructions in: %s" %(count, filename))

def main():
    parser = argparse.ArgumentParser(description="Changes all \
    							'add rsp, imm8' instructions in supplied binary to the \
                               	equivalent 'sub rsp, imm8' instruction. Warning: \
                              	will patch binary in place.")
    parser.add_argument('binary', type=str, help="path of binary to patch")

    args = parser.parse_args()

    patchBinary(args.binary)

if __name__ == "__main__":
    main()
