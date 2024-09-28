from scrapy.commands import BaseRunSpiderCommand
from scrapy.exceptions import UsageError

class Command(BaseRunSpiderCommand):
    requires_project = True