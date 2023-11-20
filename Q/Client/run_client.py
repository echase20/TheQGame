
from twisted.internet import protocol, reactor
from twisted.internet.endpoints import TCP4ClientEndpoint

from Q.Client.client import ClientFactory
from Q.Client.referee import ProxyRef
from Q.Player.dag import Dag
from Q.Player.in_housep_player import InHousePlayer


if __name__ == "__main__":
    endpoint = TCP4ClientEndpoint(reactor, 'localhost', 8000)
    factory = ClientFactory()
    #player = InHousePlayer("dilan", Dag())
    #ProxyRef(factory, player)
    endpoint.connect(factory)
    reactor.run()

