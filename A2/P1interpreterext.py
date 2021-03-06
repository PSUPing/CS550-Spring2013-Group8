#!/usr/bin/python
#
# exp2.py - Demonstration of a scanner and generator parser in Python
#               See cs550/Lectures/grammars/exp2.{l,y}
#               Uses an unambiguous grammar
#
#       See http://www.dabeaz.com/ply/ply.html for explanations and a similar (but
#       cooler) example.
#
# Kurt Schmidt
# 7/07
#
# EDITOR:  cols=80, tabstop=2
#
# NOTES:
#               the display() method everybody has is just to graphically spit the
#               actual parse tree to the screen
#
#               The grammar can be found in programext.py  (probably should be here)
#
#

import sys
from P1programext import *
import common

######   LEXER   ###############################
# Note:  This is precisely the same lexer that exp1 uses.  Could've pulled
# it out to a different file.

from ply import lex

tokens = (
		'PLUS',
		'MINUS',
		'TIMES',
		'LPAREN',
		'RPAREN',
		'LBRACKET',
		'RBRACKET',
		'SEMICOLON',
		'COMMA',
		'NUMBER',
		'ASSIGNOP',
		'WHILE',
		'DO',
		'OD',
		'IF',
		'THEN',
		'ELSE',
		'FI',
		'DEFINE',
		'PROC',
		'END',
		'IDENT',
		'CONCAT'
		)

# These are all caught in the IDENT rule, typed there.
reserved = {
	'while'		: 'WHILE',
	'do'			: 'DO',
	'od'			: 'OD',
	'if'			: 'IF',
	'then'		: 'THEN',
	'else'		: 'ELSE',
	'fi'			: 'FI',
	'define'		: 'DEFINE',
	'proc'		: 'PROC',
	'end'		: 'END'
}

# Now, this section.  We have a mapping, REs to token types (please note
# the t_ prefix).  They simply return the type.

# t_ignore is special, and does just what it says.  Spaces and tabs
t_ignore = ' \t\n\r'

# These are the simple maps
t_PLUS          = r'\+'
t_MINUS         = r'-'
t_TIMES         = r'\*'
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LBRACKET      = r'\['
t_RBRACKET      = r'\]'
t_ASSIGNOP      = r':='
t_SEMICOLON     = r';'
t_COMMA         = r','

def t_IDENT( t ):
	#r'[a-zA-Z_][a-zA-Z_0-9]*'
	r'[a-z]+'
	t.type = reserved.get( t.value, 'IDENT' )    # Check for reserved words
	return t

def t_CONCAT( t ) :
	'\|\|'
	return t

def t_NUMBER( t ) :
	r'[0-9]+'
	
	# t.value holds the string that matched.  Dynamic typing - no unions
	t.value = int( t.value )
	return t

# These are standard little ditties:
def t_newline( t ):
	r'\n+'
	t.lexer.lineno += len( t.value )

# Error handling rule
def t_error( t ):
	print "Illegal character '%s' on line %d" % ( t.value[0], t.lexer.lineno )
	return t
#t.lexer.skip( 1 )

lex.lex()

#-----   LEXER (end)   -------------------------------


######   YACC   #####################################

import ply.yacc as yacc

# create a function for each production (note the prefix)
# The rule is given in the doc string

def p_program( p ) :
	'program : stmt_list'
	P = Program( p[1] )
	#P.display()
	print 'Running Program'
	P.eval()
	P.dump()

def p_stmt_list( p ) :
	'''stmt_list : stmt SEMICOLON stmt_list 
		| stmt'''
	if len( p ) == 2 :  # single stmt => new list
		p[0] = StmtList()
		p[0].insert( p[1] )
	else :  # we have a stmtList, keep adding to front
		p[3].insert( p[1] )
		p[0] = p[3]

def p_stmt( p ) :
	'''stmt : assign_stmt
		| while_stmt
		| if_stmt
		| define_stmt'''
	p[0] = p[1]

def p_add( p ) :
	'expr : expr PLUS term'
	p[0] = Plus( p[1], p[3] )

def p_sub( p ) :
	'expr : expr MINUS term'
	p[0] = Minus( p[1], p[3] )

def p_expr_list( p ) :
	'''expr_list : expr COMMA expr_list
		| expr'''
	if len( p ) == 2 :  # single expr => new list
		p[0] = [ p[1] ]
	else :  # we have a expr_list, keep adding to front
		p[3].insert( 0, p[1] )
		p[0] = p[3]

def p_expr_term( p ) :
	'expr : term'
	p[0] = p[1]

def p_mult( p ) :
	'''term : term TIMES fact'''
	p[0] = Times( p[1], p[3] )

def p_term_CONCAT( p ) :
	'''term : term CONCAT fact'''
	p[0] = Concat( p[1], p[3] )
	
def p_term_fact( p ) :
	'term : fact'
	p[0] = p[1]

def p_fact_expr( p ) :
	'fact : LPAREN expr RPAREN'
	p[0] = p[2]

def p_fact_NUM( p ) :
	'fact : NUMBER'
	p[0] = Number( p[1] )

def p_fact_IDENT( p ) :
	'fact : IDENT'
	p[0] = Ident( p[1] )

def p_fact_list( p ) : 
	'fact : list'
	p[0] = p[1]
	
def p_fact_funcall( p ) :
	'fact : func_call'
	p[0] = p[1]

def p_assn( p ) :
	'assign_stmt : IDENT ASSIGNOP expr'
	p[0] = AssignStmt( p[1], p[3] )

def p_while( p ) :
	'while_stmt : WHILE expr DO stmt_list OD'
	p[0] = WhileStmt( p[2], p[4] )

def p_if( p ) :
	'if_stmt : IF expr THEN stmt_list ELSE stmt_list FI'
	p[0] = IfStmt( p[2], p[4], p[6] )

def p_def( p ) :
	'define_stmt : DEFINE IDENT PROC LPAREN param_list RPAREN stmt_list END'
	p[0] = DefineStmt( p[2], Proc( p[5], p[7] ))

def p_param_list( p ) :
	'''param_list : IDENT COMMA param_list
		| IDENT'''
	if len( p ) == 2 :  # single param => new list
		p[0] = [ p[1] ]
	else :  # we have a param_list, keep adding to front
		p[3].insert( 0, p[1] )
		p[0] = p[3]

def p_list(p):
	'''list : LBRACKET sequence RBRACKET
		| LBRACKET RBRACKET'''
	if len(p) == 4 :
		p[0] = ListType(p[2])
	else :
		p[0] = ListType()

def p_sequence(p):
	'''sequence : listelement COMMA sequence
		| listelement'''
	# If the array is lenght 4, it's a listelement and sequence,
	# otherwise, it is only a 'listelement'
	if len(p) == 4 :
		p[0] = []
		
		# Since a class is being used, its list variable must be accessed
		# explicitly.  This if-elif-else block handles all the different
		# combinations.
		if isinstance(p[1], ListType) and type(p[3]) is int :
			p[0].insert(0, p[3])
			p[0].insert(0, p[1].listVals)
		elif type(p[1]) is int and isinstance(p[3], ListType) :
			p[0].insert(0, p[3].listVals)
			p[0].insert(0, p[1])
		elif isinstance(p[1], ListType) and type(p[3]) is list :
			p[3].insert(0, p[1].listVals)
			p[0] = p[3]
		elif type(p[1]) is list and isinstance(p[3], ListType) :
			p[1].insert(0, p[3].listVals)
			p[0] = p[3]
		elif type(p[1]) is list and type(p[3]) is int :
			p[1].insert(0, p[3])
			p[0] = p[1]
		elif type(p[1]) is int and type(p[3]) is list :
			p[3].insert(0, p[1])
			p[0] = p[3]
		else :
			p[0].insert(0, p[3])
			p[0].insert(0, p[1])
	else :
		p[0] = p[1]

def p_listelement(p):
	'''listelement : list
		| NUMBER'''
	p[0] = p[1]

def p_func_call( p ) :
	'func_call : IDENT LPAREN expr_list RPAREN'
	p[0] = FunCall( p[1], p[3] )

# Error rule for syntax errors
def p_error( p ):
	print "Syntax error in input!", str( p )
	sys.exit( 2 )

# now, build the parser
yacc.yacc()
data = sys.stdin.read()
yacc.parse( data )
