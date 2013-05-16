VIEW=more

all: view compile view-trans view-link view-op run run-op clean
	.PHONY : all

view: compiler.py link.py peephole.py interpreter.py programext.py
	$(VIEW) compiler.py link.py peephole.py interpreter.py programext.py
compile: compiler.py link.py peephole.py interpreter.py programext.py
	python compiler.py -O -v -o simulator/prog.txt
view-trans: compiler.py link.py peephole.py interpreter.py programext.py 
	python compiler.py --trans
view-link: compiler.py link.py peephole.py interpreter.py programext.py
	python compiler.py --link
view-op: compiler.py link.py peephole.py interpreter.py programext.py
	python compiler.py --op
run: compiler.py link.py peephole.py interpreter.py programext.py simulator/main.cpp simulator/ram.cpp	
	g++ simulator/main.cpp simulator/ram.cpp -o simulator/sim
	python compiler.py -o simulator/prog.txt
	simulator/sim simulator/prog.txt simulator/mem.txt
run-op: compiler.py link.py peephole.py interpreter.py programext.py simulator/main.cpp simulator/ram.cpp	
	g++ simulator/main.cpp simulator/ram.cpp -o simulator/sim
	python compiler.py -O -o simulator/prog.txt
	simulator/sim simulator/prog.txt simulator/mem.txt
clean:
	rm *.pyc *.out parsetab.py *~ -f
