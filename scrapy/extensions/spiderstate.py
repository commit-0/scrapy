import pickle
from pathlib import Path
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.utils.job import job_dir

class SpiderState:
    """Store and load spider state during a scraping job"""

    def __init__(self, jobdir=None):
        self.jobdir = jobdir