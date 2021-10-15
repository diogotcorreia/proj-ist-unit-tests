# Copyright (C) 2021, Pedro Reis dos Santos
.SUFFIXES: .in .out .diff
MAKEFLAGS += --no-print-directory # No entering and leaving messages
GREEN=$(shell tput setaf 2)
RED=$(shell tput setaf 1)
RESET=$(shell tput op)
OK="$(GREEN)test $< PASSED$(RESET)"
KO="$(RED)test $< FAILED$(RESET)"
EXE=../proj1

all:: clean # run regression tests
	@$(MAKE) $(MFLAGS) `ls *.in | sed -e "s/in/diff/"`

.in.diff:
	@-$(EXE) < $< | diff - $*.out > $@
	@if [ `wc -l < $@` -eq 0 ]; then echo $(OK); else echo $(KO); fi;

clean::
	rm -f *.diff
