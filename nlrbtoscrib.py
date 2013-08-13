from urllib import urlopen # to open the RSS feeds
import xml.etree.ElementTree as ET # to parse XML

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

all_links = []
all_links.append('http://www.nlrb.gov/rss/rssBoardDecisions.xml')
all_links.append('http://www.nlrb.gov/rss/rssJudgesDecisions.xml')
all_links.append('http://www.nlrb.gov/rss/rssRegionalDecisions.xml')
all_links.append('http://www.nlrb.gov/rss/rssAppellateCourt.xml')
all_links.append('http://www.nlrb.gov/rss/rssAppellateCourt.xml')
all_links.append('http://www.nlrb.gov/rss/rssAppellateCourt.xml')

xml_text = xml_to_string(all_links[10])
root = ET.fromstring(xml_text)

for item in root.iter('item'):
    print get_case_info(item)
