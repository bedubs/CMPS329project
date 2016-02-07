#!/usr/bin/python

import socket
import sys
#Create a TCP/IP socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = socket.gethostname() #Get local machine name
PORT = 8008


print '\n200 NBserver version Beta ready '

#Bind socket to local host and port
try:
	s.bind((HOST,PORT))
except socket.error as msg:
	print 'Bind failed. Error code: '+ str(msg[0])+ ' Message '+ msg[1]
	sys.exit()
print 'Socket bind complete'

#start listening on socket
s.listen(1)
print 'Socket now listening'

#now keep talking with the client
while 1:
	#wait to accept a connection - bloacking call
	conn, addr = s.accept()
	print 'Connected with ' + addr[0] + ':'+str(addr[1])
	conn.send('Thank you for connecting')
	conn.close()

