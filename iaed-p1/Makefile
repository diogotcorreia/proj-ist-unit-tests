CONFIG=config
include ${CONFIG}
CC=gcc
CFLAGS=-Wall -Wextra -Werror -ansi -pedantic -g

all:: proj1
	$(MAKE) $(MFLAGS) -C $(PROJECT_PATH)
	cp $(PROJECT_PATH)$(FILE_NAME) proj1
	$(MAKE) $(MFLAGS) -C tests
proj1: $(PROJECT_PATH)*.c $(PROJECT_PATH)*.h
clean::
	rm -f proj1 tests/*.diff tests/*.myout
