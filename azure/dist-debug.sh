export CCNL_HOME="/home/todd/dist-ccn"
nohup /home/todd/dist-ccn/bin/ccn-lite-relay -v trace -s ndn2013 -u 9980 -x /tmp/mgmt-relay-a.sock > log.txt &