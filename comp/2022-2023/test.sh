#!/usr/bin/env bash
# Author: Francisco Salgueiro
# Adapted by: Diogo Correia

RED='\033[0;31m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
BOLD='\033[1m'
RESET='\033[0m'

usage() {
    echo "usage: $0 [flags] <path to executable>"
    echo "-d display diff in the terminal"
    echo "-c clean generated result files instead of testing"
    echo "-x output xml instead of generating asm"
    echo "-h help - shows this message"
}

silent_diff() {
    normal_diff "$1" "$2" > /dev/null
}

normal_diff() {
    diff -iwubZB --color <(tr -d '\n' < "$1" ) <(tr -d '\n' < "$2")
}

DIFF="silent_diff"
TARGET="asm"

while getopts ":dcxh" OPTION; do
    case "$OPTION" in
        d)
            DIFF="normal_diff"
            ;;
        c)
            MODE="clean"
            ;;
        x)
            TARGET="xml"
            ;;
        h)
            usage
            exit 0
            ;;
        *)
            usage
            echo
            echo -e "${RED}Unknown flag: -${OPTARG}${RESET}"
            exit 1
            ;;
    esac
done
shift "$(( OPTIND - 1 ))"

script_pwd=$(dirname "$0")
nok_tests="$script_pwd/nok"
ok_tests="$script_pwd/ok"
official_tests="$script_pwd/official-tests"

# Clean before tests to make sure tests are accurate
rm -f "$nok_tests/"**/*.log
rm -f "$nok_tests/"**/*.xml
rm -f "$nok_tests/"**/*.asm
rm -f "$nok_tests/"**/*.o
rm -f "$nok_tests/"**/*.exe

rm -f "$ok_tests/"*.log
rm -f "$ok_tests/"*.result
rm -f "$ok_tests/"*.xml
rm -f "$ok_tests/"*.asm
rm -f "$ok_tests/"*.o
rm -f "$ok_tests/"*.exe

if [[ -d  $official_tests ]]; then

rm -f "$official_tests/"*.log
rm -f "$official_tests/"*.result
rm -f "$official_tests/"*.xml
rm -f "$official_tests/"*.asm
rm -f "$official_tests/"*.o
rm -f "$official_tests/"*.exe

fi

if [[ "$MODE" == "clean" ]]; then
    echo
    echo -e "${GREEN}Cleaned${RESET}"
    exit 0
fi

if [[ $# != 1 ]]; then
    usage
    echo
    echo -e "${RED}Expected 1 positional arguments, found ${#}${RESET}"
    exit 1
fi

bin="$1"

if [ ! -f "$bin" ]; then
    usage
    echo
    echo -e "${RED}\"$bin\" is not a file${RESET}"
    exit 1
elif [ ! -x "$bin" ]; then
    usage
    echo
    echo -e "${RED}\"$bin\" is not executable${RESET}"
    exit 1
fi
bin="$(realpath "$bin")" # handle paths that don't start with a dot

TEST_COUNT=0
TEST_PASS_COUNT=0

echo
echo -e "${BOLD}---- [NOK Tests] ----${RESET}"
for infile in "$nok_tests/"**/*.mml; do
    test_name="$(realpath --relative-base "$nok_tests" "$infile")"
    log_output_file="$(dirname "$infile")/$(basename -s .mml "$infile").log"

    (( TEST_COUNT++ ))

    echo
    echo -e "${BOLD}Running test: ${test_name}${RESET}"
    # grep is necessary because semantic compile errors don't make the compiler exit with error 1
    "$bin" -g --target ${TARGET} "$infile" > $log_output_file 2> $log_output_file | grep -vzP "(^|\n)\d:" > /dev/null && \
        echo -e "${RED}TEST FAIL: $test_name (exited correctly when it should have failed)${RESET}" || \
        echo -e "${GREEN}TEST PASS: $test_name (exited with error as expected)${RESET}" && \
        (( TEST_PASS_COUNT++ ))
done

echo
echo -e "${BOLD}---- [OK Tests] ----${RESET}"
echo
for infile in "$ok_tests/"/*.mml; do
    test_name="$(realpath --relative-base "$ok_tests" "$infile")"
    base_name="$(basename -s .mml "$infile")"
    log_output_file="$(dirname "$infile")/$base_name.log"
    actual_output_file="$(dirname "$infile")/$base_name.result"
    expected_output_file="$(dirname "$infile")/$base_name.out"
    asm_output_file="$(dirname "$infile")/$base_name.asm"
    o_output_file="$(dirname "$infile")/$base_name.o"
    exec_output_file="$(dirname "$infile")/$base_name.exe"

    (( TEST_COUNT++ ))

    ld_options=(-melf_i386 -o "$exec_output_file" "$o_output_file" -lrts)
    # RTS is often installed in $HOME/compiladores/root, so add that to ld's path if it exists
    if [[ -d "$HOME/compiladores/root" ]]; then
        ld_options+=("-L$HOME/compiladores/root/usr/lib")
    fi
    if [[ -n $LD_EXTRA_FLAGS ]]; then
        ld_options+=("$LD_EXTRA_FLAGS")
    fi

    echo
    echo -e "${BOLD}Running test: ${test_name}${RESET}"
    if [[ $TARGET = "asm" ]]; then
        "$bin" -g --target ${TARGET} "$infile" > "$log_output_file" 2> "$log_output_file" && \
            yasm -felf32 -o "$o_output_file" "$asm_output_file" && \
            ld "${ld_options[@]}" && \
            "$(realpath "$exec_output_file")" > "$actual_output_file" && \
            "$DIFF" "$expected_output_file" "$actual_output_file" && \
            echo -e "${GREEN}TEST PASS: $test_name${RESET}" && \
            (( TEST_PASS_COUNT++ )) || \
            echo -e "${RED}TEST FAIL: $test_name${RESET}"
    else
        "$bin" -g --target ${TARGET} "$infile" > "$log_output_file" 2> "$log_output_file" && \
            echo -e "${BLUE}TEST PASS: $test_name (output was generated)${RESET}" && \
            (( TEST_PASS_COUNT++ )) || \
            echo -e "${RED}TEST FAIL: $test_name${RESET}"
    fi
done

if [[ -d  $official_tests ]]; then
    echo
    echo -e "${BOLD}---- [Official Tests] ----${RESET}"
    echo
    for infile in "$official_tests/"/*.mml; do
        test_name="$(realpath --relative-base "$official_tests" "$infile")"
        base_name="$(basename -s .mml "$infile")"
        log_output_file="$(dirname "$infile")/$base_name.log"
        actual_output_file="$(dirname "$infile")/$base_name.result"
        expected_output_file="$(dirname "$infile")/expected/$base_name.out"
        asm_output_file="$(dirname "$infile")/$base_name.asm"
        o_output_file="$(dirname "$infile")/$base_name.o"
        exec_output_file="$(dirname "$infile")/$base_name.exe"

        (( TEST_COUNT++ ))

        ld_options=(-melf_i386 -o "$exec_output_file" "$o_output_file" -lrts)
        # RTS is often installed in $HOME/compiladores/root, so add that to ld's path if it exists
        if [[ -d "$HOME/compiladores/root" ]]; then
            ld_options+=("-L$HOME/compiladores/root/usr/lib")
        fi
        if [[ -n $LD_EXTRA_FLAGS ]]; then
            ld_options+=("$LD_EXTRA_FLAGS")
        fi

        echo
        echo -e "${BOLD}Running test: ${test_name}${RESET}"
        if [[ $TARGET = "asm" ]]; then
            "$bin" -g --target ${TARGET} "$infile" > "$log_output_file" 2> "$log_output_file" && \
                yasm -felf32 -o "$o_output_file" "$asm_output_file" && \
                ld "${ld_options[@]}" && \
                "$(realpath "$exec_output_file")" > "$actual_output_file" && \
                "$DIFF" "$expected_output_file" "$actual_output_file" && \
                echo -e "${GREEN}TEST PASS: $test_name${RESET}" && \
                (( TEST_PASS_COUNT++ )) || \
                echo -e "${RED}TEST FAIL: $test_name${RESET}"
        else
            "$bin" -g --target ${TARGET} "$infile" > "$log_output_file" 2> "$log_output_file" && \
                echo -e "${BLUE}TEST PASS: $test_name (output was generated)${RESET}" && \
                (( TEST_PASS_COUNT++ )) || \
                echo -e "${RED}TEST FAIL: $test_name${RESET}"
        fi
    done
fi

echo
echo -e "${BOLD}---- [Summary] ----${RESET}"
echo -e "${BOLD}TESTS RAN: $TEST_COUNT${RESET}"
if [[ $TEST_COUNT == $TEST_PASS_COUNT ]]; then
    echo -e "${GREEN}All tests passed!${RESET}"
else
    echo -e "${GREEN}${RED}$(( TEST_COUNT - TEST_PASS_COUNT )) TESTS FAILED!${RESET}"
fi
