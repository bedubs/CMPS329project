#!/usr/bin/python

import socket
import sys


import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#create a socket object

HOST = socket.gethostname()
PORT = 8008
server_address = (HOST,PORT)
BUFFER_SIZE = 1024

sock.connect(server_address)

try:
        
	#send data
	message = 'HELO ' + HOST
	print message
	sock.sendall(message)
	data = sock.recv(BUFFER_SIZE)
	print data
	time = "Time"
	sock.sendall(time)
	data = sock.recv(BUFFER_SIZE)
	print data
	
	#look for the response
	
  
finally:
	print >>sys.stderr, 'closing socket'
	sock.close()
