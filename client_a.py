#!/usr/bin/python

# client.py
# Author: William Williamson
# Date  : 17 FEB 2016
# Project for CMPS 329
# Tested on Ubuntu 14.04
# Python v. 2.7.6 and v. 3.4.3

import socket
from socket import error as SocketError
import errno

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST, PORT = '', 8008
s.connect((HOST, PORT))

# Use list of requests to test the Server
request_test = ['HELO','HELO name','REQTIME','REQDATE','ECHO','ECHO You can say that again','REQIP','BYE']


try:
    data = s.recv(1024)

    while True:
        print('\n')
        print(data.decode('utf-8'))
        print('\n')

        while(True):
            for request in request_test:
                s.send(request.encode(encoding='utf-8'))

                # Receive and display echo of request from server
                data = s.recv(1024)
                print(data.decode(encoding='utf-8'))

                # Receive and display response from server
                data = s.recv(1024)
                print(data.decode(encoding='utf-8'))

                print('\n')

# Exception is raised when socket is closed by server,
except SocketError as e:
    if e.errno != errno.ECONNRESET:
        raise
    print('The connection has been closed by the server...goodbye.\n')
