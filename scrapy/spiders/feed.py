"""
This module implements the XMLFeedSpider which is the recommended spider to use
for scraping from an XML feed.

See documentation in docs/topics/spiders.rst
"""
from scrapy.exceptions import NotConfigured, NotSupported
from scrapy.selector import Selector
from scrapy.spiders import Spider
from scrapy.utils.iterators import csviter, xmliter_lxml
from scrapy.utils.spider import iterate_spider_output

class XMLFeedSpider(Spider):
    """
    This class intends to be the base class for spiders that scrape
    from XML feeds.

    You can choose whether to parse the file using the 'iternodes' iterator, an
    'xml' selector, or an 'html' selector.  In most cases, it's convenient to
    use iternodes, since it's a faster and cleaner.
    """
    iterator = 'iternodes'
    itertag = 'item'
    namespaces = ()

    def process_results(self, response, results):
        """This overridable method is called for each result (item or request)
        returned by the spider, and it's intended to perform any last time
        processing required before returning the results to the framework core,
        for example setting the item GUIDs. It receives a list of results and
        the response which originated that results. It must return a list of
        results (items or requests).
        """
        pass

    def adapt_response(self, response):
        """You can override this function in order to make any changes you want
        to into the feed before parsing it. This function must return a
        response.
        """
        pass

    def parse_node(self, response, selector):
        """This method must be overridden with your custom spider functionality"""
        pass

    def parse_nodes(self, response, nodes):
        """This method is called for the nodes matching the provided tag name
        (itertag). Receives the response and an Selector for each node.
        Overriding this method is mandatory. Otherwise, you spider won't work.
        This method must return either an item, a request, or a list
        containing any of them.
        """
        pass

class CSVFeedSpider(Spider):
    """Spider for parsing CSV feeds.
    It receives a CSV file in a response; iterates through each of its rows,
    and calls parse_row with a dict containing each field's data.

    You can set some options regarding the CSV file, such as the delimiter, quotechar
    and the file's headers.
    """
    delimiter = None
    quotechar = None
    headers = None

    def process_results(self, response, results):
        """This method has the same purpose as the one in XMLFeedSpider"""
        pass

    def adapt_response(self, response):
        """This method has the same purpose as the one in XMLFeedSpider"""
        pass

    def parse_row(self, response, row):
        """This method must be overridden with your custom spider functionality"""
        pass

    def parse_rows(self, response):
        """Receives a response and a dict (representing each row) with a key for
        each provided (or detected) header of the CSV file.  This spider also
        gives the opportunity to override adapt_response and
        process_results methods for pre and post-processing purposes.
        """
        pass