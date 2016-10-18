from lxml import etree

root = etree.Element('root')
print root
print root.tag

print etree.tostring(root)

child1 = etree.SubElement(root,'child1')
child2 = etree.SubElement(root,'child2')
child3 = etree.SubElement(root,'child3')
child2.text = ',TEXT2,'
child3.tail = ',TEXT3,'


print child2.text
print child3.tail
print etree.tostring(root)
print etree.tostring(root, method='text')
print root.xpath('string()')
print root.xpath('//text()')

root.remove(child1)
print etree.tostring(root)
#root.clear()
#print etree.tostring(root)

print child2.getparent()
print child2.getparent().tag
print '*'*100

root = etree.Element('root',aaa='AAAA')
print  etree.tostring(root)
root.set('bbb','BBB')
print etree.tostring(root)

print root.get('aaa')
print root.keys()
print root.values()
print root.items()
print root.attrib

print '*'*199
