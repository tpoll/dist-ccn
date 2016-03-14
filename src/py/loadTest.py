import argparse
import socket
import time
import select
import multiprocessing

import ccnlite.ndn2013 as ndn
import ccnlite.util as util





def worker(socket, name, ip, port):
    req = ndn.mkInterest(name)
    before = time.time()
    socket.sendto(req, (ip, int(port)))
    data, server = socket.recvfrom(4096)
    after = time.time()
    print ((after - before) * 1000)
    print data

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

    sockets = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for x in xrange(0, multiprocessing.cpu_count())]



    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    workers = [multiprocessing.Process(target=worker, args=(s, name, ip, port)) for s in sockets]

    for p in workers:
        print "here"
        p.daemon = True
        p.start()

    while True:
        try:
            time.sleep(10)
        except:
            break



if __name__ == '__main__':
    main()