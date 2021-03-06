 #!/usr/bin/python
#
# exp.py - Classes to represent underlying data structures for the grammar
#        below, for the mini-compiler.
#
# Kurt Schmidt
# 8/07
#
# DESCRIPTION:
#               Just a translation of the C++ implementation by Jeremy Johnson (see
#               programext.cpp)
#
# EDITOR: cols=80, tabstop=2
#
# NOTES
#       environment:
#               a dict
#
#               Procedure calls get their own environment, can not modify enclosing env
#
#       Grammar:
#               program: stmt_list
#               stmt_list:  stmt ';' stmt_list
#                   |   stmt
#               stmt:  assign_stmt
#                   |  define_stmt
#                   |  if_stmt
#                   |  while_stmt
#               assign_stmt: IDENT ASSIGNOP expr
#               define_stmt: DEFINE IDENT PROC '(' param_list ')' stmt_list END
#               if_stmt: IF expr THEN stmt_list ELSE stmt_list FI
#               while_stmt: WHILE expr DO stmt_list OD
#               param_list: IDENT ',' param_list
#                   |      IDENT
#               expr: expr '+' term
#                   | expr '-' term
#                   | term
#               term: term '*' factor
#					| term '||' factor
#                   | factor
#               factor: '(' expr ')'
#                   | NUMBER
#                   | IDENT
#                   | funcall
#					| list
#               list:           '[]'
#                   |            '[' sequence ']'
#                   |            list '||' list
#               sequence:       listelement ',' sequence
#                   |            listelement
#               listelement:     list
#                   |            NUMBER
#               funcall:  IDENT '(' expr_list ')'
#               expr_list: expr ',' expr_list
#                   |      expr
#

import sys
import common
import copy

####  CONSTANTS   ################

# the variable name used to store a proc's return value
returnSymbol = 'return'

tabstop = '  ' # 2 spaces

######   CLASSES   ##################

class Expr :
	'''Virtual base class for expressions in the language'''
	
	def __init__( self ) :
		raise NotImplementedError(
							 'Expr: pure virtual base class.  Do not instantiate' )
	
	def eval( self, nt) :
		'''Given an environment and a function table, evaluates the expression,
			returns the value of the expression (an int in this grammar)'''
		
		raise NotImplementedError(
							 'Expr.eval: virtual method.  Must be overridden.' )
	
	def display( self, nt, depth=0 ) :
		'For debugging.'
		raise NotImplementedError(
							 'Expr.display: virtual method.  Must be overridden.' )

class Number( Expr ) :
	'''Just integers'''
	
	def __init__( self, v=0 ) :
		self.value = v
	
	def eval( self, nt ) :
		return self.value
	
	def display( self, nt, depth=0 ) :
		print "%s%i" % (tabstop*depth, self.value)

# This class will allow for differentiation between a "List" and a "Sequence"
class ListType( Expr ) :
	def __init__(self, lst = []):
		if lst==[]:
			self.listVals = lst[:]
		else:
			self.listVals=lst
	
	def eval( self, nt ) :
		return self.listVals
	
	def display( self, nt, depth=0 ) :
		print "%s%s" % (tabstop*depth, self.listVals)

class Ident( Expr ) :
	'''Stores the symbol'''
	
	def __init__( self, name ) :
		self.name = name
	
	def eval( self, nt ) :
		return nt.get(self.name)
	
	def display( self, nt, depth=0 ) :
		print "%s%s" % (tabstop*depth, self.name)

class Concat( Expr ) :
	'''expression for list concatenation'''
	
	def __init__( self, lhs, rhs ) :
		'''lhs, rhs are Expr's, the operands'''

		# test type here?
		# if type( lhs ) == type( Expr ) :
		self.lhs = lhs
		self.rhs = rhs
	
	def eval( self, nt ) :
		if isinstance(self.lhs, Number) or isinstance(self.rhs, Number) :
			print('Concatenation can only occur with lists or variables containing lists!')
			return None

		return self.lhs.eval( nt ) + self.rhs.eval( nt )
	
	def display( self, nt, depth=0 ) :
		print "%sCONCAT" % (tabstop*depth)
		self.lhs.display( nt, depth+1 )
		self.rhs.display( nt, depth+1 )

class Times( Expr ) :
	'''expression for binary multiplication'''
	
	def __init__( self, lhs, rhs ) :
		'''lhs, rhs are Expr's, the operands'''
		
		# test type here?
		# if type( lhs ) == type( Expr ) :
		self.lhs = lhs
		self.rhs = rhs
	
	def eval( self, nt ) :
		if isinstance(self.lhs, ListType) or isinstance(self.rhs, ListType) :
			print('Multiplication can only occur with integers or variables containing integers!')
			return None

		return self.lhs.eval( nt) * self.rhs.eval( nt )
	
	def display( self, nt, depth=0 ) :
		print "%sMULT" % (tabstop*depth)
		self.lhs.display( nt, depth+1 )
		self.rhs.display( nt, depth+1 )
#print "%s= %i" % (tabstop*depth, self.eval( nt, ft ))

class Plus( Expr ) :
	'''expression for binary addition'''
	
	def __init__( self, lhs, rhs ) :
		self.lhs = lhs
		self.rhs = rhs
	
	def eval( self, nt ) :
		if isinstance(self.lhs, ListType) or isinstance(self.rhs, ListType) :
			print('Addition can only occur with integers or variables containing integers!')
			return None

		return self.lhs.eval( nt) + self.rhs.eval( nt )
	
	def display( self, nt, depth=0 ) :
		print "%sADD" % (tabstop*depth)
		self.lhs.display( nt, depth+1 )
		self.rhs.display( nt, depth+1 )
#print "%s= %i" % (tabstop*depth, self.eval( nt, ft ))


class Minus( Expr ) :
	'''expression for binary subtraction'''
	
	def __init__( self, lhs, rhs ) :
		self.lhs = lhs
		self.rhs = rhs
	
	def eval( self, nt ) :
		if isinstance(self.lhs, ListType) or isinstance(self.rhs, ListType) :
			print('Subtraction can only occur with integers or variables containing integers!')
			return None

		return self.lhs.eval( nt ) - self.rhs.eval( nt )
	
	def display( self, nt, depth=0 ) :
		print "%sSUB" % (tabstop*depth)
		self.lhs.display( nt, depth+1 )
		self.rhs.display( nt, depth+1 )
#print "%s= %i" % (tabstop*depth, self.eval( nt, ft ))


class FunCall( Expr ) :
	'''stores a function call:
          - its name, and arguments'''
	
	def __init__( self, name, argList=[] ) :
		self.name = name
		self.builtins = ['cons', 'car', 'cdr', 'nullp', 'intp', 'listp']
		if argList==[]:
			self.argList = argList[:]
		else:
			self.argList = argList
	
	def eval( self, nt ) :
		# Used for "built-in" functions
		if self.name in self.builtins :
			param1 = None
			param2 = None

			if len(self.argList) == 0 :
				print('Built-in statements require at least one argument!')
				return None
			
			if len(self.argList) > 0 :
				param1 = self.argList[0].eval( nt )
			
			if len(self.argList) > 1 :
				param2 = self.argList[1].eval( nt )

			# Adds param1 (int / list) to the list in param2
			if self.name == 'cons' :
				if type(param2) ==type([]) :
					return common.cons(param1, param2)
				else :
					print('cons error: Must specify two parameters and the second parameter must be a list')
					return None
			# Returns the first element in the list
			elif self.name == 'car' :
				# Make sure this is a list first
				if type(param1) is list :
					return common.car(param1)
				else :
					print('car error: Must specify a list as a parameter')
					return None
			# Returns the rest of the list (minus the first element)
			elif self.name == 'cdr' :
				# Make sure this is a list first
				if type(param1) is list :
					return common.cdr(param1)
				else :
					print('cdr error: Must specify a list as a parameter')
					return None
			# Returns 1 if param1 is null, 0 otherwise
			elif self.name == 'nullp' :
				return common.nullp(param1)
			# Returns 1 if param1 is an integer, 0 otherwise
			elif self.name == 'intp' :
				return common.intp(param1)
			# Returns 1 if param1 is a list, 0 otherwise
			elif self.name == 'listp' :
				return common.listp(param1)	
		# Used for user-defined functions
		else :
			return nt.get(self.name).apply( nt,self.argList )

	def display( self,  depth=0 ) :
		print "%sFunction Call: %s, args:" % (tabstop*depth, self.name)
		for e in self.argList :
			e.display( nt,  depth+1 )

class PropFunCall( Expr ) :
	'''stores a function call:
          - its name, and arguments'''
	
	def __init__( self, prop, argList=[] ) :
		self.prop = prop
		if argList==[]:
			self.argList = argList[:]
		else:
			self.argList = argList
	
	def eval( self, nt ) :
		return self.prop.eval(nt).apply( nt,self.argList )

	def display( self,  depth=0 ) :
		print "%sFunction Call: %s, args:" % (tabstop*depth, self.name)
		for e in self.argList :
			e.display( nt,  depth+1 )


class Proc(Expr) :
	'''stores a procedure (formal params, and the body)
		
		Note that, while each function gets its own environment, we decided not to
		allow side-effects, so, no access to any outer contexts.  Thus, nesting
		functions is legal, but no different than defining them all in the global
		environment.  Further, all calls are handled the same way, regardless of
		the calling environment (after the actual args are evaluated); the proc
		doesn't need/want/get an outside environment.'''
	
	def __init__( self,body, paramList=[] ) :
		'''expects a list of formal parameters (variables, as strings), and a
			StmtList'''
		
		if paramList==[]:
			self.parList = paramList[:]
		else:
			self.parList = paramList
		self.body = body

	def eval( self ,nt):
		newEnv = Environment(nt)
		self.env=newEnv
		return self
	
	def apply( self, nt, args ) :
				# sanity check, # of args
		if len( args ) is not len( self.parList ) :
			print "Param count does not match:"
			sys.exit( 1 )
		
		# bind parameters in new name table (the only things there right now)
		for i in range( len( args )) :
			self.env.set(self.parList[i], args[i].eval( nt))
		
		# KS Don't know what I was doin' here, but it's wrong 3/08
		# Thank you, Charles
		#[ newContext.__setitem__(p,a.eval( nt, ft ))
		#		for p in self.parList for a in args ]
		
		# evaluate the function body using the new name table and the old (only)
		# function table.  Note that the proc's return value is stored as
		# 'return in its nametable
		
		self.body.eval( self.env )
		try:
			store=self.env.get( returnSymbol )
			return store
		except:
			pass
		print "Error:  no return value"
		sys.exit( 2 )
	
	def display( self, nt,depth=0 ) :
		print "%sPROC %s :" % (tabstop*depth, str(self.parList))
		self.body.display( nt, depth+1 )

class Property(Expr):
	def __init__(self, string):
		string=string.split('.')
		self.objName=string[0]
		self.propName=string[1]
	
	def eval(self,nt):
		return nt.get(self.objName).getSub(self.propName,nt)

	def display(self, nt, depth=0):
		print "%sProperty %s :" % (tabstop*depth, str(self.objName)+"."+str(self.proName))

class Class() :
	def __init__( self,name, paramList, body,superClassName=None ) :
		self.name=name
		self.parList = paramList
		self.body = body
		self.superClassName=superClassName

	def eval( self ,nt):
		nt.set(self.name, self)
		self.env=nt
	
	def apply( self, nt, args) :
		t=copy.deepcopy(self)
		t.env = Environment(t.env)
		if len( args ) is not len( t.parList ) :
			print "Param count does not match:"
			sys.exit( 1 )
				# sanity check, # of args
				
		# bind parameters in new name table (the only things there right now)
		for i in range( len( args )) :
			t.env.set(t.parList[i], args[i].eval( nt))

		if t.superClassName is not None:
			sc=t.env.get(t.superClassName)
			newArgs=[]
			for i in sc.parList:
				newArgs.append(Ident(i))
			t.superClass=sc.apply(t.env,newArgs)
		else:
			t.superClass=None

		
		# KS Don't know what I was doin' here, but it's wrong 3/08
		# Thank you, Charles
		#[ newContext.__setitem__(p,a.eval( nt, ft ))
		#		for p in self.parList for a in args ]
		
		# evaluate the function body using the new name table and the old (only)
		# function table.  Note that the proc's return value is stored as
		# 'return in its nametable
		
		t.body.eval( t.env )
		return t
	
	def getSub(self,sub, nt):
		try:
			return self.env.env[0][sub]
		except:
			pass
		try:
			return self.superClass.getSub(sub,nt)
		except:
			raise LookupError("Class does not have the given property or method")

	def display( self, nt,depth=0 ) :
		print "%sPROC %s :" % (tabstop*depth, str(self.parList))
		self.body.display( nt, depth+1 )

#-------------------------------------------------------

class Stmt :
	'''Virtual base class for statements in the language'''
	
	def __init__( self ) :
		raise NotImplementedError(
							 'Stmt: pure virtual base class.  Do not instantiate' )
	
	def eval( self, nt) :
		'''Given an environment and a function table, evaluates the expression,
			returns the value of the expression (an int in this grammar)'''
		
		raise NotImplementedError(
							 'Stmt.eval: virtual method.  Must be overridden.' )
	
	def display( self, nt,depth=0 ) :
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
	
	def eval( self, nt) :
		nt.set(self.name,self.rhs.eval( nt))

	def display( self, nt, depth=0 ) :
		print "%sAssign: %s :=" % (tabstop*depth, self.name)
		self.rhs.display( nt, depth+1 )

class IfStmt( Stmt ) :
	
	def __init__( self, cond, tBody, fBody ) :
		'''expects:
			cond - expression (integer)
			tBody - StmtList
			fBody - StmtList'''
		
		self.cond = cond
		self.tBody = tBody
		self.fBody = fBody
	
	def eval( self, nt) :
		if self.cond.eval( nt) > 0 :
			self.tBody.eval( nt )
		else :
			self.fBody.eval( nt )
	
	def display( self, nt,  depth=0 ) :
		print "%sIF" % (tabstop*depth)
		self.cond.display( nt, depth+1 )
		print "%sTHEN" % (tabstop*depth)
		self.tBody.display( nt, depth+1 )
		print "%sELSE" % (tabstop*depth)
		self.fBody.display( nt, depth+1 )


class WhileStmt( Stmt ) :
	
	def __init__( self, cond, body ) :
		self.cond = cond
		self.body = body
	
	def eval( self, nt ) :
		while self.cond.eval( nt ) > 0 :
			self.body.eval( nt )
	
	def display( self, nt, depth=0 ) :
		print "%sWHILE" % (tabstop*depth)
		self.cond.display( nt, depth+1 )
		print "%sDO" % (tabstop*depth)
		self.body.display( nt, depth+1 )

#-------------------------------------------------------

class StmtList :
	'''builds/stores a list of Stmts'''
	
	def __init__( self ) :
		self.sl = []
	
	def insert( self, stmt ) :
		self.sl.insert( 0, stmt )
	
	def eval( self, nt ) :
		for s in self.sl :
			s.eval( nt )
	
	def display( self, nt, depth=0 ) :
		print "%sSTMT LIST" % (tabstop*depth)
		for s in self.sl :
			s.display( nt, depth+1 )



class Program :
	
	def __init__( self, stmtList ) :
		self.stmtList = stmtList
		self.nameTable = Environment()
	
	def eval( self ) :
		self.stmtList.eval( self.nameTable )
	
	def dump( self ) :
		print "Dump of Symbol Table"
		print self.nameTable
	
	def display( self, depth=0 ) :
		print "%sPROGRAM :" % (tabstop*depth)
		self.stmtList.display( self.nameTable)

class Environment :
	def __init__(self,copy=None):
		if copy==None:
			self.env=[{}]
		else:
			self.env=[{},copy]
	
	def get(self,ident):
		try:
			store=self.env[0][ident]
			return store;
		except:
			pass
		try:
			store=self.env[1].get(ident)
		except:
			raise LookupError("Identifier not in the environment")
		return store

	def set(self,ident,value):
		try:
			self.get(ident)
			try:
				a=self.env[0][ident]
				self.env[0][ident]=value
			except:
				self.env[1].set(ident,value)
		except:
			self.env[0][ident]=value

	def __str__(self):
		s=''
		s+=str(self.env[0])
		try:
			s+=','+str(self.env[1])
		except:
			pass
		return s
