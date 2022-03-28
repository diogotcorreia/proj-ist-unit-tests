#!/usr/bin/env bash
# Author: Francisco Salgueiro

usage() {
    echo "usage: $0 [flags] <relative_path_to_executable> <relative_path_to_tests_dir>"
    echo "-v display diff in the terminal"
    echo "-c clean generated result files instead of testing"
    echo "-h help - shows this message"
}

silent_diff() {
    cmp --silent "$1" "$2"
}

DIFF=silent_diff

while getopts ":vch" OPTION; do
    case "$OPTION" in
        v)
            DIFF=diff
            if command -v colordiff &>/dev/null; then
                DIFF=colordiff
            fi
            ;;
        c)
            MODE=clean
            ;;
        h)
            usage
            exit 0
            ;;
    esac
done
shift "$(( OPTIND - 1 ))"

if [[ $# -lt 2 ]]; then
    usage
    exit 1
fi

bin="$1"
tests="$2"

if [ ! -d "$tests" ]; then
    echo Test dir '"'$tests'"' is not a directory
    exit 1
elif ! ls $tests/*.in &> /dev/null; then
    echo Test dir '"'$tests'"' does not contain any tests
    exit 1
fi

# Try to clean before finishing checks to allow cleaning without compiling anything
if [[ "$MODE" == "clean" ]]; then
    rm "$tests/"*result
    exit 0
fi

if [ ! -f "$bin" ]; then
    echo '"'$bin'"' is not a file
    exit 1
elif [ ! -x "$bin" ]; then
    echo '"'$bin'"' is not executable
    exit 1
fi

for infile in "$tests/"*.in; do
    test_name="$(basename -s .in "$infile")"
    actual_output_file="$(dirname $infile)/${test_name}.result"
    expected_output_file="$(dirname $infile)/${test_name}.out"

    "$bin" < "$infile" > "$actual_output_file" && \
        "$DIFF" "$expected_output_file" "$actual_output_file" || \
        echo "TEST FAILED: $test_name"
done

if [[ "$DIFF" != "colordiff" && "$DIFF" != "silent_diff" ]]; then
    echo ""
    echo "NOTA: Instala colordiff para ver as diferenças a cores"
fi
