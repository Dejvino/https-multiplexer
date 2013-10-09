# 	HTTPS multiplexer
# Author: David Nemecek (dejvino.cz)
# Date: 2013-10-09
#
# 	Port forwarder
# Author: Mario Scondo (www.Linux-Support.com)
# Date: 2010-01-08
# Script template by Stephen Chappell
#
# This script forwards a number of configured local ports
# to local or remote socket servers based on content (HTTP/HTTPS).
#
 
import socket
import sys
import thread
import time

# following method names are defined in the HTTP protocol
httpMethods = ["GET", "HEAD", "POST", "PUT", "DELETE", "TRACE", "OPTIONS", "CONNECT", "PATCH"]

# program entry point
def main(setup, error):
    # open file for error messages
    sys.stderr = file(error, 'a')
    # read settings for port forwarding
    for settings in parse(setup):
        thread.start_new_thread(server, settings)
    # wait for <ctrl-c>
    while True:
       time.sleep(60)

# parse config file
def parse(setup):
    settings = list()
    for line in file(setup):
        parts = line.split()
        settings.append((int(parts[0]), parts[1], int(parts[2]), int(parts[3])))
    return settings

# connection accepting procedure
def server(*settings):
    try:
        dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dock_socket.bind(('', settings[0]))
        dock_socket.listen(5)
        while True:
            client_socket = dock_socket.accept()[0]
            thread.start_new_thread(forwardClientToServer, (settings, client_socket))
    finally:
        thread.start_new_thread(server, settings)

# multiplexing forwarding 
def forwardClientToServer(settings, source):
    global httpMethods
    string = ' '
    destination = None
    while string:
        string = source.recv(1024)
	# first batch determines the destination
	if string and (destination is None):
	    # guess protocol
	    http = False
	    for method in httpMethods:
		if string.startswith(method):
		    http = True
	    # spawn the right forwarding
            destination = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            destination.connect((settings[1], settings[2 if http else 3]))
            thread.start_new_thread(forwardServerToClient, (destination, source))
	# forwarding (started / running, finishing)
        if string:
            destination.sendall(string)
        else:
            source.shutdown(socket.SHUT_RD)
            destination.shutdown(socket.SHUT_WR)

# trivial forwarding
def forwardServerToClient(source, destination):
    string = ' '
    while string:
        string = source.recv(1024)
        if string:
            destination.sendall(string)
        else:
            source.shutdown(socket.SHUT_RD)
            destination.shutdown(socket.SHUT_WR)

# run!
if __name__ == '__main__':
    main('multiplexer.config', 'error.multiplexer.log')
