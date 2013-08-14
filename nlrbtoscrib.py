from urllib import urlopen # to open the RSS feeds
import xml.etree.ElementTree as ET # to parse XML
import time
import scribd
import scribd_config_local
from datetime import date
import os

def get_case_info(item):
    # Extracts info out of XML document

    case_info = {}
    case_info['title'] = item.find('title').text
    description = item.find('description').text    
    case_info['description'] = description
    dash_pos = description.find(" - ")
    case_num = description[:dash_pos].strip()
    case_info['case_num'] = case_num
    case_info['case_type'] = case_num[3:5]
    case_info['nlrb_region'] = case_num[0:2]
    case_info['involved_party'] = description[dash_pos+3:]
    case_info['pub_date'] = item.find('pubDate').text
    case_info['pdf_link'] = item.find('guid').text
    
    return case_info
    
def xml_to_string(xml_link):
    # http://docs.python.org/2/library/urllib2.html
    # Section 20.6.21 is especially helpful
    return urlopen(xml_link).read()

xml_link = 'http://www.nlrb.gov/rss/rssBoardDecisions.xml'
xml_text = xml_to_string(xml_link)
root = ET.fromstring(xml_text)

all_results = []
for item in root.iter('item'):
    all_results.append(get_case_info(item))

## Test out uploading doc to scribd

f = open('temp.pdf', 'wb')
f.write(urlopen(all_results[0]['pdf_link']).read())
f.close()

doc = scribd.api_user.upload(open('temp.pdf', 'rb'))
while doc.get_conversion_status() != 'DONE' :
    print 'Document conversion ' + doc.get_conversion_status()
    time.sleep(2)

doc.desription = all_results[0]['description']
doc.access = 'public'
doc.language = 'en'
doc.title = all_results[0]['title']
doc.when_published = date.today().isoformat()
doc.save()

os.remove('temp.pdf')

print 'Complete'
