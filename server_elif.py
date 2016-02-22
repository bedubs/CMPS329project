#!/usr/bin/python

# Tested on Ubuntu 14.04
# Python v. 2.7.6 and v. 3.4.3

import os
import socket
import time
import sys

HOST, PORT = '', 8008

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)
server_started = '\nServer is running on port ' + str(PORT) + '....\nUse ctrl c to shutdown server.'
http_response = b'200 SRP (Simple Ray Protocol) version 1.0 ready\n'
placeholder = ''

req = {
    'HELO': 'Server: 210 Hello %s, pleased to meet you.\n',
    'REQTIME': 'Server: 220 ' + time.strftime("%H:%M:%S", time.localtime()) + '\n',
    'REQDATE': 'Server: 230 ' + time.strftime("%Y-%m-%d", time.localtime()) + '\n',
    'ECHO': 'Server: 240 < need to get ECHO > \n',
    'REQIP': 'Server: 250 < need to get IP > \n',
    'BYE': 'Server: 600 See ya later!\n'
}

while True:
    print(server_started)
    try:
        conn, addr = s.accept()
        while (True):
            # display initial response to client
            conn.send(http_response)

            data = conn.recv(1024)
            if data.decode('utf-8') == 'HELO':
                conn.send('Client: ' + data)
                response = req[data.decode('utf-8').split(None,1)]
                conn.send(response)
            elif data.decode('utf-8') == 'REQTIME':
                conn.send('Client: ' + data)
                response = req[data.decode('utf-8')]
                conn.send(response)
            elif data.decode('utf-8') == 'REQDATE':
                conn.send('Client: ' + data)
                response = req[data.decode('utf-8')]
                conn.send(response)
            elif data.decode('utf-8') == 'ECHO':
                conn.send('Client: ' + data)
                response = req[data.decode('utf-8')]
                conn.send(response)
            elif data.decode('utf-8') == 'REQIP':
                conn.send('Client: ' + data)
                response = req[data.decode('utf-8')]
                conn.send(response)
            elif data.decode('utf-8') == 'BYE':
                conn.send('Client: ' + data)
                response = req[data.decode('utf-8')]
                conn.send(response)
                break
            else:
                response = data + 'make it snappy\n_>'
                conn.send(response)

            conn.close()
    except KeyboardInterrupt:
        print('\n Shutdown requested...exiting now...\n')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)