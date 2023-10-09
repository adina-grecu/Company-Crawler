import scrapy
import re
from scrapy.crawler import CrawlerProcess
import csv

class CompanySpider(scrapy.Spider):
    name = 'company_spider'

    # Read the list of websites from sample-websites.csv
    with open('data/sample-websites.csv', 'r') as f:
        urls = [url.strip() for url in f.readlines()]
        start_urls = [f'https://{url}' for url in urls]

    def extract_phone_numbers(self, text):
        # Phone number regex
        pattern = re.compile(r'''(
            (?!-\d)                 # Ensure number doesn't start with "-"
            ((\d{3}|\(\d{3}\))      # Three digits with or without parentheses
            (\s|-|\.))              # Separator
            (\d{3})                 # Three digits
            (\s|-|\.)               # Separator:
            (\d{4})                 # Four digits
        )''', re.VERBOSE)

        return pattern.findall(text)
       
    def extract_social_links(self, response):
        social_links = {}
        base_urls = {
            'facebook': 'facebook.com',
            'twitter': 'twitter.com',
            'linkedin': 'linkedin.com',
            'instagram': 'instagram.com',
            'youtube': 'youtube.com',
        }
      
        for platform, base_url in base_urls.items():
            link = response.css(f'a[href*="{base_url}"]::attr(href)').get()
            if link:
                social_links[platform] = link
        return social_links

    def parse(self, response):
        text_content = response.text
        phone_numbers = self.extract_phone_numbers(text_content)

        #filter out duplicates and incomplete numbers
        phone_numbers = list(set([phone[0] for phone in phone_numbers]))       
        
        social_media_links = self.extract_social_links(response)

        yield {
            'website': response.url,
            'phone_numbers': phone_numbers,
            'social_media_links': social_media_links,
        }

# Start the crawler
process = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': 'output.json',
    'LOG_LEVEL': 'INFO'
})

process.crawl(CompanySpider)
process.start()
