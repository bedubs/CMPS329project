#!/usr/bin/python

import socket
import sys
#Create a TCP/IP socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = socket.gethostname() #Get local machine name
PORT = 8008
server_address = (HOST,PORT)

print '\n200 NBserver version Beta ready '

#Bind socket to local host and port
try:
	s.bind(server_address)
except socket.error as msg:
	print 'Bind failed. Error code: '+ str(msg[0])+ ' Message '+ msg[1]
	sys.exit()
print 'Socket bind complete'

#start listening on socket
s.listen(1)
print 'Socket now listening'

#now keep talking with the client
while True:
	#wait to accept a connection - bloacking call
	print >>sys.stderr,'waiting for a connection'
	connection, client_address = s.accept()
	try:
		print >>sys.stderr,'connecting from', client_address
	#Recieve the data in small chunks and retransmit it
		while True:
			data = connection.recv(16)
			print >>sys.stderr,'"received "%s"' %data
			if data:
				print >>sys.stderr,'sending data back to the client'
				connection.sendall(data)
			else:
				print >>sys.stderr,'no more data from',client_address
				break
	finally:
		connection.close()

