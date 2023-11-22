from twisted.internet import reactor, protocol
from Q.Server.states import States


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


