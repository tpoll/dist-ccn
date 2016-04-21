$CCNL_NORM/bin/ccn-lite-relay -v trace -s ndn2013 -u 9999 -x /tmp/mgmt-relay-b.sock -d $CCNL_NORM/test/ndntlv
$CCNL_HOME/bin/ccn-lite-relay -v trace -s ndn2013 -u 9998 -x /tmp/mgmt-relay-a.sock

FACEID=`$CCNL_HOME/bin/ccn-lite-ctrl -x  newUDPface any 40.76.19.73 9999 \\n  | $CCNL_HOME/bin/ccn-lite-ccnb2xml | grep FACEID | sed -e 's/^[^0-9]*\([0-9]\+\).*/\1/'`
$CCNL_HOME/bin/ccn-lite-ctrl -x /tmp/mgmt-relay-b.sock prefixreg /ndn $FACEID ndn2013 \\n  | $CCNL_HOME/bin/ccn-lite-ccnb2xml


FACEID=`$CCNL_HOME/bin/ccn-lite-ctrl -x /tmp/mgmt-relay-b.sock newUDPface any 40.114.10.98 9999 \ | $CCNL_HOME/bin/ccn-lite-ccnb2xml | grep FACEID | sed -e 's/^[^0-9]*\([0-9]\+\).*/\1/'`

209.6.40.217/35341

#hello world packet
"\x06:\a\x17\b\x03ndn\b\x04test\b\nmycontent1\x14\x00\x15\x14Hello, data world 1\n\x16\x05\x1b\x01\x00\x1c\x00\x17\x00"


$CCNL_HOME/bin/ccn-lite-relay -v -s ndn2013 -u 9980-d $CCNL_HOME/test/ndntlv
