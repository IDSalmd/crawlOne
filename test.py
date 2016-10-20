
import lxml.html
'''
import urllib2
url = 'http://example.webscraping.com/'
#url = 'https://www.baidu.com/'
html =  urllib2.urlopen(url)
with open('testHtml','w') as f:
    f.writelines(html)
'''


'''

row = []
for field in self.fields:
    row.append(tree.cssselect('table > tr#places_{}__row > td.w2p_fw'
                              .format(field))[0].text_content())
'''
fields = ('area', 'population', 'iso', 'country',
                       'capital', 'continent', 'tld', 'currency_code',
                       'currency_name', 'phone', 'postal_code_format',
                       'postal_code_regex', 'languages', 'neighbours','justtest')
field = fields[0]
with open('testHtml','r') as f:
    html = f.readlines()
html = ''.join(html)
tree = lxml.html.fromstring(html)

#area = tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))
reg = 'table > tr#places_area__row > td.w2p_fw'
result = tree.cssselect(reg)
print result
for x in tree.cssselect(reg):

    print x.text_content()

for  field in range(1):
    reg = 'table > tr#places_{}__row > td.w2p_fw'.format(field)
    reg = 'div#content'
    #print reg
    element =  tree.cssselect(reg)
    #print element[0].text_content()
    if element:
        print element[0].text_content()
