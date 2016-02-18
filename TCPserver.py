#!/usr/bin/python

import socket
import sys
from datetime import time
HOST = socket.gethostname() #get local machine name
PORT = 8008
server_address = (HOST,PORT)
BUFFER_SIZE = 1024

#create a TCP/IP socket

sock = socket.socket()

try:
    sock.bind(server_address)
except socket.error as message:
    print 'Bind failed. Error code: '+ str(message[0])+ ' Message ' + message[1]
    sys.exit()

#Initial connection
print '200 SRP version 1.0 ready'

#start listening on socket
sock.listen(1)
print 'Start listening'

c_connection, c_address = sock.accept()
print 'Connecting address:',c_address
           
while True:
    data = c_connection.recv(BUFFER_SIZE)
    if not data: break
    print "received data: ", data
    #c_connection.send() echo
    if "HELO" in data:
        c_connection.send("210 hello "+HOST+" Pleased to meet you.")
        break
    else:
        c_connection.send("510 Sorry I can not service your request at this time.")
        sys.exit()
    if "Time" in data:
        c_connection.send("testing")

    else:
        sys.exit()
        
           


