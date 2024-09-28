import random
from urllib.parse import urlencode
from twisted.web.resource import Resource
from twisted.web.server import Site

class Root(Resource):
    isLeaf = True
if __name__ == '__main__':
    from twisted.internet import reactor
    root = Root()
    factory = Site(root)
    httpPort = reactor.listenTCP(8998, Site(root))
    reactor.callWhenRunning(_print_listening)
    reactor.run()