(define (boolexp expr)
   (cond ((list? expr)
      (cond ((eq? (car expr) 'boolexp) (boolexp (cadr expr)))
            ((eq? (car expr) 'and) (eval-and (cdr expr)))
            ((eq? (car expr) 'or) (eval-or (cdr expr)))
            ((eq? (car expr) 'not) (eval-not (cadr expr)))
            ((eq? (car expr) 'implies) (eval-implies (cadr expr) (car (reverse expr))))
            ((eq? (car expr) 'equiv) (eval-equiv (cadr expr) (car (reverse expr))))
            ((boolean? (car expr)) (car expr))
            ((list? (car expr)) (boolexp (car expr)))))
          ((boolean? expr) expr)
          (else "Symbol Error")))
 
(define (eval-and expr)
   (if (null? (cdr expr))
      (boolexp expr)
      (and (boolexp (car expr)) (eval-and (cdr expr)))))
 
(define (eval-or expr)
   (if (null? (cdr expr))
      (boolexp expr)
      (or (boolexp (car expr)) (eval-or (cdr expr)))))
 
(define (eval-not expr)
   (not (boolexp expr)))
 
(define (eval-implies expr1 expr2)
   (cond ((and (eq? (boolexp expr1) #t) (eq? (boolexp expr2) #t)) #t)
         ((and (eq? (boolexp expr1) #t) (eq? (boolexp expr2) #f)) #f)
         ((and (eq? (boolexp expr1) #f) (eq? (boolexp expr2) #t)) #t)
         ((and (eq? (boolexp expr1) #f) (eq? (boolexp expr2) #f)) #t)
         (else "Symbol Error")))
 
(define (eval-equiv expr1 expr2)
   (cond ((and (eq? (boolexp expr1) #t) (eq? (boolexp expr2) #t)) #t)
         ((and (eq? (boolexp expr1) #t) (eq? (boolexp expr2) #f)) #f)
         ((and (eq? (boolexp expr1) #f) (eq? (boolexp expr2) #t)) #f)
         ((and (eq? (boolexp expr1) #f) (eq? (boolexp expr2) #f)) #t)
         (else "Symbol Error")))
 
(define P #t)
 
(define Q #f)
 
(define negativeTest 348284)
 
(define simpleTest (list 'boolexp P))
 
(define andTest (list 'and P Q))
 
(define orTest (list 'or P Q))
 
(define notTest (list 'not P))
 
(define simpleTest (list 'not P))
 
(define impliesTest (list 'implies P Q))
 
(define equivTest (list 'equiv Q Q))
 
(define taut1 (list 'or P (list 'not P)))
 
(define taut2 (list 'equiv (list 'or P Q) (list 'or Q P)))
 
(define taut3 (list 'equiv (list 'or P Q) (list 'or P (list 'and (list 'not P) Q))))