#!/usr/bin/python
import re

def peephole(string):
	store=re.compile('[\S\s]*(STA|STI)\s+([VT]\d*)\s*;')
	load=re.compile('[\S\s]*(LDA|LDI)\s+([VT]\d*)\s*;')
	unneaded=[]
	inp=string.split('\n')
	for i in range(len(inp)-1):
		p1=store.match(inp[i])
		p2=load.match(inp[i+1])
		if p1 is not None and p2 is not None and ':' not in inp[i+1]:
			if p1.group(1)[-1:]==p2.group(1)[-1:]and p1.group(2)==p2.group(2):
				unneaded.append(i+1)
	output=''
	for i in range(len(inp)):
		if i not in unneaded:
			output+=inp[i]+'\n'
		while i in unneaded and ':' in inp[i] and ';' in inp[i] and inp[i].index(':')<inp[i].index(';'):
			output+=inp[i][:inp[i].index(':')] + ': '
			inp[i]=inp[i][inp[i].index(':')+1:]
	return output
