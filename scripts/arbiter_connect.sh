#!/bin/bash
p=2
s="0.5"
cmd="$@"

for (( c=0; c<$p; c++ ))
do
    $cmd && break
    sleep $s
done