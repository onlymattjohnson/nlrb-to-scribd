import scribd
import time
import scribd_config_local
from urllib2 import urlopen

item_url = 'http://mynlrb.nlrb.gov/link/document.aspx/09031d45813673ae'

f = open('temp.pdf', 'wb')
f.write(urlopen(item_url).read())
f.close()

doc = scribd.api_user.upload(open('temp.pdf', 'rb'))
while doc.get_conversion_status() != 'DONE' :
    print 'Document conversion is processing...' + doc.get_conversion_status()
    time.sleep(2)
print 'Conversion complete'

doc.title = 'test'
doc.language = 'en'
doc.access = 'public'
doc.save()

print 'Done'
