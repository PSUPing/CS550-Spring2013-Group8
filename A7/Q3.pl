my_reverse([],[]).
my_reverse([H|T],R) :- my_reverse(T,T2),append(T2,[H],R).