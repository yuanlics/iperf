#!/bin/bash
p=2
s=20

ip=$1
port=$2
b1=$3
b2=$4
b3=$5
r=$6  # -R or empty

for b in $b1 $b2 $b3
{
    for (( c=0; c<$p; c++ ))
	do
	   /usr/local/bin/iperf3 $r -c $ip -t 100 -u -l 1000 -b ${b}M -p $port --pktdir /home/nus/logs -i 1 -V >> /home/nus/client.log 2>&1 && break
	   sleep $s
	done
	sleep $s
}

exit 0 