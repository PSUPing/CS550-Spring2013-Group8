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
		if p1 is not None and p2 is not None:
			if p1.group(1)[-1:]==p2.group(1)[-1:]and p1.group(2)==p2.group(2):
				unneaded.insert(0,i+1)
	unneaded.reverse()
	output=''
	for i in range(len(inp)):
		if i not in unneaded:
			output+=inp[i]+'\n'
		while i in unneaded and ':' in inp[i] and ';' in inp[i] and inp[i].index(':')<inp[i].index(';'):
			output+=inp[i][:i.index(':')]
			inp[i]=inp[i][i.index(':')+1:]
	return output
