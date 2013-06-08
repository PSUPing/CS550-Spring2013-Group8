(assert! (rule (append-to-form () ?x ?x)))

(assert! (rule (append-to-form (?a . ?b) ?c (?a . ?d))
	(append-to-form ?b ?c ?d)))

(assert! (rule (reverse () ())))

(assert! (rule (reverse (?head . ?tail) ?q)
	(and (reverse ?tail ?rtail)
		(append-to-form ?rtail (?head) ?q))))
