import argparse
import socket
import time
import select
from multiprocessing import Process, Queue, cpu_count


import ccnlite.ndn2013 as ndn
import ccnlite.util as util


startTime = time.time()


def worker(socket, name, ip, port, queue):
    while True:
        req = ndn.mkInterest(name)
        before = time.time()
        socket.sendto(req, (ip, int(port)))
        print socket.getsockname()
        data, server = socket.recvfrom(4096)
        after = time.time()
        print ((after - before) * 1000)
        queue.put((after - before) * 1000)
        # time.sleep(.5)


def computeAvgLatency(queue):
    numRequests = 0
    totalLat = 0 #In milliseconds
    while True:
        l = queue.get()
        numRequests += 1
        totalLat += l

        # print "At second %d there has been %d requests with an average latency of %f ms" % ((time.time() - startTime), numRequests, (totalLat/ numRequests))


def main():
    parser = argparse.ArgumentParser(description='Test latency of ndn nodes')
    parser.add_argument('lci', metavar='LCI', type=str,
                    help='a labeled content identifier')
    parser.add_argument('-u', metavar='host/port', type=str,
                    help='UDP addr of access router (default: 127.0.0.1/9998)',
                    default='127.0.0.1/9998')
    

    args = parser.parse_args()
    name = util.str2lci(args.lci)
    (ip, port) = args.u.split('/')
    queue = Queue()

    sockets = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for x in xrange(0, 1)]

    workers = [Process(target=worker, args=(s, name, ip, port, queue)) for s in sockets]
    reader = Process(target=computeAvgLatency, args=(queue,))

    for p in workers:
        print "here"
        p.daemon = True
        p.start()

    reader.daemon = True
    reader.start()

    while True:
        try:
            time.sleep(10)
        except:
            break



if __name__ == '__main__':
    main()