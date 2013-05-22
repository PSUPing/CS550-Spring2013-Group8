(define (assign? expr)
	(reservedWord? expr 'assign))

(define (lookup-variable env varName)
	(if (eq? (car env) varName)
		(car (cdr env))
		(if (null? (cdr (cdr env)))
			#f
			(lookup-variable (cdr (cdr env)) varName))))

(define env (list 'test1 5 'i 7))

(define (store-variable env varName val)
	(define env (cons env (store-variable-value varName val))))

(define (store-variable-value varName val)
	(cons varName val))

(define (if? expr)
	(reservedWord? expr 'if))

(define (eval-if expr)
	(if (> (eval-expr (cadr expr)) 0)
          (eval-if-consequent (car (cdr (reverse expr))))
          (eval-if-alternative (car (reverse expr)))))

(define (eval-if-consequent expr)
	(eval-expr expr))

(define (eval-if-alternative expr)
	(eval-expr expr))

(define (eval-expr expr)
	(if (or (integer? expr) (string? expr))
		expr
		(if (list? expr)
			(cond ((eq? (car expr) '+) (eval-add (cadr expr) (car (reverse expr))))
				  ((eq? (car expr) '-) (eval-sub (cadr expr) (car (reverse expr))))
				  ((eq? (car expr) '*) (eval-mul (cadr expr) (car (reverse expr))))
				  (else "Bad Symbol"))
		    (else "Bad Input"))))

(define (while? expr)
	(reservedWord? expr 'while))

(define (eval-while expr)
	(if (> (eval-expr (cadr expr)) 0)
		((eval-expr (car (reverse)))
		(eval-while))))

(define (reservedWord? expr stmt)
	(if (list? expr)
		(if (eq? (car expr) stmt)
			#t
			#f)
		"Bad Input"))

(define (eval-add expr1 expr2)
	(+ (eval-expr expr1) (eval-expr expr2)))

(define (eval-sub expr1 expr2)
	(- (eval-expr expr1) (eval-expr expr2)))

(define (eval-mul expr1 expr2)
	(* (eval-expr expr1) (eval-expr expr2)))

(define evalIntTest 1)

(define evalAddTest (list '+ 2 3))

(define evalSubTest (list '- 2 3))

(define evalMulTest (list '* 2 3))

(define ifTest (list 'if 2 (list '+ 2 3) (list '- 2 3)))

(define elseTest (list 'if 0 (list '+ 2 3) (list '- 2 3)))

;;;;(define whileTest (list 'while 'i (list 'assign i (list '- i 1))))
