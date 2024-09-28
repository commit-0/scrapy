from urllib.parse import urljoin
from twisted.web import resource, server, static, util

class SiteTest:
    pass

class NoMetaRefreshRedirect(util.Redirect):
    pass
if __name__ == '__main__':
    from twisted.internet import reactor
    port = reactor.listenTCP(0, test_site(), interface='127.0.0.1')
    print(f'http://localhost:{port.getHost().port}/')
    reactor.run()