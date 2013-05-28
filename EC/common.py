import copy

def cons( e, L ) :
	tempList = L
	tempList.insert(0, e)
	return L

def car( L ) :
	return L[0]

def cdr( L ) :
	tempList = copy.deepcopy(L)
	
	if len(L) > 0 :
		tempList.pop(0)
		return tempList
	else :
		return None

def nullp( L ) :
	if L is None : return 1
	else : return 0

def intp( e ) :
	if type(e) is int : return 1
	else : return 0

def listp( e ) :
	if type(e) is list : return 1
	else : return 0