from subprocess import Popen, PIPE
import os
import random
from datetime import datetime

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

p = 2
s = 0.5

with open('addr_servers.txt') as fs, open('addr_clients.txt') as fc:
    slines = fs.readlines()
    clines = fc.readlines()
    ns = len(slines)
    nc = len(clines)
    
    nodeinfo = []
    for line in slines + clines:
        ip, sshport, iperfport, nodename = line.strip().split(':')
        nodeinfo.append((ip, sshport, iperfport, nodename))

timestr = datetime.now().strftime("%Y%m%d%H%M%S")

n = ns + nc
servers = set(range(ns))
clients = set(range(ns, n))
conns = []
while len(servers) > 0:
    i = random.choice(tuple(servers))  # each server is assigned a connection
    servers.remove(i)
    j = random.choice(tuple(servers.union(clients)))
    if j in servers:
        servers.remove(j)
    else:
        clients.remove(j)

    if random.random() < 0.5:
        i, j = j, i  # direction is random

    r = ''  # reverse flag
    if j >= ns:  # receiver must be a server
        i, j = j, i
        r = '-R'

    i_ip, i_sshport, _, iname = nodeinfo[i]
    j_ip, _, j_iperfport, jname = nodeinfo[j]

    lb=0
    ub=3
    b1 = round(10 ** (lb + random.random() * (ub - lb)))
    b2 = round(10 ** (lb + random.random() * (ub - lb)))
    b3 = round(10 ** (lb + random.random() * (ub - lb)))

    conns.append((timestr, i, j, r, i_ip, i_sshport, iname, j_ip, j_iperfport, jname, b1, b2, b3))

for conn in conns:
    _, _, _, r, i_ip, i_sshport, _, j_ip, j_iperfport, _, b1, b2, b3 = conn
    print(' '.join([str(v) for v in conn]))

    cmd = f"bash /home/nus/iperf/scripts/arbiter_connect.sh ssh -n -p {i_sshport} nus@{i_ip} bash iperf/scripts/iperf3_connect.sh {j_ip} {j_iperfport} {b1} {b2} {b3} {r}"
    print(cmd)
    # process = Popen(cmd.split(), stdout=None, stderr=None, close_fds=True)
