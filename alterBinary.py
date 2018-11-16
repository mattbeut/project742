#!/usr/bin/python

# Note: requires radare2 to function
# Patches (in place, so make a backup if necessary) all 'add rsp, imm8'
# instructions in a binary with the equivalent 'sub rsp, imm8' instruction

import sys
import os
from tempfile import NamedTemporaryFile
import r2pipe
import argparse

def patch(binary, addForSub, subForAdd):
	patchBytes = NamedTemporaryFile()

	r = r2pipe.open(binary)

	# Disassemble binary
	r.cmd('aa')

	if (addForSub):
		# Find all 4-byte 'add rsp, const8' instructions
		r.cmd('/c add rsp | grep " # 4:" > ' + patchBytes.name)
	if (subForAdd):
		# Find all 4-byte 'sub rsp, const8' instructions
		r.cmd('/c sub rsp | grep " # 4:" >> ' + patchBytes.name)

	count = 0
	with open(binary, 'r+b') as binfile:
		for line in patchBytes.readlines():
			# Address to patch
			patchAddr = int(line.split()[0], 16)

			# Seek to byte that must be inverted
			binfile.seek(patchAddr + 3)
			originalConst = ord(binfile.read(1))
			newConst = (~originalConst + 1) & 0xff

			# Seek back to byte to 'add'/'sub' opcode
			binfile.seek(patchAddr+2)

			opcode = ord(binfile.read(1))
			# 'add rsp' -> 'sub rsp'
			if (addForSub and opcode == 0xc4):
				binfile.seek(patchAddr+2)
				# 'sub rsp'
				binfile.write('\xec')
				# Write inverted byte
				binfile.write(chr(newConst))
				count += 1

			# 'sub rsp' -> 'add rsp'
			if (subForAdd and opcode == 0xec):
				binfile.seek(patchAddr+2)
				# 'add rsp'
				binfile.write('\xc4')
				# Write inverted byte
				binfile.write(chr(newConst))
				count += 1

	filename = os.path.basename(binary)
	print("Patched %d instructions in: %s" %(count, filename))

def main():
    parser = argparse.ArgumentParser(description="Alters a binary based on supplied \
    							arguments. Warning: will patch binary in place.")
    parser.add_argument("binary", type=str, help="path of binary to alter")
    parser.add_argument("-a", "--addForSub", help="Patch all 'add rsp, imm8' \
    		instructions for the equivalent 'sub rsp, imm8' instruction",
    		action="store_true")
    parser.add_argument("-s", "--subForAdd", help="Patch all 'sub rsp, imm8' \
    		instructions for the equivalent 'add rsp, imm8' instruction",
    		action="store_true")

    args = parser.parse_args()

    if (args.addForSub or args.subForAdd): 
		patch(args.binary, args.addForSub, args.subForAdd)

if __name__ == "__main__":
    main()
