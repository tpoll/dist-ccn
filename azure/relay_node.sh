#!/bin/dash
export CCNL_HOME="/home/todd/dist-ccn"
/home/todd/$1/bin/ccn-lite-relay $2 -s ndn2013 -u 9980 -x /tmp/mgmt-relay-a.sock > log.txt &
pid=$!
sleep 1
if ps -p $pid > /dev/null
then
   echo $pid
   exit 0
else
	exit 1
fi
