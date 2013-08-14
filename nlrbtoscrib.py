from urllib import urlopen # to open the RSS feeds
import xml.etree.ElementTree as ET # to parse XML
import time
import scribd
import scribd_config_local
from datetime import date
import os
from pymongo import MongoClient

def check_mongo(guid):
    client = MongoClient()
    db = client.nlrb
    nlrb = db.nlrb
    return nlrb.find_one({"guid": guid})

def insert_into_mongo(document_info):
    print 'Inserting ' + document_info['guid'] + ' into database.'
    client = MongoClient()
    db = client.nlrb
    nlrb = db.nlrb
    nlrb_id = nlrb.insert({'guid': document_info['guid']})
    #if nlrb_id:
    #    print 'Insertion successful.'
    #else:
    #    print 'There was a problem with inserting the field.'

    return nlrb_id

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

    guid_start_pos = case_info['pdf_link'].find('document.aspx')
    guid = case_info['pdf_link'][guid_start_pos+14:]
    case_info['guid'] = guid

    return case_info

def upload_to_scribd(document_info):
    # Check for already entered in db
    print 'Checking for ' + document_info['guid'] + ' in database...'
    
    if not check_mongo(document_info['guid']):
        print document_info['guid'] + ' not found.  Proceeding with upload...'

        print 'Opening temp file...'
        file_name = 'temp' + document_info["guid"] + '.pdf'
        # Open temp file    
        f = open(file_name, 'wb')
        f.write(urlopen(document_info['pdf_link']).read())
        f.close()

        print 'Uploading file to Scribd...'
        doc = scribd.api_user.upload(open(file_name, 'rb'))
        while doc.get_conversion_status() != 'DONE' :
            print 'Document ' + doc.get_conversion_status()
            time.sleep(2)

        # Processed, now add fields
        doc.description = document_info['description']
        doc.access = 'public'
        doc.language = 'en'
        doc.title = document_info['title']
        doc.when_published = date.today().isoformat()
        doc.save()
            
        print 'Removing temp file'
        try:
            os.remove(file_name)
            print 'Temp file removed'
        except:
            print 'Could not remove temp file'

        # Enter into mongo
        insert_into_mongo(document_info)
    else:
        print 'Item already uploaded, moving on...'

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

counter = 1
for document_info in all_results:
    print 'Uploading ' + str(counter) + ' of ' + str(len(all_results))
    upload_to_scribd(document_info)
    counter += 1

