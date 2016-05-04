An effort to make the [ccn-lite](https://github.com/cn-uofbasel/ccn-lite) distributed.

# Changes to ccn

The changes to the reference implementation of ccn-lite are mostly in
[ccn-lite-relay.c](https://github.com/tpoll/dist-ccn/blob/master/src/ccn-lite-relay.c),
[ccnl-core-fwd.c](https://github.com/tpoll/dist-ccn/blob/master/src/ccnl-core-fwd.c),
[ccnl-core.c](https://github.com/tpoll/dist-ccn/blob/master/src/ccnl-core.c),
 and [ccnl-core.h](https://github.com/tpoll/dist-ccn/blob/master/src/ccnl-core.h). The changes are mostly infrastructure to get and send data to redis. 
Redis's built in scripting  is used in order to increase efficiency, The scripts, written in Lua,  can be found in
[redis-scripts](https://github.com/tpoll/dist-ccn/tree/master/src/redis_scripts).

# How to run the relay
To run the relay, one must have installed the [hiredis](https://github.com/redis/hiredis) library into their home directory.
Then after setting the CCNL_HOME environment variable to point to the dist-ccn directory, one can run the make file.
Then one can run:

	$CCNL_HOME/bin/ccn-lite-relay -v trace -s ndn2013 -u <port> -x /tmp/mgmt-relay-b.sock -z <IP of redis node> 

to start the relay. Otherwise the interface for running and controlling a CCN node is the same as [ccn-lite](https://github.com/cn-uofbasel/ccn-lite) and can be found in their tutorial.

# Test Setup
The code used to set up the test machines (A1, 1 core, 1.75GB RAM, Ubuntu 15.10 server) instances on azure can be found in the [azure](https://github.com/tpoll/dist-ccn/tree/master/azure). While targeted for azure, the scripts and programs should be compatible with any debian based linux based system. The scripts provide an easy way to set up a machine to run any component of the project


#Load Testing
The code used to load test can be found in the [src/py](https://github.com/tpoll/dist-ccn/blob/master/src/py/) folder. [locustFile.py](https://github.com/tpoll/dist-ccn/blob/master/src/py/locustfile.py)
implements a custom class for the [locust](http://locust.io/) load testing framework. The load tester can be started
with a command  such as :

	locust --host=40.114.40.235 -f dist-ccn/src/py/locustfile.py --master

The load tester can be easily managed through its web interface.

[nodeControl.py](https://github.com/tpoll/dist-ccn/blob/master/src/py/nodeControl.py) when run on the given set of machines
runs a reliability test by killing and restarting the given machines. Note, the script only handles the starting and stopping of
nodes.




License
==============

Copyright (c) 2012-2013, Christian Tschudin, University of Basel

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
