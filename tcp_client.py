#! /bin/python3
# IMPORTS
import socket
import sys


# VARIABLES
#server_host = "10.136.132.200"
#server_port = 2222

# PROGRAM
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        server_host = input ('Enter server IP address: ')
        server_port_str = input('Choose port: 2222, 3333 or 4444: ')
        server_port = int(server_port_str)
        s.connect((server_host, server_port))
        bruger = '\nObservant: ' + input('Dit navn: ')
        while True:
            tid = 'Tid: ' + input('Tid: ')
            spiller = '\nSpiller: ' + input('Spiller: ')
            obs = '\nObservation: ' + input('Observation: ')
            message = tid + spiller + obs + bruger
            s.sendto(message.encode(), (server_host, server_port))
            print()
except KeyboardInterrupt:
    print('quitting...')
    sys.exit()

