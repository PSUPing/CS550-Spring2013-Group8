#!/usr/bin/python
#
# exp.py - Classes to represent underlying data structures for the grammar
#	 below, for the mini-compiler.
#
# Kurt Schmidt
# 8/07
#
# DESCRIPTION:
#		Just a translation of the C++ implementation by Jeremy Johnson (see
#		programext.cpp)
#
# EDITOR: cols=80, tabstop=2
#
# NOTES
#	environment:
#		a dict
#
#		Procedure calls get their own environment, can not modify enclosing env
#
#	Grammar:
#		program: stmt_list 
#		stmt_list:  stmt ';' stmt_list 
#		    |   stmt  
#		stmt:  assign_stmt 
#		    |  define_stmt 
#		    |  if_stmt 
#		    |  while_stmt 
#		assign_stmt: IDENT ASSIGNOP expr
#		define_stmt: DEFINE IDENT PROC '(' param_list ')' stmt_list END
#		if_stmt: IF expr THEN stmt_list ELSE stmt_list FI
#		while_stmt: WHILE expr DO stmt_list OD
#		param_list: IDENT ',' param_list 
#		    |      IDENT 
#		expr: expr '+' term   
#		    | expr '-' term   
#		    | term            
#		term: term '*' factor   
#		    | factor            
#		factor:     '(' expr ')'  
#		    |       NUMBER 
#		    |       IDENT 
#		    |       funcall 
#		funcall:  IDENT '(' expr_list ')'
#		expr_list: expr ',' expr_list 
#		    |      expr 
#

import sys

####  CONSTANTS   ################

	# the variable name used to store a proc's return value
returnSymbol = 'return'

tabstop = '  ' # 2 spaces

######   CLASSES   ##################
class Memory:
	constants={}
	cCount=0
	lCount=0
	pCount=0
	ft={}
	ftLabels={}
	fp='FP'
	sp='SP'
	scratch='S1'
	scratch2='S2'
	scratch3='S3'
	scratch4='S4'
	scratch5='S5'

	def __init__(self):
		self.tCount=0
		self.nCount=0
		self.nt={}

	def getLabel(self):
		Memory.lCount+=1
		return 'L'+str(Memory.lCount-1)

	def getFuncLabel(self,value) : 
		if value in Memory.ftLabels : 
			return Memory.ftLabels[value]
		else : 
			Memory.lCount += 1
			Memory.ftLabels[value] = 'L' + str(Memory.lCount - 1)
			return Memory.ftLabels[value]

	def getTemp(self):
		self.tCount+=1
		return 'T'+str(self.tCount-1)

	def transTemp(self,temp,scratch):
		if temp[0]=='T':
			index=int(temp[1:])
			s='LDA '+Memory.fp+';\n'
			s+='SUB '+Memory.getConstant(self.nCount)+';\n'
			s+='SUB '+Memory.getConstant(index)+';\n'
			s+='STA '+scratch+';\n'
			return s
		else:
			return self.transVar(temp,scratch)

	def transVar(self,var,scratch):
		index=int(var[1:])
		s='LDA '+Memory.fp+';\n'
		s+='SUB '+Memory.getConstant(index)+';\n'
		s+='STA '+scratch+';\n'
		return s

	@staticmethod
	def getConstant(value):
		if type(value) != type(0):
			raise Exception('Invalid type')
		if value in Memory.constants:
			return Memory.constants[value]	
		else:
			Memory.constants[value]='C'+str(Memory.cCount)
			Memory.cCount+=1
			return Memory.constants[value]

	@staticmethod
	def getConstantValue(consID) : 
		for value, consCount in Memory.constants.items() : 
			if consCount == consID : 
				return value

		return None

	def getVariable(self,value) :
		if type(value) != type(''):
			raise Exception('Invalid type')

		if value in self.nt:
			return self.nt[value]
		else:
			self.nt[value]='V'+str(self.nCount)
			self.nCount+=1
			return self.nt[value]

	def getVariableValue(self, varID) : 
		for value, varCount in self.nt.items() : 
			if varCount == varID : 
				return value

		return None

class Expr :
	'''Virtual base class for expressions in the language'''

	def __init__( self ) :
		raise NotImplementedError(
			'Expr: pure virtual base class.  Do not instantiate' )

	def eval( self, nt, ft ) :
		'''Given an environment and a function table, evaluates the expression,
		returns the value of the expression (an int in this grammar)'''
		raise NotImplementedError(
			'Expr.eval: virtual method.  Must be overridden.' )

	def translate(self,mem):
		'''Translate the expression into symbolic RAL code'''

		raise NotImplementedError(
			'Expr.eval: virtual method.  Must be overridden.' )

	def getHandle(self):
		'''Translate the expression into symbolic RAL code'''

		raise NotImplementedError(
			'Expr.eval: virtual method.  Must be overridden.' )


	def display( self, nt, ft, depth=0 ) :
		'For debugging.'
		raise NotImplementedError(
			'Expr.display: virtual method.  Must be overridden.' )

class Number( Expr ) :
	'''Just integers'''

	def __init__( self, v=0 ) :
		self.value = v

	def translate(self,mem):
		self.handle=Memory.getConstant(self.value)
		return ''
		
	def getHandle(self):
		return self.handle

	def eval( self, nt, ft ) :
		return self.value

	def display( self, nt, ft, depth=0 ) :
		print "%s%i" % (tabstop*depth, self.value)

class Ident( Expr ) :
	'''Stores the symbol'''

	def __init__( self, name ) :
		self.name = name

	def translate(self,mem):
		self.handle=mem.getVariable(self.name)
		return ''

	def getHandle(self):
		return self.handle

	def eval( self, nt, ft ) :
		return nt[ self.name ]

	def display( self, nt, ft, depth=0 ) :
		print "%s%s" % (tabstop*depth, self.name)


class Times( Expr ) :
	'''expression for binary multiplication'''

	def __init__( self, lhs, rhs ) :
		'''lhs, rhs are Expr's, the operands'''

		# test type here?
		# if type( lhs ) == type( Expr ) :
		self.lhs = lhs
		self.rhs = rhs

	def translate(self,mem):
		st=self.lhs.translate(mem)
		s1=self.lhs.getHandle()
		st+=self.rhs.translate(mem)
		s2=self.rhs.getHandle()
		self.handle=mem.getTemp()
		st+=mem.transTemp(self.handle,Memory.scratch)	

		st+=mem.transTemp(s1,Memory.scratch2)	
		st+=mem.transTemp(s2,Memory.scratch3)	

		st+="LDI "+Memory.scratch2+";\n"
		st+="MUL "+Memory.scratch3+";\n"

		st+="STI "+Memory.scratch+";\n"
		return st

	def getHandle(self):
		return self.handle
	
	def eval( self, nt, ft ) :
		return self.lhs.eval( nt, ft ) * self.rhs.eval( nt, ft )

	def display( self, nt, ft, depth=0 ) :
		print "%sMULT" % (tabstop*depth)
		self.lhs.display( nt, ft, depth+1 )
		self.rhs.display( nt, ft, depth+1 )
		#print "%s= %i" % (tabstop*depth, self.eval( nt, ft ))


class Plus( Expr ) :
	'''expression for binary addition'''

	def __init__( self, lhs, rhs ) :
		self.lhs = lhs
		self.rhs = rhs
	
	def eval( self, nt, ft ) :
		return self.lhs.eval( nt, ft ) + self.rhs.eval( nt, ft )

	def translate(self,mem):
		st=self.lhs.translate(mem)
		s1=self.lhs.getHandle()
		st+=self.rhs.translate(mem)
		s2=self.rhs.getHandle()
		self.handle=mem.getTemp()
		st+=mem.transTemp(self.handle,Memory.scratch)	

		st+=mem.transTemp(s1,Memory.scratch2)	
		st+=mem.transTemp(s2,Memory.scratch3)	
		st+="LDI "+Memory.scratch2+";\n"
		st+="ADD "+Memory.scratch3+";\n"

		st+="STI "+Memory.scratch+";\n"
		return st

	def getHandle(self):
		return self.handle

	def link(self) : 
		st=self.lhs.translate()
		s1=self.lhs.getHandle()
		st+=self.rhs.translate()
		s2=self.rhs.getHandle()
		st+="LDA "+s1+"; " + str(self.lhs.link(s1)) + "\n"
		st+="ADD "+s2+"; " + str(self.rhs.link(s2)) + "\n"
		self.handle=mem.getTemp()
		st+="STA "+self.handle+";\n"
		return st
		
	def display( self, nt, ft, depth=0 ) :
		print "%sADD" % (tabstop*depth)
		self.lhs.display( nt, ft, depth+1 )
		self.rhs.display( nt, ft, depth+1 )
		#print "%s= %i" % (tabstop*depth, self.eval( nt, ft ))


class Minus( Expr ) :
	'''expression for binary subtraction'''

	def __init__( self, lhs, rhs ) :
		self.lhs = lhs
		self.rhs = rhs
	
	def eval( self, nt, ft ) :
		return self.lhs.eval( nt, ft ) - self.rhs.eval( nt, ft )

	def translate(self,mem):
		st=self.lhs.translate(mem)
		s1=self.lhs.getHandle()
		st+=self.rhs.translate(mem)
		s2=self.rhs.getHandle()
		self.handle=mem.getTemp()
		st+=mem.transTemp(self.handle,Memory.scratch)	

		st+=mem.transTemp(s1,Memory.scratch2)	
		st+=mem.transTemp(s2,Memory.scratch3)	
		st+="LDI "+Memory.scratch2+";\n"
		st+="SUB "+Memory.scratch3+";\n"


		st+="STI "+Memory.scratch+";\n"
		return st

	def getHandle(self):
		return self.handle

	def display( self, nt, ft, depth=0 ) :
		print "%sSUB" % (tabstop*depth)
		self.lhs.display( nt, ft, depth+1 )
		self.rhs.display( nt, ft, depth+1 )
		#print "%s= %i" % (tabstop*depth, self.eval( nt, ft ))


class FunCall( Expr ) :
	'''stores a function call:
	  - its name, and arguments'''
	
	def __init__( self, name, argList ) :
		self.name = name
		self.argList = argList
	
	def eval( self, nt, ft ) :
		return ft[ self.name ].apply( nt, ft, self.argList )

	def translate( self,mem ) :
		func=Memory.ft[self.name]
		nP=Memory.getConstant(func.pCount)
		nV=Memory.getConstant(func.nCount)
		nT=Memory.getConstant(func.tCount)
		currentParam=mem.getTemp()
		oldSP=mem.getTemp()

		s=mem.transTemp(currentParam,Memory.scratch)	
		s+=mem.transTemp(oldSP,Memory.scratch2)	

		s="LDA "+Memory.sp+";\n"
		s+= "STI "+Memory.scratch2+";\n"
		s+= 'LDA '+Memory.fp+';\n'
		s+= 'STA '+Memory.sp+';\n'
		s+= 'ADD '+Memory.getConstant( 2)+';\n'#one for return address one for
#previous size
		s+= 'ADD '+nT+';\n'
		s+= 'ADD '+nV+';\n'
		s+= 'ADD '+nP+';\n'
		s+= 'STA '+Memory.fp+';\n'
		s+= 'STI '+Memory.scratch+';\n'
		for i in range(len(self.argList)):
			self.argList[i].translate(mem)
			handle=self.argList[i].getHandle()
			par=mem.getVariable(handle)
			#par=Memory.ft[self.name].parList[i]
			dest=mem.getVariable(par)
			s+=mem.transTemp(handle,Memory.scratch2)	
			s+=mem.transTemp(dest,Memory.scratch)	
			s+='LDI '+Memory.scratch2+';\n'
			s+='STI '+Memory.scratch+';\n'
		s+='CAL '+mem.getFuncLabel(self.name)+';\n'
		result=mem.getTemp()
		s+=mem.transTemp(result,Memory.scratch)	
		s+='LDA '+Memory.sp+';\n'
		s+='ADD '+Memory.getConstant(1)+';\n'
		s+='STI '+Memory.scratch+';\n'
		self.handle=result
		s+='LDA '+Memory.sp+';\n'
		s+='STA '+Memory.fp+';\n'
		s+=mem.transTemp(oldSP,Memory.scratch)	
		s+='LDI '+Memory.scratch+';\n'
		s+='STA '+Memory.sp+';\n'
		return s

	def getHandle(self):
		return self.handle

	def display( self, nt, ft, depth=0 ) :
		print "%sFunction Call: %s, args:" % (tabstop*depth, self.name)
		for e in self.argList :
			e.display( nt, ft, depth+1 )


#-------------------------------------------------------

class Stmt :
	'''Virtual base class for statements in the language'''

	def __init__( self ) :
		raise NotImplementedError(
			'Stmt: pure virtual base class.  Do not instantiate' )

	def eval( self, nt, ft ) :
		'''Given an environment and a function table, evaluates the expression,
		returns the value of the expression (an int in this grammar)'''

		raise NotImplementedError(
			'Stmt.eval: virtual method.  Must be overridden.' )

	def translate(self):
		raise NotImplementedError(
			'Stmt.eval: virtual method.  Must be overridden.' )


	def display( self, nt, ft, depth=0 ) :
		'For debugging.'
		raise NotImplementedError(
			'Stmt.display: virtual method.  Must be overridden.' )


class AssignStmt( Stmt ) :
	'''adds/modifies symbol in the current context'''

	def __init__( self, name, rhs ) :
		'''stores the symbol for the l-val, and the expressions which is the
		rhs'''
		self.name = name
		self.rhs = rhs

	def eval( self, nt, ft ) :
		nt[ self.name ] = self.rhs.eval( nt, ft )

	def translate(self,mem) :
		s = self.rhs.translate(mem)
		h1 = self.rhs.getHandle()
		s+=mem.transTemp(h1,Memory.scratch)	
		s += "LDI " + Memory.scratch + ";\n"
		h2 = mem.getVariable(self.name)
		s+=mem.transTemp(h2,Memory.scratch)	
		s += "STI " + Memory.scratch + ";\n"
		return (s,'')

	def display( self, nt, ft, depth=0 ) :
		print "%sAssign: %s :=" % (tabstop*depth, self.name)
		self.rhs.display( nt, ft, depth+1 )


class DefineStmt( Stmt ) :
	'''Binds a proc object to a name'''

	def __init__( self, name, proc ) :
		self.name = name
		self.proc = proc

	def eval( self, nt, ft ) :
		ft[ self.name ] = self.proc

	def translate( self,mem ) : 
		mem2=Memory()
		s=mem.getFuncLabel(self.name) + ': ' 
		trans=self.proc.translate(mem2)
		s+=trans[0]
		s+='LDA '+Memory.sp+';\n'
		s+='ADD '+Memory.getConstant(2)+';\n'

		s+='STA '+Memory.scratch+';\n'
		ret=mem2.getVariable('return')
		s+=mem.transTemp(ret,Memory.scratch2)	
		s+='LDA '+Memory.scratch2+';\n'
		s+='STI '+Memory.scratch+';\n'
		s+='LDA '+Memory.sp+';\n'
		s+='ADD '+Memory.getConstant(1)+';\n'

		s+=mem.transTemp(ret,Memory.scratch)	
		s+='STA '+Memory.scratch+';\n'
		s+='JMI '+Memory.scratch+';\n'
		Memory.ft[ self.name ] = mem2
		s+=trans[1]
		return ('',s)

	def display( self, nt, ft, depth=0 ) :
		print "%sDEFINE %s :" % (tabstop*depth, self.name)
		self.proc.display( nt, ft, depth+1 )


class IfStmt( Stmt ) :

	def __init__( self, cond, tBody, fBody ) :
		'''expects:
		cond - expression (integer)
		tBody - StmtList
		fBody - StmtList'''
		
		self.cond = cond
		self.tBody = tBody
		self.fBody = fBody

	def eval( self, nt, ft ) :
		if self.cond.eval( nt, ft ) > 0 :
			self.tBody.eval( nt, ft )
		else :
			self.fBody.eval( nt, ft )

	def translate(self,mem):
		s=self.cond.translate(mem)
		c=self.cond.getHandle()
		s+=transTemp(c,Memory.scratch)	
		l1=Memory.getLabel()
		l2=Memory.getLabel()
		s+="LDI "+Memory.scratch+";\n"
		s+="JMN "+l1+";\n"
		s+="JMZ "+l1+";\n"
		trans1=self.tBody.translate(mem)
		s+=trans1[0]
		s+="JMP "+l2+";\n"
		s+=l1+": "
		trans2=self.fBody.translate(mem)
		s+=trans2[1]
		s+=l2+": "
		return (s,trans1[1]+trans2[1])

	def display( self, nt, ft, depth=0 ) :
		print "%sIF" % (tabstop*depth)
		self.cond.display( nt, ft, depth+1 )
		print "%sTHEN" % (tabstop*depth)
		self.tBody.display( nt, ft, depth+1 )
		print "%sELSE" % (tabstop*depth)
		self.fBody.display( nt, ft, depth+1 )


class WhileStmt( Stmt ) :

	def __init__( self, cond, body ) :
		self.cond = cond
		self.body = body

	def translate(self,mem):
		l1=Memory.getLabel()
		l2=Memory.getLabel()
		s=l1+': '
		s+=self.cond.translate(mem)
		c=self.cond.getHandle()
		s+=transTemp(c,Memory.scratch)	
		s+="LDI "+Memory.scratch+";\n"
		s+="JMN "+l2+";\n"
		s+="JMZ "+l2+";\n"
		trans=self.body.translate(mem)
		s+=trans[0]
		s+="JMP "+l1+";\n"
		s+=l2+': '
		return (s,trans[1])

	def eval( self, nt, ft ) :
		while self.cond.eval( nt, ft ) > 0 :
			self.body.eval( nt, ft )

	def display( self, nt, ft, depth=0 ) :
		print "%sWHILE" % (tabstop*depth)
		self.cond.display( nt, ft, depth+1 )
		print "%sDO" % (tabstop*depth)
		self.body.display( nt, ft, depth+1 )

#-------------------------------------------------------

class StmtList :
	'''builds/stores a list of Stmts'''

	def __init__( self ) :
		self.sl = []
	
	def insert( self, stmt ) :
		self.sl.insert( 0, stmt )
	
	def eval( self, nt, ft ) :
		for s in self.sl :
			s.eval( nt, ft )

	def translate(self,mem):
		s = ''		# For the main program
		procs = ''  # For the procedures
		for e in self.sl :
			trans=e.translate(mem)
			s+=trans[0]
			procs+=trans[1]
		return (s, procs)

	def display( self, nt, ft, depth=0 ) :
		print "%sSTMT LIST" % (tabstop*depth)
		for s in self.sl :
			s.display( nt, ft, depth+1 )


class Proc :
	'''stores a procedure (formal params, and the body)

	Note that, while each function gets its own environment, we decided not to
	allow side-effects, so, no access to any outer contexts.  Thus, nesting
	functions is legal, but no different than defining them all in the global
	environment.  Further, all calls are handled the same way, regardless of
	the calling environment (after the actual args are evaluated); the proc
	doesn't need/want/get an outside environment.'''

	def __init__( self, paramList, body ) :
		'''expects a list of formal parameters (variables, as strings), and a
		StmtList'''

		self.parList = paramList
		self.body = body

	def apply( self, nt, ft, args ) :
		newContext = {}

		# sanity check, # of args
		if len( args ) is not len( self.parList ) :
			print "Param count does not match:"
			sys.exit( 1 )

		# bind parameters in new name table (the only things there right now)
		for i in range( len( args )) :
			newContext[ self.parList[i] ] = args[i].eval( nt, ft )

		# KS Don't know what I was doin' here, but it's wrong 3/08
		# Thank you, Charles
		#[ newContext.__setitem__(p,a.eval( nt, ft ))
		#		for p in self.parList for a in args ]

		# evaluate the function body using the new name table and the old (only)
		# function table.  Note that the proc's return value is stored as
		# 'return in its nametable
		
		self.body.eval( newContext, ft )
		if newContext.has_key( returnSymbol ) :
			return newContext[ returnSymbol ]
		else :
			print "Error:  no return value"
			sys.exit( 2 )

	def translate(self, mem) :
		trans=self.body.translate(mem)
		return (trans[0],trans[1])

	def display( self, nt, ft, depth=0 ) :
		print "%sPROC %s :" % (tabstop*depth, str(self.parList))
		self.body.display( nt, ft, depth+1 )


class Program :
	
	def __init__( self, stmtList ) :
		self.mem=Memory()
		self.stmtList = stmtList
		self.nameTable = {}
		self.funcTable = {}
	
	def eval( self ) :
		self.stmtList.eval( self.nameTable, self.funcTable )

	def translate(self) :
		trans = self.stmtList.translate(self.mem)
		three=Memory.getConstant(3)
		locs=Memory.getConstant(self.mem.nCount)
		temp=Memory.getConstant(self.mem.tCount)
		numC=Memory.getConstant(self.mem.cCount+1)
		s='LDA '+numC+';\n'
		s+='ADD '+three+';\n'
		s+='STA '+Memory.sp+';\n'
		s+='ADD '+locs+';\n'
		s+='ADD '+temp+';\n'
		s+='STA '+Memory.fp+';\n'
		s+=trans[0]
		s+='HLT ;\n'
		s+=trans[1]

		return s
		
	def dump( self ) :
		print "Dump of Symbol Table"
		print "Name Table"
		for k in self.nameTable :
			print "  %s -> %s " % ( str(k), str(self.nameTable[k]) )
		print "Function Table"
		for k in self.funcTable :
			print "  %s" % str(k)

	def display( self, depth=0 ) :
		print "%sPROGRAM :" % (tabstop*depth)
		self.stmtList.display( self.nameTable, self.funcTable )
