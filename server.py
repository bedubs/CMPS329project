#!/usr/bin/python

# server_dict.py
# Author: William Williamson
# Author: Neil Hoang
# Date  : 17 FEB 2016
# Project for CMPS 329
# Tested on Ubuntu 14.04
# Python v. 2.7.6 and v. 3.4.3
# and Telnet client

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


def foo(x, y):
    if len(x) >= y[1]:
        space = ' '
        placeholder = x[1:]
        # Put the value of the req[key] in the response with the placeholder
        response = y[2] % space.join(placeholder)
    else:
        response = y[3]
    return response


def bar(x, y):
    return y[2]

# Dictionary to store acceptable Client request as key and Server response as value
# dict = {Request: [function to call, expected request size, server response, error response]}
req = {
    'HELO': [foo, 2, 'Server: 210  Hello %s, pleased to meet you.\n', 'Server: 510  The \'HELO\' command requires a \'name\' argument. \n'],
    'REQTIME': [bar, 1, 'Server: 220  ' + time.strftime("%H:%M:%S", time.localtime()) + '\n', 'Server: 520  Could not connect to the time server.\n'],
    'REQDATE': [bar, 1, 'Server: 230  ' + time.strftime("%Y-%m-%d", time.localtime()) + '\n', 'Server: 530  No date for you!!!\n'],
    'ECHO': [foo, 2, 'Server: 240 %s \n', 'Server 540:  ECHO requires an argument to be echoed back.\n'],
    'REQIP': [bar, 1, 'Server: 250  Your IP is: %s \n', 'Server: 550  Cannot tell your IP. Perhaps you are using a proxy?\n'],
    'BYE': [bar, 1, 'Server: 600 See ya later!\n']
}


def handle_req(data):
    str_data = data.decode(encoding='utf-8')  # Decode data from bytes to a string
    print(str_data)  # Print to server, mostly for testing
    client_echo = 'Client: ' + str_data
    conn.send(client_echo.encode(encoding='utf-8'))  # Display client request back to the client
    request = str_data.split()  # Split request to check for arguments sent with command and store in list (request array)
    
    if request[0] in req.keys():
        if request[0] == 'REQIP':
            response = req[request[0]][0](request, req[request[0]]) % ''.join(conn.getsockname()[0])
        else:
            response = req[request[0]][0](request, req[request[0]])
    else:
        # If request is not in the dictionary, put this in response
        response = 'Server: 500  \"' + request[0] + '\" not a recognized command.\n'

    conn.send(response.encode(encoding='utf-8'))  # send it


# This function receives the Client request and sends it to handle_req()
def get_req(sock, add):

    print(sock.getsockname())
    print('Connected at port ', add)

    # display initial response to client
    sock.send(http_response)

    while True:
        time.sleep(.750)  # short delay
        data = sock.recv(1024)
        if data.decode(encoding='utf-8') == 'BYE' or data == b'BYE\r\n':
            handle_req(data)
            time.sleep(1)  # short delay
            break
        else:
            handle_req(data)

while True:
    print(server_started)
    try:
        conn, addr = s.accept()  # open connection
        get_req(conn, addr)  # send connection to get_req() to receive client requests
        conn.close()  # close connection once get_req() is completed
    except KeyboardInterrupt:
        print('\n Shutdown requested...exiting now...\n')
        try:
            sys.exit(0)  # This might be the better way when it works, but I kept getting an exception
        except SystemExit:
            os._exit(0)  # Fall back. Flushes and exits without calling cleanup handlers
