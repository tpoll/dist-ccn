import argparse
import socket
import time

import ccnlite.ndn2013 as ndn
import ccnlite.util as util




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

	before = time.time()
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	req = ndn.mkInterest(name)
	s.sendto(req, (ip, int(port)))
	data, server = s.recvfrom(4096)
	after = time.time()
	print ((after - before) * 1000)
	print data



if __name__ == '__main__':
	main()