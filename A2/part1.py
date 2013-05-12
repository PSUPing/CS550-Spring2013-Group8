import P1interpreterext

inputToParse =  raw_input('Please input your mini-language program: ')
#'list := [1, 2]; listconcat := list || [3, 4, 5]; consbadres := cons(0); consres := cons(6, list); carres := car(list); cdrres := cdr(list); nullpres := nullp(list); intpres := intp(list); listpres := listp(list); inttest := 5; intcarres := car(inttest); intcdrres := cdr(inttest); intnullpres := nullp(inttest); intintpres := intp(inttest); intlistpres := listp(inttest)'

P1interpreterext.interpret(inputToParse)
