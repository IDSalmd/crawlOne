import urllib2
url = 'http://example.webscraping.com/'
#url = 'https://www.baidu.com/'
html =  urllib2.urlopen(url)
print html.read()