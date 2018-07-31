# -*- coding: utf8 -*-

import requests
from xml.etree import ElementTree

def process(xmldata):
    articles = ElementTree.fromstring(xmldata)
    data = []
    for article in articles:
        if article.tag != 'artikel':
            continue
        entry = {}
        use_entry = True
        try:
            for field in article:
                tag = field.tag.lower()
                if tag == u'utg\xe5tt' and field.text != '0':
                    use_entry = False
                elif tag == 'sortiment' and field.text.lower() == 'bs':
                    use_entry = False
                elif tag == 'nr':
                    entry['nr'] = int(field.text)
                    entry['link'] = 'https://www.systembolaget.se/' + field.text
                elif tag == 'namn':
                    entry['namn'] = field.text
                elif tag == 'prisinklmoms':
                    entry['pris'] = float(field.text)
                elif tag == 'prisperliter':
                    entry['literpris'] = float(field.text)
                elif tag == 'volymiml':
                    entry['volym'] = float(field.text)
                elif tag == 'alkoholhalt':
                    entry['alkoholhalt'] = float(field.text.replace('%', ''))
            if use_entry:
                entry['apk'] = entry['alkoholhalt'] / entry['literpris']
                data.append(entry)
        except Exception as e:
            print(str(e))
    return sorted(data, key=lambda e: e['apk'], reverse=True)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            xmldata = f.read()
    else:
        r = requests.get('https://www.systembolaget.se/api/assortment/products/xml')
        xmldata = r.text
    data = process(xmldata)
    for i in range(50):
        print(data[i])
