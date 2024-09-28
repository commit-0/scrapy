"""
StatsMailer extension sends an email when a spider finishes scraping.

Use STATSMAILER_RCPTS setting to enable and give the recipient mail address
"""
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.mail import MailSender

class StatsMailer:

    def __init__(self, stats, recipients, mail):
        self.stats = stats
        self.recipients = recipients
        self.mail = mail