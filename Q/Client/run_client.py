from twisted.internet import reactor

from Q.Client.client import ClientFactory


if __name__ == "__main__":
    port = 8000
    reactor.listenTCP(port, ClientFactory())
    reactor.run()
