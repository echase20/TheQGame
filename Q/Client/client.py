import socket
import sys


class Client:
    """
    A client that sends data over a TCP connect to some server
    """

    def __init__(self, name, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.send(name)

    def recv(self):
        received = str(self.sock.recv(4096), "utf-8")
        print(received, "received")
        return received

    def send(self, data):
        """
        sends data over to the server
        :param data: json data
        """
        encoded_json_data = (data+"\n").encode()
        print(encoded_json_data, "sent")
        self.sock.sendall(encoded_json_data)
