#!/bin/bash

# Checking an integer to be a prime.
#
# Args:
#    $1(int): integer to verify for being a prime
# Returns:
#    str: "yes" if given number is a prime otherwise ""
function is_prime() {
    n=$1
    if [ "${n}" -lt 2 ]; then return; fi
    if [ "$((n % 2))" -eq 0 ]; then
        if [ "${n}" == "2" ]; then echo "yes"; fi
        return;
    fi
    # you have to check up to this limit only because d*d <= n
    d=$(echo "sqrt(${n})"|bc)
    for k in $(seq 3 2 ${d}); do
        if [ "$((n % k))" -eq 0 ]; then return; fi
    done
    echo "yes"
}

# for a sequence of integers checking for primes and printing
# them when found. When no number has specified then all
# primes below 100 are printed.
max_n=$1
for n in $(seq 0 ${max_n:=100}); do
    if [ "$(is_prime ${n})" == "yes" ]; then
        echo -n "${n} ";
    fi
done
