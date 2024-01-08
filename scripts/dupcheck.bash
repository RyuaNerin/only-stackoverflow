#!/bin/bash

HOST_HEADER_LINES=$(grep -c '#.*' hosts.txt)
HOST_LIST1=$(tail -n +$((${HOST_HEADER_LINES}+1)) hosts.txt | sort -nf | wc -l)
HOST_LIST2=$(tail -n +$((${HOST_HEADER_LINES}+1)) hosts.txt | sort -nf | uniq | wc -l)

if (( $HOST_LIST1 != $HOST_LIST2 )); then
    exit 1
fi
