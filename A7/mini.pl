% Part I of assignment 4
% reduction rules for arithmetic expressions.
% Author: Jeremy Johnson

% test cases.
%
% reduce_all(times(plus(2,3),minus(5,1)),V).
%    V = 20 ?
%

reduce(config(plus(E,E2),Env),config(plus(E1,E2),Env)) :- reduce(config(E,Env),config(E1,Env)).
reduce(config(I,Env),config(V,Env)) :- atom(I), lookup(Env,I,V).

reduce(plus(E,E2),plus(E1,E2)) :- reduce(E,E1).
reduce(minus(E,E2),minus(E1,E2)) :- reduce(E,E1).
reduce(times(E,E2),times(E1,E2)) :- reduce(E,E1).

reduce(plus(V,E),plus(V,E1)) :- reduce(E,E1).
reduce(minus(V,E),minus(V,E1)) :- reduce(E,E1).
reduce(times(V,E),times(V,E1)) :- reduce(E,E1).

reduce(plus(V1,V2),R) :- integer(V1), integer(V2), !, R is V1+V2.
reduce(minus(V1,V2),R) :- integer(V1), integer(V2), !, R is V1-V2.
reduce(times(V1,V2),R) :- integer(V1), integer(V2), !, R is V1*V2.

reduce_value(config(E,Env),V) :- reduce_all(config(E,Env),config(V,Env)).

reduce_all(config(V,Env),config(V,Env)) :- integer(V), !.
reduce_all(config(E,Env),config(E2,Env)) :- reduce(config(E,Env),config(E1,Env)),
reduce_all(config(E1,Env),config(E2,Env)).
reduce_all(V,V) :- integer(V), !.
reduce_all(E,E2) :- reduce(E,E1), reduce_all(E1,E2).