VIEW=more

all: view compile view-trans view-link view-op run run-op clean
	.PHONY : all

mem-size:
	echo $$RAM_MEM
view: compiler.py link.py interpreter.py programext.py
	$(VIEW) compiler.py link.py interpreter.py programext.py
compile: compiler.py link.py interpreter.py programext.py
	python compiler.py -v -o simulator/prog.txt -m $$RAM_MEM
view-trans: compiler.py link.py interpreter.py programext.py 
	python compiler.py --trans -m $$RAM_MEM
view-link: compiler.py link.py interpreter.py programext.py
	python compiler.py --link -m $$RAM_MEM
run: compiler.py link.py interpreter.py programext.py	
	python compiler.py -o simulator/prog.txt -m $$RAM_MEM
	~jjohnson/bin/ram simulator/prog.txt simulator/mem.txt
clean:
	rm *.pyc *.out parsetab.py *~ -f
