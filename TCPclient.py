#!/usr/bin/python

import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#create a socket object

HOST = socket.gethostname()
PORT = 8008
server_address = (HOST,PORT)
print >>sys.stderr,'connection to %s port %s' % server_address
s.connect(server_address)
try:
	#send data
	message = ''
	print >>sys.stderr, 'sending "%s"' % message
	s.sendall(message)
	
	#look for the response
	amount_received = 0
	amount_expected = len(message)
	
	while amount_received < amount_expected:
		data = s.recv(16)
		amount_received +=len(data)
		print >>sys.stderr, 'received "%s"' % data
finally:
	print >>sys.stderr, 'closing socket'
	s.close()

