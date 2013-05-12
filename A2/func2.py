import P1interpreterext

func2 = "list := [1, 2]; define listlen proc ( listparam ) if nullp(listparam) then return := 0 - 1 else listparam := cdr(listparam); return := 1 + listlen(listparam) fi end; x := listlen(list)"

P1interpreterext.interpret(func2)