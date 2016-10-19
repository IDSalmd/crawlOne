#coding=utf-8

import csv
import re
import urlparse
import lxml.html
from link_crawler import link_crawler

class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('countries.csv','w'))
        self.fields = ('area', 'population', 'iso', 'country',
                       'capital', 'continent', 'tld', 'currency_code',
                       'currency_name', 'phone', 'postal_code_format',
                       'postal_code_regex', 'languages', 'neighbours')
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        if re.search('/view',url):
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                #element = tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))
                regex = 'div#content'
                element = tree.cssselect(regex)
                print 'element length',len(element)
                if element:
                    row.append(element[0].text_content())
            self.writer.writerow(row)
            print row


if __name__ == '__main__':
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    link_crawler('http://www.biquge.tw/1_1011/', '/1_1011/\d+\.htm',delay=0,
                 num_retries=1, max_depth=1, max_urls=3, user_agent=user_agent,scrape_callback=ScrapeCallback())