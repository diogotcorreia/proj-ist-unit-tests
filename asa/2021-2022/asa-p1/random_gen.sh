#!/bin/bash
# Author: $ußv3r5I0n

if [ $# -eq 5 ]; then
	if [ $1 -ne 1 ] || ! [[ $2 =~ ^[0-9]+$ && $3 =~ ^[0-9]+$ && $4 =~ ^[0-9]+$ && $5 =~ ^[0-9]+$ ]]; then

		echo "ERROR: Invalid arguments"
		exit 1
	fi
	p_type=$1
	size=$2
	inc=$3
	n_seq=$4
	n_prob=$5

elif [[ $# -eq 7 ]]; then
	if [ $1 -ne 2 ] || ! [[ $2 =~ ^[0-9]+$ && $3 =~ ^[0-9]+$ && $4 =~ ^[0-9]+$ && $5 =~ ^[0-9]+$ && $6 =~ ^[0-9]+$ && $7 =~ ^[0-9]+$ ]]; then
		echo "ERROR: Invalid arguments"
		exit 1
	fi
	p_type=$1
	size1=$2
	inc1=$3
	size2=$4
	inc2=$5
	n_seq=$6
	n_prob=$7

else
	echo "Script to generate random sequences for the first project of ASA. It uses random_k."
	echo "It will generate n * p_d sequences"
	echo ""
	echo "Usage: random_gen 1 s s_i n p_d | random_gen 2 s1 s1_i s2 s2_i n p_d"
	echo "    s(n): size of the sequence (n)"
	echo "    s(n)_i: size increase for each generation"
	echo "    n: number of generations"
	echo "    p_d: probability points e.g. 1 -> {0.5}; 2 -> {0.333, 0.666}; etc."
	exit 0
fi

if [ ! -d "seq_gen" ]; then
	mkdir "seq_gen"
fi

for ((seq=1; seq<=$((n_seq)); ++seq)); do
	for (( prob_c=1; prob_c<=$((n_prob)); ++prob_c )); do
		prob=$(bc <<< "scale=3; ${prob_c}/$((n_prob+1))")
		if [ $p_type = 2 ]; then
			eval "./random_k $p_type $((size1 > size2 ? size1 : size2)) $prob $size1 $size2 > seq_gen/p${p_type}_${size1}_${size2}_${prob}\n"
		fi
		if [ $p_type = 1 ]; then
			eval "./random_k $p_type $size $prob $size > seq_gen/p${p_type}_${size}_${prob}\n"
		fi
	done
	if [ $p_type = 2 ]; then
		size1="$((size1+inc1))"
		size2="$((size2+inc2))"
	fi
	if [ $p_type = 1 ]
	then
		size="$((size+inc))"
	fi
done
echo "Sequences generated! You can find the files in seq_gen"
