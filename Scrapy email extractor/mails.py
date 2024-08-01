import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from urllib.parse import urlparse
import pandas as pd


class MailsSpider(CrawlSpider):
    
    name = 'mails'
    with open("pennysilvania web.csv") as file:
         start_urls = [line for line in file]
    # start_urls = ["https://aucy.ac.cy/"]
    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=False),
    )

    def __init__(self, *args, **kwargs):
        super(MailsSpider, self).__init__(*args, **kwargs)
        self.seen_emails = set()

    def parse_item(self, response):
        # Extract the domain from the URL (excluding subdomains like 'www')
        domain = '.'.join(urlparse(response.url).netloc.split('.')[-2:])
        
        # Find all emails in the response text
        emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", response.text)
        
        # Filter emails that match the domain
        filtered_emails = {email for email in emails if domain in email.split('@')[1]}
        
        # Yield each unique email that has not been seen before
        for email in filtered_emails:
            if email not in self.seen_emails:
                self.seen_emails.add(email)
                yield {
                    'Email': email,
                    'website':response.url
                }


#command: scrapy runspider mails.py -o pennysilvania_email.csv
