;;;; Main Program Functions
 
(define (eval prog env)
	(begin (eval-stmt-list prog env)
		   (display env)))
 
;;;; Statement Functions
 
(define (eval-stmt-list expr env)
	(if (list? expr)
		(eval-stmt-seq expr env)
		"Bad Input"))
 
(define (eval-stmt-seq expr env)
	 (if (stmt? expr)
		 (eval-stmt expr env)
         (begin (eval-stmt (car expr) env)
				(if (not (null? (cdr expr))) (eval-stmt-seq (cdr expr) env)))))
 
(define (stmt? expr)
	(if (list? expr)
    	(or (assign? expr) (if? expr) (while? expr))
        #f))
 
(define (eval-stmt expr env)
	(cond ((assign? expr) (eval-assign expr env))
		  ((if? expr) (eval-if expr env))
          ((while? expr) (eval-while expr env))
          (else "Bad Input")))
 
;;;; Assign Statement Functions and Environment Functions
 
(define (assign? expr)
	(reservedWord? expr 'assign))
 
(define (eval-assign expr env)
	(store-variable-value env (cadr expr) (eval-expr (car (reverse expr)) env)))
 
(define (lookup-variable-value env varName)
	(if (null? env)
    	#f
        (if (eq? (car (car env)) varName)
        	(cadr (car env))
            (lookup-variable-value (cdr env) varName))))
 
(define (store-variable-value env varName varValue)
	(if (null? env)
    	(set! env (cons (list varName varValue) env))
        (if (eq? (car (car env)) varName)
        	(set-car! env (list varName varValue))
            (store-variable-value (cdr env) varName varValue))))
 
;;;; If Statement Functions
 
(define (if? expr)
	(reservedWord? expr 'if))
 
(define (eval-if expr env)
	(if (> (eval-expr (cadr expr) env) 0)
		(eval-stmt-list (car (cdr (reverse expr))) env)
		(eval-stmt-list (car (reverse expr)) env)))
 
;;;; While Statement Functions
 
(define (while? expr)
	(reservedWord? expr 'while))
 
(define (eval-while expr env)
	(if (> (eval-expr (cadr expr) env) 0)
		(begin (eval-stmt-list (car (reverse expr)) env)
			   (eval-while expr env))))
 
;;;; Expression Functions
 
(define (eval-expr expr env)
	(cond ((integer? expr) expr)
		  ((or (string? expr) (symbol? expr)) (lookup-variable-value env expr))
		  ((list? expr)
		  		(cond ((eq? (car expr) '+) (eval-add (cadr expr) (car (reverse expr)) env))
					  ((eq? (car expr) '-) (eval-sub (cadr expr) (car (reverse expr)) env))
                      ((eq? (car expr) '*) (eval-mul (cadr expr) (car (reverse expr)) env))
                      (else "Bad Symbol")))
				(else "Bad Input")))
 
(define (eval-add expr1 expr2 env)
	(+ (eval-expr expr1 env) (eval-expr expr2 env)))
 
(define (eval-sub expr1 expr2 env)
	(- (eval-expr expr1 env) (eval-expr expr2 env)))
 
(define (eval-mul expr1 expr2 env)
	(* (eval-expr expr1 env) (eval-expr expr2 env)))
 
;;;; Helper Function
 
(define (reservedWord? expr stmt)
	(if (list? expr)
		(if (eq? (car expr) stmt)
			#t
            #f)
		"Bad Input"))
 
(define env '())  ;;;; Base Environment Definition - DO NOT DELETE!!!
 
;;;; Variables for testing
 
(define env '((test1 5) (i 7) (q 0)))
 
(define evalIntTest 1)
 
(define evalAddTest '(+ 2 3))
 
(define evalSubTest '(- 2 3))
 
(define evalMulTest '(* 2 3))
 
(define evalExprTest '(+ 2 i))
 
(define assignNewTest '(assign test3 22))
 
(define assignExistTest '(assign i 10))
 
(define assignExistTest2 '(assign test1 1))
 
(define ifTest '(if i (assign i (- i 1)) (assign q (+ q 2))))
 
(define elseTest '(if i (assign q (- q 1)) (assign i (+ i 2))))
 
(define whileTest '(while i (assign i (- i 1))))
 
(define stmtSeqTest (list assignExistTest assignExistTest2))
 
(define progTest (list assignExistTest ifTest whileTest))
