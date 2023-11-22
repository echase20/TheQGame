import json

from twisted.internet import reactor, protocol
from Q.Server.states import States
"""
class Client(protocol.Protocol):
    def __init__(self):
        self.packets = []
        self.newest_not_seen = 0
        self.state = States.SIGNUP

    def connectionMade(self):
        print("Connected to Server")

    def dataReceived(self, data):
        data = data.decode("utf-8")
        print(data)
        if self.state == States.SIGNUP:
            print("Server said:", data)
            self.send_data(input())
            self.state = States.RUNGAME
        elif self.state == States.RUNGAME:
            self.packets.append(data)

    def get_data(self):
        if self.newest_not_seen >= len(self.packets):
            return
        val = self.packets[self.newest_not_seen]
        self.newest_not_seen += 1
        return val

    def send_data(self, data):
        self.transport.write(data.encode())


class ClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        print('Connected.')
        return Client()
"""
import socket

class Client:
    """
    A client that sends data over a TCP connect to some server
    """

    def __init__(self, name, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.send(name)

    def recv(self):
        received = str(self.sock.recv(1024), "utf-8")
        return received

    def send(self, data):
        """
        sends data over to the server
        :param data: json data
        """
        encoded_json_data = (data+"\n").encode()
        self.sock.sendall(encoded_json_data)
