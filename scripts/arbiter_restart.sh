#!/bin/bash
pushd "$(dirname "$0")"

set -o allexport; source ./.env; set +o allexport

# bash arbiter_clean.sh

p=2
s="0.5"

while IFS=':' read -r ip port iperfport nodename
do
    for (( c=0; c<$p; c++ ))
	do
        cmd_start="nohup /usr/local/bin/iperf3 -s -p $iperfport --pktdir /home/nus/logs -i 1 -V >> /home/nus/server.log 2>&1 &"
        if [ "$nodename" == "NUS1" ]; then
            sshpass -p $NUSPWD ssh -o ConnectTimeout=10 -n -p 22 nus@localhost $cmd_start && break
        else
            sshpass -p $NUSPWD ssh -o ConnectTimeout=10 -n -p $port nus@$ip $cmd_start && break
        fi
        sleep $s
    done
    sleep $s
done < addr_servers.txt

popd
