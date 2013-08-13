from urllib import urlopen # to open the RSS feeds

def xml_to_string(xml_link):
    # http://docs.python.org/2/library/urllib2.html
    # Section 20.6.21 is especially helpful
    return urlopen(xml_link).read()

xml_link = 'http://www.nlrb.gov/rss/rssBoardDecisions.xml'
xml_text = xml_to_string(xml_link)


