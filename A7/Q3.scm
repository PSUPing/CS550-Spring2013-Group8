(assert! (rule (reverse () ())))
(assert! (rule (reverse ?start . ?end) 
	(and (append-to-form (?head) ?rest ?start) 
		(append-to-form ?tail2 (?head) ?end) 
		(reverse ?rest ?tail2))))