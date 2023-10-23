#! /bin/python3

# IMPORTS
from time import sleep
import socket
import sys
import threading
import _thread
#import pymysql

# VARIABLES

# open data file and make variable for appending data
f = open('data.txt', 'a') # a = appending 

# FUNCTIONS
def con1():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('10.136.132.200', 2222))
            s.listen(3)
            connection, addr = s.accept()
            with connection:
                print(f'Connected by {addr}')
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

def con2():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('10.136.132.200', 3333))
            s.listen(3)
            connection, addr = s.accept()
            with connection:
                print(f'Connected by {addr}')
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
        sys.exit()

def con3():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('10.136.132.200', 4444))
            s.listen(3)
            connection, addr = s.accept()
            with connection:
                print(f'Connected by {addr}')
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
        sys.exit()

# PROGRAM
_thread.start_new_thread(con1, ())
_thread.start_new_thread(con2, ())
_thread.start_new_thread(con3, ())
while True:
    print('running..')
    sleep(10)
