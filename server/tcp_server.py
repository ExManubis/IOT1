#! /bin/python3

# IMPORTS
from time import sleep
import socket
import sys
import _thread

# VARIABLES
server_ip = "ENTER IP FOR SERVER"

# open data file and make variable for appending data
f = open('data.txt', 'a') # a = appending 

# FUNCTIONS

# First create connection function with server port as argument.
def con(server_port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((server_ip, server_port))
            s.listen(3)
            connection, addr = s.accept()
            with connection:
                print(f'{addr} connected to server!')
                while True:
                    message, client = connection.recvfrom(1024)
                    print()
                    print('===============================')
                    besked = message.decode() + f'\nIP: {addr}'
                    if besked == f'\nIP: {addr}':
                        break
                    else:
                        print(besked)
                        print('===============================')
                        print()
                        f.write('==============================')
                        f.write('\n')
                        f.write(besked)
                        f.write('\n')
                        f.write('==============================')
                        f.write('\n')
                        f.close
    except KeyboardInterrupt:
        print('Quitting....')
        sys.exit()

# Define three connections for concurrent connections via TCP.
def con1():
    con(2222)

def con2():
    con(3333)

def con3():
    con(4444)

# PROGRAM
_thread.start_new_thread(con1, ())
_thread.start_new_thread(con2, ())
_thread.start_new_thread(con3, ())
print('===========================')
print('|                         |')
print('|  Welcome to SSO v.1.0!  |')
print('|                         |')
print('===========================')
while True:
    print('\nrunning...waiting for data..')
    sleep(10)