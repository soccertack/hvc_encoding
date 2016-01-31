#!/usr/bin/python
import os
import sys
import re
from common import *

def replace_instr(fpath):
	pat = re.compile(".*m(rs|sr).*el[12].*")
	with open(fpath) as f:
		if not any(re.search(pat, line) for line in f):
			return # pattern does not occur in file so we are done.
		print fpath

	with open(fpath) as f:
			
		out_fname = fpath+ ".tmp"
		out = open(out_fname, "w")
		for line in f:
			result = re.search(pat, line)
			if result is not None:
				encoding = get_encoding(line.rstrip())
				print encoding
				if encoding:
					s_after = EL1_IFDEF+"\n"
					s_after += line
					s_after += "#else\n"
					s_after += get_encoding(line.rstrip()) +"\n"
					s_after += "#endif"
					out.write(re.sub(pat, s_after, line))
				else:
					out.write(line)
			else:
	    			out.write(line)
       		out.close()
		os.rename(out_fname, fpath)

def main():
	global read_only
	read_only = 0
	if len(sys.argv) == 1:
		sys.exit()
	elif len(sys.argv) > 2 and sys.argv[2] == '-c':
		read_only = 1
	pathname = sys.argv[1]

	if pathname.endswith(('.S', '.h', '.c')):
		replace_instr(pathname)
		
	for dname, dirs, files in os.walk(pathname):
	    for fname in files:
		fpath = os.path.join(dname, fname)
		if fpath.endswith(('.S', '.h', '.c')):
			replace_instr(fpath)

if __name__ == '__main__':
	main()
