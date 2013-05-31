###############################################
# Group 8
# Assignment 2
#
# List Processing in the Mini Language
################################################

VIEW=more

all: view-part1 build view-func1 view-func2 view-part2 run-part2 clean
.PHONY : all

compile-static:
	echo "no need to compile"

compile-dynamic:
	echo "no need to compile"

run-static: static_interpreterext.py
	python static_interpreterext.py

run-dynamic: dynamic_interpreterext.py
	python dynamic_interpreterext.py

view: dynamic_interpreterext.py static_interpreterext.py static_programext.py dynamic_programext.py common.py
	more static_interpreterext.py
	more static_programext.py
	more dynamic_interpreterext.py
	more dynamic_programext.py
	more common.py

clean:
	-@rm parser.out 2> /dev/null
	-@rm parsetab.* 2> /dev/null
	-@rm *.pyc 2> /dev/null
