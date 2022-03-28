#!/usr/bin/env bash
# Author: Francisco Salgueiro

RED='\033[0;31m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
BOLD='\033[1m'
RESET='\033[0m'

usage() {
    echo "usage: $0 [flags] <path to executable> <path to tests dir>"
    echo "-d display diff in the terminal"
    echo "-v run tests in valgrind"
    echo "-c clean generated result files instead of testing"
    echo "-h help - shows this message"
}

silent_diff() {
    cmp --silent "$1" "$2"
}

noop_wrapper() {
    "$@"
}

DIFF="silent_diff"
WRAPPER="noop_wrapper"

while getopts ":dvch" OPTION; do
    case "$OPTION" in
        d)
            DIFF="diff"
            if command -v colordiff &>/dev/null; then
                DIFF="colordiff"
            fi
            ;;
        c)
            MODE="clean"
            ;;
        v)
            WRAPPER="valgrind --error-exitcode=1 --track-origins=yes"
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

if [[ $# != 2 ]]; then
    usage
    echo
    echo -e "${RED}Expected 2 positional arguments, found ${#}${RESET}"
    exit 1
fi

bin="$1"
tests="$2"

if [ ! -d "$tests" ]; then
    usage
    echo
    echo -e "${RED}Test dir \"$tests\" is not a directory${RESET}"
    exit 1
elif ! ls "$tests/"*.in &> /dev/null; then
    usage
    echo
    echo -e "${RED}Test dir \"$tests\" does not contain any tests${RESET}"
    exit 1
fi

# Try to clean before finishing checks to allow cleaning without compiling anything
if [[ "$MODE" == "clean" ]]; then
    rm "$tests/"*result
    exit 0
fi

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

for infile in "$tests/"*.in; do
    test_name="$(basename -s .in "$infile")"
    actual_output_file="$(dirname "$infile")/${test_name}.result"
    expected_output_file="$(dirname "$infile")/${test_name}.out"

    echo
    echo -e "${BOLD}Running test: ${test_name}${RESET}"
    $WRAPPER "$bin" < "$infile" > "$actual_output_file" && \
        "$DIFF" "$expected_output_file" "$actual_output_file" && \
        echo -e "${GREEN}TEST PASS: $test_name${RESET}" || \
        echo -e "${RED}TEST FAIL: $test_name${RESET}"
done

if [[ "$DIFF" != "colordiff" && "$DIFF" != "silent_diff" ]]; then
    echo ""
    echo "${YELLOW}NOTA: Instala colordiff para ver as diferenças a cores${RESET}"
fi
