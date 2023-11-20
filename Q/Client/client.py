from twisted.internet import reactor, protocol
from Q.Server.states import States


class Client(protocol.Protocol):
    def __init__(self):
        self.data = []
        self.newest_not_seen = 0
        self.state = States.SIGNUP

    def connectionMade(self):
        print("Connected to Server")

    def dataReceived(self, data):
        data = data.decode("utf-8")
        if self.state == States.SIGNUP:
            print("Server said:", data)
            self.send_data(input())
        if self.state == States.RUNGAME:
            self.data.append(data)

    def get_data(self):
        if self.newest_not_seen >= len(self.data):
            return
        val =  self.data[self.newest_not_seen]
        self.newest_not_seen += 1
        return val

    def send_data(self, data):
        self.factory.write(data.encode())


class ClientFactory(protocol.ClientFactory):
    protocol = Client
