#!/usr/bin/python

# server.py
# Author: William Williamson
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
placeholder = ''


# Dictionary to store acceptable Client request as key and Server response as value
req = {
    'HELO': 'Server: 210 Hello %s, pleased to meet you.\n',
    'REQTIME': 'Server: 220 ' + time.strftime("%H:%M:%S", time.localtime()) + '\n',
    'REQDATE': 'Server: 230 ' + time.strftime("%Y-%m-%d", time.localtime()) + '\n',
    'ECHO': 'Server: 240 %s \n',
    'REQIP': 'Server: 250 < need to get IP > \n',
    'BYE': 'Server: 600 See ya later!\n'
}


# Function to handle the request and give a response.
# This is being called from inside get_request()
def handle_req(data):
    str_data = data.decode(encoding='utf-8') # Decode data from bytes to a string
    print(str_data) # Print to server, mostly for testing
    conn.send('Client: ' + str_data) # Display client request back to the client
    request = str_data.split() # Split request to check for arguments sent with command and store in list (request array)
    # Look for request in req
    if request[0] in req.keys():
        # If the length of the request is greater than one, everything after
        # request[0] is stored in a placeholder for the string response
        if len(request) > 1:
            joiner = ' '
            placeholder = request[1:]
            # Put the value of the req[key] in the response with the placeholder
            response = req[request[0]] % joiner.join(placeholder)
        else:
            # Put only the value of req[key] if no placeholder
            response = req[request[0]]
    else:
        # If request is not in the dictionary, put this in response
        response = 'Server: Command \"' + request[0] + '\" not understood\n'

    conn.send(response.encode(encoding='utf-8')) # send it


# This function receives the Client request and sends it to handle_req()
def get_req(conn, addr):

    print('Connected at port ', addr)

    # display initial response to client
    conn.send(http_response)

    while (True):

        time.sleep(1) # short delay

        data = conn.recv(1024)

        # If request is 'BYE', break while loop after request is processed
        # The 'data == b'BYE\r\n'' part of the if statement checks for input
        # from keyboard if connected using Telnet
        if data.decode(encoding='utf-8') == 'BYE' or data == b'BYE\r\n':
            handle_req(data)
            time.sleep(1) # short delay
            break
        else:
            handle_req(data)



while True:
    print(server_started) # Prints message to server

    # Accept connections until control c is pressed, then just shutdown gracefully
    # There is probably a better way to stop the server, but I don't know how yet
    # so I'm relying on control c for now
    try:
        conn, addr = s.accept() # open connection
        get_req(conn, addr) # send connection to get_req() to receive client requests
        conn.close() # close connection once get_req() is completed
    except KeyboardInterrupt:
        print('\n Shutdown requested...exiting now...\n')
        try:
            sys.exit(0) # This might be the better way when it works, but I kept getting an exception
        except SystemExit:
            os._exit(0) # Fall back. Flushes and exits without calling cleanup handlers
