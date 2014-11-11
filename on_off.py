#!/usr/bin/env python3
import subprocess, shlex
from time import sleep

p = [0, 0]  # packets out, in
total = 0
max = 5
cutoff = 2500.0
c = 1
timeout_val = 3000.0

while True:
    t = [0] * max # initialize times to 0 ms
    while (sum(t)/len(t) <= cutoff):   # calc the avg ping <= cutoff
        r = subprocess.Popen(["ping",
                              "-c2", # + str(c),
                              "-W500",
                              "google.com"],
                             stdout=subprocess.PIPE)
        for line in r.stdout: # process each line in stdout for ping
            q = ''
            l = line.decode("utf-8")
            s = shlex.split(l)
            if len(s) == 0 or s[0] == 'PING':
                continue
            if s[0] == '64':  # sucessful ping
                p = [x.__add__(1) for x in p]
                total += float(s[6][5:])
                t[p[0]%len(t)] = float(s[6][5:])

                q += format('%.3fms' % t[p[0]%len(t)])
                q += format('\trecent: %.3fms\tavg: %.3fms\tdrop: %.2f%%' % 
                            (sum(t)/len(t),total/p[0], 100*(1-p[1]/p[0])))
                print(q)
            elif s[0] == 'Request':  # timed out
                p[0] += 1
                t[p[0]%len(t)] = timeout_val
                total += timeout_val
                q += 'Timed out'
                q += format('\trecent: %.3fms\tavg: %.3fms\tdrop: %.2f%%' % 
                            (sum(t)/len(t),total/p[0], 100*(1-p[1]/p[0])))
                print(q)


    print("Turning OFF wifi")
    subprocess.call(["networksetup", "-setairportpower", "en0", "off"])
    sleep(0.5)
    print("Turning ON wifi")
    subprocess.call(["networksetup", "-setairportpower", "en0", "on"])
    sleep(5)
    print("Starting over")
