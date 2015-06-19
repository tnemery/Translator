#--------------------------------------------
# INSTRUCTION
# Quoted strings are to be filled in by student
#
CCC = python
CCFLAGS = -g -Wall --pedantic-errors -Werror
OBJS = ""
SOURCE = lexer.py
RUNFLAGS = ""

$(OBJS): $(SOURCE)
	$(CCC) $(CCFLAGS) -c $(SOURCE)

compiler: $(OBJS)
	$(CCC) $(CCFLAGS) -o compiler $(OBJS)

clean: 
	rm -f *.o *.out
	ls

stutest.out:
	cat maintest.in
	python lexer.py maintest.in > maintest.out
	cat maintest.out
# Notice the next line. The `-' says to ignore the return code. This
# is a way to have multiple tests of errors that cause non-zero return
# codes.
#	cat stutest2.in
#	-compiler stutest2.in > stutest2.out
#	cat stutest2.out

proftest.out:
	cat proftest.in
	python lexer.py proftest.in > proftest.out
	cat proftest.out