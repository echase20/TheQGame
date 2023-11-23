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
        received = str(self.sock.recv(40 * 1080), "utf-8")
        return received

    def send(self, data):
        """
        sends data over to the server
        :param data: json data
        """
        encoded_json_data = (data+"\n").encode()
        self.sock.sendall(encoded_json_data)
