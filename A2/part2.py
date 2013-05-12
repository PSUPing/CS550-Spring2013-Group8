#!/usr/bin/env python
import P2interpreterext

inputToParse = raw_input('Please input your mini-language program: ')
#'list := [1, 2]; listconcat := list || [3, 4, 5]; consres := cons(6, list); carres := car(list); cdrres := cdr(list); nullpres := nullp(list); intpres := intp(list); listpres := listp(list); inttest := 5; intnullpres := nullp(inttest); intintpres := intp(inttest); intlistpres := listp(inttest)'

P2interpreterext.interpret(inputToParse)
