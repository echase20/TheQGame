from twisted.internet import reactor, protocol
from twisted.internet.endpoints import TCP4ClientEndpoint


class Client(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        #reactor.callInThread(self.send_data)

    def connectionMade(self):
        print("Connected to Server")
        #self.transport.write("Hello, world!".encode("utf-8"))

    def dataReceived(self, data):
        data = data.decode("utf-8")
        print("Server said:", data)
        self.transport.write(input().encode(("utf-8")))
        #self.transport.loseConnection()

    def send_data(self):
        self.factory.write(input().encode(("utf-8")))


class ClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return Client(self)



if __name__ == '__main__':
    endpoint = TCP4ClientEndpoint(reactor, 'localhost', 8000)
    endpoint.connect(ClientFactory())
    reactor.run()