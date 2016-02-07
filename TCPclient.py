#!/usr/bin/python

import socket

s = socket.socket()	#create a socket object

HOST = socket.gethostname()
PORT = 8008

s.connect((HOST, PORT))
print s.recv(1024)
s.close
