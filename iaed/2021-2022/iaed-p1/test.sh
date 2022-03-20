# Author: Francisco Salgueiro

#!/bin/bash

if [[ $# -lt 2 ]]; then
    echo "usage: $0 <relative_path_to_executable> <relative_path_to_tests_dir> <flags>"
    echo "-v flag to display diff in the terminal"
    echo "-c flag to remove generated result files"
    exit
fi

bin="${1}"
tests="${2}"

if [ "$3" == "-c" ]; then
    rm $PWD/$tests/*result
    exit
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

if [ "$3" == "-v" ]; then
    if ! command -v colordiff &> /dev/null
    then
        echo ""
        echo "NOTA: Instala colordiff para ver as diferenças a cores"
        exit
    fi
fi