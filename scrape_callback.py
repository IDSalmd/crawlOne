#coding=utf-8

import csv
import re
import urlparse
import lxml.html
from link_crawler import link_crawler

class ScapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('countries.csv','w'))
        self.fields = ('area', 'population', 'iso', 'country',
                       'capital', 'continent', 'tld', 'currency_code',
                       'currency_name', 'phone', 'postal_code_format',
                       'postal_code_regex', 'languages', 'neighbours')
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        if re.search('/view',url):
            tree = lxmlTest.html.fromstring(html)
            row = []
            for field in self.fields:
                row.append(tree.cssselect('table > tr#places_{}__row > td.w2p_fw'
                                          .format(field))[0].text_content())

if __name__ == '__main__':
    url = 'http://example.webscraping.com/'
    url_regex =  '/(index|view)'
    link_crawler(url, url_regex, scrape_callback=ScapeCallback())