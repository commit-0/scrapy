from typing import Any
from twisted.internet import defer
from twisted.internet.base import ThreadedResolver
from twisted.internet.interfaces import IHostnameResolver, IHostResolution, IResolutionReceiver, IResolverSimple
from zope.interface.declarations import implementer, provider
from scrapy.utils.datatypes import LocalCache
dnscache: LocalCache[str, Any] = LocalCache(10000)

@implementer(IResolverSimple)
class CachingThreadedResolver(ThreadedResolver):
    """
    Default caching resolver. IPv4 only, supports setting a timeout value for DNS requests.
    """

    def __init__(self, reactor, cache_size, timeout):
        super().__init__(reactor)
        dnscache.limit = cache_size
        self.timeout = timeout

@implementer(IHostResolution)
class HostResolution:

    def __init__(self, name):
        self.name = name

@provider(IResolutionReceiver)
class _CachingResolutionReceiver:

    def __init__(self, resolutionReceiver, hostName):
        self.resolutionReceiver = resolutionReceiver
        self.hostName = hostName
        self.addresses = []

@implementer(IHostnameResolver)
class CachingHostnameResolver:
    """
    Experimental caching resolver. Resolves IPv4 and IPv6 addresses,
    does not support setting a timeout value for DNS requests.
    """

    def __init__(self, reactor, cache_size):
        self.reactor = reactor
        self.original_resolver = reactor.nameResolver
        dnscache.limit = cache_size