#!/bin/bash

# Define the digits
digits=(2 6 7 8)

# Iterate through all combinations
for d1 in "${digits[@]}"; do
    for d2 in "${digits[@]}"; do
        for d3 in "${digits[@]}"; do
            for d4 in "${digits[@]}"; do
                for d5 in "${digits[@]}"; do
                    echo "$d1$d2$d3$d4$d5"
                    curl -H "content-type:application/json" -d "{\"answer\":\"$d1$d2$d3$d4$d5\"}" "https://hhc24-frostykeypad.holidayhackchallenge.com/submit?id=null"
                    sleep 1
                done
            done
        done
    done
done
