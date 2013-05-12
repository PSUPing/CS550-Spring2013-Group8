###############################################
# Group 8
# Assignment 2
#
# List Processing in the Mini Language
################################################

VIEW=more

all: view-part1 build view-func1 view-func2 view-part2 run-part2 clean
.PHONY : all

view-part1: common.py P1interpreterext.py P1programext.py
	$(VIEW) common.py
	$(VIEW) P1interpreterext.py
	$(VIEW) P1programext.py

build:
	echo "No need to build"

run-part1: P1interpreterext.py
	python P1interpreterext.py

view-func1: func1
	$(VIEW) func1

view-func2: func2
	$(VIEW) func2

view-part2: P2funcs.py
	$(VIEW) P2funcs.py

run-part2: P2interpreterext.py
	python P2interpreterext.py

clean:
	-@rm parser.out 2> /dev/null
	-@rm parsetab.* 2> /dev/null
	-@rm *.pyc 2> /dev/null
