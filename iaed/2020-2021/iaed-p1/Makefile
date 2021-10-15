CONFIG=config
include ${CONFIG}
CC=gcc
CFLAGS=-Wall -Wextra -Werror -ansi -pedantic -g

all::
	$(MAKE) $(MFLAGS) -C $(PROJECT_PATH)
	cp $(PROJECT_PATH)$(FILE_NAME) proj1
	$(MAKE) $(MFLAGS) -C tests
clean::
	rm -f proj1 tests/*.diff tests/*.myout
