#!/bin/bash
# Argument 1 is the IP address of the target face, while argument 2 is the prefix 
# to be registered
export CCNL_HOME="/home/todd/comp/ccn-dist"
FACEID=`$CCNL_HOME/bin/ccn-lite-ctrl -x  /tmp/mgmt-relay-a.sock newUDPface any $1 9980 \\n  | $CCNL_HOME/bin/ccn-lite-ccnb2xml | grep FACEID | sed -e 's/^[^0-9]*\([0-9]\+\).*/\1/'`
$CCNL_HOME/bin/ccn-lite-ctrl -x /tmp/mgmt-relay-a.sock prefixreg $2 $FACEID ndn2013 \\n  | $CCNL_HOME/bin/ccn-lite-ccnb2xml