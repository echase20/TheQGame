from twisted.internet import reactor, protocol
from twisted.internet.endpoints import TCP4ClientEndpoint

from Q.Client.referee import ProxyRef
from Q.Server.states import States


class Client(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.state = States.SIGNUP
        #reactor.callInThread(self.send_data)

    def connectionMade(self):
        print("Connected to Server")
        #self.transport.write("Hello, world!".encode("utf-8"))

    def dataReceived(self, data):
        if self.state == States.SIGNUP:
            data = data.decode("utf-8")
            print("Server said:", data)
            self.transport.write(input().encode(("utf-8")))
            #self.transport.loseConnection()
        if self.state == States.RUNGAME:
            data = data.decode("utf-8")

    def recv(self):
        return None

    def send_data(self):
        self.factory.write(input().encode(("utf-8")))


class ClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return Client(self)

if __name__ == '__main__':
    endpoint = TCP4ClientEndpoint(reactor, 'localhost', 8000)
    endpoint.connect(ClientFactory())
    reactor.run()