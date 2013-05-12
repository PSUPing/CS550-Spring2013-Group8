import P1interpreterext

func1 = "list := [1, 2]; define listlen proc ( listparam ) return := 0; templist := listparam; i := listp(templist); while i do templist := cdr(templist); i := listp(templist); return := return + 1 od; return := return - 1 end; lenoflist := listlen(list)"

func1 = "define addr proc(n) if n then return := n + addr(n-1) else return := 0 fi end; n := 3; s := addr(n)"

P1interpreterext.interpret(func1)