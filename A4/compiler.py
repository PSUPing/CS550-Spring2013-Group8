# Compiler with options and compile method
# dn95
import interpreter
import argparse
import sys
import link as linker
import re
#import peephole

aparser = argparse.ArgumentParser(description='Compiler for Mini Language')
#aparser.add_argument('-O', '--Optimize', const=True, default=False, nargs='?', help='optimize compiling with peephole, default=no')
aparser.add_argument('-v', '--verbose', const=True, default=False, nargs='?', help='verbose, print all the information along')
aparser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout, help='output file')
aparser.add_argument('-m', '--memorySize', type=int, help='memorySize')
aparser.add_argument('--trans', const=True, nargs='?', default=False, help='for display purpose only')
aparser.add_argument('--link', const=True, nargs='?', default=False, help='for display purpose only')

#aparser.add_argument('--op', const=True, nargs='?', default=False, help='for display purpose only')

# compile method, which calls translate, optionally calls optimize, and then calls link
# parameters: Program p, Boolean verbose mode, Boolean optimize mode
# return the compiled program
def compile(P,memorySize, verbose=False, trans=False, link=False): #optimize=False, op=False

	print 'Compiling Program..'
	translate=P.translate()
	if verbose or trans:
		print 'Translated code:'
		print translate + "\n"
		if trans: return 
	#if optimize or op:
	#	print 'Providing Peephole Optimization..'
	#	peepholeCode = peephole.peephole(translate)
	#	if verbose or op:
	#		print 'Optimized code:'
	#		print peepholeCode + "\n"
	#		if op: return 
	#else:
	#	peepholeCode = translate
	print 'Linking Code..'
	linked= linker.linker(translate, P.mem,memorySize)
	if verbose or link:
		print 'Linked code:'
		print linked
		if link: return 
	return linked 

# output method, print RAL to file
# parameter: Compiled code, Boolean verbose mode, File output file
def output(compiled, output, verbose=False):
	output.write(compiled)
	if verbose:
		print 'Output RAL to', output.name 
	output.close()

a = aparser.parse_args(sys.argv[1:])
s = ''
for l in sys.stdin:
	s+=l
parsed = interpreter.parse(s)
compiled = compile(parsed,a.memorySize, a.verbose, a.trans, a.link) #a.Optimize,, a.op
if a.trans or a.link: #or a.op
	exit()
else:
	output(compiled, a.output, a.verbose)
