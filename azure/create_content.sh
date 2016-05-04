#!/bin/dash
#Createst x number of different content types
number=1
name="/ndn/test/mycontent"
content="Hello, data world "
export CCNL_HOME="/home/todd/dist-ccn"

while [ "$number" -le $1 ]
do
    echo  $name$number
	echo $content$number | ($CCNL_HOME/bin/ccn-lite-mkC -s ndn2013 $name$number > $CCNL_HOME/test/ndntlv/mycontent$number.ndntlv)
    number=`expr $number + 1 `
done