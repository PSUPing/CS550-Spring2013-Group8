#!/usr/bin/python
#
# exp2.py - Demonstration of a scanner and generator parser in Python
#		See cs550/Lectures/grammars/exp2.{l,y}
#		Uses an unambiguous grammar
#
#	See http://www.dabeaz.com/ply/ply.html for explanations and a similar (but
#	cooler) example.
#
# Kurt Schmidt
# 7/07
#
# EDITOR:  cols=80, tabstop=2
#
# NOTES:
#		the display() method everybody has is just to graphically spit the
#		actual parse tree to the screen
#
#		The grammar can be found in programext.py  (probably should be here)
#
#

import sys
import peephole
import link
from programext import *

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
	'SEMICOLON',
	'NUMBER',
	'ASSIGNOP',
	'WHILE',
	'DO',
	'OD',
	'IF',
	'THEN',
	'ELSE',
	'FI',
	'IDENT'
)

	# These are all caught in the IDENT rule, typed there.
reserved = {
		'while' : 'WHILE',
		'do'		: 'DO',
		'od'		: 'OD',
		'if'		: 'IF',
		'then'	: 'THEN',
		'else'	: 'ELSE',
		'fi'		: 'FI',
		}

# Now, this section.  We have a mapping, REs to token types (please note
# the t_ prefix).  They simply return the type.

	# t_ignore is special, and does just what it says.  Spaces and tabs
t_ignore = ' \t'

	# These are the simple maps
t_PLUS		= r'\+'
t_MINUS   = r'-'
t_TIMES		= r'\*'
t_LPAREN	= r'\('
t_RPAREN	= r'\)'
t_ASSIGNOP = r':='
t_SEMICOLON = r';'

def t_IDENT( t ):
	#r'[a-zA-Z_][a-zA-Z_0-9]*'
	r'[a-z]+'
	t.type = reserved.get( t.value, 'IDENT' )    # Check for reserved words
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
	print 'Compiling Program'
	translate=P.translate()
	print translate+'\n'
	print 'Providing Peephole Optimization'
	peepholeCode = peephole.peephole(translate) + "\n"
	print(peepholeCode)
	print 'Linking Code'
	print(link.linker(peepholeCode, P.getMemory()))
	
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
				| if_stmt'''
	p[0] = p[1]

def p_add( p ) :
	'expr : expr PLUS term'
	p[0] = Plus( p[1], p[3] )

def p_sub( p ) :
	'expr : expr MINUS term'
	p[0] = Minus( p[1], p[3] )

def p_expr_term( p ) :
	'expr : term'
	p[0] = p[1]

def p_mult( p ) :
	'''term : term TIMES fact'''
	p[0] = Times( p[1], p[3] )

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

def p_assn( p ) :
	'assign_stmt : IDENT ASSIGNOP expr'
	p[0] = AssignStmt( p[1], p[3] )

def p_while( p ) :
	'while_stmt : WHILE expr DO stmt_list OD'
	p[0] = WhileStmt( p[2], p[4] )

def p_if( p ) :
	'if_stmt : IF expr THEN stmt_list ELSE stmt_list FI'
	p[0] = IfStmt( p[2], p[4], p[6] )

# Error rule for syntax errors
def p_error( p ):
	print "Syntax error in input!", str( p )
	sys.exit( 2 )

	# now, build the parser

def compile(stringToCompile) :
	yacc.yacc()
	yacc.parse(stringToCompile)

string1 = "i := 5; q := 0; while i do i := i - 1 od; if i then q := 1 + 5 else q := 1 - 5 fi; q := q * 2"

compile(string1)
