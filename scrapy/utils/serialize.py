import datetime
import decimal
import json
from typing import Any
from itemadapter import ItemAdapter, is_item
from twisted.internet import defer
from scrapy.http import Request, Response

class ScrapyJSONEncoder(json.JSONEncoder):
    DATE_FORMAT = '%Y-%m-%d'
    TIME_FORMAT = '%H:%M:%S'

class ScrapyJSONDecoder(json.JSONDecoder):
    pass