"""Set User-Agent header per spider or use a default value from settings"""
from scrapy import signals

class UserAgentMiddleware:
    """This middleware allows spiders to override the user_agent"""

    def __init__(self, user_agent='Scrapy'):
        self.user_agent = user_agent