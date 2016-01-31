import os
import sys
import re

# Note: this list MUST be synced with the el1 reg in arch/arm64/include/asm/kvm_host.h 
el1_list = [
"__invalid_sysreg__",
"mpidr_el1",      
"csselr_el1",     
"sctlr_el1",      
"actlr_el1",      
"cpacr_el1",      
"ttbr0_el1",      
"ttbr1_el1",      
"tcr_el1",        
"esr_el1",        
"afsr0_el1",      
"afsr1_el1",      
"far_el1",        
"mair_el1",       
"vbar_el1",       
"contextidr_el1", 
"tpidr_el0",      
"tpidrro_el0",    
"tpidr_el1",      
"amair_el1",      
"cntkctl_el1",    
"par_el1",        
"mdscr_el1",      
"mdccint_el1",    
]
# Note: this list MUST be synced with the el2 reg in arch/arm64/include/asm/hvc_encoding.h
el2_list = [
"elr_el2",
"spsr_el2",
"sp_el2",
"amair_el2",
"mair_el2",
"tcr_el2",
"ttbr0_el2",
"vtcr_el2",
"vttbr_el2",
"vmpidr_el2",
"vpidr_el2",
"mdcr_el2",
"cnthctl_el2",
"cnthp_ctl_el2",
"cnthp_cval_el2",
"cnthp_tval_el2",
"cntvoff_el2",
"actlr_el2",
"afsr0_el2",
"afsr1_el2",
"cptr_el2",
"esr_el2",
"far_el2",
"hacr_el2",
"hcr_el2",
"hpfar_el2",
"hstr_el2",
"rmr_el2",
"rvbar_el2",
"sctlr_el2",
"tpidr_el2",
"vbar_el2"
]

INSTR_SHIFT = 14
INSTR_MRS = 3 
INSTR_MSR = 2
INSTR_OTHER = 1

IMM_SHIFT = 13
EL2_SHIFT = 12
SYSREG_SHIFT = 5

EL1_IFDEF="#ifndef CONFIG_EL1_HYP"

def get_encoding(line):
	prefix =""
	line = line.lstrip() # Remove preceding tab
	sp = re.split('[ ,\t]*', line)
	i = 0
	while True:
		if sp[i] == 'mrs':
			is_mrs = True
			break;
		elif sp[i] == 'msr':
			is_mrs = False
			break;
		prefix += sp[i]
		i += 1
		if i >= len(sp):
			print 'This is not msr/mrs instruction'
			return

	encoding = 0

	if is_mrs:
		encoding |= (INSTR_MRS << INSTR_SHIFT)
		gpreg = sp[i+1]
		sysreg = sp[i+2]
	else:
		encoding |= (INSTR_MSR << INSTR_SHIFT)
		gpreg = sp[i+2]
		sysreg = sp[i+1]

	if (sysreg[-3:] == 'el1') or (sysreg[-3:] == 'el0'):
		if sysreg not in el1_list:
			print sysreg, 'is not in the list'
			return
		encoding |= (el1_list.index(sysreg) << SYSREG_SHIFT)
	elif sysreg[-3:] == 'el2':
		encoding |= ( 1 << EL2_SHIFT)
		if sysreg not in el2_list:
			print sysreg, 'is not in the list'
			return
		encoding |= (el2_list.index(sysreg) << SYSREG_SHIFT)
	else:
		print line
		print 'error: sysreg name is not correct'
		return

	if gpreg == 'lr':
		gpreg_num = 30
	elif gpreg == 'xzr':
		gpreg_num = 31
	else:
		gpreg_num = int(gpreg[1:])
	encoding |= gpreg_num

	#sub = '%s\thvc\t#%s' % (prefix, format(encoding, '#04x'))
	sub = 'hvc\t#%s' % (format(encoding, '#04x'))
	return sub


