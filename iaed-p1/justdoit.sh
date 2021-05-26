#!/bin/bash

### Make files are efficient and all but this is a tiny project, compiling it more times than necessary is not that much of a bother...
### Written by Raf 2021-03-29

exename="exe_tmp"

GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
NC="\033[0m"

# Valgrind flag: if valgrind is present in console, valgrind will be used when
# running the tests and count all memory leaks that appear
valgrind=${2:-false}
leak_count=0
mem_error_count=0

# CD into this script's directory
# There are several alternatives but this one seems to be the most compatible one
cd "$(dirname "${BASH_SOURCE[0]}")"

if [ $# -lt 1 ]; then
	echo Please provide the location of your .c files as an argument to this script!
	echo "Make sure it is a valid path (for example, ../proj)"
	echo "You can also provide 'clean' to get rid of those nasty .diff and .myout files!"
	exit
fi

rm -f tests/*.diff tests/*.myout

if [ "$1" = "clean" ]; then
	echo "All squeaky clean!"
	exit
fi

echo Hi $USER! Let\'s get this party started!

gcc -ansi -pedantic -Wall -Wextra -o $exename $1/*.c

passed=0
total=0

echo ----------

for tid in tests/*.in
do
	((total++))
	tid=$(basename -s .in $tid)
	if [ "$valgrind" == "valgrind" ]; then
		valgrind ./$exename < tests/$tid.in > tests/$tid.myout 2>valgrind.out
		grep -q "All heap blocks were freed -- no leaks are possible" valgrind.out
		result_leak=$?
		if [ "$result_leak" -gt 0 ]; then
			((leak_count++))
		fi
		grep -q "ERROR SUMMARY: 0 errors" valgrind.out
		result_mem=$?
		if [ "$result_mem" -gt 0 ]; then
			((mem_error_count++))
		fi
	else
		./$exename < tests/$tid.in > tests/$tid.myout
	fi
	diff -y --suppress-common-lines tests/$tid.myout tests/$tid.out > tests/$tid.diff # original didn't use -u but ok
	
	if [ "$(wc -l < tests/$tid.diff)" -eq 0 ]; then
		if [ "$valgrind" == "valgrind" ]; then
			if [ "$result_leak" -eq 0 ] && [ "$result_mem" -eq 0 ]; then
				status="${GREEN}PASSED. 0 MEMORY LEAKS/ERRORS${NC}"
			else
				status="${RED}PASSED. BUT WITH MEMORY LEAKS/ERRORS! ${NC}"
			fi
		else
			status="${GREEN}PASSED${NC}"
		fi
		((passed++))
	else
		status="${RED}FAILED${NC}"
	fi

	padding=""
	len="${#tid}"
	while [ $len -lt 5 ]; do
		padding=" $padding"
		((len++))
	done

	echo -e "> Test $tid$padding - $status"
done

rm -f $exename

echo ----------

if [ $passed -eq $total ]; then
	if [ "$valgrind" == "valgrind" ]; then
		if [ "$mem_error_count" -gt 0 ] || [ "$leak_count" -gt 0 ]; then
			echo -e "Result: ${YELLOW}ALL CLEAR... BUT WITH MEMORY ${leak_count} LEAKS AND ${mem_error_count} MEMORY ERRORS.${NC}"
		else
			echo -e "Result: ${GREEN}ALL CLEAR! 0 MEMORY LEAKS/ERROR FOUND :D${NC}"
		fi

		rm -f valgrind.out
	else
		echo -e "Result: ${GREEN}ALL CLEAR! :D${NC}"
	fi
else
	((failed = total - passed))
	echo -e "Result: ${RED}Some tests failed :(${NC}"
	echo -e "\nYou've failed ${RED}${failed}${NC} tests!"
fi

if [ "$valgrind" != "valgrind" ]; then
	echo "Run with './justdoit.sh [path] valgrind' for memory check"
fi

echo 

if (which lizard >/dev/null); then
	if lizard $1 -L 50 -Tnloc=25 -C 12 -m -w; then
		echo -e "Bonus: ${GREEN}Nice!${NC} None of your functions are too big!"
	else
		echo -e "Bonus: ${RED}Oh no!${NC} The functions above have been diagnosed with clinical obesity! Try to get them to use at most 25 lines of code (NLOC)."
	fi
elif (pip3 list | grep lizard >/dev/null); then
	if python -m lizard $1 -L 50 -Tnloc=25 -C 12 -m -w; then
		echo -e "Bonus: ${GREEN}Nice!${NC} None of your functions are too big!"
	else
		echo -e "Bonus: ${RED}Oh no!${NC} The functions above have been diagnosed with clinical obesity! Try to get them to use at most 25 lines of code (NLOC)."
	fi
else
	echo "Pro Tip: Install lizard so I can check for obese functions"
fi
