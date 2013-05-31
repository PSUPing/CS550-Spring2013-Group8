import copy

#this file contains all the functions that are used to make and manipulate
#lists

#prepends e to L
def cons( e, L ) :
	tempList = L
	tempList.insert(0, e)
	return L

#returns the first element of L
def car( L ) :
	return L[0]

#returns the rest of the list L except for the first element
def cdr( L ) :
	tempList = copy.deepcopy(L)
	
	if len(L) > 0 :
		tempList.pop(0)
		return tempList
	else :
		return None

#returns true if L is None
def nullp( L ) :
	if L is None : return 1
	else : return 0

#returns true if e is an int
def intp( e ) :
	if type(e) is int : return 1
	else : return 0

#returns true if e is a list
def listp( e ) :
	if type(e) is list : return 1
	else : return 0
