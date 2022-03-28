#!/usr/bin/env bash
# Author: Francisco Salgueiro

usage() {
    echo "usage: $0 [flags] <relative_path_to_executable> <relative_path_to_tests_dir>"
    echo "-v display diff in the terminal"
    echo "-c clean generated result files instead of testing"
    echo "-h help - shows this message"
}

DIFF=true # no-op successful command

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

bin="${1}"
tests="${2}"

if [[ "$MODE" == "clean" ]]; then
    rm "$PWD/$tests/"*result
    exit 0
fi

for infile in $PWD/$tests/*.in; do
    basename=${infile%.*}
    ($PWD/$bin) < $infile > $basename.result
    cmp --silent $basename.result $basename.out || echo "$basename TEST FAILED" 
    if [ "$3" == "-v" ]; then
        if ! command -v colordiff &> /dev/null; then
            diff $basename.result $basename.out
        else
            colordiff $basename.result $basename.out        
        fi
    fi
done

if [[ "$DIFF" != "colordiff" ]]; then
    echo ""
    echo "NOTA: Instala colordiff para ver as diferenças a cores"
fi
