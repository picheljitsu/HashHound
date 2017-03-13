#! /usr/bin/python

# Author: Matt Pichelmayer
# Created this as a complement to Robert J. Hansen's (https://github.com/rjhansen) NSRL server and NSRL lookup client.  
# The intent is to: 
# 	1) Add flexibility and interoperability with whitelisting tools.   
# 	2) Be modular; this script can be ran as a server, ran as an imported module or ran locally.
#	  3) Interoperate with the nsrllookup client.

import binascii
import socket
import sys
import argparse
import time # testing purposes only
from nsrlstore import nsrl_store

def check_positive(port):
	int_port = int(port)
	if int_port <= 0:
		raise argparse.ArgumentTypeError("%s is an invalid port" % port)
	else:
		return int_port

def check_ip(address):
	return address

parser = argparse.ArgumentParser(description="NSRL UDP Listener")
parser.add_argument("-f","--file", dest="nsrl_filename", required=True)
parser.add_argument("-p","--port", type=check_positive,required=False,default=9120)
parser.add_argument("-i","--interface", type=check_ip,required=False,default="172.16.120.69")
parser.add_argument("-s","--store",dest="hdfs_store_path",required=False,default="/usr/share/store.h5")
args = parser.parse_args()
port = args.port
server = args.interface
nsrl_file = args.nsrl_filename
hdfs_store_path = args.hdfs_store_path

store = nsrl_store(nsrl_file,hdfs_store_path)

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = (server, port)
listener.bind(server_address)
listener.listen(5)
print server_address

print >>sys.stderr, 'starting up on %s port %s' % server_address
print >>sys.stderr, '\nwaiting to receive message'
x = 0 
conn, addr = listener.accept()

while True:

	try:

		data = conn.recv(43690)
		if data.startswith('Version:'):
			print "[+] Version detection from client %s" % conn
			reply = conn.sendall("OK\n")
			print "Reply Sent"
			x +=1
		if data.startswith('query '):
			data = data.rstrip('\r\n')
			data = data.split()[1]
	 		sha1 = store.hash_query(data)
	 		print sha1
	 		time.sleep(5)
			conn.sendall(sha1)

	except socket.error, e:
		print e, "SOCKET ERROR"
	except IOError, e:
		print e + "IO Error"
	except KeyboardInterrupt:
		conn.close()
		print "Listener stopped"
		sys.exit()
		break

