###############################################
# Group 8
# Assignment 2
#
# List Processing in the Mini Language
################################################

VIEW=more

all: view-part1 build view-func1 view-func2 view-part2 run-part2 clean
.PHONY : all

run: oop_interpreterext.py
	python oop_interpreterext.py

view-semantics: semantics
	cat semantics

view-implementation: implementation
	cat implementation

view-code: common.py oop_interpreterext.py oop_programext.py
	cat common.py
	cat oop_interpreterext.py
	cat oop_programext.py

view-tests: testDescriptions
	cat testDescriptions

clean:
	-@rm parser.out 2> /dev/null
	-@rm parsetab.* 2> /dev/null
	-@rm *.pyc 2> /dev/null
