#!/bin/bash
pushd "$(dirname "$0")"

set -o allexport; source ./.env; set +o allexport

p=2
s="0.5"

for f in addr_servers.txt addr_clients.txt
do
    while IFS=':' read -r ip port iperfport nodename
    do 
        for (( c=0; c<$p; c++ ))
        do
            cmd_upload="python3 iperf/scripts/iperf3_upload.py -n $nodename"
            if [ "$nodename" == "NUS1" ]; then
                sshpass -p $NUSPWD ssh -o ConnectTimeout=10 -n -p 22 nus@localhost $cmd_upload && break
            else
                sshpass -p $NUSPWD ssh -o ConnectTimeout=10 -n -p $port nus@$ip $cmd_upload && break
            fi
            sleep $s
        done
        sleep $s
    done < $f
done

popd