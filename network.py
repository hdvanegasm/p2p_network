'''
This is a basic implementation of a client for a P2P network.
'''

import socket
import sys

class Client(object):

    def __init__(self, address):

        self.socket = self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Make the connection
        self.socket.connect((address, 5000))
        

class Server(object):

    def __init__(self, byte_size):
        try:
            # List with connections to the server
            self.connections = []

            # List of peers connected
            self.peers = []

            # Socket instantiation and setup
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind socket to local host
            self.socket.bind(('127.0.0.1', 5000))

            self.socket.listen(1)

            self.byte_size = byte_size

            print('==> Server running.')

        except Exception as exception:
            print(exception)
            sys.exit()


    def handler(self, connection_handler, ip_port_tuple):
        try:
            while True:
                data = connection_handler.recv(self.byte_size)

                # Check if the peer wants to disconnect
                for connection in self.connections:
                    if data and data.decode('utf-8') == 'q':
                        self.disconnect(connection, ip_port_tuple)
                        return
                    else:
                        connection.send(data.decode('utf-8'))
        except Exception as exception:
            print(exception)
            sys.exit()


    def disconnect(self, connection, ip_port_tuple):
        self.connections.remove(connection)
        self.peers.remove(ip_port_tuple)
        connection.close()
        self.send_peers()
        print('NOTIFICATION: {} disconnected.'.format(ip_port_tuple))


    def send_peers(self):
        peer_list = ""
        for peer in self.peers:
            peer_list += str(peer[0]) + ','

        for connection in self.connections:
            connection.send('\x11' + bytes(peer_list, 'utf-8'))