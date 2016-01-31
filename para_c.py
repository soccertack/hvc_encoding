#!/usr/bin/python
import os
import sys
import re
from common import *

"""
        asm volatile(
                "hvc #0x1234\n\t"
                "str x1, [%0]\n\t"
                ::"r" (ctxt->sys_regs[MPIDR_EL1]):"x1");
"""
filename='/users/jintackl/nested/arch/arm64/kvm/hyp/sysreg-sr.c'
def main():
	pat=re.compile("read_sysreg")
	with open(filename) as f:
		for line in f:
			result = re.search(pat, line)
			if result is not None:
				var = line.split('=')[0]
				reg = re.split('[()]', line)[1]
				instr = "mrs	x1, "+reg
				encoded_instr = get_encoding(instr)
				if encoded_instr:
					var = var.strip()
					print "\tasm volatile("
					print "\t\t\"%s\\n\\t\""%encoded_instr
					print "\t\t\"str\tx1, [\%0]\\n\\t\""
					print "\t\t::\"r\" (%s):\"x1\");"%var

if __name__ == '__main__':
	main()
